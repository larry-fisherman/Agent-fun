import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage
from agent.tools import make_market_server
from environment.market import Market
import pandas as pd
from evaluation.metrics import total_return, max_drawdown


async def main():
    prices = pd.read_csv("data/prices.csv", index_col=0, parse_dates=True)
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
        system_prompt="You're an autonomus trader managing this portfolio. You make the decisions to buy and sell without human intervention. You can only use the tools that have been assigned and all trades fill at today's close. The goal is to maximize profits. With each trade, provide a short summary of what you did and why."
    )

    values = [market.portfolio()['total_value']]
    done = False
    week = 0
    max_weeks = 4

    while not done and week < max_weeks:
        prompt = f"Today is {market.today()}. Review your portfolio and recent price history, then make any trades you think are worthwhile."
        await run_step(prompt, options)

        for day in range(5):    #5 trading days in a week
            if not market.advance():
                done = True
                break
            values.append(market.portfolio()['total_value'])

        week += 1

    print("Final portfolio:", market.portfolio())
    print(f"Return: {total_return(values)}%")
    print(f"Max drawdown: {max_drawdown(values)}%")

async def run_step(prompt: str, options: ClaudeAgentOptions) -> None:
    async for message in query(prompt=prompt, options=options):        
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)  
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name} {block.input}") 
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}") 


asyncio.run(main())