from vectorstore.semantic_search import (
    SemanticSearchService,
)

from rag.context_builder import (
    ContextBuilder,
)

from rag.prompt_builder import (
    PromptBuilder,
)

from rag.llm_service import (
    LLMService,
)

from rag.response_validator import (
    ResponseValidator,
)


class RAGService:

    def __init__(self):

        self.search = (
            SemanticSearchService()
        )

        self.context_builder = (
            ContextBuilder()
        )

        self.prompt_builder = (
            PromptBuilder()
        )

        self.llm = (
            LLMService()
        )

        self.validator = (
            ResponseValidator()
        )

    def ask(self,question,):

        if not question.strip():

            raise ValueError(
                "Question cannot be empty."
            )

        results = self.search.search(
            question
        )

        if not results:

            return {
                "question": question,
                "context": "",
                "results": [],
                "answer": (
                    "No relevant donor records were found."
                ),
            }

        context = (
            self.context_builder.build(
                results
            )
        )

        prompt = (
            self.prompt_builder.build(
                question=question,
                context=context,
            )
        )

        answer = self.llm.generate(
            prompt
        )

        validation = self.validator.validate(
            answer,
            context,
        )

        return {
            "question": question,
            "context": context,
            "results": results,
            "answer": answer,
            "validation": validation,
        }