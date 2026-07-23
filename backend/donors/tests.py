import importlib
import sys
from unittest.mock import patch

from django.test import SimpleTestCase

from donors.management.commands.generate_embeddings import Command as GenerateEmbeddingsCommand
from donors.signals import donor_deleted, donor_saved


class DonorSignalTests(SimpleTestCase):
    @patch("donors.signals.SingleEmbeddingGenerator")
    def test_donor_saved_creates_embedding_for_new_donor(self, mock_generator):
        generator = mock_generator.return_value
        donor_saved(None, None, created=True)

        generator.create.assert_called_once()
        generator.update.assert_not_called()

    @patch("donors.signals.SingleEmbeddingGenerator")
    def test_donor_saved_updates_embedding_for_existing_donor(self, mock_generator):
        generator = mock_generator.return_value
        donor_saved(None, None, created=False)

        generator.update.assert_called_once()
        generator.create.assert_not_called()

    @patch("donors.signals.SingleEmbeddingGenerator")
    def test_donor_deleted_removes_embedding(self, mock_generator):
        generator = mock_generator.return_value

        donor_deleted(None, None)

        generator.delete.assert_called_once()


class GenerateEmbeddingsCommandTests(SimpleTestCase):
    @patch("donors.management.commands.generate_embeddings.Embeddinggenerator")
    def test_generate_embeddings_command_instantiates_generator(self, mock_embedding_generator):
        generator = mock_embedding_generator.return_value
        command = GenerateEmbeddingsCommand()

        command.handle()

        mock_embedding_generator.assert_called_once_with()
        generator.generate.assert_called_once_with()


class EmbeddingImportTests(SimpleTestCase):
    def test_single_embedding_generator_imports_without_sentence_transformers(self):
        sys.modules.pop("embeddings.single_embedding", None)
        sys.modules.pop("embeddings.embedding_service", None)

        original_import = __import__

        def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "sentence_transformers":
                raise ImportError("No module named 'sentence_transformers'")
            return original_import(name, globals, locals, fromlist, level)

        with patch("builtins.__import__", side_effect=guarded_import):
            module = importlib.import_module("embeddings.single_embedding")

        self.assertTrue(hasattr(module, "SingleEmbeddingGenerator"))
