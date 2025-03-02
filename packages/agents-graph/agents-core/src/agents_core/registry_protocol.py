from typing import Protocol, Type
from agents_core.agent import Agent


class AgentRegistryProtocol(Protocol):
    """Defines a protocol for agent registries."""

    def register(self, name: str, agent_cls: Type[Agent]) -> None:
        """Registers an agent class."""
        pass

    def get_agent(self, name: str) -> Type[Agent]:
        """Retrieves an agent class by name."""
        pass
