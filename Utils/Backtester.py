from Utils.metrics import sharpe,total_return,max_drawdown
from Utils.portfolio import Portfolio
from Utils.Kelly import kelly_criterion

def run_backtests(df,actions,starting_cash):
    portfolio = Portfolio(starting_cash)
    equity_curve = []
    for i in range(len(actions)):
        current_price = df["Close"].iloc[i]
        if actions[i] == "Buy":
            wins = [t for t in portfolio.trade_history if t > 0]
            losses = [abs(t) for t in portfolio.trade_history if t < 0]
            if len(wins) >= 3 and len(losses) >= 3:
                fraction = kelly_criterion(wins, losses)
            else:
                fraction = 0.95
            amount = int((portfolio.cash * fraction) / current_price)
            portfolio.buy(current_price,amount)
        elif actions[i] == "Sell":
            amount = portfolio.shares
            portfolio.sell(current_price,amount)
        equity_curve.append(portfolio.portfolio_value(current_price))
    final_value = portfolio.portfolio_value(df["Close"].iloc[-1])
    totalreturn = total_return(final_value, starting_cash)
    maxdrawdown = max_drawdown(equity_curve)
    sharperatio = sharpe(equity_curve)
    return (final_value, equity_curve, totalreturn, maxdrawdown, sharperatio)
