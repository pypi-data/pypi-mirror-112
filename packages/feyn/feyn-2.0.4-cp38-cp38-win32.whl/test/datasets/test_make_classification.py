import unittest
import pytest
import feyn

class TestMakeClassification(unittest.TestCase):

    def test_make_classification(self):
        import pandas as pd
        from sklearn.datasets import make_classification
        from sklearn.model_selection import train_test_split
        
        random_state = 42
        train, test = feyn.datasets.make_classification(random_state=random_state)

        X, y = make_classification(random_state=random_state)
        data = pd.DataFrame(X, columns=[f'x{i}' for i in range(X.shape[1])])
        data['y'] = y
        train_act, test_act = train_test_split(data, random_state=random_state)

        assert all(train == train_act)
        assert all(test == test_act)

    def test_raise_error_for_bad_kwarg(self):
        with pytest.raises(Exception) as e_info:
            feyn.datasets.make_classification(flavour='yellow')
