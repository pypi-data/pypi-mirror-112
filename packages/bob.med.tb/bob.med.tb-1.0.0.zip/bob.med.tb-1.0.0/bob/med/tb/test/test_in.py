#!/usr/bin/env python
# coding=utf-8


"""Tests for Indian dataset"""

import os

import numpy
import nose.tools

from ..data.indian import dataset
from .utils import rc_variable_set

def test_protocol_consistency():

    # Default protocol
    subset = dataset.subsets("default")
    nose.tools.eq_(len(subset), 3)

    assert "train" in subset
    nose.tools.eq_(len(subset["train"]), 83)
    for s in subset["train"]:
        assert s.key.startswith("DatasetA/Training/")

    assert "validation" in subset
    nose.tools.eq_(len(subset["validation"]), 20)
    for s in subset["validation"]:
        assert s.key.startswith("DatasetA/Training/")

    assert "test" in subset
    nose.tools.eq_(len(subset["test"]), 52)
    for s in subset["test"]:
        assert s.key.startswith("DatasetA/Testing/")

    # Check labels
    for s in subset["train"]:
        assert s.label in [0.0, 1.0]
    
    for s in subset["validation"]:
        assert s.label in [0.0, 1.0]
    
    for s in subset["test"]:
        assert s.label in [0.0, 1.0]

    # Cross-validation fold 0-4
    for f in range(5):
        subset = dataset.subsets("fold_"+str(f))
        nose.tools.eq_(len(subset), 3)

        assert "train" in subset
        nose.tools.eq_(len(subset["train"]), 111)
        for s in subset["train"]:
            assert s.key.startswith("DatasetA")

        assert "validation" in subset
        nose.tools.eq_(len(subset["validation"]), 28)
        for s in subset["validation"]:
            assert s.key.startswith("DatasetA")

        assert "test" in subset
        nose.tools.eq_(len(subset["test"]), 16)
        for s in subset["test"]:
            assert s.key.startswith("DatasetA")

        # Check labels
        for s in subset["train"]:
            assert s.label in [0.0, 1.0]
        
        for s in subset["validation"]:
            assert s.label in [0.0, 1.0]
        
        for s in subset["test"]:
            assert s.label in [0.0, 1.0]

    # Cross-validation fold 5-9
    for f in range(5, 10):
        subset = dataset.subsets("fold_"+str(f))
        nose.tools.eq_(len(subset), 3)

        assert "train" in subset
        nose.tools.eq_(len(subset["train"]), 112)
        for s in subset["train"]:
            assert s.key.startswith("DatasetA")

        assert "validation" in subset
        nose.tools.eq_(len(subset["validation"]), 28)
        for s in subset["validation"]:
            assert s.key.startswith("DatasetA")

        assert "test" in subset
        nose.tools.eq_(len(subset["test"]), 15)
        for s in subset["test"]:
            assert s.key.startswith("DatasetA")

        # Check labels
        for s in subset["train"]:
            assert s.label in [0.0, 1.0]
        
        for s in subset["validation"]:
            assert s.label in [0.0, 1.0]
        
        for s in subset["test"]:
            assert s.label in [0.0, 1.0]

@rc_variable_set('bob.med.tb.indian.datadir')
def test_loading():

    def _check_size(size):
        if size[0] >= 1024 and size[0] <= 2320 and size[1] >= 1024 and size[1] <= 2828:
            return True
        return False    

    def _check_sample(s):

        data = s.data
        assert isinstance(data, dict)
        nose.tools.eq_(len(data), 2)

        assert "data" in data
        nose.tools.ok_(_check_size(data["data"].size)) # Check size
        nose.tools.eq_(data["data"].mode, "L") # Check colors

        assert "label" in data
        assert data["label"] in [0, 1] # Check labels

    limit = 30  #use this to limit testing to first images only, else None

    subset = dataset.subsets("default")
    for s in subset["train"][:limit]:
        _check_sample(s)

@rc_variable_set('bob.med.tb.indian.datadir')
def test_check():
    nose.tools.eq_(dataset.check(), 0)