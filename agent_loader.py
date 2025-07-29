import os
import importlib
from agents.core.retry_utils import retry_on_exception

@retry_on_exception(max_retries=3, initial_delay=1, backoff_factor=2)
def call_agent(agent_name, task):
    """
    Dynamically loads and calls the specified agent with the provided task.
    If missing, auto-generates the agent as a Python stub under known directories.
    """
    try:
        agent_name = agent_name.replace("-", "_")
        subdirs = ['orchestrators', 'specialized', 'universal']
        module_path = None
        agent_file_path = None
        found = False

        for subdir in subdirs:
            check_path = os.path.join("agents", subdir, f"{agent_name}.py")
            if os.path.exists(check_path):
                module_path = f"agents.{subdir}.{agent_name}"
                found = True
                break
            if not agent_file_path:
                # Save default fallback path to create agent here if not found anywhere
                agent_file_path = check_path
                module_path = f"agents.{subdir}.{agent_name}"

        # Agent doesn't exist anywhere, so create the stub
        if not found and agent_file_path:
            os.makedirs(os.path.dirname(agent_file_path), exist_ok=True)
            with open(agent_file_path, "w") as f:
                f.write(f'''def run(task):\n    return {{\n        "agent": "{agent_name}",\n        "status": "auto-generated",\n        "output": f"Stub handling task: {{task}}"\n    }}\n''')
            print(f"[!] Auto-created missing agent: {agent_file_path}")

        # Now load the module
        agent_module = importlib.import_module(module_path)

        if hasattr(agent_module, "run"):
            return agent_module.run(task)
        else:
            raise AttributeError(f"Agent '{agent_name}' does not have a 'run' method.")

    except Exception as e:
        raise RuntimeError(f"Error running agent '{agent_name}': {e}") from e
