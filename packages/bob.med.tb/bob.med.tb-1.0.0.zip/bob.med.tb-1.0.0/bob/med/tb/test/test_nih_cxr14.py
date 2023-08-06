#!/usr/bin/env python
# coding=utf-8


"""Tests for NIH CXR14 dataset"""

import os

import numpy
import torch
import nose.tools

from ..data.nih_cxr14_re import dataset
from ..configs.datasets.nih_cxr14_re.default import dataset as dataset_2
from .utils import rc_variable_set


def test_protocol_consistency():

    # Default protocol
    subset = dataset.subsets("default")
    nose.tools.eq_(len(subset), 3)

    assert "train" in subset
    nose.tools.eq_(len(subset["train"]), 98637)
    for s in subset["train"]:
        assert s.key.startswith("images/000")

    assert "validation" in subset
    nose.tools.eq_(len(subset["validation"]), 6350)
    for s in subset["validation"]:
        assert s.key.startswith("images/000")

    assert "test" in subset
    nose.tools.eq_(len(subset["test"]), 4054)
    for s in subset["test"]:
        assert s.key.startswith("images/000")

    # Check labels
    for s in subset["train"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    for s in subset["validation"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    for s in subset["test"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    # Idiap protocol
    subset = dataset.subsets("idiap")
    nose.tools.eq_(len(subset), 3)

    assert "train" in subset
    nose.tools.eq_(len(subset["train"]), 98637)
    for s in subset["train"]:
        assert s.key.startswith("images/000")

    assert "validation" in subset
    nose.tools.eq_(len(subset["validation"]), 6350)
    for s in subset["validation"]:
        assert s.key.startswith("images/000")

    assert "test" in subset
    nose.tools.eq_(len(subset["test"]), 4054)
    for s in subset["test"]:
        assert s.key.startswith("images/000")

    # Check labels
    for s in subset["train"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    for s in subset["validation"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]

    for s in subset["test"]:
        for l in list(set(s.label)):
            assert l in [0.0, 1.0]


@rc_variable_set("bob.med.tb.nih_cxr14_re.datadir")
def test_loading():
    def _check_size(size):
        if size == (1024, 1024):
            return True
        return False

    def _check_sample(s):

        data = s.data
        assert isinstance(data, dict)
        nose.tools.eq_(len(data), 2)

        assert "data" in data
        nose.tools.ok_(_check_size(data["data"].size))  # Check size
        nose.tools.eq_(data["data"].mode, "RGB")  # Check colors

        assert "label" in data
        assert len(data["label"]) == 14  # Check labels

    limit = 30  # use this to limit testing to first images only, else None

    subset = dataset.subsets("default")
    for s in subset["train"][:limit]:
        _check_sample(s)
