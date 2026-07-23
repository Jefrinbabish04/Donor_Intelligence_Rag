from django.core.management.base import (
    BaseCommand,
)

from vectorstore.build_index import (
    IndexBuilder,
)


class Command(BaseCommand):

    help = "Build FAISS index."

    def handle(
        self,
        *args,
        **kwargs,
    ):

        builder = IndexBuilder()

        builder.build()

        self.stdout.write(
            self.style.SUCCESS(
                "Index build completed."
            )
        )