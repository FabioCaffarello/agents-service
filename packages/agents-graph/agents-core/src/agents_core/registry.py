from typing import Type, Dict
from agents_core.agent import Agent
from agents_core.base_agent import BaseMetadataAgent


class AgentRegistry:
    """Concrete implementation of AgentRegistryProtocol."""

    _registry: Dict[str, Type[Agent]] = {"base": BaseMetadataAgent}

    def register(self, name: str, agent_cls: Type[Agent]) -> None:
        """Register a new agent class."""
        self._registry[name] = agent_cls

    def get_agent(self, name: str) -> Type[Agent]:
        """Retrieve an agent by name."""
        if name not in self._registry:
            raise ValueError(f"Agent '{name}' not found in registry.")
        return self._registry[name]
