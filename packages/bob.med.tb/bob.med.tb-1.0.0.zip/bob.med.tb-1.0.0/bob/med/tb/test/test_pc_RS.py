#!/usr/bin/env python
# coding=utf-8


"""Tests for Extended Padchest dataset"""

import os

import numpy
import nose.tools

from ..data.padchest_RS import dataset
from .utils import rc_variable_set

def test_protocol_consistency():

    # tb_idiap protocol
    subset = dataset.subsets("tb_idiap")
    nose.tools.eq_(len(subset), 3)

    assert "train" in subset
    nose.tools.eq_(len(subset["train"]), 160)

    assert "validation" in subset
    nose.tools.eq_(len(subset["validation"]), 40)

    assert "test" in subset
    nose.tools.eq_(len(subset["test"]), 50)

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
        assert data["label"] in [0.0, 1.0] # Check labels

    limit = 30  #use this to limit testing to first images only, else None

    subset = dataset.subsets("tb_idiap")
    for s in subset["train"][:limit]:
        _check_sample(s)