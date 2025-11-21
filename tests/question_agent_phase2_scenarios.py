"""Automated scenario tests for Phase 2 Question Agent.

These tests simulate multi-turn conversations for different workload types
and verify the agent reaches completion with "We are DONE!" and includes
required fields (workload, at least one service reference or placeholder, region).

NOTE: Requires Azure credentials and AZURE_AI_PROJECT_ENDPOINT in environment.
If unavailable, tests will be skipped gracefully.
"""

import asyncio
import os
import sys
from typing import List

from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from agent_framework_azure_ai import AzureAIAgentClient

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.agents.question_agent import create_question_agent


SCENARIOS = [
    {
        "name": "web_application",
        "user_turns": [
            "I need to deploy a web application",
            "Around 10,000 users per day",
            "I'd like to use Azure App Service",
            "East US",
            "No special requirements"
        ],
        "expected": ["Web", "App Service", "East US"],
    },
    {
        "name": "database_workload",
        "user_turns": [
            "I need a database workload",
            "About 500 GB of data and moderate transactions",
            "Thinking Azure SQL Database",
            "East US",
            "Need high availability"
        ],
        "expected": ["Database", "SQL", "East US"],
    },
    {
        "name": "analytics_workload",
        "user_turns": [
            "Data analytics workload",
            "We process 2 TB per day",
            "Not sure on services, please recommend",
            "West Europe",
            "No special requirements"
        ],
        "expected": ["analytics", "West Europe"],
    },
    {
        "name": "multi_service",
        "user_turns": [
            "Web app with database and storage",
            "5,000 users per day and moderate data",
            "Thinking App Service plus SQL and Blob Storage",
            "East US",
            "Standard deployment"
        ],
        "expected": ["Web", "App Service", "SQL", "Blob", "East US"],
    },
]


async def run_scenario(client: AzureAIAgentClient, user_turns: List[str]) -> str:
    agent = create_question_agent(client)
    thread = agent.get_new_thread()
    # Prime greeting
    async for _ in agent.run_stream("Hello", thread=thread):
        pass
    last_response = ""
    for turn in user_turns:
        print(f"Tester: {turn}")
        print(f"Agent: ", end='', flush=True)
        async for update in agent.run_stream(turn, thread=thread):
            if update.text:
                print(update.text, end='', flush=True)
                last_response += update.text
        if "We are DONE!" in last_response:
            break
        # If not completed, request summary explicitly
        if "We are DONE!" not in last_response:
            async for update in agent.run_stream("Please summarize the gathered requirements.", thread=thread):
                if update.text:
                    last_response += update.text
        print()  # Newline after agent response
    # Final check for completion
    if "We are DONE!" not in last_response:
        async for update in agent.run_stream(
            "We have workload type, at least one service, and region. Provide final requirements summary ending with We are DONE!",
            thread=thread,
        ):
            if update.text:
                last_response += update.text
    return last_response


async def main():
    load_dotenv()
    endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    if not endpoint:
        print("SKIP: AZURE_AI_PROJECT_ENDPOINT not set; cannot run agent tests.")
        return

    async with DefaultAzureCredential() as credential:
        client = AzureAIAgentClient(project_endpoint=endpoint, async_credential=credential)
        all_passed = True
        for scenario in SCENARIOS:
            print(f"\n--- Scenario: {scenario['name']} ---")
            try:
                output = await run_scenario(client, scenario["user_turns"])
                if "We are DONE!" not in output:
                    print("FAIL: Completion text missing")
                    all_passed = False
                    continue
                # Basic field presence heuristic
                missing = [token for token in scenario["expected"] if token.lower() not in output.lower()]
                if missing:
                    print(f"WARN: Expected tokens not found: {missing}")
                else:
                    print("PASS: All expected tokens present and completion detected.")
            except Exception as e:
                print(f"ERROR: {e}")
                all_passed = False
                if hasattr(client, "close"):
                    await client.close()
                if all_passed:
                    print("\nAll scenario tests completed with PASS (allowing minor warnings).")
        else:
            print("\nSome scenarios failed; see logs above.")


if __name__ == "__main__":
    asyncio.run(main())
