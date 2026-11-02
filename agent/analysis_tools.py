import pandas as pd


def signal_table(prices: pd.DataFrame, signal: str, horizon_weeks: int, start_index: int = 30) -> pd.DataFrame:
    if not 1 <= horizon_weeks <= 4:
        raise ValueError("horizon_weeks must be between 1 and 4")
    rows = []
    h = horizon_weeks * 5
    for d in range(start_index, len(prices) - h, 5):        
        week = prices.iloc[d] / prices.iloc[d - 5] - 1   
        market = week.mean()
        for t in prices.columns:
            if signal == "own_1w":
                value = week[t]
            elif signal == "own_4w":
                value = prices[t].iloc[d] / prices[t].iloc[d - 20] - 1      
            elif signal == "market_1w":
                value = market
            elif signal == "relative_1w":
                value = week[t] - market
            else:
                raise ValueError(f"unknown signal {signal}")
            forward = prices[t].iloc[d + h] / prices[t].iloc[d] - 1
            rows.append({"signal": value, "forward": forward})

    df = pd.DataFrame(rows)
    df["bucket"] = pd.qcut(df["signal"], 5, labels=[1, 2, 3, 4, 5], duplicates="drop")
    return df.groupby("bucket", observed=True).agg(
        low=("signal", "min"), high=("signal", "max"), count=("forward", "size"),
        avg_next=("forward", "mean"), pct_positive=("forward", lambda x: (x > 0).mean()))
