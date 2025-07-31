import os
import re
import json
import datetime
from agent_loader import call_agent


def run_orchestration(task):
    final_output = {}

    # Step 1: Tech Lead generates task breakdown
    tech_lead_output = call_agent(
        "tech-lead-orchestrator",
        f"Break this task into subtasks and assign each to the right specialist:\n\n{task}"
    )

    # Step 2: Project Analyst turns breakdown into JSON
    project_analyst_output = call_agent(
        "project-analyst",
        f"Given this breakdown from the tech lead:\n{tech_lead_output}\n\n"
        "Return a JSON object mapping agent names to their assigned subtasks. "
        "You may return either a string or a list of strings per agent. Example:\n"
        '{ "api-architect": ["Design endpoints"], "frontend-developer": "Build login screen" }'
    )

    print("\n📄 Project Analyst Output:\n")
    print(project_analyst_output)

    # ✅ Require human approval before proceeding
    approval = input("\n✅ Proceed with executing these subtasks? (y/n): ").strip().lower()
    if approval != "y":
        print("❌ Execution cancelled by user.")
        return

    # Step 3: Parse JSON safely (strip markdown block, extract real JSON)
    try:
        cleaned_output = project_analyst_output.strip()
        match = re.search(r"```json(.*?)```", cleaned_output, re.DOTALL)
        if not match:
            raise ValueError("❌ Failed to extract valid JSON block from analyst output.")

        json_block = match.group(1).strip()
        subtask_map = json.loads(json_block)
    except Exception as e:
        print(f"❌ JSON parsing error: {e}")
        print("\n⚠️ Could not execute sub-agents due to JSON error.")
        return

    # Step 4: Dispatch subtasks to sub-agents
    for agent_name, subtask in subtask_map.items():
        subtasks = subtask if isinstance(subtask, list) else [subtask]
        for i, each_task in enumerate(subtasks):
            print(f"\n📣 Calling {agent_name} (subtask {i+1})...")
            result = call_agent(agent_name, each_task)
            if agent_name not in final_output:
                final_output[agent_name] = []
            final_output[agent_name].append({
                "task": each_task,
                "result": result
            })
            print(f"✅ {agent_name} completed subtask {i+1}:\n{result}")

    print("\n✅ All subtasks completed.\n")

    # Step 5: Save results to file
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = f"orchestration_output_{timestamp}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2)
    print(f"\n💾 Results saved to {output_path}")

    # Step 6: Create markdown files for each agent if not already present
    os.makedirs("agents/orchestrators", exist_ok=True)
    for agent_name in final_output:
        file_path = os.path.join("agents", "orchestrators", f"{agent_name}.md")
        if not os.path.exists(file_path):
            # Use the first task as a sample for the .md prompt
            task_description = final_output[agent_name][0]["task"]
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# {agent_name.replace('-', ' ').title()}\n\n")
                f.write("## Task\n")
                f.write(f"{task_description}\n\n")
                f.write("## Guidance\n")
                f.write("You are an expert agent. Carefully read the task above and produce your best output.\n")
                f.write("## Expected Output Format\n")
                f.write("- Clear, concise, and domain-specific results.\n")
                f.write("- No filler text. No introductions. No apologies.\n")
                f.write("- Output directly answers the task.\n")
            print(f"📄 Created new prompt file: {file_path}")
        else:
            print(f"⚠️ Prompt file already exists: {file_path}")

    return final_output
