from pathlib import Path
import json

from donors.models import Donor

from embeddings.embedding_service import (
    EmbeddingService,
)

from vectorstore.faiss_service import (
    FAISSService,
)


class SemanticSearchService:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.faiss = FAISSService()

        self.faiss.load_index()

        metadata_path = (
            Path(__file__).parent.parent
            / "embeddings"
            / "storage"
            / "metadata.json"
        )

        with open(
            metadata_path,
            encoding="utf-8",
        ) as file:

            self.metadata = json.load(file)

    def search(
        self,
        query,
        top_k=5,
    ):

        query_embedding = (
            self.embedding_service.generate_embedding(
                query
            )
        )

        distances, indices = (
            self.faiss.search(
                query_embedding,
                top_k,
            )
        )

        database_ids = []

        for index in indices[0]:

            item = self.metadata[index]

            database_ids.append(
                item["database_id"]
            )

        donors = Donor.objects.filter(
            id__in=database_ids
        )

        results = []

        donor_lookup = {
            donor.id: donor
            for donor in donors
        }

        for distance, index in zip(
            distances[0],
            indices[0],
        ):

            item = self.metadata[index]

            donor = donor_lookup.get(
                item["database_id"]
            )

            if donor:

                results.append(
                    {
                        "donor": donor,
                        "distance": float(distance),
                    }
                )

        return results