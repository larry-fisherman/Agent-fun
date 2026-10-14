import pandas as pd
from environment.market import Market
from evaluation.metrics import total_return, max_drawdown


prices= pd.read_csv("data/prices.csv", index_col=0, parse_dates=True)
STARTING_CASH = 100_000
m = Market(prices, STARTING_CASH, start_index=30)

per_ticker = STARTING_CASH / len(prices.columns)
for t in prices.columns:
    shares = int(per_ticker // m.price(t))
    print(m.buy(t, shares))

values = [m.portfolio()["total_value"]]
while m.advance():
    values.append(m.portfolio()["total_value"])

print(m.portfolio())
print(f"Return: {total_return(values):.1f}%")
print(f"Max drawdown: {max_drawdown(values):.1f}%")