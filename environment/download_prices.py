import yfinance as yf

def download(start: str, end: str, out_path: str) -> None:
    TICKERS = ["AAPL", "MSFT", "GOOGL"]
    df = yf.download(TICKERS, start, end, auto_adjust=True)
    df = df["Close"]
    df = df.dropna()
    df.to_csv(out_path)
    print(df.head())

if __name__ == "__main__":
    download("2018-01-01", "2020-01-01", "data/prices_train.csv")