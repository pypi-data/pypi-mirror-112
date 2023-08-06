#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for measure functions"""

import os
import random
import unittest

import numpy
import nose.tools

from ..utils.measure import (
    base_measures,
    bayesian_measures,
    beta_credible_region,
    get_centered_maxf1
)
from ..engine.evaluator import sample_measures_for_threshold

def test_centered_maxf1():

    # Multiple max F1
    f1_scores = numpy.array([0.8, 0.9, 1.0, 1.0, 1.0, 0.3])
    thresholds = numpy.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7])

    maxf1, threshold = get_centered_maxf1(f1_scores, thresholds)

    nose.tools.eq_(maxf1, 1.0)
    nose.tools.eq_(threshold, 0.5)

    # Single max F1
    f1_scores = numpy.array([0.8, 0.9, 1.0, 0.9, 0.7, 0.3])
    thresholds = numpy.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7])

    maxf1, threshold = get_centered_maxf1(f1_scores, thresholds)

    nose.tools.eq_(maxf1, 1.0)
    nose.tools.eq_(threshold, 0.4)

class TestFrequentist(unittest.TestCase):
    """
    Unit test for frequentist base measures
    """

    def setUp(self):
        self.tp = random.randint(1, 100)
        self.fp = random.randint(1, 100)
        self.tn = random.randint(1, 100)
        self.fn = random.randint(1, 100)

    def test_precision(self):
        precision = base_measures(self.tp, self.fp, self.tn, self.fn)[0]
        self.assertEqual((self.tp) / (self.tp + self.fp), precision)

    def test_recall(self):
        recall = base_measures(self.tp, self.fp, self.tn, self.fn)[1]
        self.assertEqual((self.tp) / (self.tp + self.fn), recall)

    def test_specificity(self):
        specificity = base_measures(self.tp, self.fp, self.tn, self.fn)[2]
        self.assertEqual((self.tn) / (self.tn + self.fp), specificity)

    def test_accuracy(self):
        accuracy = base_measures(self.tp, self.fp, self.tn, self.fn)[3]
        self.assertEqual(
            (self.tp + self.tn) / (self.tp + self.tn + self.fp + self.fn),
            accuracy,
        )

    def test_jaccard(self):
        jaccard = base_measures(self.tp, self.fp, self.tn, self.fn)[4]
        self.assertEqual(self.tp / (self.tp + self.fp + self.fn), jaccard)

    def test_f1(self):
        p, r, s, a, j, f1 = base_measures(self.tp, self.fp, self.tn, self.fn)
        self.assertEqual(
            (2.0 * self.tp) / (2.0 * self.tp + self.fp + self.fn), f1
        )
        self.assertAlmostEqual((2 * p * r) / (p + r), f1)  # base definition


class TestBayesian:
    """
    Unit test for bayesian base measures
    """

    def mean(self, k, l, lambda_):
        return (k + lambda_) / (k + l + 2 * lambda_)

    def mode1(self, k, l, lambda_):  # (k+lambda_), (l+lambda_) > 1
        return (k + lambda_ - 1) / (k + l + 2 * lambda_ - 2)

    def test_beta_credible_region_base(self):
        k = 40
        l = 10
        lambda_ = 0.5
        cover = 0.95
        got = beta_credible_region(k, l, lambda_, cover)
        # mean, mode, lower, upper
        exp = (
            self.mean(k, l, lambda_),
            self.mode1(k, l, lambda_),
            0.6741731038857685,
            0.8922659692341358,
        )
        assert numpy.isclose(got, exp).all(), f"{got} <> {exp}"

    def test_beta_credible_region_small_k(self):

        k = 4
        l = 1
        lambda_ = 0.5
        cover = 0.95
        got = beta_credible_region(k, l, lambda_, cover)
        # mean, mode, lower, upper
        exp = (
            self.mean(k, l, lambda_),
            self.mode1(k, l, lambda_),
            0.37137359936800574,
            0.9774872340008449,
        )
        assert numpy.isclose(got, exp).all(), f"{got} <> {exp}"

    def test_beta_credible_region_precision_jeffrey(self):

        # simulation of situation for precision TP == FP == 0, Jeffrey's prior
        k = 0
        l = 0
        lambda_ = 0.5
        cover = 0.95
        got = beta_credible_region(k, l, lambda_, cover)
        # mean, mode, lower, upper
        exp = (
            self.mean(k, l, lambda_),
            0.0,
            0.0015413331334360135,
            0.998458666866564,
        )
        assert numpy.isclose(got, exp).all(), f"{got} <> {exp}"

    def test_beta_credible_region_precision_flat(self):

        # simulation of situation for precision TP == FP == 0, flat prior
        k = 0
        l = 0
        lambda_ = 1.0
        cover = 0.95
        got = beta_credible_region(k, l, lambda_, cover)
        # mean, mode, lower, upper
        exp = (self.mean(k, l, lambda_), 0.0, 0.025000000000000022, 0.975)
        assert numpy.isclose(got, exp).all(), f"{got} <> {exp}"

    def test_bayesian_measures(self):

        tp = random.randint(100000, 1000000)
        fp = random.randint(100000, 1000000)
        tn = random.randint(100000, 1000000)
        fn = random.randint(100000, 1000000)

        _prec, _rec, _spec, _acc, _jac, _f1 = base_measures(tp, fp, tn, fn)
        prec, rec, spec, acc, jac, f1 = bayesian_measures(
            tp, fp, tn, fn, 0.5, 0.95
        )

        # Notice that for very large k and l, the base frequentist measures
        # should be approximately the same as the bayesian mean and mode
        # extracted from the beta posterior.  We test that here.
        assert numpy.isclose(
            _prec, prec[0]
        ), f"freq: {_prec} <> bays: {prec[0]}"
        assert numpy.isclose(
            _prec, prec[1]
        ), f"freq: {_prec} <> bays: {prec[1]}"
        assert numpy.isclose(_rec, rec[0]), f"freq: {_rec} <> bays: {rec[0]}"
        assert numpy.isclose(_rec, rec[1]), f"freq: {_rec} <> bays: {rec[1]}"
        assert numpy.isclose(
            _spec, spec[0]
        ), f"freq: {_spec} <> bays: {spec[0]}"
        assert numpy.isclose(
            _spec, spec[1]
        ), f"freq: {_spec} <> bays: {spec[1]}"
        assert numpy.isclose(_acc, acc[0]), f"freq: {_acc} <> bays: {acc[0]}"
        assert numpy.isclose(_acc, acc[1]), f"freq: {_acc} <> bays: {acc[1]}"
        assert numpy.isclose(_jac, jac[0]), f"freq: {_jac} <> bays: {jac[0]}"
        assert numpy.isclose(_jac, jac[1]), f"freq: {_jac} <> bays: {jac[1]}"
        assert numpy.isclose(_f1, f1[0]), f"freq: {_f1} <> bays: {f1[0]}"
        assert numpy.isclose(_f1, f1[1]), f"freq: {_f1} <> bays: {f1[1]}"

        # We also test that the interval in question includes the mode and the
        # mean in this case.
        assert (prec[2] < prec[1]) and (
            prec[1] < prec[3]
        ), f"precision is out of bounds {_prec[2]} < {_prec[1]} < {_prec[3]}"
        assert (rec[2] < rec[1]) and (
            rec[1] < rec[3]
        ), f"recall is out of bounds {_rec[2]} < {_rec[1]} < {_rec[3]}"
        assert (spec[2] < spec[1]) and (
            spec[1] < spec[3]
        ), f"specif. is out of bounds {_spec[2]} < {_spec[1]} < {_spec[3]}"
        assert (acc[2] < acc[1]) and (
            acc[1] < acc[3]
        ), f"accuracy is out of bounds {_acc[2]} < {_acc[1]} < {_acc[3]}"
        assert (jac[2] < jac[1]) and (
            jac[1] < jac[3]
        ), f"jaccard is out of bounds {_jac[2]} < {_jac[1]} < {_jac[3]}"
        assert (f1[2] < f1[1]) and (
            f1[1] < f1[3]
        ), f"f1-score is out of bounds {_f1[2]} < {_f1[1]} < {_f1[3]}"