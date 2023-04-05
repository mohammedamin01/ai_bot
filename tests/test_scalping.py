import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from scalping import make_trade

@pytest.fixture
def historical_data():
data = {
"timestamp": [pd.Timestamp("2022-01-01"), pd.Timestamp("2022-01-02")],
"open": [1.0, 2.0],
"high": [2.0, 3.0],
"low": [0.5, 1.5],
"close": [1.5, 2.5],
"volume": [1000, 2000]
}
return pd.DataFrame(data).set_index("timestamp")

def test_make_trade_buy(historical_data):
with patch("scalping.load_model") as mock_load_model:
mock_load_model.return_value = MockLSTMModel()
with patch("scalping.make_api_call") as mock_make_api_call:
make_trade(historical_data=historical_data)
mock_make_api_call.assert_called_with("buy")

def test_make_trade_sell(historical_data):
with patch("scalping.load_model") as mock_load_model:
mock_load_model.return_value = MockLSTMModel(prediction=0.4)
with patch("scalping.make_api_call") as mock_make_api_call:
make_trade(historical_data=historical_data)
mock_make_api_call.assert_called_with("sell")

class MockLSTMModel:
def predict(self, data):
return np.array([[0.6], [0.4]])