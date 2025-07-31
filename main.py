import os
import json
import datetime
from agent_loader import call_agent
from save_outputs import save_agent_output
from save_project_files import save_project_files

def git_safe_commit(workspace_dir, timestamp):
    print("\n🔄 Committing files to GitHub...")

    os.system("git add .gitattributes")
    os.system(f"git add {workspace_dir}")

    # Detect if anything is staged
    diff_check = os.system("git diff --cached --quiet")
    if diff_check == 0:
        print("🟡 No new changes to commit.")
        return

    os.system(f'git commit -m "Auto-generated build on {timestamp}"')  # ✅ FIXED: pathspec issue
    os.system("git push")
    print("✅ Git push complete.")

def create_git_attributes():
    if not os.path.exists(".gitattributes"):
        with open(".gitattributes", "w") as f:
            f.write("* text=auto\n")
        print("🧼 Created .gitattributes for clean line endings.")

def run_orchestration(task_description):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    build_folder = f"superbuild_{timestamp}"
    build_dir = os.path.join("build", build_folder)
    workspace_dir = os.path.join("workspace", build_folder)

    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(workspace_dir, exist_ok=True)
    create_git_attributes()

    final_outputs = {}

    tasks = {
        "ml_engineer": "Model Quantization",
        "voice_interface_developer": "Voice Interface (Offline)",
        "ui_ux_developer": "Embedded UI",
        "devops_engineer": "Output"
    }

    for agent_name, agent_task in tasks.items():
        print(f"\n🛠 {agent_name.replace('_', ' ').title()}: Working on task -> {agent_task}")

        try:
            agent_code_path = os.path.join("agents", "orchestrators", f"{agent_name}.py")
            if not os.path.exists(agent_code_path):
                print(f"[!] Auto-created missing agent: {agent_code_path}")
                with open(agent_code_path, "w") as f:
                    f.write(f"def run(task):\n    return f'Agent {agent_name} received task: {{task}}'\n")

            result = call_agent(agent_name, f"Build task: {agent_task}")
            save_agent_output(agent_name, [ {"task": agent_task, "result": result} ], root_folder=build_dir)
            final_outputs[agent_name] = result
            print(f"✅ {agent_name} Done")

        except Exception as e:
            print(f"❌ {agent_name} error: {e}")
            save_agent_output(agent_name, [ {"task": agent_task, "error": str(e)} ], root_folder=build_dir)

    print("\n🚧 Phase 2: Generating source code from agent output...")

    code_generated = False

    for agent_name, markdown_content in final_outputs.items():
        try:
            print(f"🧠 Claude writing code for {agent_name}...")
            code_response = call_agent(
                "code-writer-agent",
                f"""You're an AI engineer. Output the following Python file(s) based on this task description:

{markdown_content}

Return only this format:
{{
  "files": [
    {{ "filename": "your_module.py", "content": "print('Hello')" }}
  ]
}}"""
            )

            if isinstance(code_response, dict) and "files" in code_response:
                save_project_files(code_response["files"], workspace_dir)
                code_generated = True
            else:
                print(f"⚠️ No files returned for {agent_name}. Response: {code_response}")

        except Exception as e:
            print(f"❌ Failed to write code for {agent_name}: {e}")

    if code_generated:
        git_safe_commit(workspace_dir, timestamp)
    else:
        print("🟡 No code files generated — skipping Git commit.")

    print("\n🎉 Orchestration complete. All files are ready.")

if __name__ == "__main__":
    example_task = (
        "Build a deployable military LLM system with quantized model, offline voice interface, "
        "embedded UI, and edge-device support."
    )
    run_orchestration(example_task)
