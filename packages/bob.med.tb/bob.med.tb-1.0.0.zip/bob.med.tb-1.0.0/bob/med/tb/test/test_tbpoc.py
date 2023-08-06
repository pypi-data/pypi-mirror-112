#!/usr/bin/env python
# coding=utf-8


"""Tests for TB-POC dataset"""

import os

import numpy
import nose.tools

from ..data.tbpoc import dataset
from .utils import rc_variable_set

def test_protocol_consistency():

    # Cross-validation fold 0-6
    for f in range(7):
        subset = dataset.subsets("fold_"+str(f))
        nose.tools.eq_(len(subset), 3)

        assert "train" in subset
        nose.tools.eq_(len(subset["train"]), 292)
        for s in subset["train"]:
            assert s.key.upper().startswith("TBPOC_CXR/TBPOC-")

        assert "validation" in subset
        nose.tools.eq_(len(subset["validation"]), 74)
        for s in subset["validation"]:
            assert s.key.upper().startswith("TBPOC_CXR/TBPOC-")

        assert "test" in subset
        nose.tools.eq_(len(subset["test"]), 41)
        for s in subset["test"]:
            assert s.key.upper().startswith("TBPOC_CXR/TBPOC-")

        # Check labels
        for s in subset["train"]:
            assert s.label in [0.0, 1.0]
        
        for s in subset["validation"]:
            assert s.label in [0.0, 1.0]
        
        for s in subset["test"]:
            assert s.label in [0.0, 1.0]

    # Cross-validation fold 7-9
    for f in range(7, 10):
        subset = dataset.subsets("fold_"+str(f))
        nose.tools.eq_(len(subset), 3)

        assert "train" in subset
        nose.tools.eq_(len(subset["train"]), 293)
        for s in subset["train"]:
            assert s.key.upper().startswith("TBPOC_CXR/TBPOC-")

        assert "validation" in subset
        nose.tools.eq_(len(subset["validation"]), 74)
        for s in subset["validation"]:
            assert s.key.upper().startswith("TBPOC_CXR/TBPOC-")

        assert "test" in subset
        nose.tools.eq_(len(subset["test"]), 40)
        for s in subset["test"]:
            assert s.key.upper().startswith("TBPOC_CXR/TBPOC-")

        # Check labels
        for s in subset["train"]:
            assert s.label in [0.0, 1.0]
        
        for s in subset["validation"]:
            assert s.label in [0.0, 1.0]
        
        for s in subset["test"]:
            assert s.label in [0.0, 1.0]

@rc_variable_set('bob.med.tb.tbpoc.datadir')
def test_loading():

    image_size_portrait = (2048, 2500)
    image_size_landscape = (2500, 2048)

    def _check_size(size):
        if size == image_size_portrait:
            return True
        elif size == image_size_landscape:
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

    subset = dataset.subsets("fold_0")
    for s in subset["train"][:limit]:
        _check_sample(s)

@rc_variable_set('bob.med.tb.tbpoc.datadir')
def test_check():
    nose.tools.eq_(dataset.check(), 0)