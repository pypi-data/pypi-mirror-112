#!/usr/bin/env python
# coding=utf-8


"""Tests for HIV-TB_RS dataset"""

import os

import numpy
import nose.tools

from ..data.hivtb_RS import dataset
from .utils import rc_variable_set

def test_protocol_consistency():

    # Cross-validation fold 0-2
    for f in range(3):
        subset = dataset.subsets("fold_"+str(f))
        nose.tools.eq_(len(subset), 3)

        assert "train" in subset
        nose.tools.eq_(len(subset["train"]), 174)
        for s in subset["train"]:
            assert s.key.startswith("HIV-TB_Algorithm_study_X-rays/")

        assert "validation" in subset
        nose.tools.eq_(len(subset["validation"]), 44)
        for s in subset["validation"]:
            assert s.key.startswith("HIV-TB_Algorithm_study_X-rays/")

        assert "test" in subset
        nose.tools.eq_(len(subset["test"]), 25)
        for s in subset["test"]:
            assert s.key.startswith("HIV-TB_Algorithm_study_X-rays/")

        # Check labels
        for s in subset["train"]:
            assert s.label in [0.0, 1.0]
        
        for s in subset["validation"]:
            assert s.label in [0.0, 1.0]
        
        for s in subset["test"]:
            assert s.label in [0.0, 1.0]

    # Cross-validation fold 3-9
    for f in range(3, 10):
        subset = dataset.subsets("fold_"+str(f))
        nose.tools.eq_(len(subset), 3)

        assert "train" in subset
        nose.tools.eq_(len(subset["train"]), 175)
        for s in subset["train"]:
            assert s.key.startswith("HIV-TB_Algorithm_study_X-rays/")

        assert "validation" in subset
        nose.tools.eq_(len(subset["validation"]), 44)
        for s in subset["validation"]:
            assert s.key.startswith("HIV-TB_Algorithm_study_X-rays/")

        assert "test" in subset
        nose.tools.eq_(len(subset["test"]), 24)
        for s in subset["test"]:
            assert s.key.startswith("HIV-TB_Algorithm_study_X-rays/")

        # Check labels
        for s in subset["train"]:
            assert s.label in [0.0, 1.0]
        
        for s in subset["validation"]:
            assert s.label in [0.0, 1.0]
        
        for s in subset["test"]:
            assert s.label in [0.0, 1.0]

def test_loading():  

    def _check_sample(s):

        data = s.data

        assert isinstance(data, dict)
        nose.tools.eq_(len(data), 2)

        assert "data" in data
        nose.tools.eq_(len(data["data"]), 14) # Check radiological signs

        assert "label" in data
        assert data["label"] in [0, 1] # Check labels

    limit = 30  #use this to limit testing to first images only, else None

    subset = dataset.subsets("fold_0")
    for s in subset["train"][:limit]:
        _check_sample(s)