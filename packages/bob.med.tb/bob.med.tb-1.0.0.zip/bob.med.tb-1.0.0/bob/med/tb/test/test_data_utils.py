#!/usr/bin/env python
# coding=utf-8


"""Tests for data utils"""

import os
import copy

import numpy
import nose.tools

from ..configs.datasets.montgomery_RS import fold_0 as mc
from .utils import rc_variable_set

@rc_variable_set('bob.med.tb.montgomery.datadir')
def test_random_permute():

    test_set = mc.dataset["test"]

    original = numpy.zeros((len(test_set)))
    
    # Store second feature values
    for k, s in enumerate(test_set._samples):
        original[k] = s.data['data'][2]

    # Permute second feature values
    test_set.random_permute(2)

    nb_equal = 0.0
    
    for k, s in enumerate(test_set._samples):
        
        if original[k] == s.data['data'][2]:
            nb_equal += 1
        else:
            # Value is somewhere else in array
            assert s.data['data'][2] in original
    
    # Max 30% of samples have not changed
    assert nb_equal/len(test_set) < 0.30
