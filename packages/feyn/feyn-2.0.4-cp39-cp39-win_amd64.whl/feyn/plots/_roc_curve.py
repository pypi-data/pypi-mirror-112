import matplotlib.pyplot as plt
import numpy as np
import typing
from ._themes import Theme


def plot_roc_curve(
    y_true: typing.Iterable,
    y_pred: typing.Iterable,
    threshold: float = None,
    title: str = "ROC curve",
    ax=None,
    **kwargs,
):
    """
    Plot a ROC curve for a classification model.

    A receiver operating characteristic curve, or ROC curve, is an illustration of the diagnostic ability of a binary classifier. The method was developed for operators of military radar receivers, which is why it is so named.

    Arguments:
        y_true -- Expected values (Truth).
        y_pred -- Predicted values.
        threshold -- Plots a point on the ROC curve of the true positive rate and false positive rate at the given threshold. Default is None
        title -- Title of the plot.
        ax -- matplotlib axes object to draw to, default None

    Raises:
        ValueError: When y_true and y_pred do not have same shape
        ValueError: When threshold is not between 0 and 1
    """

    if ax is None:
        ax = plt.gca()

    import sklearn.metrics

    fpr, tpr, _ = sklearn.metrics.roc_curve(y_true, y_pred)
    roc_auc = sklearn.metrics.auc(fpr, tpr)

    ax.set_title(title)

    if threshold is not None:
        if threshold >= 1:
            raise ValueError("threshold must be strictly between 0 and 1")
        if 0 >= threshold:
            raise ValueError("threshold must be strictly between 0 and 1")

        fpr_at_thres = _false_positive_rate(y_true, y_pred, threshold)
        tpr_at_thres = _true_positive_rate(y_true, y_pred, threshold)

        ax.vlines(x=fpr_at_thres, ymin=0, ymax=tpr_at_thres, ls="--", lw=1.5)
        ax.hlines(y=tpr_at_thres, xmin=0, xmax=fpr_at_thres, ls="--", lw=1.5)
        ax.scatter(fpr_at_thres, tpr_at_thres, marker="o", s=50, c="k")
        ax.annotate(
            text=f"({fpr_at_thres:.2f}, {tpr_at_thres:.2f})",
            xy=(fpr_at_thres, tpr_at_thres),
            xytext=(3, -10),
            textcoords="offset points",
        )
        precision = _precision(y_true, y_pred, threshold)
        recall = tpr_at_thres
        accuracy = _accuracy(y_true, y_pred, threshold)
        f1_score = _f1score(y_true, y_pred, threshold)

        text_str = "\n".join(
            (
                f"Threshold: {threshold: .2f}",
                f"Accuracy: {accuracy: .2f}",
                f"F1 score: {f1_score: .2f}",
                f"Precision: {precision: .2f}",
                f"Recall: {recall: .2f}",
            )
        )
        props = dict(boxstyle="round", facecolor="white", alpha=0.5)
        ax.text(0.975, 0.05, text_str, bbox=props, ha="right")

    else:
        if "label" in kwargs:
            kwargs["label"] += " AUC = %0.2f" % roc_auc
        else:
            kwargs["label"] = "AUC = %0.2f" % roc_auc

    ax.plot(fpr, tpr, **kwargs)

    if threshold is None:
        ax.legend(loc="lower right")

    ax.plot([0, 1], [0, 1], "--", c=Theme.color("accent"))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_ylabel("True Positive Rate")
    ax.set_xlabel("False Positive Rate")

    return ax


def _true_positive_count(y_true, y_pred, threshold):
    # all actual positives predicted positive
    actual_positives = y_true == 1
    tp_count = np.sum(y_pred[actual_positives] >= threshold)
    return tp_count


def _true_negative_count(y_true, y_pred, threshold):
    # all actual negatives predicted negative
    actual_negatives = y_true == 0
    tn_count = np.sum(y_pred[actual_negatives] < threshold)
    return tn_count


def _false_positive_count(y_true, y_pred, threshold):
    # all actual negatives predicted positive
    actual_negatives = y_true == 0
    tn_count = np.sum(y_pred[actual_negatives] >= threshold)
    return tn_count


def _false_negative_count(y_true, y_pred, threshold):
    # all actual positives predicted negative
    actual_positives = y_true == 1
    fn_count = np.sum(y_pred[actual_positives] < threshold)
    return fn_count


def _true_positive_rate(y_true, y_pred, threshold):
    # also known as recall
    tp_count = _true_positive_count(y_true, y_pred, threshold)
    fn_count = _false_negative_count(y_true, y_pred, threshold)

    tpr = tp_count / (tp_count + fn_count)
    return tpr


def _false_positive_rate(y_true, y_pred, threshold):
    tn_count = _true_negative_count(y_true, y_pred, threshold)
    fp_count = _false_positive_count(y_true, y_pred, threshold)

    fpr = fp_count / (tn_count + fp_count)
    return fpr


def _precision(y_true, y_pred, threshold):
    tp_count = _true_positive_count(y_true, y_pred, threshold)
    fp_count = _false_positive_count(y_true, y_pred, threshold)

    precision = tp_count / (tp_count + fp_count)
    return precision


def _accuracy(y_true, y_pred, threshold):
    tp_count = _true_positive_count(y_true, y_pred, threshold)
    fn_count = _false_negative_count(y_true, y_pred, threshold)
    tn_count = _true_negative_count(y_true, y_pred, threshold)
    fp_count = _false_positive_count(y_true, y_pred, threshold)

    accuracy = (tp_count + tn_count) / (tp_count + fn_count + tn_count + fp_count)
    return accuracy


def _f1score(y_true, y_pred, threshold):
    precision = _precision(y_true, y_pred, threshold)
    recall = _true_positive_rate(y_true, y_pred, threshold)

    f1_score = (2 * precision * recall) / (precision + recall)
    return f1_score
