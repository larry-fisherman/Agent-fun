import asyncio
from agent.agent import main
from agent.reviewer import reflect
from environment.buy_and_hold import baseline
import json
from pathlib import Path
from agent.memory import load_lessons

TRAIN = "data/prices_train.csv"
TEST = "data/prices.csv"


async def run_experiment(name: str, rounds: int = 3, test_runs: int = 3, max_weeks: int = 150):
    lessons = None
    lessons_path = None
    exp_dir = Path("experiments/runs") / name      
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    for r in range(1, rounds + 1):
        result = await run_or_resume(exp_dir / f"train_r{r}.result.json",
                                    exp_dir / f"train_r{r}.jsonl",
                                    data_path=TRAIN, lessons_path=lessons_path, max_weeks=max_weeks)
        lessons_path = exp_dir / f"lessons_v{r}.txt"
        if lessons_path.exists():
            lessons = load_lessons(lessons_path)
        else:
            lessons = await reflect(result["log_path"], TRAIN, str(lessons_path), previous_lessons=lessons)

    test_results = []
    for i in range(1, test_runs +1):
        result = await run_or_resume(exp_dir / f"test_{i}.result.json",
                                    exp_dir / f"test_{i}.jsonl",
                                    data_path=TEST, lessons_path=lessons_path, max_weeks=max_weeks)

        test_results.append(result)
        print(result)

    b = baseline(TEST)
    print("\n===== TEST RESULTS =====")
    print(f"Buy-and-hold:          {b['return']:+.1f}%  dd {b['max_drawdown']:.1f}%")
    print(f"No-lessons baseline:   +24.1% avg  dd -35.7% avg   (from earlier runs)")
    for i, r in enumerate(test_results, 1):
        print(f"With lessons, run {i}:  {r['return']:+.1f}%  dd {r['max_drawdown']:.1f}%   {r['log_path']}")

def load_result(path):
    path = Path(path)
    return json.loads(path.read_text()) if path.exists() else None


def save_result(result, path):
    Path(path).write_text(json.dumps(result))


async def run_or_resume(result_path, log_path, **main_args):
    result = load_result(result_path)
    if result is not None:
        print(f"skip (done): {result_path}")
        return result
    Path(log_path).unlink(missing_ok=True)          # clear any half-finished log
    result = await main(log_path=str(log_path), **main_args)
    save_result(result, result_path)
    return result


if __name__ == "__main__":
    asyncio.run(run_experiment())  
