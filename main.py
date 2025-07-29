from dotenv import load_dotenv
import os
import argparse
from orchestrator import run_orchestration

# ✅ Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# 🛠️ Parse command-line arguments
parser = argparse.ArgumentParser(description="Claude Orchestrator")
parser.add_argument("--task", type=str, required=True, help="Main project task to assign")
args = parser.parse_args()

# 🚀 Run the orchestration
if __name__ == "__main__":
    output = run_orchestration(args.task)
    print("\n✅ Final Orchestration Output:\n")
    print(output)
