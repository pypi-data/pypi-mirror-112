#!/usr/bin/env python
# coding=utf-8


"""Tests for the aggregated Montgomery-Shenzhen-Indian-Padchest dataset"""

import os

import numpy
import nose.tools

from ..configs.datasets.mc_ch_in_pc import default as mc_ch_in_pc
from ..configs.datasets.montgomery import default as mc
from ..configs.datasets.shenzhen import default as ch
from ..configs.datasets.indian import default as indian
from ..configs.datasets.padchest import tb_idiap as pc
from .utils import rc_variable_set

@rc_variable_set('bob.med.tb.montgomery.datadir')
@rc_variable_set('bob.med.tb.shenzhen.datadir')
@rc_variable_set('bob.med.tb.indian.datadir')
@rc_variable_set('bob.med.tb.padchest.datadir')
def test_dataset_consistency():

    # Default protocol
    mc_ch_in_pc_dataset = mc_ch_in_pc.dataset
    assert isinstance(mc_ch_in_pc_dataset, dict)

    mc_dataset = mc.dataset
    ch_dataset = ch.dataset
    in_dataset = indian.dataset
    pc_dataset = pc.dataset

    assert "train" in mc_ch_in_pc_dataset
    nose.tools.eq_(
        len(mc_ch_in_pc_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"]) + len(pc_dataset["train"])
        )

    assert "test" in mc_ch_in_pc_dataset
    nose.tools.eq_(
        len(mc_ch_in_pc_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"]) + len(pc_dataset["test"])
        )