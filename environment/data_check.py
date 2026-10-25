import pandas as pd
from environment.market import Market
from evaluation.metrics import total_return, max_drawdown



def rebalance_equal(m: Market, targets: list[str]) -> None:
    for t, shares in list(m.positions.items()):
        m.sell(t, shares)
    per_stock = m.cash / len(targets)
    for t in targets:
        shares = int(per_stock // m.price(t))
        if shares > 0:
            m.buy(t, shares)

def oracle_values(prices: pd.DataFrame, start_index: int, starting_cash: float = 100_000) -> dict:
    m = Market(prices, starting_cash, start_index=start_index)
    values = {}
    day = 0

    while True:
        if day % 5 == 0:                  
            dropped = []
            for t in prices.columns:
                h = m.get_history(t, 6)
                change = (h.iloc[-1] - h.iloc[0]) / h.iloc[0]
                if change < -0.04:
                    dropped.append(t)
            if dropped:
                rebalance_equal(m, dropped)
            else: 
                rebalance_equal(m, list(prices.columns))


        values[m.today()] = m.portfolio()["total_value"]
        if not m.advance():
            break
        day += 1

    return values, switches


if __name__ == "__main__":
    from environment.anonymize import anonymize
    from environment.buy_and_hold import baseline
    train = anonymize(pd.read_csv("data/synthetic/strong_train.csv", index_col=0, parse_dates=True))
    test = anonymize(pd.read_csv("data/synthetic/strong_test.csv", index_col=0, parse_dates=True))

    for level in ("no_pattern", "weak", "medium", "strong"):
        path = f"data/synthetic/{level}_test.csv"
        prices = anonymize(pd.read_csv(path, index_col=0, parse_dates=True))
        v = list(oracle_values(prices, start_index=30).values())
        b = baseline(path)
        print(f"{level:>10}: oracle {total_return(v):+.1f}%   buy-and-hold {b['return']:+.1f}%   "
              f"edge {total_return(v) - b['return']:+.1f}")
