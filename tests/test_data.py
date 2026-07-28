import pytest
from src.data_processing import DataProcessor

def test_data_loading():
    dp = DataProcessor()
    X, y = dp.load_data()
    assert X.shape[0] == y.shape[0]
    assert X.shape[1] == 8
