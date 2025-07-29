import os
import sys
import json
from agent_loader import load_agent_prompt
from agent_loader import call_agent  # Assuming same structure as orchestrator uses

def run_agent(agent_name, task=None):
    # Load the prompt markdown for the agent
    prompt = load_agent_prompt(agent_name)

    if not prompt:
        print(f"❌ No prompt found for agent '{agent_name}'.")
        return

    # If an explicit task is passed, use that (e.g. to override)
    input_text = f"{prompt}\n\nTask:\n{task}" if task else prompt

    print(f"\n📤 Sending task to agent: {agent_name}")
    print("=" * 40)

    # Call Claude (or the backend LLM agent)
    try:
        result = call_agent(agent_name, input_text)
        print(f"\n✅ Response from agent {agent_name}:\n")
        print(result)
        return result
    except Exception as e:
        print(f"❌ Agent execution error for {agent_name}: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_agent.py <agent_name> [optional_task_override]")
        sys.exit(1)

    agent = sys.argv[1]
    override_task = sys.argv[2] if len(sys.argv) > 2 else None
    run_agent(agent, override_task)
