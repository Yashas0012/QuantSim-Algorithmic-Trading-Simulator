import pandas as pd
import numpy as np


def ma_crossover(df,short_window = 20,long_window = 50):
    closes = df["Close"].to_numpy()
    long_window_ma_values = np.full(len(closes),np.nan)
    for f in range(long_window,len(closes)):
        long_window_ma_values[f] = closes[f-long_window:f].mean()
    short_window_ma_values = np.full(len(closes), np.nan)
    for s in range(short_window, len(closes)):
        short_window_ma_values[s] = closes[s-short_window:s].mean()
    action = []
    for i in range(1,len(closes)):
        if i < short_window:
            action.append(None)
        else:
            if long_window_ma_values[i-1] < short_window_ma_values[i-1] and long_window_ma_values[i] > short_window_ma_values[i]:
                action.append("Buy")
            elif long_window_ma_values[i-1] > short_window_ma_values[i-1] and long_window_ma_values[i] <  short_window_ma_values[i]:
                action.append("Sell")
            else:
                action.append(None)
    return action

if __name__ == "__main__":
    from data.generator import generate_ohlcv
    df = generate_ohlcv()
    print(ma_crossover(df))
    