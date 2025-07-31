import os
import anthropic
import json

def run(task):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        temperature=0.3,
        system="You are a project analyst. Given a technical breakdown, return a valid JSON object mapping agent names to their assigned subtasks. Do not return any explanation — only the JSON.",
        messages=[
            {
                "role": "user",
                "content": f"Here is the tech lead breakdown:\n\n{task}\n\nReturn valid JSON with agents and their subtasks."
            }
        ]
    )

    text = response.content[0].text.strip()

    try:
        return json.loads(text)
    except Exception as e:
        raise ValueError(f"Claude response could not be parsed as JSON:\n{text}\n\nError: {e}")
