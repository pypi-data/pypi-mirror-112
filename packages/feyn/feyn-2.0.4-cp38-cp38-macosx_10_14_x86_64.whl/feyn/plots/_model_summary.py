import numpy as np
import feyn

from typing import Iterable, Optional

from feyn.plots._svg_toolkit import SVGGraphToolkit
from feyn.metrics import (
    get_pearson_correlations,
    get_mutual_information,
    get_spearmans_correlations,
    get_summary_information,
)

def plot_model_summary(
    model: feyn.Model,
    dataframe: Iterable,
    corr_func: Optional[str] = None,
    compare_data: Optional[Iterable] = None,
    labels: Optional[Iterable[str]] = None,
):  # -> "SVG":
    """
    Plot a model displaying the signal path and summary metrics for the provided feyn.Model and DataFrame.

    Arguments:
        model {feyn.Model}   -- A feyn.Model we want to describe given some data.
        dataframe {Iterable} -- A Pandas DataFrame for showing metrics.

    Keyword Arguments:
        corr_func {Optional[str]} -- A name for the correlation function to use as the node signal, either 'mutual_information', 'pearson' or 'spearman' are available. (default: {None} defaults to 'pearson')
        compare_data {Optional[Iterable]} -- A Pandas DataFrame or list of DataFrames for showing additional metrics. (default: {None})
        labels {Optional[Iterable[str]]} - A list of labels to use instead of the default labels. Should match length of comparison data + 1.

    Raises:
        ValueError: Raised if the name of the correlation function is not understood, or if invalid dataframes are passed.

    Returns:
        SVG -- SVG of the model summary.
    """
    if corr_func is None:
        corr_func = "pearson"

    _validate_dataframe(dataframe)

    compare_data = _sanitize_data_inputs(compare_data)
    labels = _create_labels(labels, [dataframe] + compare_data)
    signal_func, legend = _get_corr_func(corr_func)

    node_signal = signal_func(model, dataframe)

    if _is_mutual_information(corr_func):
        node_signal = np.abs(node_signal)
        color_range = node_signal
        cmap = "feyn-highlight"
        colorbar_labels = ["low", "high"]
    elif _is_pearson(corr_func) or _is_spearman(corr_func):
        color_range = [-1, 1]
        cmap = "feyn-diverging"
        colorbar_labels = ["-1", "0", "+1"]

    summary = get_summary_information(model, dataframe)

    gtk = SVGGraphToolkit()
    gtk.add_graph(
        model, show_loss=False
    ).color_nodes(
        by=node_signal, crange=color_range, cmap=cmap
    ).label_nodes(
        [np.round(sig, 2) for sig in node_signal]
    ).add_colorbars(
        legend, color_text=colorbar_labels, cmap=cmap
    ).add_summary_information(
        summary, labels[0]
    )

    if compare_data is not None:
        for l_idx, cdata in enumerate(compare_data):
            compare_summary = get_summary_information(model, cdata)
            gtk.add_summary_information(compare_summary, labels[l_idx+1], short=True)

    from IPython.display import HTML

    return HTML(gtk._repr_html_())


def _sanitize_data_inputs(compare_data):
    if compare_data is None:
        compare_data = []

    # Wrap in a list to allow multiple comparisons
    if not isinstance(compare_data, list):
        compare_data = [compare_data]

    for cdata in compare_data:
        _validate_dataframe(cdata)

    return compare_data

def _validate_dataframe(df):
    if not type(df).__name__ == "DataFrame":
        raise ValueError("All passed datasets must be a Pandas DataFrame")

def _create_labels(labels, target_list):
    if labels is None:
        labels = ['Training Metrics', 'Test']

    # Magically add labels to match if a sufficient amount is not provided
    if len(labels) != len(target_list):
        # Append labels for differences only
        labels += [f'Comp. {i}' for i in range(len(labels), len(target_list))]

    return labels

def _is_pearson(corr_func):
    return corr_func in ["pearson", "pearsons"]

def _is_mutual_information(corr_func):
    return corr_func in ["mi", "mutual_information", "mutual information"]

def _is_spearman(corr_func):
    return corr_func in ["spearman", "spearmans"]

def _get_corr_func(corr_func):
    if _is_mutual_information(corr_func):
        signal_func = get_mutual_information
        legend = "Mutual Information"
    elif _is_pearson(corr_func):
        signal_func = get_pearson_correlations
        legend = "Pearson correlation"
    elif _is_spearman(corr_func):
        signal_func = get_spearmans_correlations
        legend = "Spearman's correlation"
    else:
        raise ValueError("Correlation function name not understood.")
    return signal_func, legend
