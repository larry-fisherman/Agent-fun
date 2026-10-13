import yfinance as yf


TICKERS = ["AAPL", "MSFT", "GOOGL"]
df = yf.download(TICKERS, start="2020-01-01", end="2023-01-01", auto_adjust=True)
df = df["Close"]
df = df.dropna()
df.to_csv("data/prices.csv")
print(df.head())