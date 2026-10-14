import json
from typing import Any
from claude_agent_sdk import tool, create_sdk_mcp_server
from environment.market import Market


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

