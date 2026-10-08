import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage, query, AgentDefinition
from tools import bank_server


async def main():
    options=ClaudeAgentOptions(
        mcp_servers={"bank": bank_server},
        allowed_tools=["mcp__bank__get_account_balance", "Agent", "mcp__bank__create_account", "mcp__bank__transfer_money"],
        model="claude-haiku-4-5-20251001", 
        max_turns=8,
        agents={
            "balance-agent": AgentDefinition(
                description="Looks up the user's current account balance. Use for any balance question.",
                prompt="You look up and report the account balance. Be brief.",
            ),

            "money-transfer-agent": AgentDefinition(
                description="Transfers money between accounts. Use for any transfer question.",
                prompt="You initiate a transfer of money between accounts. Be brief.",
            ),

            "transaction-history-agent": AgentDefinition(
                description="Retrieves the user's transaction history. Use for any transaction history question.",
                prompt="You retrieve and summarize the user's transaction history. Be brief.",
            ),

            "account-creation-agent": AgentDefinition(
                description="Creates a new bank account for the user. Use for any account creation question.",
                prompt="You create a new bank account for the user. Be brief.",
            )
        },
    )
    async for message in query(
        prompt="transfer $500 from tim to greg",
        options=options,
    ):
        
        # Print human-readable output
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)  # Claude's reasoning
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")  # Tool being called
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")  # Final result


asyncio.run(main())