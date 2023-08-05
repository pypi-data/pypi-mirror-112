from datasets import Dataset
import numpy as np
import pytest
from transformers import AutoTokenizer, EvalPrediction

from azureml.automl.dnn.nlp.classification.common.constants import (
    DatasetLiterals,
    ModelNames,
    MultiClassParameters
)
from azureml.automl.dnn.nlp.classification.io.read.dataloader import _concat_text_and_preserve_label
from azureml.automl.dnn.nlp.classification.multiclass.utils import compute_metrics, preprocess_function


@pytest.mark.usefixtures('MulticlassDatasetTester')
@pytest.mark.parametrize('multiple_text_column', [True, False])
@pytest.mark.parametrize('include_label_col', [True, False])
class TestTextClassificationTrainerTests:
    """Tests for utility functions for multi-class text classification."""
    def test_preprocess_function(self, MulticlassDatasetTester, include_label_col):
        input_df = MulticlassDatasetTester.get_data().copy()
        input_set = Dataset.from_pandas(_concat_text_and_preserve_label(input_df))
        if include_label_col:
            label_list = input_set.unique(DatasetLiterals.LABEL_COLUMN)
        else:
            label_list = None
        fn_kwargs = {'tokenizer': AutoTokenizer.from_pretrained(ModelNames.BERT_BASE_CASED, use_fast=True),
                     'padding': MultiClassParameters.MAX_LEN_PADDING,
                     'max_seq_length': MultiClassParameters.MAX_SEQ_LENGTH,
                     'label_to_id': {v: i for i, v in enumerate(label_list)} if label_list else label_list}
        preproc_data = input_set.map(preprocess_function, batched=True, fn_kwargs=fn_kwargs)
        assert all(len(example['attention_mask']) == MultiClassParameters.MAX_SEQ_LENGTH and
                   len(example['input_ids']) == MultiClassParameters.MAX_SEQ_LENGTH and
                   len(example['token_type_ids']) == MultiClassParameters.MAX_SEQ_LENGTH for example in preproc_data)

    def test_compute_metrics(self, MulticlassDatasetTester, include_label_col):
        input_df = MulticlassDatasetTester.get_data().copy()
        input_set = Dataset.from_pandas(_concat_text_and_preserve_label(input_df))
        if include_label_col:
            label_list = input_set.unique(DatasetLiterals.LABEL_COLUMN)
        else:
            label_list = ['ABC', 'PQR', 'XYZ']
        num_examples = len(input_df)
        predictions = np.random.rand(num_examples, len(label_list))
        label_ids = np.random.randint(0, high=len(label_list), size=num_examples)
        metrics = compute_metrics(EvalPrediction(predictions, label_ids))
        assert metrics['accuracy'] >= 0.0
