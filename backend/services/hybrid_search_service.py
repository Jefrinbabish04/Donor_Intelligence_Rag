from chat.conversation_memory import ConversationMemory
from chat.query_rewriter import QueryRewriter
from documents.services.document_search_service import DocumentSearchService
from vectorstore.semantic_search import SemanticSearchService


class HybridSearchService:

    def __init__(self):
        self.donor_search = SemanticSearchService()
        self.document_search = DocumentSearchService()
        self.memory = ConversationMemory()
        self.rewriter = QueryRewriter()

    def search(self, query, top_k=5, history=None):
        if history is None:
            history = self.memory.get_history()

        rewritten_query = self.rewriter.rewrite(query, history)

        donor_results = self.donor_search.search(rewritten_query, top_k=top_k)
        document_results = self.document_search.search(rewritten_query, top_k=top_k)

        merged_results = []

        for donor in donor_results:
            merged_results.append(
                {
                    "source": "donor",
                    "data": donor,
                    "score": donor.get("distance"),
                }
            )

        for document in document_results:
            merged_results.append(
                {
                    "source": "document",
                    "data": document,
                    "score": document.get("score"),
                }
            )

        merged_results.sort(key=lambda item: item["score"])

        return merged_results
