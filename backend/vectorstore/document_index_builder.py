from vectorstore.faiss_service import FAISSService


class DocumentIndexBuilder:

    INDEX_PATH = "backend/documents/storage/document.index"

    def build(self, embeddings):
        faiss = FAISSService()

        faiss.build_index(embeddings)

        faiss.save_index(self.INDEX_PATH)
        