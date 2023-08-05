from datasets import Dataset
import pytest
from unittest.mock import MagicMock, patch

from azureml.automl.dnn.nlp.classification.common.constants import DatasetLiterals
from azureml.automl.dnn.nlp.classification.io.read.dataloader import _concat_text_and_preserve_label
from azureml.automl.dnn.nlp.classification.io.read.pytorch_dataset_wrapper import PyTorchMulticlassDatasetWrapper
from azureml.automl.dnn.nlp.classification.multiclass.trainer import TextClassificationTrainer


@pytest.mark.usefixtures('MulticlassDatasetTester')
@pytest.mark.parametrize('multiple_text_column', [True, False])
@pytest.mark.parametrize('include_label_col', [True])
class TestTextClassificationTrainerTests:
    """Tests for Text Classification trainer."""

    @patch("azureml.automl.dnn.nlp.classification.multiclass.trainer.AutoModelForSequenceClassification")
    @patch("azureml.automl.dnn.nlp.classification.multiclass.trainer.Trainer")
    @patch("azureml.automl.dnn.nlp.classification.multiclass.trainer.AutoMLPretrainedDNNProvider")
    def test_train_valid(self, provider_mock, trainer_mock, auto_model_mock, MulticlassDatasetTester):
        train_df = MulticlassDatasetTester.get_data().copy()
        validation_df = MulticlassDatasetTester.get_data().copy()
        training_set = Dataset.from_pandas(_concat_text_and_preserve_label(train_df))
        validation_set = Dataset.from_pandas(_concat_text_and_preserve_label(validation_df))
        label_list = training_set.unique(DatasetLiterals.LABEL_COLUMN)
        training_set = PyTorchMulticlassDatasetWrapper(training_set, label_list)
        validation_set = PyTorchMulticlassDatasetWrapper(validation_set, label_list)

        # provider mock
        provider = MagicMock()
        provider.get_model_dirname.return_value = "data/bert-base-cased"
        provider_mock.return_value = provider

        auto_model = MagicMock()
        auto_model.from_pretrained.return_value = MagicMock()
        auto_model_mock.return_value = auto_model

        trainer_multiclass = TextClassificationTrainer(label_list)

        mock_trainer = MagicMock()
        mock_trainer.train.return_value = MagicMock()
        mock_trainer.evaluate.return_value = {"key": "val"}
        trainer_mock.return_value = mock_trainer

        trainer_multiclass.train(training_set)

        # train function
        trainer_multiclass.trainer.train.assert_called_once()
        trainer_multiclass.trainer.save_model.assert_called_once()
        trainer_multiclass.trainer.save_state.assert_called_once()

        # validate function
        results = trainer_multiclass.validate(validation_set)
        trainer_multiclass.trainer.evaluate.assert_called_once()
        assert results is not None
        assert "key" in results.keys()
        assert trainer_multiclass.trainer.log_metrics.call_count == 2
        assert trainer_multiclass.trainer.save_metrics.call_count == 2
