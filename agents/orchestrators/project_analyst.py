
## 🔧 Immediate Fix: Wrap the returned JSON in triple backticks


import json

def run(task):
    subtasks_by_agent = {
        "api_architect": [
            "Design facial recognition API",
            "Implement crypto donation endpoint"
        ],
        "frontend_developer": [
            "Build login screen with facial scan",
            "Create crypto donation UI"
        ],
        "security_engineer": [
            "Encrypt facial data",
            "Implement user verification"
        ]
    }

    # 🛠️ Wrap the JSON string in triple backticks like markdown
    return f"```json\n{json.dumps(subtasks_by_agent, indent=2)}\n```"