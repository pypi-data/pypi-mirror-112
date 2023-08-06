#!/usr/bin/env python
# coding=utf-8

def _maker(protocol):

    from ....data.padchest_RS import dataset as raw
    from .. import make_dataset as mk

    return mk(
        [raw.subsets(protocol)]
        )