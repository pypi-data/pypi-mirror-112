# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Scoring functions that can load a serialized model and predict."""

from datasets import Dataset
import logging
import numpy as np
import os
import pandas as pd
import scipy
from transformers import (
    AutoConfig,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    default_data_collator,
)
from typing import Any, List, Tuple

from azureml.automl.dnn.nlp.classification.common.constants import (
    DatasetLiterals,
    ModelNames,
    MultiClassInferenceLiterals
)
from azureml.automl.dnn.nlp.classification.io.read.dataloader import _concat_text_and_preserve_label
from azureml.automl.dnn.nlp.classification.io.read.pytorch_dataset_wrapper import PyTorchMulticlassDatasetWrapper
from azureml.automl.dnn.nlp.classification.multiclass.utils import compute_metrics
from azureml.automl.dnn.nlp.common.constants import (
    OutputLiterals,
    Warnings
)
from azureml.core import Dataset as AmlDataset
from azureml.core.run import Run

logger = logging.getLogger(__name__)


class MulticlassInferencer:
    """Class to perform inferencing using training runId and on an unlabeled dataset"""

    def __init__(self,
                 run: Run,
                 device: str):
        """Function to initialize the inferencing object

        :param: Run object
        :param device: device to be used for inferencing
        """
        self.run_object = run
        self.device = device

        if self.device == "cpu":
            logger.warning(Warnings.CPU_DEVICE_WARNING)

        self.workspace = self.run_object.experiment.workspace

    def download_file(
            self,
            run: Run,
            log_friendly_file_name: str,
            path: str,
            file_name: str
    ) -> None:
        """Downloads files associated with the run.

        :param run: run context of the run that produced the model
        :param log_friendly_file_name: file name for artifact to log
        :param path: artifacts directory path
        :file_name: file name for artifact
        """
        logger.info("Start downloading {} artifact".format(log_friendly_file_name))
        run.download_file(os.path.join(path, file_name), output_file_path=file_name)
        logger.info("Finished downloading CONFIG artifact")

    def load_training_artifacts(
            self,
            run: Run,
            artifacts_dir: str
    ) -> Tuple[AutoModelForSequenceClassification, AutoTokenizer, List[Any]]:
        """Load the training artifacts.

        :param run: run context of the run that produced the model
        :param artifacts_dir: artifacts directory
        :return: returns the model, tokenizer and config from the model's training
        """
        logger.info("Start fetching model from artifacts")
        self.download_file(run, "TOKENIZER", artifacts_dir, MultiClassInferenceLiterals.TOKENIZER_FILE_NAME)
        self.download_file(run, "MODEL", artifacts_dir, MultiClassInferenceLiterals.MODEL_FILE_NAME)
        self.download_file(run, "TRAINING_ARGS", artifacts_dir, MultiClassInferenceLiterals.TRAINING_ARGS)
        self.download_file(run, "LABEL_LIST", artifacts_dir, MultiClassInferenceLiterals.LABEL_LIST)
        model_name_or_path = ModelNames.BERT_BASE_CASED
        # TODO: figure out why the tokenizer.config isn't working out
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        label_list = np.load(MultiClassInferenceLiterals.LABEL_LIST)
        config = AutoConfig.from_pretrained(model_name_or_path, num_labels=len(label_list))
        model = AutoModelForSequenceClassification.from_pretrained(MultiClassInferenceLiterals.MODEL_FILE_NAME,
                                                                   config=config)
        logger.info("Training artifacts restored successfully")
        return model, tokenizer, label_list

    def predict(self,
                trainer: Trainer,
                test_dataset: PyTorchMulticlassDatasetWrapper,
                df: pd.DataFrame,
                label_list: List[Any]) -> pd.DataFrame:
        """Generate predictions using model

        :param model: Trained model
        :param vectorizer: vectorizer
        :param df: DataFrame to make predictions on
        :param inference_data_loader: dataloader
        :return: Dataframe with predictions
        """
        predictions = trainer.predict(test_dataset=test_dataset).predictions
        preds = np.argmax(predictions, axis=1)
        probas = scipy.special.softmax(predictions, axis=1)
        pred_probas = np.amax(probas, axis=1)
        predicted_labels = [label_list[item] for item in preds]
        predicted_df = df.copy()
        if trainer.is_world_process_zero():
            predicted_df[DatasetLiterals.LABEL_COLUMN] = np.array(predicted_labels)
            predicted_df[DatasetLiterals.LABEL_CONFIDENCE] = np.array(pred_probas)

        return predicted_df

    def score(self, input_dataset_id: str) -> pd.DataFrame:
        """Generate predictions from input files.

        :param input_dataset_id: The input dataset id
        :return: Dataframe with predictions
        """
        model, tokenizer, label_list = self.load_training_artifacts(self.run_object, OutputLiterals.OUTPUT_DIR)
        trainer = Trainer(
            model=model,
            compute_metrics=compute_metrics,
            tokenizer=tokenizer,
            data_collator=default_data_collator,
        )
        # Fetch AmlDataset object
        ds = AmlDataset.get_by_id(self.workspace, input_dataset_id)
        logger.info("Type of input Dataset is: {}".format(type(ds)))

        # Convert AmlDataset to dataframe and obtain dataloader
        df = ds.to_pandas_dataframe()
        inference_set = Dataset.from_pandas(_concat_text_and_preserve_label(df))
        if DatasetLiterals.LABEL_COLUMN in inference_set.column_names:
            inference_set = inference_set.remove_columns(DatasetLiterals.LABEL_COLUMN)
        inference_data = PyTorchMulticlassDatasetWrapper(inference_set, label_list, infer_data=True)
        return self.predict(trainer, inference_data, df, label_list)
