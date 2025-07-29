def run(task):
    # Temporary logic — replace with real breakdown later
    return {
        "message": "[Tech Lead] I received the task and would normally break it into subtasks.",
        "input": task,
        "subtasks": [
            f"Research how to approach: {task}",
            f"Assign specialist agents for: {task}",
            "Ensure all required tech stack elements are accounted for"
        ]
    }
