from data.generator import generate_ohlcv
from Utils.Backtester import run_backtests
import random
def Monte_Carlo(num_simulations,stratergy):
    results = []
    for n in range(num_simulations):
        seed = random.randint(1,100)
        df = generate_ohlcv(seed)
        actions = stratergy(df)
        results.append(run_backtests(df,actions,10_000)) 
    return results

