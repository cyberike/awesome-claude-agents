import os
import anthropic

def run(task):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-3-opus-20240229",  # Use claude-3-sonnet for faster responses
        max_tokens=1024,
        temperature=0.7,
        system="You are a highly skilled software engineer that completes assigned subtasks in a clear, actionable way.",
        messages=[
            {"role": "user", "content": task}
        ]
    )

    return {
        "agent": "frontend_developer",
        "status": "completed",
        "output": response.content[0].text.strip() if response.content else "No output from Claude"
    }
