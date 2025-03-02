from abc import ABC, abstractmethod


class Agent(ABC):
    """Abstract base class for all agents."""

    @abstractmethod
    def run(self, **kwargs) -> dict:
        """Execute the agent's logic."""
        pass
