from pathlib import Path

import numpy as np

from vectorstore.faiss_service import (
    FAISSService,
)


class IndexBuilder:

    def build(self):

        embeddings_path = (
            Path(__file__).parent.parent
            / "embeddings"
            / "storage"
            / "embeddings.npy"
        )

        embeddings = np.load(
            embeddings_path
        )

        service = FAISSService()

        service.build_index(
            embeddings
        )

        service.save_index()

        print(
            "FAISS index created successfully."
        )