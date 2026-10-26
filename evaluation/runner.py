import asyncio
from agent.agent import main
from agent.reviewer import reflect
from environment.buy_and_hold import baseline
import json
from pathlib import Path
from agent.memory import load_lessons

TRAIN = "data/prices_train.csv"
TEST = "data/prices.csv"


async def run_experiment(name: str, rounds: int = 3, test_runs: int = 3, max_weeks: int = 150, risk: bool=False, show_prices: bool = False, train_path: str = TRAIN, test_path: str = TEST):
    lessons = None
    lessons_path = None
    exp_dir = Path("experiments/runs") / name      
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    for r in range(1, rounds + 1):
        result = await run_or_resume(exp_dir / f"train_r{r}.result.json",
                                    exp_dir / f"train_r{r}.jsonl",
                                    data_path=train_path, lessons_path=lessons_path, max_weeks=max_weeks)
        lessons_path = exp_dir / f"lessons_v{r}.txt"
        if lessons_path.exists():
            lessons = load_lessons(lessons_path)
        else:
            lessons = await reflect(result["log_path"], train_path, str(lessons_path), previous_lessons=lessons, risk=risk, show_prices=show_prices)
    test_results = []
    for i in range(1, test_runs +1):
        result = await run_or_resume(exp_dir / f"test_{i}.result.json",
                                    exp_dir / f"test_{i}.jsonl",
                                    data_path=test_path, lessons_path=lessons_path, max_weeks=max_weeks)

        test_results.append(result)
        print(result)

    b = baseline(test_path)
    print("\n===== TEST RESULTS =====")
    print(f"Buy-and-hold:          {b['return']:+.1f}%  dd {b['max_drawdown']:.1f}%")
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

async def run_test(name: str, data_path: str, lessons_path: str | None, runs: int = 3, max_weeks: int = 150):
    exp_dir = Path("experiments/runs") / name
    exp_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i in range(1, runs + 1):
        result = await run_or_resume(exp_dir / f"test_{i}.result.json",
                                     exp_dir / f"test_{i}.jsonl",
                                     data_path=data_path, lessons_path=lessons_path, max_weeks=max_weeks)
        results.append(result)

    b = baseline(data_path)
    print(f"\n===== {name} =====")
    print(f"Buy-and-hold:  {b['return']:+.1f}%  dd {b['max_drawdown']:.1f}%")
    for i, r in enumerate(results, 1):
        print(f"Run {i}:         {r['return']:+.1f}%  dd {r['max_drawdown']:.1f}%")
    return results

HOLDOUT = "data/prices_(23-25).csv"

async def holdout():
    # the lessons from previous run are used on different data
    await run_test("reflextion_v1_(23-25)", HOLDOUT,
                   lessons_path="experiments/runs/reflexion_v1/lessons_v3.txt")
    # the same agent with NO lessons, on the same new period (the control)
    await run_test("reflextion_v1_(23-25)_nolessons", HOLDOUT, lessons_path=None)

async def risk_experiment(prefix: str = "reflexion_risk", max_weeks: int = 150):
    # train on 2018–19 with the risk-aware reviewer, then test on 2020–22
    await run_experiment(name=prefix, risk=True, max_weeks=max_weeks)
    # test the same final lessons on 2023–24
    await run_test(f"{prefix}_(23-25)", HOLDOUT,
                   lessons_path=f"experiments/runs/{prefix}/lessons_v3.txt",
                   max_weeks=max_weeks)

async def synthetic_experiment(levels=('strong', 'medium', 'weak', 'no_pattern'), prefix: str = "synth", max_weeks: int = 150):
    for level in levels:
        train = f"data/synthetic/{level}_train.csv"
        test = f"data/synthetic/{level}_test.csv"
        await run_experiment(name=f"{prefix}_{level}", train_path=train, test_path=test, risk=True, show_prices=True, max_weeks=max_weeks)
        await run_test(f"{prefix}_{level}_nolessons", test, lessons_path=None, max_weeks=max_weeks)

if __name__ == "__main__":
    asyncio.run(synthetic_experiment(prefix="reflexion_v3", max_weeks=150))



