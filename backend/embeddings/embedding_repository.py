from pathlib import Path
import json
import numpy as np


class EmbeddingRepository:

    def __init__(self):
        self.storage = Path(__file__).parent / "storage"

    @property
    def embedding_file(self):
        return self.storage / "embeddings.npy"

    @property
    def metadata_file(self):
        return self.storage / "metadata.json"

    def load_embeddings(self):
        return np.load(self.embedding_file)

    def save_embeddings(self, embeddings):
        np.save(self.embedding_file, embeddings)

    def load_metadata(self):
        with open(self.metadata_file, encoding="utf-8") as f:
            return json.load(f)

    def save_metadata(self, metadata):
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

    def find_embedding_index(
    self,
    database_id,
):

        metadata = self.load_metadata()

        for index, item in enumerate(metadata):

            if item["database_id"] == database_id:

                return index

        return None

    def update_embedding(
        self,
        database_id,
        embedding,
    ):

        embeddings = self.load_embeddings()

        index = self.find_embedding_index(
            database_id
        )

        if index is None:

            raise ValueError(
                "Embedding not found."
            )

        embeddings[index] = embedding

        self.save_embeddings(
            embeddings
        )
    def add_embedding(self,metadata_item,embedding,):

        embeddings = self.load_embeddings()
        metadata = self.load_metadata()
        embeddings = np.vstack(
            [
                embeddings,
                embedding.reshape(1,-1),
            ]
        )

        metadata.append(
            metadata_item
        )

        self.save_embeddings(embeddings)
        self.save_metadata(metadata)

    def delete_embedding(self,database_id,):
        embeddings = self.load_embeddings()

        metadata = self.load_metadata()

        index = self.find_embedding_index(
            database_id
        )

        if index is None:
            return

        embeddings = np.delete(
            embeddings,
            index,
            axis=0,
        )

        metadata.pop(index)

        self.save_embeddings(
            embeddings
        )

        self.save_metadata(
            metadata
        )