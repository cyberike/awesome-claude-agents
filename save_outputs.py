import os
from datetime import datetime

def sanitize_filename(name):
    return name.replace(" ", "_").replace("/", "-").lower()

def save_agent_output(agent_name, task_result, root_folder="build"):
    os.makedirs(root_folder, exist_ok=True)
    
    filename = f"{sanitize_filename(agent_name)}.md"
    filepath = os.path.join(root_folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Agent: {agent_name}\n")
        f.write(f"**Saved on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for entry in task_result:
            f.write(f"## Task\n{entry['task']}\n\n")

            result = entry.get("result", {})
            if isinstance(result, dict):
                f.write(f"**Status:** {result.get('status', 'unknown')}\n\n")
                f.write("### Output\n")
                f.write("```\n")
                f.write(result.get("output", "No output returned."))
                f.write("\n```\n\n")
            else:
                f.write("❌ No structured result\n")
                f.write(f"Error: {entry.get('error', 'Unknown error')}\n\n")

    print(f"💾 Saved: {filepath}")
