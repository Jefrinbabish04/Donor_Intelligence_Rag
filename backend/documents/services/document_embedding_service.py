from embeddings.embedding_service import EmbeddingService

import numpy as np


class DocumentEmbeddingService:

    def __init__(self):

        self.embedding_service = EmbeddingService()

    def generate(
        self,
        document_id,
        filename,
        chunks,
    ):

        embeddings = []

        metadata = []

        for chunk in chunks:

            vector = self.embedding_service.generate_embedding(
                chunk["text"]
            )

            embeddings.append(vector)

            metadata.append(
                {
                    "document_id": document_id,
                    "filename": filename,
                    "page": chunk["page"],
                    "chunk": chunk["chunk"],
                    "text": chunk["text"],
                }
            )

        embeddings = np.array(
            embeddings,
            dtype="float32",
        )

        return embeddings, metadata