from typing import Iterable, Optional
import feyn
import numpy as np
from pandas import DataFrame


class BaseReportingMixin:
    def squared_error(self, data: Iterable):
        """
        Compute the model's squared error loss on the provided data.

        This function is a shorthand that is equivalent to the following code:
        > y_true = data[<output col>]
        > y_pred = model.predict(data)
        > se = feyn.losses.squared_error(y_true, y_pred)

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            nd.array -- The losses as an array of floats.

        """
        pred = self.predict(data)
        return feyn.losses.squared_error(data[self.target], pred)

    def absolute_error(self, data: Iterable):
        """
        Compute the model's absolute error on the provided data.

        This function is a shorthand that is equivalent to the following code:
        > y_true = data[<output col>]
        > y_pred = model.predict(data)
        > se = feyn.losses.absolute_error(y_true, y_pred)

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            nd.array -- The losses as an array of floats.

        """
        pred = self.predict(data)
        return feyn.losses.absolute_error(data[self.target], pred)

    def binary_cross_entropy(self, data: Iterable):
        """
        Compute the model's binary cross entropy on the provided data.

        This function is a shorthand that is equivalent to the following code:
        > y_true = data[<output col>]
        > y_pred = model.predict(data)
        > se = feyn.losses.binary_cross_entropy(y_true, y_pred)

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            nd.array -- The losses as an array of floats.

        """
        pred = self.predict(data)
        return feyn.losses.binary_cross_entropy(data[self.target], pred)

    def accuracy_score(self, data: Iterable):
        """
        Compute the model's accuracy score on a data set.

        The accuracy score is useful to evaluate classification models. It is the fraction of the preditions that are correct. Formally it is defned as

        (number of correct predictions) / (total number of preditions)

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            accuracy score for the predictions
        """
        pred = self.predict(data)
        return feyn.metrics.accuracy_score(data[self.target], pred)

    def accuracy_threshold(self, data: Iterable):
        """
        Compute the accuracy score of predictions with optimal threshold

        The accuracy score is useful to evaluate classification models. It is the fraction of the preditions that are correct. Accuracy is normally calculated under the assumption that the threshold that separates true from false is 0.5. Hovever, this is not the case when a model was trained with another population composition than on the one which is used.

        This function first computes the threshold limining true from false classes that optimises the accuracy. It then returns this threshold along with the accuracy that is obtained using it.

        Arguments:
            true -- Expected values
            pred -- Predicted values

        Returns a tuple with:
            threshold that maximizes accuracy
            accuracy score obtained with this threshold

        """
        pred = self.predict(data)
        return feyn.metrics.accuracy_threshold(data[self.target], pred)

    def roc_auc_score(self, data: Iterable):
        """
        Calculate the Area Under Curve (AUC) of the ROC curve.

        A ROC curve depicts the ability of a binary classifier with varying threshold.

        The area under the curve (AUC) is the probability that said classifier will
        attach a higher score to a random positive instance in comparison to a random
        negative instance.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            AUC score for the predictions
        """
        pred = self.predict(data)
        return feyn.metrics.roc_auc_score(data[self.target], pred)

    def r2_score(self, data: Iterable):
        """
        Compute the model's r2 score on a data set

        The r2 score for a regression model is defined as
        1 - rss/tss

        Where rss is the residual sum of squares for the predictions, and tss is the total sum of squares.
        Intutively, the tss is the resuduals of a so-called "worst" model that always predicts the mean. Therefore, the r2 score expresses how much better the predictions are than such a model.

        A result of 0 means that the model is no better than a model that always predicts the mean value
        A result of 1 means that the model perfectly predicts the true value

        It is possible to get r2 scores below 0 if the predictions are even worse than the mean model.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            r2 score for the predictions
        """
        pred = self.predict(data)
        return feyn.metrics.r2_score(data[self.target], pred)

    def mae(self, data):
        """
        Compute the model's mean absolute error on a data set.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            MAE for the predictions
        """
        pred = self.predict(data)
        return feyn.metrics.mae(data[self.target], pred)

    def mse(self, data):
        """
        Compute the model's mean squared error on a data set.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            MSE for the predictions
        """
        pred = self.predict(data)
        return feyn.metrics.mse(data[self.target], pred)

    def rmse(self, data):
        """
        Compute the model's root mean squared error on a data set.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.

        Returns:
            RMSE for the predictions
        """
        pred = self.predict(data)
        return feyn.metrics.rmse(data[self.target], pred)

    def plot_confusion_matrix(
        self,
        data: Iterable,
        threshold: float = 0.5,
        labels: Iterable = None,
        title: str = "Confusion matrix",
        color_map="feyn-primary",
        ax=None,
    ) -> None:

        """
        Compute and plot a Confusion Matrix.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            threshold -- Boundary of True and False predictions, default 0.5
            labels -- List of labels to index the matrix
            title -- Title of the plot.
            color_map -- Color map from matplotlib to use for the matrix
            ax -- matplotlib axes object to draw to, default None
        """
        pred = self.predict(data) >= threshold
        feyn.plots.plot_confusion_matrix(
            data[self.target], pred, labels, title, color_map, ax
        )

    def plot_segmented_loss(
        self,
        data: Iterable,
        by: Optional[str] = None,
        loss_function="squared_error",
        title="Segmented Loss",
        ax=None,
    ) -> None:
        """
        Plot the loss by segment of a dataset.

        This plot is useful to evaluate how a model performs on different subsets of the data.

        Example:
        > models = qlattice.sample_models(["age","smoker","heartrate"], output="heartrate")
        > models = feyn.fit_models(models, data)
        > best = models[0]
        > feyn.plots.plot_segmented_loss(best, data, by="smoker")

        This will plot a histogram of the model loss for smokers and non-smokers separately, which can help evaluate wheter the model has better performance for euther of the smoker sub-populations.

        You can use any column in the dataset as the `by` parameter. If you use a numerical column, the data will be binned automatically.

        Arguments:
            data -- The dataset to measure the loss on.
            by -- The column in the dataset to segment by.
            loss_function -- The loss function to compute for each segmnent,
            title -- Title of the plot.
            ax -- matplotlib axes object to draw to
        """

        feyn.plots.plot_segmented_loss(
            self, data, by=by, loss_function=loss_function, title=title, ax=ax
        )

    def plot_roc_curve(
        self,
        data: Iterable,
        threshold: float = None,
        title: str = "ROC curve",
        ax=None,
        **kwargs
    ) -> None:
        """
        Plot the model's ROC curve.

        This is a shorthand for calling feyn.plots.plot_roc_curve.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            threshold -- Plots a point on the ROC curve of the true positive rate and false positive rate at the given threshold. Default is None
            title -- Title of the plot.
            ax -- matplotlib axes object to draw to, default None
            **kwargs -- additional options to pass on to matplotlib
        """
        pred = self.predict(data)
        feyn.plots.plot_roc_curve(
            data[self.target], pred, threshold, title, ax, **kwargs
        )

    def plot_probability_scores(
        self, data: Iterable, title="", nbins=10, h_args=None, ax=None
    ):
        """Plots the histogram of probability scores in binary
        classification problems, highlighting the negative and
        positive classes. Order of truth and prediction matters.

        Arguments:
            data -- Data set including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
        Keyword Arguments:
            title {str} -- plot title (default: {''})
            nbins {int} -- number of bins (default: {10})
            h_args {dict} -- histogram kwargs (default: {None})
            ax {matplotlib.axes._subplots.AxesSubplot} -- axes object (default: {None})
        """

        true = data[self.target]
        pred = self.predict(data)

        feyn.plots.plot_probability_scores(true, pred, title, nbins, h_args, ax)

    def plot_partial(
        self, data: DataFrame, by: str, fixed: Optional[dict] = None, ax=None
    ):
        """
        Plot a partial dependence plot.
        This plot is useful to interpret the effect of a specific feature on the model output.

        Example:
        > models = qlattice.sample_models(["age","smoker","heartrate"], output="heartrate")
        > models = feyn.fit_models(models, data)
        > best = models[0]
        > best.plot_partial(data, by="age")

        You can use any column in the dataset as the `by` parameter.
        If you use a numerical column, the feature will vary from min to max of that varialbe in the training set.
        If you use a categorical column, the feature will display all categories, sorted by the average prediction of that category.

        Arguments:
            model -- The model to plot.
            data -- The dataset to measure the loss on.
            by -- The column in the dataset to interpret by.
            fixed -- A dictionary of features and associated values to hold fixed
        """
        feyn.plots.plot_partial(self, data, by, fixed, ax)

    def plot_response_1d(
        self, data: Iterable, by: str, input_constraints: Optional[dict] = None
    ) -> None:

        """Plot the response of a model to a single feature given by `by`.
        The remaining model features are fixed by default as the middle
        quantile (median). Additional quantiles are added if the model has
        a maximum of 3 features. You can change this behavior by determining
        `input_contraints` yourself. Any number of model features can be added to it.

        Arguments:
            model {feyn.Model} -- Model to be analysed
            data {Iterable} -- Data frame
            by {str} -- Model feature to plot model response

        Keyword Arguments:
            input_contraints {Optional[dict]} -- Feature values to be fixed (default: {None})
            ax {matplotlib.axes} -- matplotlib axes object to draw to (default: {None})

        Returns:
            (ax, ax_top, ax_right) -- The three axes (main, top, right) that make up the plot
        """

        feyn.plots.plot_model_response_1d(self, data, by, input_constraints)

    def plot_regression(
        self, data: Iterable, title: str = "Actuals vs Prediction", ax=None
    ):
        """This plots the true values on the x-axis and the predicted values on the y-axis.
        On top of the plot is the line of equality y=x.
        The closer the scattered values are to the line the better the predictions.
        The line of best fit between y_true and y_pred is also calculated and plotted. This line should be close to the line y=x

        Arguments:
            data {typing.Iterable} -- The dataset to determine regression quality. It contains input names and output name of the model as columns

        Keyword Arguments:
            title {str} -- (default: {"Actuals vs Predictions"})
            ax {AxesSubplot} -- (default: {None})
        """

        y_true = data[self.target]
        y_pred = self.predict(data)

        feyn.plots.plot_regression(y_true, y_pred, title, ax)

    def plot_residuals(self, data: Iterable, title: str = "Residuals plot", ax=None):
        """This plots the predicted values against the residuals (y_true - y_pred).

        Arguments:
            y_true {typing.Iterable} -- True values
            y_pred {typing.Iterable} -- Predicted values

        Keyword Arguments:
            title {str} -- (default: {"Residual plot"})
            ax {[type]} -- (default: {None})
        """

        y_true = data[self.target]
        y_pred = self.predict(data)

        feyn.plots.plot_residuals(y_true, y_pred, title, ax)
