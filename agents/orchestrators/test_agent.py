import os
import anthropic
import json
from dotenv import load_dotenv

load_dotenv()

def run(task):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Extract role-specific prompt if this is a structured task
    if isinstance(task, dict):
        role = task.get("role", "test_agent")
        task_hint = task.get("task_hint", "")
        context = task.get("context", "")
        
        system_prompt = f"""You are a {role}. {task_hint}
        
Given the context: {context}

Return a JSON object with this exact structure:
{{
    "markdown": "A detailed markdown report of your analysis and recommendations",
    "files": {{
        "relative/path/to/file": "file content here",
        "another/file.py": "more content"
    }}
}}

The markdown should be a professional report. The files object is optional - only include it if you need to create actual code or config files."""
        
        user_content = f"Task: {task_hint}\nContext: {context}"
    else:
        system_prompt = "You are a highly skilled software engineer who completes assigned subtasks in a clear, actionable way. Return your response as a JSON object with 'markdown' field containing your detailed analysis."
        user_content = str(task)

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        temperature=0.3,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}]
    )

    text = response.content[0].text.strip()

    # Try to parse as JSON first
    try:
        result = json.loads(text)
        return result
    except json.JSONDecodeError:
        # Fallback: return as markdown string
        return {
            "markdown": text,
            "files": None
        }
