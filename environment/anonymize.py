import pandas as pd


def anonymize(prices: pd.DataFrame) -> pd.DataFrame:
    anon = prices.copy()

    # 1. Price levels: every stock starts at 100
    anon = anon / anon.iloc[0] * 100

    # 2. Tickers: AAPL, GOOGL, MSFT -> STOCK_A, STOCK_B, STOCK_C
    names = []                                  
    for n in range(len(prices.columns)):         
        names.append(f"STOCK_{chr(65 + n)}")     
    anon.columns = names                         


    # 3. Dates: 2020-01-02, ... -> Day 0, Day 1, ...
    days = []
    for n in range(len(anon.index)):
        days.append(f"Day {n}")
    anon.index = days

    return anon
