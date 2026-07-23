import csv
import json
from datetime import date
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from donors.models import Donor


class Command(BaseCommand):

    help = "Import donor records from a CSV file."

    def add_arguments(self, parser):

        parser.add_argument(
            "csv_file",
            type=str,
            help="Path to the donor CSV file.",
        )

    def handle(self, *args, **options):

        csv_path = Path(
            options["csv_file"]
        )

        if not csv_path.exists():

            self.stderr.write(
                self.style.ERROR(
                    f"File not found: {csv_path}"
                )
            )

            return

        donors_to_create = []

        skipped = 0

        with csv_path.open(
            "r",
            encoding="utf-8",
        ) as csv_file:

            reader = csv.DictReader(
                csv_file
            )

            for row_number, row in enumerate(
                reader,
                start=2,
            ):

                try:

                    donor_id = (
                        row["donor_id"].strip()
                    )

                    if Donor.objects.filter(
                        donor_id=donor_id
                    ).exists():

                        skipped += 1

                        continue

                    tags = json.loads(
                        row["tags"] or "[]"
                    )

                    donor = Donor(
                        donor_id=donor_id,
                        name=row["name"].strip(),
                        age=int(row["age"]),
                        gender=row["gender"].strip(),
                        blood_group=row[
                            "blood_group"
                        ].strip(),
                        phone=row["phone"].strip(),
                        email=row["email"].strip(),
                        address=row["address"].strip(),
                        city=row["city"].strip(),
                        state=row["state"].strip(),
                        country=row[
                            "country"
                        ].strip(),
                        medical_history=row[
                            "medical_history"
                        ].strip(),
                        last_donation_date=(
                            date.fromisoformat(
                                row[
                                    "last_donation_date"
                                ]
                            )
                        ),
                        eligible_date=(
                            date.fromisoformat(
                                row["eligible_date"]
                            )
                        ),
                        donation_count=int(
                            row["donation_count"]
                        ),
                        notes=row["notes"].strip(),
                        hospital=row[
                            "hospital"
                        ].strip(),
                        latitude=(
                            row["latitude"]
                            or None
                        ),
                        longitude=(
                            row["longitude"]
                            or None
                        ),
                        tags=tags,
                    )

                    donors_to_create.append(
                        donor
                    )

                except (
                    KeyError,
                    ValueError,
                    json.JSONDecodeError,
                ) as error:

                    self.stderr.write(
                        self.style.WARNING(
                            f"Skipping row "
                            f"{row_number}: "
                            f"{error}"
                        )
                    )

                    skipped += 1

        with transaction.atomic():

            Donor.objects.bulk_create(
                donors_to_create,
                batch_size=500,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created: "
                f"{len(donors_to_create)}"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                f"Skipped: {skipped}"
            )
        )