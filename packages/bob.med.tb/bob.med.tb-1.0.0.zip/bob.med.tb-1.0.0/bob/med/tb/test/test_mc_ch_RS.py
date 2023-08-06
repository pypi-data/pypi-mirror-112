#!/usr/bin/env python
# coding=utf-8


"""Tests for the aggregated Montgomery-Shenzhen dataset"""

import os

import numpy
import nose.tools

from ..configs.datasets.mc_ch_RS import default as mc_ch_RS
from ..configs.datasets.montgomery_RS import default as mc_RS
from ..configs.datasets.shenzhen_RS import default as ch_RS
from ..configs.datasets.mc_ch_RS import fold_0 as mc_ch_f0
from ..configs.datasets.montgomery_RS import fold_0 as mc_f0
from ..configs.datasets.shenzhen_RS import fold_0 as ch_f0
from ..configs.datasets.mc_ch_RS import fold_1 as mc_ch_f1
from ..configs.datasets.montgomery_RS import fold_1 as mc_f1
from ..configs.datasets.shenzhen_RS import fold_1 as ch_f1
from ..configs.datasets.mc_ch_RS import fold_2 as mc_ch_f2
from ..configs.datasets.montgomery_RS import fold_2 as mc_f2
from ..configs.datasets.shenzhen_RS import fold_2 as ch_f2
from ..configs.datasets.mc_ch_RS import fold_3 as mc_ch_f3
from ..configs.datasets.montgomery_RS import fold_3 as mc_f3
from ..configs.datasets.shenzhen_RS import fold_3 as ch_f3
from ..configs.datasets.mc_ch_RS import fold_4 as mc_ch_f4
from ..configs.datasets.montgomery_RS import fold_4 as mc_f4
from ..configs.datasets.shenzhen_RS import fold_4 as ch_f4
from ..configs.datasets.mc_ch_RS import fold_5 as mc_ch_f5
from ..configs.datasets.montgomery_RS import fold_5 as mc_f5
from ..configs.datasets.shenzhen_RS import fold_5 as ch_f5
from ..configs.datasets.mc_ch_RS import fold_6 as mc_ch_f6
from ..configs.datasets.montgomery_RS import fold_6 as mc_f6
from ..configs.datasets.shenzhen_RS import fold_6 as ch_f6
from ..configs.datasets.mc_ch_RS import fold_7 as mc_ch_f7
from ..configs.datasets.montgomery_RS import fold_7 as mc_f7
from ..configs.datasets.shenzhen_RS import fold_7 as ch_f7
from ..configs.datasets.mc_ch_RS import fold_8 as mc_ch_f8
from ..configs.datasets.montgomery_RS import fold_8 as mc_f8
from ..configs.datasets.shenzhen_RS import fold_8 as ch_f8
from ..configs.datasets.mc_ch_RS import fold_9 as mc_ch_f9
from ..configs.datasets.montgomery_RS import fold_9 as mc_f9
from ..configs.datasets.shenzhen_RS import fold_9 as ch_f9

def test_dataset_consistency():

    # Default protocol
    mc_ch_RS_dataset = mc_ch_RS.dataset
    assert isinstance(mc_ch_RS_dataset, dict)

    mc_RS_dataset = mc_RS.dataset
    ch_RS_dataset = ch_RS.dataset

    assert "train" in mc_ch_RS_dataset
    nose.tools.eq_(
        len(mc_ch_RS_dataset["train"]), 
        len(mc_RS_dataset["train"]) + len(ch_RS_dataset["train"])
        )

    assert "validation" in mc_ch_RS_dataset
    nose.tools.eq_(
        len(mc_ch_RS_dataset["validation"]), 
        len(mc_RS_dataset["validation"]) + len(ch_RS_dataset["validation"])
        )

    assert "test" in mc_ch_RS_dataset
    nose.tools.eq_(
        len(mc_ch_RS_dataset["test"]), 
        len(mc_RS_dataset["test"]) + len(ch_RS_dataset["test"])
        )

    # f0 protocol
    mc_ch_dataset = mc_ch_f0.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f0.dataset
    ch_dataset = ch_f0.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f1 protocol
    mc_ch_dataset = mc_ch_f1.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f1.dataset
    ch_dataset = ch_f1.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f2 protocol
    mc_ch_dataset = mc_ch_f2.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f2.dataset
    ch_dataset = ch_f2.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f3 protocol
    mc_ch_dataset = mc_ch_f3.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f3.dataset
    ch_dataset = ch_f3.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f4 protocol
    mc_ch_dataset = mc_ch_f4.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f4.dataset
    ch_dataset = ch_f4.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f5 protocol
    mc_ch_dataset = mc_ch_f5.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f5.dataset
    ch_dataset = ch_f5.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f6 protocol
    mc_ch_dataset = mc_ch_f6.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f6.dataset
    ch_dataset = ch_f6.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f7 protocol
    mc_ch_dataset = mc_ch_f7.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f7.dataset
    ch_dataset = ch_f7.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f8 protocol
    mc_ch_dataset = mc_ch_f8.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f8.dataset
    ch_dataset = ch_f8.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )

    # f9 protocol
    mc_ch_dataset = mc_ch_f9.dataset
    assert isinstance(mc_ch_dataset, dict)

    mc_dataset = mc_f9.dataset
    ch_dataset = ch_f9.dataset

    assert "train" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"])
        )

    assert "validation" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"])
        )

    assert "test" in mc_ch_dataset
    nose.tools.eq_(
        len(mc_ch_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"])
        )