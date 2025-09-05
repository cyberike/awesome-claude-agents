# agents/executor_agent.py

def handle(task_description: str, state=None):
    print("[Executor Agent] Called with task:", task_description)
    print("[Executor Agent] Executing known action...")

    # Simulated execution logic
    result = "target reached successfully"
    updated_state = [s * 0.95 for s in state] if state else None

    return {
        "status": "execution_complete",
        "result": result,
        "updated_state": updated_state,
    }
