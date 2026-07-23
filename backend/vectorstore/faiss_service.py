from pathlib import Path

import faiss
import numpy as np


class FAISSService:

    def __init__(self):
        self.index = None

        self.storage_path = (
            Path(__file__).resolve().parent / "storage"
        )

        self.storage_path.mkdir(
            exist_ok=True
        )

    def build_index(self, embeddings):

        embeddings = embeddings.astype(np.float32)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(
            embeddings
        )

    def save_index(self, index_path=None):

        if index_path is None:
            index_path = self.storage_path / "donor.index"
        else:
            index_path = Path(index_path)

        index_path.parent.mkdir(parents=True, exist_ok=True)

        faiss.write_index(
            self.index,
            str(index_path),
        )

    def load_index(self, index_path=None):

        if index_path is None:
            index_path = self.storage_path / "donor.index"
        else:
            index_path = Path(index_path)

        self.index = faiss.read_index(
            str(index_path)
        )

    def search(
        self,
        query_embedding,
        top_k=5,
    ):

        query_embedding = (
            query_embedding.astype(np.float32)
            .reshape(1, -1)
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k,
        )

        return distances, indices