import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from azureml.automl.dnn.nlp.ner.inference.score import score
from azureml.data import FileDataset
from mocks import MockRun


class NERScoreTests(unittest.TestCase):
    """Tests for NER scorer."""

    @patch("azureml.automl.dnn.nlp.ner.inference.score.open")
    @patch("azureml.automl.dnn.nlp.ner.inference.score.DatasetWrapper")
    @patch("azureml.automl.dnn.nlp.ner.inference.score.Trainer")
    @patch("azureml.automl.dnn.nlp.ner.inference.score.get_labels")
    @patch("azureml.core.Dataset.get_by_id")
    @patch("azureml.automl.dnn.nlp.ner.inference.score.AutoModelForTokenClassification")
    @patch("azureml.automl.dnn.nlp.ner.inference.score.AutoTokenizer")
    @patch("azureml.automl.dnn.nlp.ner.inference.score.AutoConfig")
    @patch("azureml.automl.dnn.nlp.common.utils.Run")
    def test_score(
            self, run_mock, config_mock, tokenizer_mock, model_mock, get_by_id_mock,
            get_labels_mock, trainer_mock, dataset_mock, open_mock
    ):
        mock_run = MockRun()
        run_mock.get_context.return_value = mock_run
        run_mock.download_file.return_value = None
        config_mock.from_pretrained.return_value = MagicMock()
        tokenizer_mock.from_pretrained.return_value = MagicMock()
        model_mock.from_pretrained.return_value = MagicMock()
        dataset_mock = MagicMock(FileDataset)
        dataset_mock.download.return_value = MagicMock()
        dataset_mock.to_path.return_value = ["/test.text"]
        get_by_id_mock.return_value = dataset_mock

        label_list = ["O", "B-MISC", "I-MISC", "B-PER"]
        get_labels_mock.return_value = label_list

        trainer = MagicMock()
        batch_size = 1
        seq_len = 3
        predictions = np.random.rand(batch_size, seq_len, len(label_list))
        label_ids = np.random.randint(0, high=len(label_list), size=(batch_size, seq_len))
        trainer.predict.return_value = predictions, label_ids, {"metrics": 0.5}
        trainer.is_world_process_zero.return_value = True
        trainer_mock.return_value = trainer
        open_mock.return_value = MagicMock()

        score(
            mock_run.id,
            "mock_dataset_id",
            "ner_data",
            "output_dir"
        )
        self.assertEqual(open_mock.call_count, 3)


if __name__ == "__main__":
    unittest.main()
