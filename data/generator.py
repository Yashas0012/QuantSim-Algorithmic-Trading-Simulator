import pandas as pd
import numpy as np
import random
s = random.randint(30,70)
def generate_ohlcv(n_days = 1000 ,start_price = 152.00,seed = s):
    rng = np.random.default_rng(seed)
    daily_returns = rng.normal(0.0005,0.02,n_days)
    multipliers = 1 + daily_returns
    close_price = np.cumprod(multipliers) * start_price
    open_price = np.concatenate([np.array([start_price]),close_price[:-1]])
    high = np.maximum(open_price,close_price) + rng.normal(0,0.01*close_price,n_days)
    low = np.minimum(open_price,close_price) - rng.normal(0,0.01*close_price,n_days)
    volume = (1_000_000 * rng.lognormal(0,0.5,n_days)).astype(int)  
    dates = pd.date_range(start = "2020-01-01", periods = n_days , freq = "B")
    return pd.DataFrame({
        "Date" : dates,
        "Open" : open_price,
        "High" : high,
        "Low"  : low,
        "Close": close_price,
        "Volume": volume

                })

if __name__ == "__main__":
    print(generate_ohlcv())
     
