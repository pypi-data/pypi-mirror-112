#!/usr/bin/env python
# coding=utf-8


"""Tests for Padchest dataset"""

import os

import numpy
import nose.tools

from ..data.padchest import dataset
from .utils import rc_variable_set

def test_protocol_consistency():

    # Default protocol
    subset = dataset.subsets("idiap")
    nose.tools.eq_(len(subset), 1)

    assert "train" in subset
    nose.tools.eq_(len(subset["train"]), 96269)

    # Check labels
    for s in subset["train"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    # Cross-validation 2
    subset = dataset.subsets("tb_idiap")
    nose.tools.eq_(len(subset), 2)

    assert "train" in subset
    nose.tools.eq_(len(subset["train"]), 200)

    # Check labels
    for s in subset["train"]:
        assert s.label in [0.0, 1.0]

    assert "test" in subset
    nose.tools.eq_(len(subset["test"]), 50)

    # Check labels
    for s in subset["test"]:
        assert s.label in [0.0, 1.0]

    # Cross-validation 3
    subset = dataset.subsets("no_tb_idiap")
    nose.tools.eq_(len(subset), 2)

    assert "train" in subset
    nose.tools.eq_(len(subset["train"]), 54371)

    # Check labels
    for s in subset["train"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    assert "validation" in subset
    nose.tools.eq_(len(subset["validation"]), 4052)

    # Check labels
    for s in subset["validation"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

@rc_variable_set('bob.med.tb.padchest.datadir')
def test_check():
    nose.tools.eq_(dataset.check(), 0)