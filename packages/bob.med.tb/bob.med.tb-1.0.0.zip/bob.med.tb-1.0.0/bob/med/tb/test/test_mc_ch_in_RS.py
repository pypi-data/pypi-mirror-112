#!/usr/bin/env python
# coding=utf-8


"""Tests for the aggregated Montgomery-Shenzhen-Indian dataset"""

import os

import numpy
import nose.tools

from ..configs.datasets.mc_ch_in_RS import default as mc_ch_in_RS
from ..configs.datasets.montgomery_RS import default as mc_RS
from ..configs.datasets.shenzhen_RS import default as ch_RS
from ..configs.datasets.indian_RS import default as indian_RS
from ..configs.datasets.mc_ch_in_RS import fold_0 as mc_ch_in_f0
from ..configs.datasets.montgomery_RS import fold_0 as mc_f0
from ..configs.datasets.shenzhen_RS import fold_0 as ch_f0
from ..configs.datasets.indian_RS import fold_0 as indian_f0
from ..configs.datasets.mc_ch_in_RS import fold_1 as mc_ch_in_f1
from ..configs.datasets.montgomery_RS import fold_1 as mc_f1
from ..configs.datasets.shenzhen_RS import fold_1 as ch_f1
from ..configs.datasets.indian_RS import fold_1 as indian_f1
from ..configs.datasets.mc_ch_in_RS import fold_2 as mc_ch_in_f2
from ..configs.datasets.montgomery_RS import fold_2 as mc_f2
from ..configs.datasets.shenzhen_RS import fold_2 as ch_f2
from ..configs.datasets.indian_RS import fold_2 as indian_f2
from ..configs.datasets.mc_ch_in_RS import fold_3 as mc_ch_in_f3
from ..configs.datasets.montgomery_RS import fold_3 as mc_f3
from ..configs.datasets.shenzhen_RS import fold_3 as ch_f3
from ..configs.datasets.indian_RS import fold_3 as indian_f3
from ..configs.datasets.mc_ch_in_RS import fold_4 as mc_ch_in_f4
from ..configs.datasets.montgomery_RS import fold_4 as mc_f4
from ..configs.datasets.shenzhen_RS import fold_4 as ch_f4
from ..configs.datasets.indian_RS import fold_4 as indian_f4
from ..configs.datasets.mc_ch_in_RS import fold_5 as mc_ch_in_f5
from ..configs.datasets.montgomery_RS import fold_5 as mc_f5
from ..configs.datasets.shenzhen_RS import fold_5 as ch_f5
from ..configs.datasets.indian_RS import fold_5 as indian_f5
from ..configs.datasets.mc_ch_in_RS import fold_6 as mc_ch_in_f6
from ..configs.datasets.montgomery_RS import fold_6 as mc_f6
from ..configs.datasets.shenzhen_RS import fold_6 as ch_f6
from ..configs.datasets.indian_RS import fold_6 as indian_f6
from ..configs.datasets.mc_ch_in_RS import fold_7 as mc_ch_in_f7
from ..configs.datasets.montgomery_RS import fold_7 as mc_f7
from ..configs.datasets.shenzhen_RS import fold_7 as ch_f7
from ..configs.datasets.indian_RS import fold_7 as indian_f7
from ..configs.datasets.mc_ch_in_RS import fold_8 as mc_ch_in_f8
from ..configs.datasets.montgomery_RS import fold_8 as mc_f8
from ..configs.datasets.shenzhen_RS import fold_8 as ch_f8
from ..configs.datasets.indian_RS import fold_8 as indian_f8
from ..configs.datasets.mc_ch_in_RS import fold_9 as mc_ch_in_f9
from ..configs.datasets.montgomery_RS import fold_9 as mc_f9
from ..configs.datasets.shenzhen_RS import fold_9 as ch_f9
from ..configs.datasets.indian_RS import fold_9 as indian_f9

def test_dataset_consistency():

    # Default protocol
    mc_ch_in_RS_dataset = mc_ch_in_RS.dataset
    assert isinstance(mc_ch_in_RS_dataset, dict)

    mc_RS_dataset = mc_RS.dataset
    ch_RS_dataset = ch_RS.dataset
    in_RS_dataset = indian_RS.dataset

    assert "train" in mc_ch_in_RS_dataset
    nose.tools.eq_(
        len(mc_ch_in_RS_dataset["train"]), 
        len(mc_RS_dataset["train"]) + len(ch_RS_dataset["train"]) \
            + len(in_RS_dataset["train"])
        )

    assert "validation" in mc_ch_in_RS_dataset
    nose.tools.eq_(
        len(mc_ch_in_RS_dataset["validation"]), 
        len(mc_RS_dataset["validation"]) + len(ch_RS_dataset["validation"]) \
            + len(in_RS_dataset["validation"])
        )

    assert "test" in mc_ch_in_RS_dataset
    nose.tools.eq_(
        len(mc_ch_in_RS_dataset["test"]), 
        len(mc_RS_dataset["test"]) + len(ch_RS_dataset["test"]) \
            + len(in_RS_dataset["test"])
        )

    # Fold 0
    mc_ch_in_dataset = mc_ch_in_f0.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f0.dataset
    ch_dataset = ch_f0.dataset
    in_dataset = indian_f0.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 1
    mc_ch_in_dataset = mc_ch_in_f1.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f1.dataset
    ch_dataset = ch_f1.dataset
    in_dataset = indian_f1.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 2
    mc_ch_in_dataset = mc_ch_in_f2.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f2.dataset
    ch_dataset = ch_f2.dataset
    in_dataset = indian_f2.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 3
    mc_ch_in_dataset = mc_ch_in_f3.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f3.dataset
    ch_dataset = ch_f3.dataset
    in_dataset = indian_f3.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 4
    mc_ch_in_dataset = mc_ch_in_f4.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f4.dataset
    ch_dataset = ch_f4.dataset
    in_dataset = indian_f4.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 5
    mc_ch_in_dataset = mc_ch_in_f5.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f5.dataset
    ch_dataset = ch_f5.dataset
    in_dataset = indian_f5.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 6
    mc_ch_in_dataset = mc_ch_in_f6.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f6.dataset
    ch_dataset = ch_f6.dataset
    in_dataset = indian_f6.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 7
    mc_ch_in_dataset = mc_ch_in_f7.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f7.dataset
    ch_dataset = ch_f7.dataset
    in_dataset = indian_f7.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 8
    mc_ch_in_dataset = mc_ch_in_f8.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f8.dataset
    ch_dataset = ch_f8.dataset
    in_dataset = indian_f8.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )

    # Fold 9
    mc_ch_in_dataset = mc_ch_in_f9.dataset
    assert isinstance(mc_ch_in_dataset, dict)

    mc_dataset = mc_f9.dataset
    ch_dataset = ch_f9.dataset
    in_dataset = indian_f9.dataset

    assert "train" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["train"]), 
        len(mc_dataset["train"]) + len(ch_dataset["train"]) \
            + len(in_dataset["train"])
        )

    assert "validation" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["validation"]), 
        len(mc_dataset["validation"]) + len(ch_dataset["validation"]) \
            + len(in_dataset["validation"])
        )

    assert "test" in mc_ch_in_dataset
    nose.tools.eq_(
        len(mc_ch_in_dataset["test"]), 
        len(mc_dataset["test"]) + len(ch_dataset["test"]) \
            + len(in_dataset["test"])
        )