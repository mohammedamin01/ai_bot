import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from utils.data_preprocessing import preprocess_data
from utils.feature_engineering import engineer_features
from utils.noise_outlier_handling import handle_noise_outliers

def load_data():
    """
    Loads the latest historical data from data/historical_data.csv
    """
    data = pd.read_csv("data/historical_data.csv")
    X, y = engineer_features(data)
    X, y = handle_noise_outliers(X, y)
    X = preprocess_data(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    return X_train, y_train, X_test, y_test

def train_model(X_train, y_train, X_test, y_test, best_params):
    """
    Trains the machine learning model using the provided data and hyperparameters
    """
    model = Sequential()
    model.add(LSTM(units=best_params["lstm_units"], return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dropout(best_params["dropout"]))
    model.add(LSTM(units=best_params["lstm_units"]))
    model.add(Dropout(best_params["dropout"]))
    model.add(Dense(units=1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(X_train, y_train, epochs=best_params["epochs"], batch_size=best_params["batch_size"], validation_data=(X_test, y_test))
    model.save("models/model.h5")
