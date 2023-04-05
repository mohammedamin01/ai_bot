import numpy as np
import pandas as pd


def remove_outliers(df):
    """
    Removes outliers from a pandas DataFrame using the Z-score method.
    """
    # Calculate the Z-score for each value in the DataFrame
    z_scores = np.abs((df - df.mean()) / df.std())

    # Remove rows where any value has a Z-score greater than 3
    df = df[(z_scores < 3).all(axis=1)]

    return df


def smooth_data(df, window=5):
    """
    Smooths a pandas DataFrame using a rolling window.
    """
    # Apply a rolling mean to the DataFrame
    smoothed = df.rolling(window=window).mean()

    # Drop the first (window - 1) rows, which will contain NaN values
    smoothed = smoothed.dropna()

    return smoothed


def handle_noise_outliers(df):
    """
    Handles noise and outliers in a pandas DataFrame.
    """
    # Remove outliers from the DataFrame
    df = remove_outliers(df)

    # Smooth the data using a rolling window
    df = smooth_data(df)

    return df
