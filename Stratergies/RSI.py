import numpy as np
import pandas as pd

def RSI(df, period = 14):
    actions = []
    change = df["Close"].diff()
    gain = change.clip(lower = 0)
    loss = -change.clip(upper = 0)

    avg_gain = gain.ewm(alpha = 1/period, min_periods = period).mean()
    avg_loss = loss.ewm(alpha = 1/period, min_periods = period).mean()
    RS = avg_gain/avg_loss
    RSI_value = 100 - (100/(1+RS))
    for value in RSI_value:
        if value < 40:
            actions.append("Buy")
        elif value > 60:
            actions.append("Sell")
        else:
            actions.append(None)

    return actions


if __name__ == "__main__":
    from data.generator import generate_ohlcv
    df = generate_ohlcv()
    print(RSI(df))
  