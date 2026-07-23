import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker


fake = Faker("en_IN")
Faker.seed(42)
random.seed(42)


TOTAL_DONORS = 500

BLOOD_GROUPS = [
    "A+",
    "A-",
    "B+",
    "B-",
    "AB+",
    "AB-",
    "O+",
    "O-",
]

GENDERS = [
    "Male",
    "Female",
    "Other",
]

CITIES = {
    "Chennai": "Tamil Nadu",
    "Coimbatore": "Tamil Nadu",
    "Madurai": "Tamil Nadu",
    "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana",
    "Kochi": "Kerala",
    "Thiruvananthapuram": "Kerala",
}

MEDICAL_HISTORIES = [
    "",
    "No known medical conditions",
    "History of mild anemia",
    "Seasonal allergies",
    "Hypertension under monitoring",
]

NOTES = [
    "",
    "Available for emergency donation",
    "Prefers weekend contact",
    "Frequent donor",
    "Contact before scheduling",
]

HOSPITALS = [
    "City General Hospital",
    "Community Blood Centre",
    "Regional Medical Centre",
    "Government General Hospital",
]


def generate_donor(index):
    city = random.choice(list(CITIES.keys()))
    state = CITIES[city]

    last_donation_date = (
        date.today() - timedelta(days=random.randint(90, 730))
    )

    eligible_date = last_donation_date + timedelta(days=90)

    tags = random.sample(
        [
            "frequent-donor",
            "emergency-contact",
            "weekend-available",
            "regular-donor",
        ],
        k=random.randint(0, 2),
    )

    return {
        "donor_id": f"DONOR-{index:04d}",
        "name": fake.name(),
        "age": random.randint(18, 60),
        "gender": random.choice(GENDERS),
        "blood_group": random.choice(BLOOD_GROUPS),
        "phone": fake.phone_number(),
        "email": fake.email(),
        "address": fake.address().replace("\n", ", "),
        "city": city,
        "state": state,
        "country": "India",
        "medical_history": random.choice(MEDICAL_HISTORIES),
        "last_donation_date": last_donation_date.isoformat(),
        "eligible_date": eligible_date.isoformat(),
        "donation_count": random.randint(0, 15),
        "notes": random.choice(NOTES),
        "hospital": random.choice(HOSPITALS),
        "latitude": "",
        "longitude": "",
        "tags": json.dumps(tags),
    }


def main():
    project_root = Path(__file__).resolve().parent.parent

    output_file = (
        project_root
        / "datasets"
        / "donors_500.csv"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    donors = [
        generate_donor(index)
        for index in range(1, TOTAL_DONORS + 1)
    ]

    fieldnames = list(donors[0].keys())

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(donors)

    print(
        f"Generated {TOTAL_DONORS} donor records."
    )

    print(
        f"Dataset saved to: {output_file}"
    )


if __name__ == "__main__":
    main()