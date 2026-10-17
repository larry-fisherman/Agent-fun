import asyncio
import json
from datetime import datetime
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage
from agent.tools import make_market_server
from environment.market import Market
import pandas as pd
from evaluation.metrics import total_return, max_drawdown
from environment.anonymize import anonymize


async def main(anonymize_data: bool = True):
    run_name = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode = "anon" if anonymize_data else "real"
    log_path = Path("experiments/results") / f"{run_name}_{mode}.jsonl"
    prices = pd.read_csv("data/prices.csv", index_col=0, parse_dates=True)
    if anonymize_data:
        prices = anonymize(prices)

    market = Market(prices, 100_000, start_index=30)

    options=ClaudeAgentOptions(
        tools=[],
        mcp_servers={"market": make_market_server(market)},
        allowed_tools=[
            "mcp__market__get_portfolio", 
            "mcp__market__buy", 
            "mcp__market__sell", 
            "mcp__market__get_price_history"
        ],
        model="claude-haiku-4-5-20251001", 
        max_turns=8,
        system_prompt="You're an autonomous trader managing this portfolio. You make the decisions to buy and sell without human intervention. You can only use the tools that have been assigned and all trades fill at today's close. The goal is to maximize profits. With each trade, provide a short summary of what you did and why."
    )

    values = [market.portfolio()['total_value']]
    done = False
    week = 0
    max_weeks = 150

    while not done and week < max_weeks:
        prompt = f"Today is {market.today()}. Review your portfolio and recent price history, then make any trades you think are worthwhile."
        print(f"\n===== Week {week + 1}: {market.today()} =====")

        step = await run_step(prompt, options)
        step['week'] = week + 1
        step['date'] = market.today()
        step['portfolio_after'] = market.portfolio()
        with open(log_path, 'a') as f:
            f.write(json.dumps(step) + '\n')

        for _ in range(5):    #5 trading days in a week
            if not market.advance():
                done = True
                break
            values.append(market.portfolio()['total_value'])

        week += 1

    print("Final portfolio:", market.portfolio())
    print(f"Return: {total_return(values):.1f}%")
    print(f"Max drawdown: {max_drawdown(values):.1f}%")

async def run_step(prompt: str, options: ClaudeAgentOptions) -> dict:
    texts = []
    cost = None
    tool_calls = []

    async for message in query(prompt=prompt, options=options):        
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)  
                    texts.append(block.text)
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name} {block.input}") 
                    tool_calls.append({'name': block.name, 'input': block.input})
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}") 
            cost = message.total_cost_usd

    return {"text": "\n".join(texts), "tool_calls": tool_calls, "cost_of_run": cost}

if __name__ == "__main__":
    asyncio.run(main())
