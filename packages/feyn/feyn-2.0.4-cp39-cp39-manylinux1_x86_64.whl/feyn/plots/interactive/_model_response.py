import feyn
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoLocator, FixedLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
from feyn.plots import plot_model_response_1d
from typing import Iterable, Union, Dict

from contextlib import contextmanager
@contextmanager
def _set_backend():
    import matplotlib
    backend = matplotlib.get_backend()
    try:
        yield matplotlib.use('svg')
    finally:
        matplotlib.use(backend)

def interactive_model_response_1d(model: feyn.Model, data: Iterable, input_constraints: Dict[str, Union[Iterable, float, str]] = None):
    """Plot an interactive version of the feyn.plots.plot_model_response_1d (model.plot_response_1d),
        that allows you to change the response variable `by`.

    Arguments:
        model {feyn.Model} -- The model to calculate the response for
        data {Iterable} -- The data to be analyzed

    Keyword Arguments:
        input_constraints {dict} -- The constraints on the remaining model inputs (default: {None})
    """

    from ipywidgets.widgets import interactive
    from IPython.display import display

    output = model.output
    cat_list = _determine_categories(model)

    if input_constraints is None:
        input_constraints = {}
        for feat in model.features:
            if feat in cat_list:
                input_constraints[feat] = np.argmax(data[feat].value_counts())
            else:
                input_constraints[feat] = data[feat].median()

    with _set_backend():
        fig, ax = plt.subplots(figsize=(8, 8))
        ax, ax_top, ax_right = _append_xyaxes(ax)

        line1, = ax.plot(0, 0)
        line2, = ax.plot(0, 0, 'o', color='grey', alpha=0.3)

        # Histograms
        hist0, bins0, width0 = _get_hist_bins(0.)
        bar_top = ax_top.bar(bins0, hist0, color='grey', alpha=0.6, width=width0)
        bar_right = ax_right.barh(bins0, hist0, color='grey', alpha=0.6, height=width0)

    def _update(**kwargs):
        by = kwargs.pop('by')
        x = _x_values(data, by, cat_list)
        y = _get_prediction(model, x, by, input_constraints)
        axes_pred = [x, y]
        axes_true = [data[by], data[output]]
        axes_labels = [by, f"Predicted {output}"]
        ranges = _get_data_ranges(axes_pred, axes_true)

        if by in cat_list:
            axes_pred = list(reversed(axes_pred))
            axes_true = list(reversed(axes_true))
            axes_labels = list(reversed(axes_labels))
            ranges = list(reversed(ranges))

            # Translate ticks to categories
            ticks_loc = np.linspace(0., 1., len(axes_pred[1]))
            ax.set_yticks(ticks_loc)
            ax.set_yticklabels(axes_pred[1])

            # Sanitize data to be consistent with ticks
            axes_pred[1] = ticks_loc
            axes_true[1] = axes_true[1].astype('category').cat.codes
            axes_true[1] /= max(axes_true[1])

            # Convert to scatter
            line1.set_linestyle('')
            line1.set_marker('o')
        else:
            ax.yaxis.set_major_locator(AutoLocator())
            ticks_loc = ax.get_yticks().tolist()
            ax.yaxis.set_major_locator(FixedLocator(ticks_loc))
            ax.set_yticklabels([_value_to_string(tick) for tick in ticks_loc])
            line1.set_linestyle('-')
            line1.set_marker('')

        ax.set_xlim(*ranges[0])
        ax.set_ylim(*ranges[1])

        ax.set_xlabel(axes_labels[0])
        ax.set_ylabel(axes_labels[1])

        line1.set_data(*axes_pred)
        line1.set_label(_determine_label(input_constraints))
        line2.set_data(*axes_true)

        # Histograms
        hist_top, bins_top, width_top = _get_hist_bins(axes_true[0])
        hist_right, bins_right, height_right = _get_hist_bins(axes_true[1])

        [bar.set_height(hist_top[i]) for i, bar in enumerate(bar_top)]
        [bar.set_x(bins_top[i]) for i, bar in enumerate(bar_top)]
        [bar.set_width(width_top) for bar in bar_top]
        ax_top.relim()
        ax_top.autoscale_view()

        [bar.set_width(hist_right[i]) for i, bar in enumerate(bar_right)]
        [bar.set_y(bins_right[i]) for i, bar in enumerate(bar_right)]
        [bar.set_height(height_right) for bar in bar_right]
        ax_right.relim()
        ax_right.autoscale_view()

        legend_title = ", ".join(input_constraints.keys())
        ax.legend(title=legend_title, loc="center left", bbox_to_anchor=(1.35, 0.5))

        display(fig)

    kwargs = {}
    kwargs['by'] = model.features

    return interactive(_update, **kwargs)

def _determine_categories(model):
    return [node.name for node in model if "cat" in node.spec]


def _get_data_ranges(data_axis_1, data_axis_2):
    ranges = []
    for data_1, data_2 in zip(data_axis_1, data_axis_2):
        min_val = min(data_1.min(), data_2.min())
        max_val = max(data_1.max(), data_2.max())
        ranges.append(_pad_axis_range(min_val, max_val))

    return ranges


def _pad_axis_range(min_val, max_val):
    if isinstance(min_val, str) or isinstance(max_val, str):
        return -0.05, 1.05
    else:
        padding = (max_val - min_val) * 0.05
        return min_val - padding, max_val + padding


def _value_to_string(value):
    if isinstance(value, float) or isinstance(value, int):
        value = f"{float(value):.3}"
    else:
        value = str(value)
    return value


def _x_values(data, by, cat_list):
    if by in cat_list:
        x = np.unique(data[by])
    else:
        x = np.linspace(data[by].min(), data[by].max(), 100)
    return x


def _get_prediction(model, x, by, input_constraints):
    from pandas import DataFrame

    input_values = input_constraints.copy()
    input_values[by] = x.copy()
    return model.predict(DataFrame(input_values))


def _append_xyaxes(ax_main):
    # Takes axes and appends two axes on top and to right

    ax_main.set_aspect("auto")

    # Make the divisions
    divider = make_axes_locatable(ax_main)

    ax_x = divider.append_axes("top", size=1.4, pad=0.2, sharex=ax_main)
    ax_y = divider.append_axes("right", size=1.4, pad=0.2, sharey=ax_main)

    # Make nice ticks
    ax_main.tick_params(direction="in", top=True, right=True)
    ax_x.tick_params(direction="in", labelbottom=False)
    ax_y.tick_params(direction="in", labelleft=False)

    return ax_main, ax_x, ax_y


def _get_hist_bins(data):
    hist, bins = np.histogram(data, bins=31)
    width = (bins[1] - bins[0]) * 0.85

    return hist, bins[:-1], width


def _determine_label(partial):
    values = partial.values()
    string_values = [_value_to_string(value) for value in values]

    return ", ".join(string_values)
