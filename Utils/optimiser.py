from Utils.metrics import sharpe
from Utils.Backtester import run_backtests




short_range = [n for n in range(5,31,5)]
long_range = [n for n in range(20,101,20)]

param_grid_ma = []
param_grid_RSI = []
for short in short_range:
    for long in long_range:
        if short < long:
            param_grid_ma.append({
                "short_window" : short ,
                "long_window" : long
            }) 

period = [n for n in range (5,40,5)]
for number in period:
    param_grid_RSI.append({
        "period" : number
    })



def optimise(strategy, df, param_grid):
    best_score = -999
    best_params = None
    results = []

    for params in param_grid:
        signals = strategy(df, **params)
        final_value, equity_curve, totalreturn, maxdrawdown, sharpe_ratio = run_backtests(df, signals, 10000)
        score = sharpe_ratio
        results.append({
            "params" : params,
            "score"  : sharpe_ratio,
            "final_value" : final_value
        })
        


        if score > best_score:
            best_score = score
            best_params = params

    return best_params, best_score, results