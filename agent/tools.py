from typing import Any
from claude_agent_sdk import tool, create_sdk_mcp_server
import json
from pathlib import Path

DB = Path("accounts.json")


def load() -> dict:
    return json.loads(DB.read_text()) if DB.exists() else {}


def save(data: dict) -> None:
    DB.write_text(json.dumps(data, indent=2))


@tool("create_account", "Creates a new bank account for the user.", {"owner": str})
async def create_account(args: dict[str, Any]) -> dict[str, Any]:
    accounts = load()
    if args['owner'] in accounts:
        return {"content": [{"type": "test", "text": "Account already exists."}], "is_error": True}
    accounts[args['owner']] = {"balance": 0.0}
    save(accounts)
    return {"content": [{"type": "text", "text": f"Account created for {args['owner']}."}]}

@tool("get_account_balance", "Returns the user's current account balance in dollars.", {"owner": str})
async def get_account_balance(args: dict[str, Any]) -> dict[str, Any]:
    accounts = load()
    if args['owner'] not in accounts:
        return {"content": [{"type": "text", "text": "Account not found."}], "is_error": True}
    return {"content": [{"type": "text", "text": f"${accounts[args['owner']]['balance']:.2f}"}]}

@tool("transfer_money", "Transfers money between accounts.", {"from_account": str, "to_account": str, "amount": float})
async def transfer_money(args: dict[str, Any]) -> dict[str, Any]:
    accounts = load()
    from_account = args['from_account']
    to_account = args['to_account']
    if from_account not in accounts:
        return {"content": [{"type": "text", "text": "From account not found."}], "is_error": True}
    if to_account not in accounts:
        return {"content": [{"type": "text", "text": "To account not found."}], "is_error": True}
    if accounts[from_account]['balance'] < args['amount']:
        return {"content": [{"type": "text", "text": "Insufficient funds."}], "is_error": True}
    accounts[from_account]['balance'] -= args['amount']
    accounts[to_account]['balance'] += args['amount']
    save(accounts)
    return {"content": [{"type": "text", "text": f"Transferred ${args['amount']:.2f} from {from_account} to {to_account}."}]}


bank_server = create_sdk_mcp_server(
    name="bank",
    version="1.0.0",
    tools=[get_account_balance, create_account, transfer_money],
)