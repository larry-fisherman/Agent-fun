import numpy as np
import pandas as pd
from pathlib import Path


def generate_prices(n_days: int, strength: float, seed: int, n_stocks: int = 3, start_index: int = 30, drift: float = 0.0003, vol: float = 0.015, threshold: float = -0.04) -> pd.DataFrame:
    """Random-walk prices with a planted rebound: after a weekly drop worse than
        `threshold`, a stock gets `strength` extra daily return for the next 5 days."""
    rng = np.random.default_rng(seed)
    prices = np.zeros((n_days, n_stocks))
    prices[0] = 100.0
    boost_left = np.zeros(n_stocks)

    for t in range(1, n_days):
        # normal price movement
        daily = drift + vol * rng.standard_normal(n_stocks)
        # planted rebound movement
        daily = daily +np.where(boost_left > 0, strength, 0.0)
        prices[t] = prices[t - 1] * (1 + daily)
        boost_left = np.maximum(boost_left - 1, 0)

        is_decision_day = t >= start_index and (t - start_index) % 5 == 0
        if is_decision_day:
            week_return = prices[t] / prices[t - 5] - 1
            boost_left = np.where(week_return < threshold, 5, boost_left)
    index = pd.bdate_range("2000-01-03", periods=n_days)
    columns = [f"S{i + 1}" for i in range(n_stocks)]
    return pd.DataFrame(prices, index=index, columns=columns)


if __name__ == "__main__":
    out = Path("data/synthetic")
    out.mkdir(parents=True, exist_ok=True)
    levels = {"strong": 0.010, "medium": 0.004, "weak": 0.0015, "no_pattern": 0.0}
    for name, strength in levels.items():
        generate_prices(504, strength, seed=1).to_csv(out / f"{name}_train.csv")
        generate_prices(504, strength, seed=2).to_csv(out / f"{name}_test.csv")

