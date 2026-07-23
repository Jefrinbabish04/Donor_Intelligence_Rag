import json
from pathlib import Path

import numpy as np

from documents.chunking.text_chunker import TextChunker
from documents.loaders.pdf_loader import PDFLoader
from documents.services.document_embedding_service import DocumentEmbeddingService
from embeddings.embedding_service import EmbeddingService
from vectorstore.faiss_service import FAISSService


class DocumentSearchService:

    def __init__(self, index_path=None, metadata_path=None):

        self.embedding_service = EmbeddingService()

        self.faiss = FAISSService()

        base_dir = Path(__file__).resolve().parent.parent

        if index_path is None:
            index_path = base_dir / "storage" / "document.index"

        if metadata_path is None:
            metadata_path = base_dir / "storage" / "document_metadata.json"

        self._ensure_index_and_metadata(index_path, metadata_path)

        self.faiss.load_index(index_path)

        with open(
            metadata_path,
            "r",
            encoding="utf-8",
        ) as file:

            self.metadata = json.load(file)

    def _ensure_index_and_metadata(self, index_path, metadata_path):

        index_path = Path(index_path)
        metadata_path = Path(metadata_path)

        if index_path.exists() and metadata_path.exists():
            return

        index_path.parent.mkdir(parents=True, exist_ok=True)

        sample_pdf = (
            Path(__file__).resolve().parent.parent / "samples" / "hospital_guidelines.pdf"
        )

        if not sample_pdf.exists():
            raise FileNotFoundError(
                f"No document sample found at {sample_pdf}."
            )

        loader = PDFLoader()
        pages = loader.load(sample_pdf)

        chunks = TextChunker().chunk(pages)

        embedding_service = DocumentEmbeddingService()
        embeddings, embedding_metadata = embedding_service.generate(
            document_id=1,
            filename=sample_pdf.name,
            chunks=chunks,
        )

        self.faiss.build_index(embeddings)
        self.faiss.save_index(index_path)

        metadata = []
        for item in embedding_metadata:
            metadata.append(
                {
                    "text": item["text"],
                    "page": item["page"],
                    "chunk": item["chunk"],
                    "filename": item["filename"],
                }
            )

        with open(
            metadata_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(metadata, file, ensure_ascii=False, indent=2)

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
                top_k=top_k,
            )
        )

        results = []

        distances = np.atleast_1d(distances)
        indices = np.atleast_1d(indices)

        if distances.ndim == 1:
            distances = distances.reshape(1, -1)
        if indices.ndim == 1:
            indices = indices.reshape(1, -1)

        for distance_row, index_row in zip(distances, indices):
            for distance, index in zip(distance_row, index_row):
                item = self.metadata[int(index)]

                results.append(
                    {
                        "text": item["text"],
                        "page": item["page"],
                        "chunk": item["chunk"],
                        "filename": item["filename"],
                        "score": float(distance),
                    }
                )

        return results