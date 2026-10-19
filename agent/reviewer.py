from evaluation.graders import load_log
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage
from environment.buy_and_hold import buy_and_hold_values
from environment.anonymize import anonymize
import pandas as pd
from agent.memory import extract_lessons, save_lessons
from pathlib import Path


REVIEWER_PROMPT = """You review the performance of an autonomous trading agent and write lessons to improve it.

## The simulation
- The agent manages $100,000 across 3 anonymised stocks (STOCK_A, STOCK_B, STOCK_C).
- It makes one decision per week. Trades fill at that day's closing price. Each row's value is recorded right after that week's trades.So the change from row N to row N+1 is caused by the holdings after week N's trades.
- There are no transaction costs, no fees, and no slippage. Do not attribute results to trading costs.
- The agent's goal is to beat a buy-and-hold strategy that splits the cash equally across the 3 stocks on the first day and never trades.

## What you are given
A week-by-week table with: the trades made that week, the agent's portfolio value,
the buy-and-hold value on the same day, and the gap between them (negative = agent is behind).

## How to analyse
- The gap changes provides information on where the buy and hold strategy did better.
- For those periods where there is a large gap, look at what the agent was doing differently from buy-and-hold.
- Only report a pattern if it occurs several times. One bad week is not a lesson.

## What the lessons are for
Your lessons will be added to the agent's instructions for a DIFFERENT time period it has never seen.
So each lesson must be a general rule of behaviour: no day numbers, no week numbers, no stock names in the lesson itself.

## Rules for evidence
- Support every lesson with at least 2 rows from the table, copied exactly.
- If you cannot find enough evidence, write fewer lessons. 2 well-supported lessons are better than 5 weak ones.
- Do not give generic trading advice (e.g. "diversify", "manage risk") unless the table shows that specific mistake.

## Output format
For each lesson:
LESSON: <one or two sentence rule the agent can follow>
EVIDENCE: <copied rows>
WHY: <what the rows show>

Then end with the lessons only, with no evidence, inside tags:
<lessons>
1. ...
2. ...
</lessons>
"""


def summarize_log(path, bah) -> str:
    rows = load_log(path)
    lines = []
    for row in rows:
        trades = []
        for call in row['tool_calls']:
            if call['name'].endswith('buy') or call['name'].endswith('sell'):
                action = 'BUY' if call['name'].endswith('buy') else 'SELL'
                trades.append(f'{action} {call['input']['ticker']} {call['input']['shares']}')
        trade_text = ', '.join(trades) if trades else '(no trades)'
        value = row['portfolio_after']['total_value']
        bah_value = bah[row['date']]
        gap = ((value - bah_value) / bah_value) * 100
        lines.append(f'Week {row['week']} | {row['date']} | {trade_text} | agent value ${value:,.0f} | buy & hold ${bah_value:,.0f} | gap {gap:+.1f}%')
    start_value = rows[0]['portfolio_after']['total_value']
    end_value = rows[-1]['portfolio_after']['total_value']
    agent_return = ((end_value - start_value) / start_value) * 100
    bah_return = ((list(bah.values())[-1] - list(bah.values())[0]) / list(bah.values())[0]) * 100
    lines.append(f'Final: agent {agent_return:+.1f}%, buy-and-hold {bah_return:+.1f}%')
    return '\n'.join(lines)

async def review (summary: str, previous_lessons: str | None = None) -> str:
    options = ClaudeAgentOptions(
        tools = [],
        model = "claude-sonnet-5-5", 
        max_turns = 1,
        system_prompt = REVIEWER_PROMPT,
    )

    prompt = f"Here is the trading agent's week-by-week record:\n\n{summary}\n\n"

    if previous_lessons:
        prompt += (
            "During this run, the agent was following these lessons:\n"
            f"{previous_lessons}\n\n"
            "Judge each lesson against the record: keep it if the agent followed it and it helped, "
            "revise it if it was unclear or only partly helped, and drop it if it hurt.\n\n"
        )
    
    prompt += "Write your lessons."

    texts = []
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    texts.append(block.text)
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}") 
    return '\n'.join(texts)
    
async def reflect(log_path: str, data_path: str, out_path: str, previous_lessons: str | None = None) -> str:
    prices = anonymize(pd.read_csv(data_path, index_col=0, parse_dates=True))
    bah = buy_and_hold_values(prices, start_index=30)
    summary = summarize_log(log_path, bah)
    review_text = await review(summary, previous_lessons)
    out_path = Path(out_path)
    review_path = out_path.with_name(out_path.stem + "_review.txt")
    save_lessons(review_text, review_path)
    lessons = extract_lessons(review_text)
    save_lessons(lessons, out_path)
    return lessons


