#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from ..models.pasa import build_pasa
from ..utils.summary import summary


class Tester(unittest.TestCase):
    """
    Unit test for model architectures
    """

    def test_summary_driu(self):
        model = build_pasa()
        s, param = summary(model)
        self.assertIsInstance(s, str)
        self.assertIsInstance(param, int)
