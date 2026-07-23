import time

from evaluation.evaluator import Evaluator


class Benchmark:

    def run(self, rag_service, dataset):
        start = time.time()

        score = Evaluator().evaluate(rag_service, dataset)

        end = time.time()

        return {
            "score": score,
            "latency": end - start,
        }
