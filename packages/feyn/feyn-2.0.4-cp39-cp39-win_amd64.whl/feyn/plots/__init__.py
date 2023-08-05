"""
This module contains functions to help plotting evaluation metrics for feyn and other models.
"""

from ._plots import (
    plot_confusion_matrix,
    plot_segmented_loss,
    plot_regression,
    plot_residuals,
)
from ._partial2d import plot_partial2d
from ._model_response import plot_model_response_1d, plot_partial
from ._model_summary import plot_model_summary
from ._graph_flow import plot_activation_flow
from ._set_style import abzu_mplstyle
from ._themes import Theme
from ._probability_plot import plot_probability_scores
from ._roc_curve import plot_roc_curve

from . import interactive


__all__ = [
    "plot_confusion_matrix",
    "plot_regression_metrics",
    "plot_segmented_loss",
    "plot_roc_curve",
    "plot_model_response_1d"
    "plot_partial"
    "plot_partial2d",
    "plot_model_summary",
    "plot_activation_flow",
    "plot_probability_scores",
    "plot_regression",
    "plot_residuals",
    "Theme",
    "interactive",
]
