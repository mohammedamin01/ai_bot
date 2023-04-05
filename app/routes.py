from flask import Flask, render_template
from trading import make_trade, monitor_performance
from utils.hyperparameter_tuning import hyperparameter_tuning
from utils.model_training import train_model, load_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/make_trade")
def trade():
    try:
        make_trade()
        return "Trade executed successfully!"
    except Exception as e:
        return f"Error occurred while executing trade: {e}"

@app.route("/monitor_performance")
def monitor():
    try:
        performance = monitor_performance()
        return f"Bot performance: {performance}"
    except Exception as e:
        return f"Error occurred while monitoring bot performance: {e}"

@app.route("/train_model")
def train():
    try:
        # load training data
        X_train, y_train, X_test, y_test = load_data()

        # perform hyperparameter tuning
        best_params = hyperparameter_tuning(X_train, y_train)

        # train model using best parameters
        train_model(X_train, y_train, X_test, y_test, best_params)

        return "Model trained successfully!"
    except Exception as e:
        return f"Error occurred while training model: {e}"

if __name__ == "__main__":
    app.run()
