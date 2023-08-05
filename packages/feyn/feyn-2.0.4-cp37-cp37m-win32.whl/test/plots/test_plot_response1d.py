import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from feyn.plots._model_response import (
    _determine_fixed_values,
    _cleanse_fixed_values,
    _features_not_by_or_in_fixed,
    _expand_fixed_value_combinations,
    _determine_by_input,
    _determine_max_char_len,
    _legend_table,
    _determine_legend,
    _determine_spacing_of_cols,
    _get_data_ranges,
    _set_partials_data,
)


class TestPlotResponse1d(unittest.TestCase):
    def setUp(self) -> None:
        self.data_4inputs = {
            "x1": [0, 1, 2, 3, 4, 5],
            "x2": [0, 0.1, 0.2, 0.3, 0.4, 0.5],
            "x3": [10, 11, 12, 13, 14, 15],
            "cat": ["apples", "apples", "pears", "oranges", "oranges", "apples"],
        }

        self.data_3inputs = self.data_4inputs.copy()
        self.data_3inputs.pop("x3")
        self.cat_list = ["cat"]
        self.by = "x2"

    def test_determine_fixed_values(self):

        with self.subTest("Assigns median if fixed is none and more than 3 keys"):
            fixed = None
            expected = {"x1": [2.5], "x3": [12.5], "cat": "apples"}
            actual = _determine_fixed_values(
                pd.DataFrame(self.data_4inputs), self.by, fixed, self.cat_list
            )

            assert actual == expected

        with self.subTest("Assigns median for features not fixed and more than 3 keys"):
            fixed = {"x1": 0}
            expected = {"x1": 0, "x3": [12.5], "cat": "apples"}
            actual = _determine_fixed_values(
                pd.DataFrame(self.data_4inputs), self.by, fixed, self.cat_list
            )

            assert actual == expected

        with self.subTest(
            "Assigns top 3 occuring categories for categoricals not fixed and 3 keys"
        ):
            fixed = {"x1": 4}
            expected = {"x1": 4, "cat": ["apples", "oranges", "pears"]}
            actual = _determine_fixed_values(
                pd.DataFrame(self.data_3inputs), self.by, fixed, self.cat_list
            )

            assert all(actual["cat"] == expected["cat"])

        with self.subTest("Assignes quartiles for features not fixed and 3 keys"):
            fixed = {"cat": "apples"}
            expected = {"x1": [1.25, 2.5, 3.75], "cat": "apples"}
            actual = _determine_fixed_values(
                pd.DataFrame(self.data_3inputs), self.by, fixed, self.cat_list
            )
            assert actual == expected

    def test_features_not_by_or_in_fixed(self):

        feature_list = ["x1", "x2", "x3", "x4"]
        fixed = {"x1": None}
        by = "x2"
        expected = ["x3", "x4"]
        actual = _features_not_by_or_in_fixed(feature_list, fixed, by)
        assert set(actual) == set(expected)

    def test_cleanse_fixed_values(self):

        with self.subTest("If float is passed then turned into list"):
            fixed = {"a": 4}
            expected = {"a": [4]}
            actual = _cleanse_fixed_values(fixed)
            assert actual == expected

        with self.subTest("If string is passed then turned into list"):
            fixed = {"a": "apples"}
            expected = {"a": ["apples"]}
            actual = _cleanse_fixed_values(fixed)
            assert actual == expected

        with self.subTest("If list is passed then nothing is done"):
            fixed = {"a": ["b", 4, "c"]}
            expected = fixed
            actual = _cleanse_fixed_values(fixed)
            assert actual == expected

    def test_expand_fixed_value_combinations(self):

        fixed = {"a": [2, 3], "b": [5, 6]}
        expected = [
            {"a": 2, "b": 5},
            {"a": 2, "b": 6},
            {"a": 3, "b": 5},
            {"a": 3, "b": 6},
        ]
        actual = _expand_fixed_value_combinations(fixed)
        assert actual == expected

    def test_determine_by_input(self):

        with self.subTest(
            "If by is numerical then linspace between min and max is returned"
        ):
            expected = np.linspace(0, 0.5, 100)
            actual = _determine_by_input(
                pd.DataFrame(self.data_4inputs), self.by, is_categorical=False
            )
            assert all(actual == expected)

        with self.subTest("If by is categorical then all unique categories are passed"):
            expected = ["apples", "oranges", "pears"]
            actual = _determine_by_input(
                pd.DataFrame(self.data_4inputs), "cat", is_categorical=True
            )
            assert all(actual == expected)

    def test_get_data_ranges(self):
        with self.subTest(
            "Takes the minimum and maximum of both sets, and adds a padding"
        ):
            axis_1 = [np.arange(0, 10 + 1), np.arange(0, 5 + 1)]
            axis_2 = [np.arange(5, 15 + 1), np.arange(-5, 2 + 1)]

            # Hardcoded for illustrative purposes
            min1, max1 = 0, 15
            min2, max2 = -5, 5

            diffs = [max1 - min1, max2 - (min2)]
            paddings = [diffs[0] * 0.05, diffs[1] * 0.05]

            expecteds = (min1 - paddings[0], max1 + paddings[0]), (
                min2 - paddings[1],
                max2 + paddings[1],
            )
            actuals = _get_data_ranges(axis_1, axis_2)

            for expected, actual in zip(expecteds, actuals):
                self.assertAlmostEqual(expected[0], actual[0])
                self.assertAlmostEqual(expected[1], actual[1])

    def test_legend(self):
        partials = [
            {"x1": 1.23, "x2": "apples", "x3": 123.456},
            {"x1": 987, "x2": "bananas", "x3": 100100},
        ]
        with self.subTest("Partial dictionary mapped to 2d np.array"):
            expected = np.array(
                [
                    ["x1", "x2", "x3"],
                    ["1.23", "apples", "1.23e+02"],
                    ["9.87e+02", "bananas", "1e+05"],
                ]
            )
            actual = _legend_table(partials)
            np.testing.assert_array_equal(actual, expected)

        with self.subTest("Find maximum character length in 1d np.array"):
            arr = np.array(
                ["potatoes", "a really long string", "a little bit longer string"]
            )
            expected = 26
            actual = _determine_max_char_len(arr)
            self.assertEqual(expected, actual)

        with self.subTest("Determine spacing of columns in 2d np.array"):
            mat = np.array(
                [
                    ["a", "a really long string", "shorter string"],
                    ["a quite long string", "tiny", "b"],
                    ["tiny string", "another big long string", "c"],
                ]
            )
            expected = np.array([22, 26, 14])
            actual = _determine_spacing_of_cols(mat, buffer=3)
            np.testing.assert_array_equal(expected, actual)

        with self.subTest("Partial dictionary mapped to formatted strings"):
            expected_title = np.array(
                [" " * 5 + "x1" + " " * 9 + "x2" + " " * 8 + "x3" + " " * 6]
            )
            expected_labels = np.array(
                [
                    "1.23" + " " * 7 + "apples" + " " * 4 + "1.23e+02",
                    "9.87e+02" + " " * 3 + "bananas" + " " * 3 + "1e+05" + " " * 3,
                ],
            )

            actual_title, actual_labels = _determine_legend(partials, buffer=3)
            np.testing.assert_array_equal(expected_title, actual_title)
            np.testing.assert_array_equal(expected_labels, actual_labels)

    def test_set_partials_data(self):

        with self.subTest("Data is set to initialized plots"):
            fixed_labels = ['banana plot']
            ax = plt.subplot()
            plots = [ax.plot(0., 0.)[0]]
            x = np.linspace(0, 1, 10)
            y = 2 * x
            axes = [x, y]
            _set_partials_data([axes], fixed_labels, plots, reverse_axis=False)

            expected_data = (x, y)
            actual = plots[0].get_data()
            np.testing.assert_array_almost_equal(expected_data[0], actual[0])
            np.testing.assert_array_almost_equal(expected_data[1], actual[1])
            #actual = _plot_partials(
            #    model, self.data_4inputs, "x1", fixed={"x2": [0.3], "x3": [12], "cat": ["oranges"]}, cat_list=self.cat_list, ax=ax
            #)
            #assert (actual is not None)

        #with self.subTest(
        #    "If by is categorical then by should be on the y axes and output on the x axes"
        #):
         #   fig, ax = plt.subplots()
         #   ax = _plot_partials(
         #       model, self.data_4inputs, "cat", fixed={"x2": [0.3], "x3": [12], "x1": [1]}, cat_list=self.cat_list, ax=ax
         #   )
         #   expected = "Predicted output_name", "cat"
         #   actual = ax.get_xlabel(), ax.get_ylabel()
         #   assert expected == actual


class FakeModel:
    def __init__(self):
        self.output = "output_name"

    def predict(self, data):
        return np.ones(len(data))
