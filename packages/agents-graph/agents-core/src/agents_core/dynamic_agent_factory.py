import importlib
from typing import List
from agents_core.base_agent import BaseAgent  # adjust import path as needed


class DynamicAgentFactory:
    def __init__(self, llm):
        self.llm = llm
        self.agent_registrations = self._get_agent_registrations()

    def _get_agent_registrations(self) -> List[dict]:
        return [
            {
                "alias": "joke_generator",
                "class_path": "agents.joke_agents.JokeGeneratorAgent",
                "config": {"prompt_template": "Write a short joke about {topic}"},
            },
            {
                "alias": "joke_improver",
                "class_path": "agents.joke_agents.JokeImproverAgent",
                "config": {
                    "prompt_template": "Make this joke funnier by adding wordplay: {joke}"
                },
            },
            {
                "alias": "joke_polisher",
                "class_path": "agents.joke_agents.JokePolisherAgent",
                "config": {
                    "prompt_template": "Add a surprising twist to this joke: {improved_joke}"
                },
            },
            {
                "alias": "ip_detector",
                "class_path": "agents.scraping_agents.IPBlockDetectorAgent",
            },
        ]

    def create_agent(self, alias: str) -> BaseAgent:
        """
        Create an agent instance by its alias.
        """
        agent_info = next(
            (item for item in self.agent_registrations if item["alias"] == alias), None
        )
        if not agent_info:
            raise ValueError(f"Agent with alias '{alias}' not found.")

        class_path = agent_info["class_path"]
        module_name, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        agent_class = getattr(module, class_name)

        return agent_class(alias, self.llm, agent_info.get("config", {}))

    def create_agents(self, aliases: list) -> dict:
        """
        Create multiple agents and return a dict mapping alias -> agent instance.
        """
        return {alias: self.create_agent(alias) for alias in aliases}
