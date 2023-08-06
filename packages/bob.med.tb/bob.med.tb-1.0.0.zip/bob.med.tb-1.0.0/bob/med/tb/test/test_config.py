#!/usr/bin/env python
# coding=utf-8

import nose.tools

import torch
from torch.utils.data import ConcatDataset
import numpy as np
import contextlib
from bob.extension import rc

from .utils import rc_variable_set
from ..configs.datasets import get_samples_weights, get_positive_weights

from . import mock_dataset

# Download test data and get their location if needed
montgomery_datadir = mock_dataset()

# we only iterate over the first N elements at most - dataset loading has
# already been checked on the individual datset tests. Here, we are only
# testing for the extra tools wrapping the dataset
N = 10


@contextlib.contextmanager
def rc_context(**new_config):
    old_rc = rc.copy()
    rc.update(new_config)
    try:
        yield
    finally:
        rc.clear()
        rc.update(old_rc)


@rc_variable_set("bob.med.tb.montgomery.datadir")
def test_montgomery():

    def _check_subset(samples, size):
        nose.tools.eq_(len(samples), size)
        for s in samples[:N]:
            nose.tools.eq_(len(s), 3)
            assert isinstance(s[0], str) #key
            nose.tools.eq_(s[1].shape, (1, 512, 512)) #planes, height, width
            nose.tools.eq_(s[1].dtype, torch.float32)
            assert isinstance(s[2], int) #label
            assert s[1].max() <= 1.0
            assert s[1].min() >= 0.0

    from ..configs.datasets.montgomery.default import dataset

    nose.tools.eq_(len(dataset), 4)
    _check_subset(dataset["__train__"], 110)
    _check_subset(dataset["__valid__"], 110)
    _check_subset(dataset["train"], 110)
    _check_subset(dataset["test"], 28)

def test_get_samples_weights():

    # Temporarily modify Montgomery datadir
    new_value = {"bob.med.tb.montgomery.datadir": montgomery_datadir}
    with rc_context(**new_value):

        from ..configs.datasets.montgomery.default import dataset

        train_samples_weights = get_samples_weights(dataset['__train__']).numpy()

        unique, counts = np.unique(train_samples_weights, return_counts=True)
        
        np.testing.assert_equal(counts, np.array([51, 37]))
        np.testing.assert_equal(unique, np.array(1 / counts, dtype=np.float32))

@rc_variable_set('bob.med.tb.nih_cxr14_re.datadir')
def test_get_samples_weights_multi():

    from ..configs.datasets.nih_cxr14_re.default import dataset

    train_samples_weights = get_samples_weights(dataset['__train__']).numpy()
    
    np.testing.assert_equal(
        train_samples_weights, 
        np.ones(len(dataset['__train__']))
        )

def test_get_samples_weights_concat():

    # Temporarily modify Montgomery datadir
    new_value = {"bob.med.tb.montgomery.datadir": montgomery_datadir}
    with rc_context(**new_value):

        from ..configs.datasets.montgomery.default import dataset

        train_dataset = ConcatDataset((dataset['__train__'], dataset['__train__']))

        train_samples_weights = get_samples_weights(train_dataset).numpy()

        unique, counts = np.unique(train_samples_weights, return_counts=True)
        
        np.testing.assert_equal(counts, np.array([102, 74]))
        np.testing.assert_equal(unique, np.array(2 / counts, dtype=np.float32))

@rc_variable_set('bob.med.tb.nih_cxr14_re.datadir')
def test_get_samples_weights_multi_concat():

    from ..configs.datasets.nih_cxr14_re.default import dataset

    train_dataset = ConcatDataset((dataset['__train__'], dataset['__train__']))

    train_samples_weights = get_samples_weights(train_dataset).numpy()

    ref_samples_weights = np.concatenate((
        torch.full((len(dataset['__train__']),), 1. / len(dataset['__train__'])),
        torch.full((len(dataset['__train__']),), 1. / len(dataset['__train__'])),
        ))
    
    np.testing.assert_equal(train_samples_weights, ref_samples_weights)

def test_get_positive_weights():

    # Temporarily modify Montgomery datadir
    new_value = {"bob.med.tb.montgomery.datadir": montgomery_datadir}
    with rc_context(**new_value):

        from ..configs.datasets.montgomery.default import dataset

        train_positive_weights = get_positive_weights(dataset['__train__']).numpy()

        np.testing.assert_equal(
            train_positive_weights, 
            np.array([51.0/37.0], 
            dtype=np.float32)
            )

@rc_variable_set('bob.med.tb.nih_cxr14_re.datadir')
def test_get_positive_weights_multi():

    from ..configs.datasets.nih_cxr14_re.default import dataset

    train_positive_weights = get_positive_weights(dataset['__train__']).numpy()
    valid_positive_weights = get_positive_weights(dataset['__valid__']).numpy()

    assert torch.all(
        torch.eq(
            torch.FloatTensor(np.around(train_positive_weights, 4)),
            torch.FloatTensor(
                np.around(
                    [
                        0.9195434,
                        0.9462068,
                        0.8070095,
                        0.94879204,
                        0.767055,
                        0.8944615,
                        0.88212335,
                        0.8227136,
                        0.8943905,
                        0.8864118,
                        0.90026057,
                        0.8888551,
                        0.884739,
                        0.84540284,
                    ],
                    4,
                )
            ),
        )
    )

    assert torch.all(
        torch.eq(
            torch.FloatTensor(np.around(valid_positive_weights, 4)),
            torch.FloatTensor(
                np.around(
                    [
                        0.9366929,
                        0.9535433,
                        0.79543304,
                        0.9530709,
                        0.74834645,
                        0.88708663,
                        0.86661416,
                        0.81496066,
                        0.89480317,
                        0.8888189,
                        0.8933858,
                        0.89795274,
                        0.87181103,
                        0.8266142,
                    ],
                    4,
                )
            ),
        )
    )

def test_get_positive_weights_concat():

    # Temporarily modify Montgomery datadir
    new_value = {"bob.med.tb.montgomery.datadir": montgomery_datadir}
    with rc_context(**new_value):

        from ..configs.datasets.montgomery.default import dataset

        train_dataset = ConcatDataset((dataset['__train__'], dataset['__train__']))

        train_positive_weights = get_positive_weights(train_dataset).numpy()

        np.testing.assert_equal(
            train_positive_weights, 
            np.array([51.0/37.0], 
            dtype=np.float32)
            )

@rc_variable_set('bob.med.tb.nih_cxr14_re.datadir')
def test_get_positive_weights_multi_concat():

    from ..configs.datasets.nih_cxr14_re.default import dataset

    train_dataset = ConcatDataset((dataset['__train__'], dataset['__train__']))
    valid_dataset = ConcatDataset((dataset['__valid__'], dataset['__valid__']))

    train_positive_weights = get_positive_weights(train_dataset).numpy()
    valid_positive_weights = get_positive_weights(valid_dataset).numpy()

    assert torch.all(
        torch.eq(
            torch.FloatTensor(np.around(train_positive_weights, 4)),
            torch.FloatTensor(
                np.around(
                    [
                        0.9195434,
                        0.9462068,
                        0.8070095,
                        0.94879204,
                        0.767055,
                        0.8944615,
                        0.88212335,
                        0.8227136,
                        0.8943905,
                        0.8864118,
                        0.90026057,
                        0.8888551,
                        0.884739,
                        0.84540284,
                    ],
                    4,
                )
            ),
        )
    )

    assert torch.all(
        torch.eq(
            torch.FloatTensor(np.around(valid_positive_weights, 4)),
            torch.FloatTensor(
                np.around(
                    [
                        0.9366929,
                        0.9535433,
                        0.79543304,
                        0.9530709,
                        0.74834645,
                        0.88708663,
                        0.86661416,
                        0.81496066,
                        0.89480317,
                        0.8888189,
                        0.8933858,
                        0.89795274,
                        0.87181103,
                        0.8266142,
                    ],
                    4,
                )
            ),
        )
    )