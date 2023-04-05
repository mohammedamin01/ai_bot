import pandas as pd
import time
import requests
from utils.data_preprocessing import preprocess_data

def collect_data():
    """
    Collects real-time data from the exchange API and returns it as a pandas dataframe
    """
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        "fsym": "BTC",
        "tsym": "USD",
        "limit": 1, # get latest data point
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # raise an exception for any HTTP errors
        data = response.json()["Data"]["Data"]
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["time"], unit="s")
        df = df.set_index("timestamp")
        df = df[["open", "high", "low", "close", "volumeto"]]
        df.columns = ["open", "high", "low", "close", "volume"]
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching real-time data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return None

def preprocess_real_time_data():
    """
    Collects real-time data from the exchange API and preprocesses it
    """
    data = collect_data()
    if data is None:
        return
    try:
        data = preprocess_data(data)
        data = data.reshape(1, data.shape[0], data.shape[1])
        return data
    except Exception as e:
        print(f"Error preprocessing real-time data: {e}")
        return None

def continuously_collect_data(sleep_time=300):
    """
    Continuously collects real-time data and appends it to the historical data file
    """
    while True:
        data = collect_data()
        if data is None:
            time.sleep(sleep_time)
            continue
        try:
            with open("data/historical_data.csv", "a") as f:
                data.to_csv(f, header=False)
        except Exception as e:
            print(f"Error appending data to historical data file: {e}")
        time.sleep(sleep_time)

def get_latest_data():
    """
    Returns the latest data point from the historical data file
    """
    try:
        data = pd.read_csv("data/historical_data.csv", index_col=0)
        latest_data = data.iloc[-1]
        return latest_data.to_dict()
    except Exception as e:
        print(f"Error fetching latest data point: {e}")
        return None
