import tensorflow as tf
import pandas as pd
import numpy as np
import requests
import json
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import LSTM, Dense, Attention
from utils.data_preprocessing import preprocess_data
from app.data_stream import DataStreamer

def make_trade():
    try:
        # Load model
        model = load_model("models/model.h5")

        # Create data streamer instance
        streamer = DataStreamer()

        # Initialize trading parameters
        current_price = streamer.get_data()
        stop_loss = current_price * 0.98
        dynamic_stop_loss = current_price * 0.99
        take_profit1 = current_price * 1.01
        take_profit2 = current_price * 1.02

        # Execute trade
        while True:
            # Get latest data from data streamer
            current_price = streamer.get_data()
            data = pd.read_csv("data/historical_data.csv")
            data.loc[len(data)] = [current_price]
            data.to_csv("data/historical_data.csv", index=False)

            # Preprocess data
            data = preprocess_data(data)

            # Reshape data for model
            data = np.reshape(data, (data.shape[0], data.shape[1], 1))

            # Make prediction
            prediction = model.predict(data)[-1][0]

            # Determine trade
            price_change = current_price / data[-2][0] - 1
            stop_loss -= price_change
            dynamic_stop_loss -= price_change
            take_profit1 += price_change
            take_profit2 += price_change
            if prediction > 0.5:
                # Buy
                buy_price = current_price
                make_api_call("buy")
                while True:
                    current_price = streamer.get_data()
                    if current_price <= stop_loss or current_price <= dynamic_stop_loss:
                        make_api_call("sell")
                        break
                    elif current_price >= take_profit1:
                        make_api_call("sell")
                        make_api_call("buy")
                        take_profit1 = current_price * 1.01
                        take_profit2 = current_price * 1.02
                    elif current_price >= take_profit2:
                        make_api_call("sell")
                        make_api_call("buy")
                        take_profit1 = current_price * 1.01
                        take_profit2 = current_price * 1.02
            else:
                # Sell
                sell_price = current_price
                make_api_call("sell")
                while True:
                    current_price = streamer.get_data()
                    if current_price >= stop_loss or current_price >= dynamic_stop_loss:
                        make_api_call("buy")
                        break
                    elif current_price <= take_profit1:
                        make_api_call("buy")
                        make_api_call("sell")
                        take_profit1 = current_price * 0.99
                        take_profit2 = current_price * 0.98
                    elif current_price <= take_profit2:
                        make_api_call("buy")
                        make_api_call("sell")
                        take_profit1 = current_price * 0.99
                        take_profit2 = current_price * 0.98
    except Exception as e:
        raise Exception("Error occurred while executing trade") from e


def train_model(X_train, y_train, X_test, y_test, best_params):
    try:
        # Build model architecture
        model = Sequential()
        model.add(Attention(32, input_shape=(X_train.shape[1], 1)))
        model.add(Dense(1, activation='sigmoid'))

        # Compile model
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        # Train model
        model.fit(X_train, y_train, epochs=best_params['epochs'], batch_size=best_params['batch_size'], validation_data=(X_test, y_test))

        # Save model
        model.save("models/model.h5")
    except Exception as e:
        raise Exception("Error occurred while training model") from e
