import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import numpy as np

from documents.services.document_search_service import DocumentSearchService


class DocumentSearchServiceTests(unittest.TestCase):
    def test_service_initializes_from_explicit_paths_and_returns_results(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            metadata_path = temp_path / "document_metadata.json"
            metadata_path.write_text(
                json.dumps(
                    [
                        {
                            "text": "Blood should be stored at 2-8°C.",
                            "page": 1,
                            "chunk": 1,
                            "filename": "guidelines.pdf",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            index_path = temp_path / "document.index"
            index_path.write_bytes(b"fake-index")

            fake_faiss = mock.Mock()
            fake_faiss.search.return_value = (
                np.array([0.25]),
                np.array([[0]]),
            )

            fake_embedding_service = mock.Mock()
            fake_embedding_service.generate_embedding.return_value = np.array([0.1, 0.2])

            with mock.patch(
                "documents.services.document_search_service.EmbeddingService",
                return_value=fake_embedding_service,
            ), mock.patch(
                "documents.services.document_search_service.FAISSService",
                return_value=fake_faiss,
            ):
                service = DocumentSearchService(
                    index_path=index_path,
                    metadata_path=metadata_path,
                )

                results = service.search("What is the blood storage temperature?", top_k=1)

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["text"], "Blood should be stored at 2-8°C.")
            self.assertEqual(results[0]["page"], 1)
            self.assertEqual(results[0]["chunk"], 1)
            self.assertEqual(results[0]["filename"], "guidelines.pdf")
            self.assertAlmostEqual(results[0]["score"], 0.25)
            fake_faiss.load_index.assert_called_once_with(index_path)


if __name__ == "__main__":
    unittest.main()
