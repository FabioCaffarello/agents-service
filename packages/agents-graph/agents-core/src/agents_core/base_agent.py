from agents_core.agent import Agent
from application.value_objects.agent_id import AgentID


class BaseMetadataAgent(Agent):
    """A simple agent implementation that accepts a name."""

    def __init__(self, name: str):
        self.id = AgentID.generate()
        self.name = name


class BaseAgent(BaseMetadataAgent):
    def __init__(self, name: str, llm, config: dict):
        super().__init__(name)
        self.llm = llm
        self.config = config

    def run(self, **kwargs) -> dict:
        # Optionally, you can implement a default behavior.
        return {"status": "BaseAgent run called", "config": self.config}
