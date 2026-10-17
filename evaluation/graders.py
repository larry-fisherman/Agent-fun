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

if __name__ == "__main__":
    for path in sorted(Path("experiments/results").glob("*.jsonl")):
        rows = load_log(path)
        anonymized = "_anon" in path.name
        leaks = find_leaks(rows, anonymized)
        print(f"{path.name} (anonymized={anonymized}): {len(leaks)} leaky weeks out of {len(rows)}")
        for leak in leaks:
            print(f"    week {leak['week']} ({leak['date']}): '{leak['word']}'")
