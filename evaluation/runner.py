import asyncio
from agent.agent import main
from agent.reviewer import reflect
from environment.buy_and_hold import baseline


TRAIN = "data/prices_train.csv"
TEST = "data/prices.csv"


async def run_experiment(rounds: int = 3, test_runs: int = 3, max_weeks: int = 150):
    lessons = None
    lessons_path = None

    for r in range(1, rounds + 1):
        result = await main(data_path=TRAIN, lessons_path=lessons_path, max_weeks=max_weeks)
        lessons_path = f"experiments/lessons/lessons_train_v{r}.txt"
        lessons = await reflect(result["log_path"], TRAIN, lessons_path, previous_lessons=lessons)

    test_results = []
    for _ in range(test_runs):
        result = await main(data_path=TEST, lessons_path=lessons_path, max_weeks=max_weeks)
        test_results.append(result)
        print(result)

    b = baseline(TEST)
    print("\n===== TEST RESULTS =====")
    print(f"Buy-and-hold:          {b['return']:+.1f}%  dd {b['max_drawdown']:.1f}%")
    print(f"No-lessons baseline:   +24.1% avg  dd -35.7% avg   (from earlier runs)")
    for i, r in enumerate(test_results, 1):
        print(f"With lessons, run {i}:  {r['return']:+.1f}%  dd {r['max_drawdown']:.1f}%   {r['log_path']}")

if __name__ == "__main__":
    asyncio.run(run_experiment(max_weeks=4))   # dry run first
