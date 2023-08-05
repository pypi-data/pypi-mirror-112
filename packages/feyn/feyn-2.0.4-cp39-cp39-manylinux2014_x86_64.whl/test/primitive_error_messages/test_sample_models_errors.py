import unittest
import pytest

from feyn._qlattice import connect_qlattice, _kind_to_output_stype, _sanitize_iterable, _validate_names, _validate_mc

import pandas as pd
import numpy as np

class TestSampleModelsErrors(unittest.TestCase):

    def setUp(self):
        self.ql = connect_qlattice()
        self.input_names = ["hello", "hola"]
        self.output_name = "apples"

    def test_input_errors(self):
        with self.subTest("ValueError when input names is a number"):
            with pytest.raises(ValueError) as ve:
                input_names = 45
                self.ql.sample_models(
                    input_names=input_names,
                    output_name=self.output_name,
                    max_complexity=1
                )
            assert str(ve.value) == f"Can not interpret {input_names} as a list"

        with self.subTest("ValueError when input names contains a number"):
            with pytest.raises(ValueError) as ve:
                input_names = ["hello", 42]
                self.ql.sample_models(
                    input_names=input_names,
                    output_name=self.output_name,
                    max_complexity=1
                )
            assert str(ve.value) == "Input names needs to be a python list of strings."

        with self.subTest("ValueError when input names contains duplicates"):
            with pytest.raises(ValueError) as ve:
                input_names = ["hello", "hello"]
                self.ql.sample_models(
                    input_names=input_names,
                    output_name=self.output_name,
                    max_complexity=1
                )
            assert str(ve.value) == "Duplicate input names are found"

        with self.subTest("Exception when no inputs are passed"):
            with pytest.raises(Exception) as ex:
                input_names = []
                self.ql.sample_models(
                    input_names=input_names,
                    output_name=self.output_name,
                    max_complexity=1
                )
            assert str(ex.value) == "A QLattice simulation must have at least one input feature."


    def test_output_name_errors(self):
        with pytest.raises(ValueError) as ve:
            output_name = 42
            self.ql.sample_models(
                input_names=self.input_names,
                output_name=output_name,
                max_complexity=1
            )
        assert str(ve.value) == f"output_name {output_name} is not a string."

    def test_max_complexity_errors(self):
        with self.subTest("ValueError when max_complexity is not a number"):
            with pytest.raises(ValueError) as ve:
                mc = "apples"
                self.ql.sample_models(
                    input_names=self.input_names,
                    output_name=self.output_name,
                    max_complexity=mc
                )
            assert str(ve.value) == f"Could not interpret max_complexity {mc} as an integer."

        with self.subTest("ValueError when max_complexity is negative"):
            with pytest.raises(ValueError) as ve:
                mc = -20
                self.ql.sample_models(
                    input_names=self.input_names,
                    output_name=self.output_name,
                    max_complexity=mc
                )
            assert str(ve.value) == f"max_complexity needs to be greater than 0, but was {mc}."

    def test_kind_errors(self):
        with pytest.raises(ValueError) as ve:
            kind = "hello"
            self.ql.sample_models(
                input_names=self.input_names,
                output_name=self.output_name,
                kind=kind,
                max_complexity=1
            )
        assert str(ve.value) == "Model kind not understood. Please choose either a 'regressor' or a 'classifier'."

    def test_query_string_errors(self):
        with pytest.raises(ValueError) as ve:
            query_str = 42
            self.ql.sample_models(
                input_names=self.input_names,
                output_name=self.output_name,
                max_complexity=1,
                query_string=query_str
            )
        assert str(ve.value) == "query_string is not a string."

    def test_function_names_errors(self):
        with self.subTest("ValueError when function names is a number"):
            with pytest.raises(ValueError) as ve:
                fnames = 34
                self.ql.sample_models(
                    input_names=self.input_names,
                    output_name=self.output_name,
                    max_complexity=1,
                    function_names=fnames
                )
            assert str(ve.value) == "function_names needs to be a python list of strings."

        with self.subTest("ValueError when no functions are recognised"):
            with pytest.raises(ValueError) as ve:
                fnames = ["apples", "oranges"]
                self.ql.sample_models(
                    input_names=self.input_names,
                    output_name=self.output_name,
                    max_complexity=1,
                    function_names=fnames
                )
            assert str(ve.value) == f"No functions in {fnames} were recognised."




