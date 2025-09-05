# agents/exploration_agent.py

def handle(task_description: str, state=None):
    print("[Exploration Agent] Called with task:", task_description)
    print("[Exploration Agent] Exploring new options...")

    # Simulated exploration logic
    decision = "mapped unknown region"
    updated_state = [s + 0.01 for s in state] if state else None

    return {
        "status": "exploration_complete",
        "result": decision,
        "updated_state": updated_state,
    }
