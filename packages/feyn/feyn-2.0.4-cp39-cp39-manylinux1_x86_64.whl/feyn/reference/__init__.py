"""
This module contains reference models that can be used for comparison with feyn models.
"""
import numpy as np
import typing

from .._base_reporting_mixin import BaseReportingMixin


class ConstantModel(BaseReportingMixin):
    def __init__(self, output_name, const):
        self.const = const
        self.target = output_name

    def predict(self, data: typing.Iterable):
        return np.full(len(data), self.const)


class SKLeanClassifier(BaseReportingMixin):
    def __init__(self, sklearn_classifier:type, data, output_name, **kwargs):
        self.features = list(data.columns)
        if output_name in self.features:
            self.features.remove(output_name)
            
        self.target = output_name

        self._model = sklearn_classifier(**kwargs)
        self._model.fit(X=data[self.features], y=data[self.target])

    def predict(self, X: typing.Iterable):
        if type(X).__name__ == "DataFrame":
            X = X[self.features].values

        elif type(X).__name__ == "dict":
            X = np.array([X[col] for col in self.features]).T

        pred = self._model.predict_proba(X)[:, 1]
        return pred


class LogisticRegressionClassifier(SKLeanClassifier):
    def __init__(self, data, output_name, **kwargs):
        import sklearn.linear_model
        if "penalty" not in kwargs:
            kwargs["penalty"]="none"
        super().__init__(sklearn.linear_model.LogisticRegression, data, output_name, **kwargs)

    def summary(self, ax=None):
        import pandas as pd    
        return pd.DataFrame(data={"coeff": self._model.coef_[0]}, index=self.features)


class RandomForestClassifier(SKLeanClassifier):
    def __init__(self, data, output_name, **kwargs):
        import sklearn.ensemble
        super().__init__(sklearn.ensemble.RandomForestClassifier, data, output_name, **kwargs)


class GradientBoostingClassifier(SKLeanClassifier):
    def __init__(self, data, output_name, **kwargs):
        import sklearn.ensemble
        super().__init__(sklearn.ensemble.GradientBoostingClassifier, data, output_name, **kwargs)



class SKLearnRegressor(BaseReportingMixin):
    def __init__(self, sklearn_regressor:type, data, output_name, **kwargs):
        self.features = list(data.columns)
        if output_name in self.features:
            self.features.remove(output_name)
            
        self.target = output_name

        self._model = sklearn_regressor(**kwargs)
        self._model.fit(X=data[self.features], y=data[self.target])

    def predict(self, X: typing.Iterable):
        if type(X).__name__ == "DataFrame":
            X = X[self.features].values

        elif type(X).__name__ == "dict":
            X = np.array([X[col] for col in self.features]).T

        pred = self._model.predict(X)
        return pred


class LinearRegression(SKLearnRegressor):
    def __init__(self, data, output_name, **kwargs):
        import sklearn.linear_model
        super().__init__(sklearn.linear_model.LinearRegression, data, output_name, **kwargs)
