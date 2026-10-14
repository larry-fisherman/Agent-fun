import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage, AgentDefinition
from agent.tools import make_market_server
from environment.market import Market
import pandas as pd


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

    async for message in query(
        prompt="Check my portfolio, look at the last 20 days of AAPL, then decide whether to buy some. Explain why.",
        options=options,
    ):        
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)  
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}") 
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}") 

    print("\nFinal portfolio:", market.portfolio())

asyncio.run(main())