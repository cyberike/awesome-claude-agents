import os
import importlib
import json
from agents.core.retry_utils import retry_on_exception
import anthropic
from dotenv import load_dotenv

# 🔄 Load environment variables from .env file
load_dotenv()

@retry_on_exception(max_retries=3, initial_delay=1, backoff_factor=2)
def call_agent(agent_name, task):
    """
    Loads or creates the agent file, sends the task to Claude, and returns structured output.
    """
    try:
        agent_name = agent_name.replace("-", "_")
        subdirs = ['orchestrators', 'specialized', 'universal']
        module_path = None
        agent_file_path = None
        found = False

        # Search known agent directories
        for subdir in subdirs:
            check_path = os.path.join("agents", subdir, f"{agent_name}.py")
            if os.path.exists(check_path):
                module_path = f"agents.{subdir}.{agent_name}"
                found = True
                break
            if not agent_file_path:
                agent_file_path = check_path
                module_path = f"agents.{subdir}.{agent_name}"

        # Auto-create missing agent file with Claude integration
        if not found and agent_file_path:
            os.makedirs(os.path.dirname(agent_file_path), exist_ok=True)
            with open(agent_file_path, "w") as f:
                f.write(f'''import os
import anthropic
import json
from dotenv import load_dotenv

load_dotenv()

def run(task):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Extract role-specific prompt if this is a structured task
    if isinstance(task, dict):
        role = task.get("role", "{agent_name}")
        task_hint = task.get("task_hint", "")
        context = task.get("context", "")
        
        system_prompt = f"""You are a {{role}}. {{task_hint}}
        
Given the context: {{context}}

Return a JSON object with this exact structure:
{{{{
    "markdown": "A detailed markdown report of your analysis and recommendations",
    "files": {{{{
        "relative/path/to/file": "file content here",
        "another/file.py": "more content"
    }}}}
}}}}

The markdown should be a professional report. The files object is optional - only include it if you need to create actual code or config files."""
        
        user_content = f"Task: {{task_hint}}\\nContext: {{context}}"
    else:
        system_prompt = "You are a highly skilled software engineer who completes assigned subtasks in a clear, actionable way. Return your response as a JSON object with 'markdown' field containing your detailed analysis."
        user_content = str(task)

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        temperature=0.3,
        system=system_prompt,
        messages=[{{"role": "user", "content": user_content}}]
    )

    text = response.content[0].text.strip()

    # Try to parse as JSON first
    try:
        result = json.loads(text)
        return result
    except json.JSONDecodeError:
        # Fallback: return as markdown string
        return {{
            "markdown": text,
            "files": None
        }}
''')
            print(f"[!] Auto-created missing agent: {agent_file_path}")

        # Load and call the agent's run() function
        agent_module = importlib.import_module(module_path)

        if hasattr(agent_module, "run"):
            return agent_module.run(task)
        else:
            raise AttributeError(f"Agent '{agent_name}' does not have a 'run' method.")

    except Exception as e:
        raise RuntimeError(f"Error running agent '{agent_name}': {e}") from e
