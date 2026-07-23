import re


class ResponseValidator:

    def validate(self, answer, context):
        answer_words = set(re.findall(r"\w+", answer.lower()))
        context_words = set(re.findall(r"\w+", context.lower()))

        missing = sorted(answer_words - context_words)

        return {
            "is_supported": len(missing) == 0,
            "missing_words": missing,
        }
