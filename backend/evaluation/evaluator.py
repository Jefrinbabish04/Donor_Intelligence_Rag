from evaluation.metrics import KeywordMetric


class Evaluator:

    def __init__(self, metric=None):
        self.metric = metric or KeywordMetric()

    def evaluate(self, rag_service, dataset):
        scores = []

        for item in dataset:
            response = rag_service.ask(item["question"])
            score = self.metric.score(response["answer"], item["expected_keywords"])
            scores.append(score)

        return sum(scores) / len(scores) if scores else 0.0
