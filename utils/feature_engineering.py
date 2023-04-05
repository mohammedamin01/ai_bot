from ta.volatility import BollingerBands
from ta.trend import MACD as MACD2
from ta.trend import IchimokuIndicator

def add_technical_indicators(df):
    # Add technical indicators to the dataframe
    # Relative Strength Index (RSI)
    rsi_indicator = RSIIndicator(close=df["close"], window=14)
    df["rsi"] = rsi_indicator.rsi()

    # Stochastic Oscillator
    stochastic_oscillator = StochasticOscillator(
        high=df["high"], low=df["low"], close=df["close"], window=14, smooth_window=3
    )
    df["stoch"] = stochastic_oscillator.stoch()

    # Exponential Moving Average (EMA)
    ema_20 = EMAIndicator(close=df["close"], window=20)
    df["ema_20"] = ema_20.ema_indicator()

    # Moving Average Convergence Divergence (MACD)
    macd = MACD(close=df["close"], window_fast=12, window_slow=26, window_sign=9)
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()

    # Bollinger Bands
    bb_indicator = BollingerBands(close=df["close"], window=50, window_dev=3)
    df["bb_bbm"] = bb_indicator.bollinger_mavg()
    df["bb_bbh"] = bb_indicator.bollinger_hband()
    df["bb_bbl"] = bb_indicator.bollinger_lband()

    # Moving Average Crossover (MAC)
    mac_indicator = MACD2(close=df["close"], window_fast=5, window_slow=10, window_sign=15)
    df["mac"] = mac_indicator.macd()

    # Ichimoku Clouds
    ichimoku_indicator = IchimokuIndicator(high=df["high"], low=df["low"], window1=5, window2=26, window3=100)
    df["ichimoku_base_line"] = ichimoku_indicator.ichimoku_base_line()
    df["ichimoku_conversion_line"] = ichimoku_indicator.ichimoku_conversion_line()
    df["ichimoku_a"] = ichimoku_indicator.ichimoku_a()
    df["ichimoku_b"] = ichimoku_indicator.ichimoku_b()

    return df
