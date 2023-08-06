#!/usr/bin/env python
# coding=utf-8

def _maker(protocol, resize_size=512, cc_size=512, RGB=False):

    from ....data.hivtb_RS import dataset as raw
    from .. import make_dataset as mk

    return mk(
        [raw.subsets(protocol)]
        )