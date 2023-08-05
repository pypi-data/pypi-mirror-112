# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Entry script that is invoked by the driver script from automl."""

from azureml.core.run import Run
from azureml.automl.dnn.nlp.classification.io.read import dataloader
from azureml.automl.dnn.nlp.classification.io.write.save_utils import save_score_script
from azureml.automl.dnn.nlp.classification.multiclass.trainer import TextClassificationTrainer
from azureml.automl.dnn.nlp.common.constants import OutputLiterals
from azureml.train.automl.runtime._entrypoints.utils.common import parse_settings


def run(automl_settings):
    """Invoke training by passing settings and write the output model.
    :param automl_settings: dictionary with automl settings
    """
    run = Run.get_context()
    workspace = run.experiment.workspace

    automl_settings_obj = parse_settings(run, automl_settings)  # Parse settings internally initializes logger

    dataset_id = automl_settings_obj.dataset_id
    if hasattr(automl_settings_obj, "validation_dataset_id"):
        validation_dataset_id = automl_settings_obj.validation_dataset_id
    else:
        validation_dataset_id = None

    training_set, validation_set, label_list = dataloader.dataset_loader(dataset_id, validation_dataset_id,
                                                                         workspace, multiclass_training=True)
    trainer_class = TextClassificationTrainer(label_list)
    trainer_class.train(training_set)
    if validation_set is not None:
        results = trainer_class.validate(validation_set)
        run.log('accuracy', results['eval_accuracy'])
    save_score_script(OutputLiterals.SCORE_SCRIPT_MULTICLASS)
