import unittest

import torch

from fastNLP.core.batch import Batch
from fastNLP.core.dataset import DataSet, create_dataset_from_lists
from fastNLP.core.field import TextField, LabelField
from fastNLP.core.instance import Instance

raw_texts = ["i am a cat",
             "this is a test of new batch",
             "ha ha",
             "I am a good boy .",
             "This is the most beautiful girl ."
             ]
texts = [text.strip().split() for text in raw_texts]
labels = [0, 1, 0, 0, 1]

# prepare vocabulary
vocab = {}
for text in texts:
    for tokens in text:
        if tokens not in vocab:
            vocab[tokens] = len(vocab)


class TestCase1(unittest.TestCase):
    def test(self):
        data = DataSet()
        for text, label in zip(texts, labels):
            x = TextField(text, is_target=False)
            y = LabelField(label, is_target=True)
            ins = Instance(text=x, label=y)
            data.append(ins)

        # use vocabulary to index data
        data.index_field("text", vocab)

        # define naive sampler for batch class
        class SeqSampler:
            def __call__(self, dataset):
                return list(range(len(dataset)))

        # use batch to iterate dataset
        data_iterator = Batch(data, 2, SeqSampler(), False)
        for batch_x, batch_y in data_iterator:
            self.assertEqual(len(batch_x), 2)
            self.assertTrue(isinstance(batch_x, dict))
            self.assertTrue(isinstance(batch_x["text"], torch.LongTensor))
            self.assertTrue(isinstance(batch_y, dict))
            self.assertTrue(isinstance(batch_y["label"], torch.LongTensor))


class TestCase2(unittest.TestCase):
    def test(self):
        data = DataSet()
        for text in texts:
            x = TextField(text, is_target=False)
            ins = Instance(text=x)
            data.append(ins)
        data_set = create_dataset_from_lists(texts, vocab, has_target=False)
        self.assertTrue(type(data) == type(data_set))