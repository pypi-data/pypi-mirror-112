import unittest
import pytest
import numpy as np

from feyn.plots._roc_curve import _true_positive_count, _true_negative_count, _false_negative_count, _false_positive_count, _true_positive_rate, _false_positive_rate, _precision, _accuracy, _f1score
from feyn.plots import plot_roc_curve

class TestROCCurve(unittest.TestCase):
    def setUp(self):
        self.actuals = np.array([1,0,0,1,1])
        self.preds = np.array(
            [0.6,
            0.9,
            0.2,
            0.8,
            0.2]
            )
        self.threshold = 0.5
    
    def test_true_positive_count(self):
        actual_tpc = 2
        desired = _true_positive_count(self.actuals, self.preds, self.threshold)
        assert actual_tpc == desired

    def test_true_negative_count(self):
        actual_tnc = 1
        desired = _true_negative_count(self.actuals, self.preds, self.threshold)
        assert actual_tnc == desired

    def test_false_negative_count(self):
        actual_fnc = 1
        desired = _false_negative_count(self.actuals, self.preds, self.threshold)
        assert actual_fnc == desired

    def test_false_positive_count(self):
        actual_fpc = 1
        desired = _false_positive_count(self.actuals, self.preds, self.threshold)
        assert actual_fpc == desired

    def test_true_positive_rate(self):
        actual_tpr = 2 / 3
        desired = _true_positive_rate(self.actuals, self.preds, self.threshold)
        assert actual_tpr == desired

    def test_false_positive_rate(self):
        actual_fpr = 1 / 2
        desired = _false_positive_rate(self.actuals, self.preds, self.threshold)
        assert actual_fpr == desired

    def test_precision(self):
        actual_precision = 2 / 3
        desired = _precision(self.actuals, self.preds, self.threshold)
        assert actual_precision == desired

    def test_accuracy(self):
        actual_accuracy = 3 / 5
        desired = _accuracy(self.actuals, self.preds, self.threshold)
        assert actual_accuracy == desired

    def test_f1score(self):
        actual_f1_score = (2 * (2/3) * (2/3)) / (2/3 + 2/3)
        desired = _f1score(self.actuals, self.preds, self.threshold)
        assert actual_f1_score == desired

    def test_plot_roc_curve(self):
        ax = plot_roc_curve(self.actuals, self.preds)
        assert ax is not None

    def test_plot_roc_curve_w_threshold(self):
        ax = plot_roc_curve(self.actuals, self.preds, self.threshold)
        assert ax is not None