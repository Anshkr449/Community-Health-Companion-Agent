from typing import Dict, Any
from project.agents.planner import planner
from project.agents.worker import worker
from project.agents.evaluator import evaluator
from project.memory.session_memory import SessionMemory
from project.core.context_engineering import build_context
from project.core.observability import ObservabilityLogger


class MainAgent:
    def __init__(self):
        self.memory = SessionMemory()
        self.logger = ObservabilityLogger()

    def handle_message(self, user_input: str) -> Dict[str, Any]:
        self.logger.log("user_message_received", {"user_input": user_input})
        self.memory.add_message("user", user_input)

        memory_context = self.memory.get_context()
        context = build_context(user_input, memory_context)
        self.logger.log("context_built", {"context_keys": list(context.keys())})

        planner_message = planner.plan(context)
        self.logger.log("planner_completed", planner_message)

        worker_message = worker.execute(planner_message)
        self.logger.log("worker_completed", {
            "task": worker_message.get("task"),
            "used_tools": worker_message.get("context", {}).get("used_tools", [])
        })

        evaluation = evaluator.evaluate(worker_message)
        self.logger.log("evaluator_completed", {
            "approved": evaluation["approved"],
            "issues": evaluation["issues"]
        })

        final_response = evaluation["response"]
        self.memory.add_message("assistant", final_response)

        return {
            "response": final_response,
            "approved": evaluation["approved"],
            "issues": evaluation["issues"],
            "logs": self.logger.get_logs(),
            "metadata": evaluation.get("metadata", {})
        }


def run_agent(user_input: str):
    agent = MainAgent()
    result = agent.handle_message(user_input)
    return result["response"]
