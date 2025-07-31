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

    system_prompt = "You are a highly skilled software engineer who completes assigned subtasks in a clear, actionable way."

    if "project_analyst" in __file__:
        system_prompt = "You are a project analyst. Given a technical breakdown, return valid JSON that maps agent names to subtasks. Output only a valid JSON object."

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        temperature=0.3,
        system=system_prompt,
        messages=[{{"role": "user", "content": task}}]
    )

    text = response.content[0].text.strip()

    try:
        return json.loads(text) if "project_analyst" in __file__ else {{
            "agent": "{agent_name}",
            "status": "completed",
            "output": text
        }}
    except Exception as e:
        raise ValueError(f"Claude returned non-JSON for {{agent_name}}:\\n{{text}}\\n\\nError: {{e}}")
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
