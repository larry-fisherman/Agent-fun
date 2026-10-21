import pandas as pd
from environment.market import Market
from evaluation.metrics import total_return, max_drawdown


def momentum_values(prices: pd.DataFrame, start_index: int, lookback: int = 30, margin: float = 5.0, starting_cash: float = 100_000) -> dict:
    m = Market(prices, starting_cash, start_index=start_index)
    held = None 
    values = {}
    day = 0
    switches = 0

    while True:
        if day % 5 == 0:                  
            scores = {}
            for t in prices.columns:
                h = m.get_history(t, lookback + 1)
                scores[t] = (h.iloc[-1] - h.iloc[0]) / h.iloc[0] * 100

            best = max(scores, key=scores.get)

            if held is None or (best != held and scores[best] - scores[held] > margin):
                if held is not None:
                    m.sell(held, m.positions[held])  
                shares = int(m.cash // m.price(best))
                m.buy(best, shares)  
                held = best
                switches += 1

        values[m.today()] = m.portfolio()["total_value"]
        if not m.advance():
            break
        day += 1

    return values, switches


if __name__ == "__main__":
    from environment.anonymize import anonymize
    train = anonymize(pd.read_csv("data/prices_train.csv", index_col=0, parse_dates=True))
    test = anonymize(pd.read_csv("data/prices.csv", index_col=0, parse_dates=True))

    print("TRAIN (choose settings here)")
    results = []
    for lookback in (20, 30):
        for margin in (0, 5):
            values, switches = momentum_values(train, 30, lookback, margin)
            v = list(values.values())
            print(f"  lookback={lookback} margin={margin}: {total_return(v):+.1f}%  dd {max_drawdown(v):.1f}%  switches {switches}")
            results.append((total_return(v), lookback, margin))

    _, best_lb, best_margin = max(results)
    values, switches = momentum_values(test, 30, best_lb, best_margin)
    v = list(values.values())
    print(f"TEST with lookback={best_lb} margin={best_margin}: {total_return(v):+.1f}%  dd {max_drawdown(v):.1f}%  switches {switches}")
