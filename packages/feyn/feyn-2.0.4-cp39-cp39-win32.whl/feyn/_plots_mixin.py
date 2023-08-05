from typing import Iterable, Optional, Dict, Union
import feyn


class PlotsMixin:
    def plot(
        self,
        data: Iterable,
        compare_data: Optional[Iterable] = None,
        corr_func: Optional[str] = None,
        labels: Optional[Iterable[str]] = None,
    ) -> "SVG":
        """
        Plot the model's summary metrics and show the signal path.

        This is a shorthand for calling feyn.plots.plot_model_summary.

        Arguments:
            data {Iterable} -- Data set including both input and expected values. Must be a pandas.DataFrame.

        Keyword Arguments:
            compare_data {Optional[Iterable]} -- Additional data set including both input and expected values. A pandas.DataFrame or a list of pd.DataFrame for multiple comparisons. (default: {None})
            corr_func {Optional[str]} -- Correlation function to use in showing the importance of individual nodes. Must be either "mutual_information", "pearson" or "spearman". (default: {None} -> "pearson")
            labels {Optional[Iterable[str]]} - A list of labels to use instead of the default labels. Must be size 2 if using comparison dataset, else 1.

        Returns:
            SVG -- SVG of the model summary.
        """
        return feyn.plots._model_summary.plot_model_summary(
            self, data, corr_func=corr_func, compare_data=compare_data, labels=labels
        )

    def plot_flow(self, data: Iterable, sample: Iterable) -> "SVG":
        """Plots the flow of activations through the model, for the provided sample. Uses the provided data as background information for visualization.

        Returns:
            SVG -- SVG of the model activation flow.
        """
        return feyn.plots.plot_activation_flow(self, data, sample)

    def plot_partial2d(
        self,
        data: "DataFrame",
        fixed: Dict[str, Union[int, float]] = None,
        ax: Optional["Axes"] = None,
        resolution: int = 1000,
    ) -> None:
        """
        Visualize the response of a model to numerical inputs using a partial plot. The partial plot comes in two parts:

        1. A colored background indicating the response of the model in a 2D space given the fixed values. A lighter color corresponds to a bigger output from the model.
        2. Scatter-plotted data on top of the background. In a classification scenario, red corresponds to true positives, and blue corresponds to true negatives. For regression, the color gradient shows the true distribution of the output value. Two sizes are used in the scatterplot, the larger dots correspond to the data that matches the values in fixed and the smaller ones have data different from the values in fixed.

        Arguments:
            data {DataFrame} -- The data that will be scattered in the model.

        Keyword Arguments:
            fixed {Dict[str, Union[int, float]]} -- Dictionary with values we fix in the model. The key is a feature name in the model and the value is a number that the feature is fixed to. (default: {{}})
            ax {Optional[plt.Axes.axes]} -- Optional matplotlib axes in which to make the partial plot. (default: {None})
            resolution {int} -- The resolution at which we sample the 2D feature space for the background. (default: {1000})

        Raises:
            ValueError: Raised if the model features names minus the fixed value names are more than two, meaning that you need to fix more values to reduce the dimensionality and make a 2D plot possible.
            ValueError: Raised if one of the features you are trying to plot in a 2D space is a categorical.
        """
        feyn.plots._partial2d.plot_partial2d(self, data, fixed, ax, resolution)
