import json
from typing import Any
from claude_agent_sdk import tool, create_sdk_mcp_server
from environment.market import Market
import pandas as pd
from agent.analysis_tools import signal_table


def reply(text: str, error: bool = False) -> dict[str, Any]:
    result = {"content": [{"type": "text", "text": text}]}
    if error:
        result["is_error"] = True
    return result

def make_market_server(market: Market):
    tickers = ", ".join(market.prices.columns)

    @tool("get_portfolio", "Returns today's date, cash, share positions, and total portfolio value.", {})
    async def get_portfolio(args: dict[str, Any]) -> dict[str, Any]:
        return reply(json.dumps(market.portfolio()))
    
    @tool("buy", f"Buy whole shares of a stock at today's closing price. Available tickers: {tickers}.", {"ticker": str, "shares": int})
    async def buy(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return reply(market.buy(args['ticker'], args['shares']))
        except ValueError as e:
            return reply(str(e), error=True)
    
    @tool("sell", f"Sells whole shares of a stock you own at today's closing price. Available tickers: {tickers}.", {"ticker": str, "shares": int})
    async def sell(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return reply(market.sell(args['ticker'], args['shares']))
        except ValueError as e:
            return reply(str(e), error=True)
    
    @tool("get_price_history", f"Returns daily closing prices for one stock, ending today. Available tickers: {tickers}.", {"ticker": str, "days": int})
    async def get_price_history(args: dict[str, Any]) -> dict[str, Any]:  
        try:
            history = market.get_history(args['ticker'], args['days'])
        except ValueError as e:
            return reply(str(e), error=True)
        return reply(history.round(2).to_string())

    return create_sdk_mcp_server(
        name="market", 
        version="1.0.0", 
        tools=[get_portfolio, buy, get_price_history, sell]
    )

def make_analysis_server(prices: pd.DataFrame):
    @tool("signal_table",
          "Splits all stock-weeks in this period into 5 equal groups by a signal measured at a decision, "
          "and shows the average return over the following weeks for each group. "
          "Signals: own_1w, own_4w, market_1w, relative_1w. horizon_weeks: 1 to 4.",
          {"signal": str, "horizon_weeks": int})
    async def signal_table_tool(args):
        try:
            table = signal_table(prices, args["signal"], args["horizon_weeks"])
        except ValueError as e:
            return reply(str(e), error=True)
        return reply(table.round(4).to_string())

    return create_sdk_mcp_server(name="analysis", version="1.0.0", tools=[signal_table_tool])




