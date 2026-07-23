
from django.core.management.base import BaseCommand

from embeddings.generate_embeddings import (
    Embeddinggenerator,
)


class Command(BaseCommand):

    help = "Generate donor embeddings."

    def handle(self, *args, **kwargs):

        generator = Embeddinggenerator()
        generator.generate()

        self.stdout.write(
            self.style.SUCCESS(
                "Embedding generation completed."
            )
        )

