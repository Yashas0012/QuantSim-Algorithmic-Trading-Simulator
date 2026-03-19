import numpy as np
import pandas as pd

def total_return(final_value,starting_value):
    return  ((final_value-starting_value)/starting_value)

def max_drawdown(equity_curve):
    if len(equity_curve) == 0:
        return 0
    equity_curve = np.array(equity_curve)
    max_drawdown = 0
    running_max = equity_curve[0]

    for value in equity_curve:
        if value > running_max:
            running_max = value

        drawdown = (value - running_max) / running_max

        if drawdown < max_drawdown:
            max_drawdown = drawdown

    return max_drawdown

def sharpe(equity_curve):
    if len(equity_curve) == 0:
        return 0
    equity_curve = np.array(equity_curve)
    returns = np.diff(equity_curve)/equity_curve[:-1]
    average_return = np.mean(returns)
    standard_deviation = np.std(returns,ddof = 1)
    if standard_deviation == 0 or np.isnan(standard_deviation):
        return 0
    else:
        return (average_return/standard_deviation) * (252**(0.5))
