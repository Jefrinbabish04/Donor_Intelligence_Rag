from django.db.models.signals import (
    post_save,
    post_delete,
)

from django.dispatch import receiver

from donors.models import Donor

from embeddings.single_embedding import SingleEmbeddingGenerator


@receiver(post_save, sender=Donor)
def donor_saved(sender, instance, created, **kwargs):

    print("Donor saved.")

    generator = SingleEmbeddingGenerator()

    if created:
        generator.create(instance)
    else:
        generator.update(instance)


@receiver(post_delete, sender=Donor)
def donor_deleted(sender, instance, **kwargs):

    print("Donor deleted.")

    SingleEmbeddingGenerator().delete(instance)