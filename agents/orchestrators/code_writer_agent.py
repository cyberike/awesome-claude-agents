import os
import anthropic
import json
import re
from dotenv import load_dotenv

load_dotenv()

def clean_claude_json(text):
    # Remove code fences and any accidental formatting
    text = text.strip().strip("`")

    if text.lower().startswith("json"):
        text = text[4:]

    # Remove control characters
    text = re.sub(r"[\x00-\x1F\x7F]", "", text)

    # Escape backslashes and control codes that break JSON loading
    text = text.replace("\\n", "\\\\n").replace("\\t", "\\\\t").replace("\\r", "")

    return text.strip()


def run(task):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    system_prompt = (
        "You are an expert AI software engineer. Your job is to write real Python code "
        "based on functional descriptions or markdown specs. Return a JSON object containing "
        "a 'files' array, where each item has a 'filename' and its 'content'.\n\n"
        "Format:\n"
        "{\n"
        "  \"files\": [\n"
        "    {\"filename\": \"main.py\", \"content\": \"print('hello world')\" }\n"
        "  ]\n"
        "}\n\n"
        "Do not return markdown, triple backticks, or any explanations. Return only JSON."
    )

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4096,
        temperature=0.2,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": task
            }
        ]
    )

    raw_text = response.content[0].text.strip()

    try:
        cleaned = clean_claude_json(raw_text)
        return json.loads(cleaned)

    except Exception as e:
        # Save the raw output for inspection
        with open("debug_claude_raw.txt", "w", encoding="utf-8") as f:
            f.write(raw_text)

        raise ValueError(f"Claude returned invalid JSON.\n\nCleaned:\n{cleaned}\n\nError: {e}")
