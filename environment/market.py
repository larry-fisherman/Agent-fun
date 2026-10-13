import pandas as pd

class Market:
    def __init__(self, prices: pd.DataFrame, starting_cash: float):
        self.prices = prices
        self.i = 0
        self.cash = starting_cash
        self.positions = {}

    def today(self) -> str:
        date = self.prices.index[self.i]
        return date.strftime("%Y-%m-%d")
    
    def get_history(self, ticker: str, lookback_days: int) -> pd.DataFrame:
        start = max(0, self.i - lookback_days + 1)
        return self.prices[ticker].iloc[start : self.i + 1]
    
    def buy(self, ticker: str, shares: int) -> str:
        cost = shares * self.price(ticker)
        if cost > self.cash:
            return "Insufficient cash"
        self.cash -= cost
        self.positions[ticker] = self.positions.get(ticker, 0) + shares
        return f"Bought {shares} shares of {ticker} at ${self.price(ticker):.2f}"

    def sell(self, ticker: str, shares: int) -> str:
        proceeds = shares * self.price(ticker)
        if self.positions[ticker] not in self.positions:
            return "No shares to sell"
        if self.positions[ticker] < shares:
            return "Insufficient shares"
        self.cash += proceeds
        self.postions[ticker] = self.positions.get(ticker, 0) - shares
        return f"Sold {shares} shares of {ticker} at ${self.price(ticker):.2f}"
    
    def portfolio(self) -> dict:
        total = self.cash
        date = self.prices.index[self.i]
        for ticker, shares in self.positions.items():
            total += shares * self.price(ticker)
        return {"date": self.today(), "cash": float(self.cash), "positions": dict(self.positions), "total_value": float(total)}

    def advance(self) -> bool:
        if self.i < len(self.prices) - 1:
            self.i += 1
            return True
        else:
            return False

    def price(self, ticker: str) -> float:
        return self.prices.iloc[self.i][ticker]
