import re


class KeywordMetric:

    def score(self, answer, expected_keywords):
        answer_words = set(re.findall(r"\w+", answer.lower()))

        matched = 0

        for word in expected_keywords:
            if str(word).lower() in answer_words:
                matched += 1

        return matched / len(expected_keywords) if expected_keywords else 1.0
