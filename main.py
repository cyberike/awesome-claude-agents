import os
import json
import datetime
from agent_loader import call_agent
from save_outputs import save_agent_output

def run_orchestration(task_description):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    build_folder = f"superbuild_{timestamp}"
    build_dir = os.path.join("build", build_folder)
    workspace_dir = os.path.join("workspace", build_folder)
    
    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(workspace_dir, exist_ok=True)

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
            # Auto-create agent file if missing
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

    # Phase 2: Convert .md into .py source code
    print("\n🚧 Phase 2: Generating source code from agent output...")
    for agent_name, markdown_content in final_outputs.items():
        try:
            code_output = call_agent(
                "code-writer-agent",
                f"Convert this agent spec into real Python code. Return code only. Task:\n\n{markdown_content}"
            )
            filename = os.path.join(workspace_dir, f"{agent_name}.py")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code_output)
            print(f"📦 Wrote: {filename}")
        except Exception as e:
            print(f"⚠️ Failed to write code for {agent_name}: {e}")

    # GitHub push
    print("\n🔄 Committing files to GitHub...")
    os.system("git add .")
    os.system(f"git commit -m 'Auto-generated build on {timestamp}'")
    os.system("git push")

    print("\n🎉 Orchestration complete. All files are ready.")

if __name__ == "__main__":
    example_task = (
        "Build a deployable military LLM system with quantized model, offline voice interface, "
        "embedded UI, and edge-device support."
    )
    run_orchestration(example_task)
