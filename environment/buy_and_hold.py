import pandas as pd
from environment.market import Market
from evaluation.metrics import total_return, max_drawdown
from environment.anonymize import anonymize


def buy_and_hold_values(prices: pd.DataFrame, start_index: int, starting_cash: float = 100_000) -> dict:
    m = Market(prices, starting_cash, start_index=start_index)
    per_ticker = starting_cash / len(prices.columns)
    for t in prices.columns:
        shares = int(per_ticker // m.price(t))
        m.buy(t, shares)

    values = {m.today(): m.portfolio()["total_value"]}
    while m.advance():
        values[m.today()] = m.portfolio()["total_value"]
    return values

def baseline(data_path: str, start_index: int = 30) -> dict:
    prices = anonymize(pd.read_csv(data_path, index_col=0, parse_dates=True))
    v = list(buy_and_hold_values(prices, start_index).values())
    return {"return": total_return(v), "max_drawdown": max_drawdown(v)}

if __name__ == "__main__":
    prices = pd.read_csv("data/prices.csv", index_col=0, parse_dates=True)
    values = buy_and_hold_values(prices, start_index=30)
    v = list(values.values())
    print(f"Return: {total_return(v):.1f}%")
    print(f"Max drawdown: {max_drawdown(v):.1f}%")
