import pandas as pd

class Market:
    def __init__(self, prices: pd.DataFrame, starting_cash: float, start_index: int = 0):
        self.prices = prices
        self.i = start_index
        self.cash = starting_cash
        self.positions = {}

    def _check_ticker(self, ticker: str) -> None:
        if ticker not in self.prices.columns:
            available = ", ".join(self.prices.columns)
            raise ValueError(f"Unknown ticker '{ticker}'. Available: {available}")

    def _check_shares(self, shares: int) -> None:
        if shares <= 0:
            raise ValueError("Shares must be a positive whole number.")

    def today(self) -> str:
        date = self.prices.index[self.i]
        if hasattr(date, 'strftime'):
            return date.strftime("%Y-%m-%d")
        return str(date)
    
    def get_history(self, ticker: str, lookback_days: int) -> pd.DataFrame:
        self._check_ticker(ticker)
        start = max(0, self.i - lookback_days + 1)
        return self.prices[ticker].iloc[start : self.i + 1]
    
    def buy(self, ticker: str, shares: int) -> str:
        self._check_ticker(ticker)
        self._check_shares(shares)
        cost = shares * self.price(ticker)
        if cost > self.cash:
            raise ValueError(f"Insufficient cash: need ${cost:.2f}, have ${self.cash:.2f}")
        self.cash -= cost
        self.positions[ticker] = self.positions.get(ticker, 0) + shares
        return f"Bought {shares} shares of {ticker} at ${self.price(ticker):.2f}"

    def sell(self, ticker: str, shares: int) -> str:
        self._check_ticker(ticker)
        self._check_shares(shares)
        owned = self.positions.get(ticker, 0)
        if owned < shares:
            raise ValueError(f"Insufficient shares: you own {owned} {ticker}")
        self.cash += shares * self.price(ticker)
        self.positions[ticker] = owned - shares
        if self.positions[ticker] == 0:
            del self.positions[ticker]
        return f"Sold {shares} shares of {ticker} at ${self.price(ticker):.2f}"
    
    def portfolio(self) -> dict:
        total = self.cash
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
