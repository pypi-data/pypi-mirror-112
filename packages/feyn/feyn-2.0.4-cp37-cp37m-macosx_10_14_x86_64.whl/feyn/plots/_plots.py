"""Various helper functions to compute and plot metrics."""
import itertools

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import typing
import feyn.losses
import feyn.metrics

from ._themes import Theme

# Sets the default theme and triggers matplotlib stylings
Theme.set_theme()


def plot_confusion_matrix(
    y_true: typing.Iterable,
    y_pred: typing.Iterable,
    labels: typing.Iterable = None,
    title: str = "Confusion matrix",
    color_map="feyn-primary",
    ax=None,
) -> None:
    """
    Compute and plot a Confusion Matrix.

    Arguments:
        y_true -- Expected values (Truth)
        y_pred -- Predicted values
        labels -- List of labels to index the matrix
        title -- Title of the plot.
        color_map -- Color map from matplotlib to use for the matrix
        ax -- matplotlib axes object to draw to, default None
    Returns:
        [plot] -- matplotlib confusion matrix
    """
    if ax is None:
        ax = plt.gca()

    if labels is None:
        labels = np.union1d(y_pred, y_true)

    cm = feyn.metrics.confusion_matrix(y_true, y_pred)

    ax.set_title(title)
    tick_marks = range(len(labels))
    ax.set_xticks(tick_marks)
    ax.set_xticklabels(labels, rotation=45)

    ax.set_yticks(tick_marks)
    ax.set_yticklabels(labels)

    thresh = cm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        ax.text(
            j,
            i,
            format(cm[i, j], "d"),
            horizontalalignment="center",
            color=Theme.color("light") if cm[i, j] > thresh else Theme.color("dark"),
        )

    ax.set_ylabel("Expected")
    ax.set_xlabel("Predicted")

    img = ax.imshow(cm, interpolation="nearest", cmap=color_map)
    plt.colorbar(img, ax=ax)

    return ax

def plot_segmented_loss(
    model: feyn.Model,
    data: typing.Iterable,
    by: typing.Optional[str] = None,
    loss_function="squared_error",
    title="Segmented Loss",
    ax=None,
) -> None:
    """
    Plot the loss by segment of a dataset.

    This plot is useful to evaluate how a model performs on different subsets of the data.

    Example:
    > qg = qlattice.get_regressor(["age","smoker","heartrate"], output="heartrate")
    > qg.fit(data)
    > best = qg[0]
    > feyn.plots.plot_segmented_loss(best, data, by="smoker")

    This will plot a histogram of the model loss for smokers and non-smokers separately, which can help evaluate wheter the model has better performance for euther of the smoker sub-populations.

    You can use any column in the dataset as the `by` parameter. If you use a numerical column, the data will be binned automatically.

    Arguments:
        model -- The model to plot.
        data -- The dataset to measure the loss on.
        by -- The column in the dataset to segment by.
        loss_function -- The loss function to compute for each segmnent,
        title -- Title of the plot.
        ax -- matplotlib axes object to draw to
    """

    if by is None:
        by = model[-1].name

    bins, cnts, statistic = feyn.metrics.segmented_loss(model, data, by, loss_function)

    if ax is None:
        ax = plt.gca()

    ax.set_title(title)

    ax.set_xlabel("Segmented by " + by)
    ax.set_ylabel("Number of samples")

    if type(bins[0]) == tuple:
        bins = [(e[0] + e[1]) / 2 for e in bins]
        w = 0.8 * (bins[1] - bins[0])
        ax.bar(bins, height=cnts, width=w)
    else:
        ax.bar(bins, height=cnts)

    ax2 = ax.twinx()
    ax2.set_ylabel("Loss")
    ax2.plot(bins, statistic, c=Theme.color("accent"), marker="o")
    ax2.set_ylim(bottom=0)

    return ax


def plot_regression(
    y_true: typing.Iterable,
    y_pred: typing.Iterable,
    title: str = "Actuals vs Predictions",
    ax=None,
):
    """This plots this true values on the x-axis and the predicted values on the y-axis.
    On top of the plot is the line of equality y=x.
    The closer the scattered values are to the line the better the predictions.
    The line of best fit between y_true and y_pred is also calculated and plotted. This line should be close to the line y=x

    Arguments:
        y_true {typing.Iterable} -- True values
        y_pred {typing.Iterable} -- Predicted values

    Keyword Arguments:
        title {str} -- (default: {"Actuals vs Predictions"})
        ax {AxesSubplot} -- (default: {None})

    Returns:
        AxesSubplot -- Scatter plot of y_pred and y_true with line of best fit and line of equality
    """
    from sklearn.linear_model import LinearRegression

    # We change to numpy array because sklearn linear regression isn't compatible with pandas Series
    if type(y_true).__name__ == "Series":
        y_true = y_true.values

    if ax is None:
        fig, ax = plt.subplots()

    ax.scatter(y_true, y_pred)

    lin_reg = LinearRegression()
    lin_reg.fit(X=y_true.reshape(-1, 1), y=y_pred)
    coef = lin_reg.coef_[0]
    bias = lin_reg.intercept_

    mini = np.min([np.min(y_true), np.min(y_pred)])
    maxi = np.max([np.max(y_true), np.max(y_pred)])

    min_max_pred = lin_reg.predict(X=np.array([mini, maxi]).reshape(-1, 1))

    # Line of equality
    ax.plot([mini, maxi], [mini, maxi], ls="--", lw=1, label="line of equality")

    # Line of best fit of y_pred vs y_true
    ax.plot(
        [mini, maxi],
        min_max_pred,
        ls="--",
        lw=1,
        label=f"least squares: {coef:.2f}X + {bias:.2f}",
    )

    ax.set_title(title)
    ax.set_xlabel("Actuals")
    ax.set_ylabel("Predictions")
    ax.legend()

    return ax


def plot_residuals(
    y_true: typing.Iterable,
    y_pred: typing.Iterable,
    title: str = "Residual plot",
    ax=None,
):
    """This plots the predicted values against the residuals (y_true - y_pred).

    Arguments:
        y_true {typing.Iterable} -- True values
        y_pred {typing.Iterable} -- Predicted values

    Keyword Arguments:
        title {str} -- (default: {"Residual plot"})
        ax {[type]} -- (default: {None})

    Returns:
        AxesSubplot -- Scatter plot of residuals against predicted values
    """

    if ax is None:
        fig, ax = plt.subplots()

    residuals = y_true - y_pred

    ax.scatter(y_pred, residuals)
    ax.axhline(lw=1, ls="--")
    ax.set_title(title)
    ax.set_xlabel("Predictions")
    ax.set_ylabel("Residuals")

    return ax
