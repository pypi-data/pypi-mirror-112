# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Entry script that is invoked by the driver script from automl."""
import logging
import importlib

from azureml.automl.dnn.nlp.classification.io.read import dataloader
from azureml.automl.dnn.nlp.classification.io.write.save_utils import save_model, save_score_script
from azureml.automl.dnn.nlp.classification.multilabel.bert_class import BERTClass
from azureml.automl.dnn.nlp.classification.multilabel.trainer import PytorchTrainer
from azureml.automl.dnn.nlp.common.constants import OutputLiterals
from azureml.automl.dnn.nlp.classification.multilabel.distributed_trainer import HorovodDistributedTrainer
from azureml.automl.dnn.nlp.common import utils

from azureml.core.run import Run
from azureml.train.automl.runtime._entrypoints.utils import common

horovod_spec = importlib.util.find_spec("horovod")
has_horovod = horovod_spec is not None

_logger = logging.getLogger(__name__)


def run(automl_settings):
    """Invoke training by passing settings and write the output model.
    :param automl_settings: dictionary with automl settings
    """
    run = Run.get_context()
    workspace = run.experiment.workspace

    automl_settings_obj = common.parse_settings(run, automl_settings)  # Parse settings internally initializes logger

    is_gpu = automl_settings_obj.is_gpu if hasattr(automl_settings_obj, "is_gpu") else True  # Expect gpu by default
    dataset_id = automl_settings_obj.dataset_id
    if hasattr(automl_settings_obj, "validation_dataset_id"):
        valid_dataset_id = automl_settings_obj.validation_dataset_id
    else:
        valid_dataset_id = None

    training_set, validation_set, num_label_cols = dataloader.dataset_loader(dataset_id, valid_dataset_id,
                                                                             workspace, multiclass_training=False)

    if hasattr(automl_settings_obj, "enable_distributed_dnn_training") and \
            automl_settings_obj.enable_distributed_dnn_training is True and has_horovod:
        trainer = HorovodDistributedTrainer(BERTClass, num_label_cols)
    else:
        trainer = PytorchTrainer(BERTClass, num_label_cols, is_gpu)
    model = trainer.train(training_set)

    if utils.is_main_process() and validation_set is not None:
        accuracy, f1_score_micro, f1_score_macro = trainer.compute_metrics(validation_set)

        # Log metrics
        run.log('accuracy', accuracy)
        run.log('f1_score_micro', f1_score_micro)
        run.log('f1_score_macro', f1_score_macro)

        save_model(model)
        save_score_script(OutputLiterals.SCORE_SCRIPT)
