import json
from pathlib import Path


# events
EVENT_WORDS = [
    "covid", "pandemic", "coronavirus", "lockdown", "vaccine", "federal reserve", "the fed", "rate hike", "inflation", "recession", "fed ", "interest rate",
    ]
# companies and tickers
NAME_WORDS = [
    "apple", "microsoft", "google", "alphabet", "aapl", "msft", "googl",
    ]



def load_log(path) -> list[dict]:
    rows = []
    with open(path) as f:
        for line in f:
            rows.append(json.loads(line))
    return rows
    
def find_leaks(rows: list[dict], anonymized: bool) -> list[dict]:
    words = EVENT_WORDS + NAME_WORDS if anonymized else EVENT_WORDS
    leaks = []
    for row in rows:
        text = row['text'].lower()
        for word in words:
            if word in text:
                leaks.append({"week": row["week"], "date": row["date"], "word": word})
                break
    return leaks

def largest_position_pct(row: dict, prices) -> float:
    """% of the portfolio in the single largest position, for one week."""
    p = row["portfolio_after"]
    position_values = [shares * prices.loc[row["date"], ticker]
                       for ticker, shares in p["positions"].items()]
    largest = max(position_values) if position_values else 0
    return largest / p["total_value"] * 100


def concentration(rows: list[dict], prices) -> float:
    """Average % of the portfolio held in the single largest position."""
    pcts = [largest_position_pct(row, prices) for row in rows]
    return sum(pcts) / len(pcts)

def trade_count(rows: list[dict]) -> int:
    count = 0
    for row in rows:
        for call in row["tool_calls"]:
            if call["name"].endswith('buy') or call['name'].endswith('sell'):
                count += 1
    return count

if __name__ == "__main__":
    import pandas as pd
    from environment.anonymize import anonymize

    def load_prices(path):
        return pd.read_csv(path, index_col=0, parse_dates=True)

    PRICES = {
        "train_anon": anonymize(load_prices("data/prices_train.csv")),
        "test_anon": anonymize(load_prices("data/prices.csv")),
        "test_real": load_prices("data/prices.csv"),
    }

    paths = sorted(Path("experiments/results/baseline").glob("*.jsonl")) + \
            sorted(Path("experiments/runs").glob("*/*.jsonl"))

    for path in paths:
        rows = load_log(path)
        is_real = path.parent.name == "baseline" and "_anon" not in path.name
        if is_real:
            prices = PRICES["test_real"]
        elif path.name.startswith("train"):
            prices = PRICES["train_anon"]
        else:
            prices = PRICES["test_anon"]

        leaks = find_leaks(rows, anonymized=not is_real)
        print(f"{path.parent.name}/{path.name}: leaks {len(leaks)}, "
              f"trades {trade_count(rows)}, concentration {concentration(rows, prices):.0f}%")
