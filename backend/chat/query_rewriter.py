class QueryRewriter:

    def rewrite(self, question, history):
        if not history:
            return question

        previous_user_question = None

        for message in reversed(history):
            if message.get("role") == "user":
                previous_user_question = message.get("content")
                break

        if previous_user_question is None:
            return question

        follow_up_words = [
            "what about",
            "and",
            "also",
            "him",
            "her",
            "them",
            "those",
            "it",
        ]

        lower_question = question.lower()

        if any(lower_question.startswith(word) for word in follow_up_words):
            return f"{previous_user_question} {question}"

        return question
