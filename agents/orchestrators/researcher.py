import os
import anthropic
import json
from dotenv import load_dotenv

load_dotenv()

def run(task):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    system_prompt = "You are a highly skilled software engineer who completes assigned subtasks in a clear, actionable way."

    if "project_analyst" in __file__:
        system_prompt = "You are a project analyst. Given a technical breakdown, return valid JSON that maps agent names to subtasks. Output only a valid JSON object."

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        temperature=0.3,
        system=system_prompt,
        messages=[{"role": "user", "content": task}]
    )

    text = response.content[0].text.strip()

    try:
        return json.loads(text) if "project_analyst" in __file__ else {
            "agent": "researcher",
            "status": "completed",
            "output": text
        }
    except Exception as e:
        raise ValueError(f"Claude returned non-JSON for {agent_name}:\n{text}\n\nError: {e}")
