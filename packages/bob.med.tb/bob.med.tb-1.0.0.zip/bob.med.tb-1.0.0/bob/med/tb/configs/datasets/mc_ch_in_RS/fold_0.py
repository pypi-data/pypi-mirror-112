#!/usr/bin/env python
# coding=utf-8

""" Aggregated dataset composed of Montgomery, Shenzhen and Indian datasets
(cross validation fold 0) """

from . import _maker

dataset = _maker("fold_0")