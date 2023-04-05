import numpy as np
from sklearn.model_selection import GridSearchCV
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from models.ltsm import train_lstm_model
from .data import load_data


def create_model(num_units=256, dropout_rate=0.2, optimizer='adam'):
    # create LSTM model
    model = Sequential()
    model.add(LSTM(num_units, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer=optimizer)
    return model

num_units = [64, 128, 256, 512]
epochs = [100, 150, 200]
param_grid = dict(num_units=num_units, epochs=epochs)

def hyperparameter_tuning(X_train, y_train):
    # define model
    model = KerasRegressor(build_fn=create_model, verbose=0)
    # define the grid search parameters
    num_units = [32, 64, 128, 256]
    dropout_rate = [0.1, 0.2, 0.3]
    optimizer = ['adam', 'sgd']
    epochs = [50, 100, 150]
    batch_size = [32, 64, 128]
    param_grid = dict(num_units=num_units, dropout_rate=dropout_rate, optimizer=optimizer, epochs=epochs, batch_size=batch_size)
    # grid search
    grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, cv=3, scoring='neg_mean_squared_error')
    grid_result = grid.fit(X_train, y_train)
    # print results
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    return grid_result.best_params_

if __name__ == "__main__":
    # load training data
    X_train, y_train, X_test, y_test = load_data()

    # perform hyperparameter tuning
    best_params = hyperparameter_tuning(X_train, y_train)

    # train LSTM model using best parameters
    train_lstm_model(X_train, y_train, X_test, y_test, best_params)

