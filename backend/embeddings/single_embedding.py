from embeddings.embedding_service import EmbeddingService
from embeddings.text_builder import donor_to_text
from embeddings.embedding_repository import EmbeddingRepository


class SingleEmbeddingGenerator:

    def __init__(self):

        self.service = (
            EmbeddingService()
        )
        self.repository = (
    EmbeddingRepository()
)

    def generate(
        self,
        donor,
    ):

        text = donor_to_text(
            donor
        )

        return self.service.generate_embedding(
            text
        )
    
    def update(self,donor,):

        embedding = self.generate(
            donor
        )

        self.repository.update_embedding(
            donor.id,
            embedding,
        )
    def create(
        self,
        donor,
    ):

        embedding = self.generate(
            donor
        )

        metadata = {
            "database_id": donor.id,
            "donor_id": donor.donor_id,
            "name": donor.name,
        }

        self.repository.add_embedding(
            metadata,
            embedding,
        )
    def delete(
        self,
        donor,
    ):

        self.repository.delete_embedding(
            donor.id
        )