# test_curiosity_routing_full.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from agents.orchestrators.curiosity_router import route_task
from agents.exploration_agent import handle as exploration_handle
from agents.executor_agent import handle as executor_handle


# Fake input
task = "navigate to checkpoint"
state = [0.1, 0.2, -0.1, 0.0]
action = [0.05, -0.03]
next_state = [0.12, 0.18, -0.09, 0.01]
extrinsic_reward = 0.0  # Try 1.0 to switch routing

# Get route decision
agent = route_task(task, state, action, next_state, extrinsic_reward)

# Call appropriate agent
if agent == "exploration_agent":
    result = exploration_handle(task, state=next_state)
elif agent == "executor_agent":
    result = executor_handle(task, state=next_state)
else:
    raise Exception("Unknown agent returned by router")

print("\n[Result]")
print(result)
