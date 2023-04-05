import pandas as pd
import requests
import time

def fetch_live_data():
    """
    Fetches live data from the CryptoCompare API and returns it as a pandas dataframe
    """
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        "fsym": "BTC",
        "tsym": "USD",
        "limit": 2000, # get last 2000 days of day data
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
        print(f"Error fetching live data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return None

def append_live_data():
    """
    Fetches live data and appends it to the historical data
    """
    live_data = fetch_live_data()
    if live_data is None:
        return
    try:
        historical_data = pd.read_csv("data/historical_data.csv", index_col="timestamp")
        new_data = pd.concat([historical_data, live_data])
        new_data = new_data[~new_data.index.duplicated(keep="first")] # remove duplicates
        new_data.to_csv("data/historical_data.csv")
    except Exception as e:
        print(f"Error appending live data: {e}")
