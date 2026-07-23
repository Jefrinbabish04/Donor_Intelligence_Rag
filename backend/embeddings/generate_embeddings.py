from pathlib import Path
import json

import numpy as np

from donors.models import Donor

from embeddings.embedding_service import EmbeddingService
from embeddings.text_builder import donor_to_text

from embeddings.embedding_repository import (
    EmbeddingRepository
)

class Embeddinggenerator:
    def __init__(self):

        self.repository = (EmbeddingRepository())
        self.embedding_service = EmbeddingService()
        self.storage_path =(
            Path(__file__).parent / "storage"
        )
        self.storage_path.mkdir(
            exist_ok = True
        )

    def generate(self):
        donors = Donor.objects.all()
        embeddings = []
        metadata = []

        for donor in donors:
            text = donor_to_text(donor)

            vector = self.embedding_service.generate_embedding(
                text
            )

            embeddings.append(vector)
            metadata.append(
                {
                    "donor_id":donor.donor_id,
                    "database_id":donor.id,
                    "name":donor.name,
                }
            )
        embeddings = np.array(
            embeddings
        )
        self.repository.save_embeddings(
        embeddings)

        with open(
            self.storage_path / "metadata.json",
            "w",
            encoding="utf-8",
        ) as file:
            self.repository.save_metadata(
    metadata
)
        print(f"Generated {len(metadata)}embeddings.")