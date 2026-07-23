try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover - exercised by regression test
    SentenceTransformer = None


class EmbeddingService:
    def __init__(self):
        if SentenceTransformer is None:
            raise ImportError(
                "sentence_transformers is required to generate embeddings."
            )

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def generate_embedding(self, text):
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding
