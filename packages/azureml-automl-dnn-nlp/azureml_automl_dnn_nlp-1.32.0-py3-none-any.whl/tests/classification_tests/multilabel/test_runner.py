import pytest
import unittest
from unittest.mock import patch
import importlib

from azureml.automl.dnn.nlp.classification.multilabel import runner

horovod_spec = importlib.util.find_spec("horovod")
has_horovod = horovod_spec is not None


class MockExperiment:

    def __init__(self):
        self.workspace = "some_workspace"


class MockRun:

    def __init__(self):
        self.experiment = MockExperiment()
        self.metrics = {}
        self.duplicate_metric_logged = False

    def log(self, key, value):
        if key in self.metrics.keys():
            self.duplicate_metric_logged = True
        self.metrics[key] = value


class MockTrainer:

    def __init__(self):
        self.n_train_called = 0
        self.train_called_last_with = None
        self.n_compute_called = 0
        self.compute_called_with = None

    def train(self, train_dataset):
        self.n_train_called = self.n_train_called + 1
        self.train_called_last_with = train_dataset
        return "some_model"

    def compute_metrics(self, valid_dataset):
        self.n_compute_called = self.n_compute_called + 1
        self.compute_called_with = valid_dataset
        return 0.5, 0.6, 0.7


class MockAutoMLSettings:
    def __init__(self, distributed):
        self.is_gpu = True
        self.dataset_id = "some_dataset_id"
        self.validation_dataset_id = "some_validation_dataset_id"
        self.enable_distributed_dnn_training = distributed


def test_runner():
    automl_settings = {"is_gpu": True,
                       "dataset_id": "some_training_set",
                       "validation_dataset_id": "some_validation_set",
                       "enable_distributed_dnn_training": False}

    mock_run = MockRun()
    mocked_trainer = MockTrainer()

    with patch("azureml.core.run.Run.get_context", return_value=mock_run):
        dataset_loader_patch = "azureml.automl.dnn.nlp.classification.io.read.dataloader.dataset_loader"
        dataset_loader_return = ("some_training_set", "some_validation_set", 3)
        with patch(dataset_loader_patch, return_value=dataset_loader_return):
            parse_settings_path = "azureml.train.automl.runtime._entrypoints.utils.common.parse_settings"
            with patch(parse_settings_path, return_value=MockAutoMLSettings(False)):
                trainer_init = "azureml.automl.dnn.nlp.classification.multilabel.runner.PytorchTrainer"
                with patch(trainer_init, return_value=mocked_trainer):
                    runner.run(automl_settings)

    assert mocked_trainer.train_called_last_with == "some_training_set"
    assert mocked_trainer.compute_called_with == "some_validation_set"

    assert mocked_trainer.n_train_called == 1
    assert mocked_trainer.n_compute_called == 1

    assert mock_run.metrics["accuracy"] == 0.5
    assert mock_run.metrics["f1_score_micro"] == 0.6
    assert mock_run.metrics["f1_score_macro"] == 0.7


@unittest.skipIf(not has_horovod, "Horovod not installed")
@pytest.mark.parametrize('is_main_process, enable_distributed',
                         [pytest.param(True, True),
                          pytest.param(False, True),
                          pytest.param(True, False)])
def test_runner_distributed(is_main_process, enable_distributed):
    automl_settings = {"is_gpu": True,
                       "dataset_id": "some_training_set",
                       "validation_dataset_id": "some_validation_set",
                       "enable_distributed_dnn_training": True}

    mock_run = MockRun()
    mocked_pytorch_trainer = MockTrainer()
    mocked_distributed_trainer = MockTrainer()

    with patch("azureml.core.run.Run.get_context", return_value=mock_run):
        dataset_loader_patch = "azureml.automl.dnn.nlp.classification.io.read.dataloader.dataset_loader"
        dataset_loader_return = ("some_training_set", "some_validation_set", 3)
        with patch(dataset_loader_patch, return_value=dataset_loader_return):
            parse_settings_path = "azureml.train.automl.runtime._entrypoints.utils.common.parse_settings"
            with patch(parse_settings_path, return_value=MockAutoMLSettings(enable_distributed)):
                trainer_init = "azureml.automl.dnn.nlp.classification.multilabel.runner.PytorchTrainer"
                distributed_init = "azureml.automl.dnn.nlp.classification.multilabel.runner.HorovodDistributedTrainer"
                with patch("azureml.automl.dnn.nlp.common.utils.is_main_process", return_value=is_main_process):
                    with patch(trainer_init, return_value=mocked_pytorch_trainer):
                        with patch(distributed_init, return_value=mocked_distributed_trainer):
                            runner.run(automl_settings)

    if enable_distributed:
        assert mocked_pytorch_trainer.n_train_called == 0
        assert mocked_pytorch_trainer.n_compute_called == 0
        assert mocked_distributed_trainer.n_train_called == 1

        if is_main_process:
            assert mocked_distributed_trainer.n_compute_called == 1
        else:
            assert mocked_distributed_trainer.n_compute_called == 0
    else:
        assert mocked_pytorch_trainer.n_train_called == 1
        assert mocked_pytorch_trainer.n_compute_called == 1
        assert mocked_distributed_trainer.n_train_called == 0
        assert mocked_distributed_trainer.n_compute_called == 0
