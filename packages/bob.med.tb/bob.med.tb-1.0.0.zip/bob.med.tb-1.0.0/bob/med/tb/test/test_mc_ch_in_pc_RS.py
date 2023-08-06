#!/usr/bin/env python
# coding=utf-8


"""Tests for the aggregated Montgomery-Shenzhen-Indian-Padchest(TB) dataset"""

import os

import numpy
import nose.tools

from ..configs.datasets.mc_ch_in_pc_RS import default as mc_ch_in_pc
from ..configs.datasets.montgomery_RS import default as mc_RS
from ..configs.datasets.shenzhen_RS import default as ch_RS
from ..configs.datasets.indian_RS import default as in_RS
from ..configs.datasets.padchest_RS import tb_idiap as pc_RS

def test_dataset_consistency():

    # Default protocol
    mc_ch_in_pc_dataset = mc_ch_in_pc.dataset
    assert isinstance(mc_ch_in_pc_dataset, dict)

    mc_RS_dataset = mc_RS.dataset
    ch_RS_dataset = ch_RS.dataset
    in_RS_dataset = in_RS.dataset
    pc_RS_dataset = pc_RS.dataset

    assert "train" in mc_ch_in_pc_dataset
    nose.tools.eq_(
        len(mc_ch_in_pc_dataset["train"]), 
        len(mc_RS_dataset["train"]) + len(ch_RS_dataset["train"]) \
            + len(in_RS_dataset["train"]) + len(pc_RS_dataset["train"])
        )

    assert "validation" in mc_ch_in_pc_dataset
    nose.tools.eq_(
        len(mc_ch_in_pc_dataset["validation"]), 
        len(mc_RS_dataset["validation"]) + len(ch_RS_dataset["validation"]) \
            + len(in_RS_dataset["validation"])
            + len(pc_RS_dataset["validation"])
        )

    assert "test" in mc_ch_in_pc_dataset
    nose.tools.eq_(
        len(mc_ch_in_pc_dataset["test"]), 
        len(mc_RS_dataset["test"]) + len(ch_RS_dataset["test"]) \
            + len(in_RS_dataset["test"]) + len(pc_RS_dataset["test"])
        )