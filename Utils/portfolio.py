class Portfolio:

    def __init__(self , starting_cash):
        self.cash = starting_cash
        self.shares = 0
        self.trades = []
        self.avg_buy_price = 0
        self.trade_history = []
    
    def buy(self,price,amount):
        self.cash -= price * amount
        self.shares += amount
        self.avg_buy_price = price
    
    def sell(self,price,amount):

        self.cash += price * amount
        self.shares -= amount
        profit = (price - self.avg_buy_price) * amount
        self.trade_history.append(profit)
    
    def portfolio_value(self,current_price):
        Valtotal = self.cash + (self.shares * current_price)
        return Valtotal
    
if __name__ == "__main__":
    p = Portfolio(10000)
    print("Starting cash:", p.cash)
    p.buy(150, 10)
    print("After buying 10 shares at $150:")
    print("Cash:", p.cash)
    print("Shares:", p.shares)
    print("Portfolio value:", p.portfolio_value(150))
    p.sell(160, 10)
    print("After selling 10 shares at $160:")
    print("Cash:", p.cash)
    print("Portfolio value:", p.portfolio_value(160))