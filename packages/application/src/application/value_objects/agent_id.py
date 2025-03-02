import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class AgentID:
    """Value Object representing an Agent's unique identifier."""

    value: str

    def __post_init__(self):
        """Ensure the ID is a valid UUID."""
        try:
            uuid.UUID(self.value)  # Validate UUID format
        except ValueError:
            raise ValueError(f"Invalid AgentID: {self.value}")

    @classmethod
    def generate(cls) -> "AgentID":
        """Generate a new AgentID."""
        return cls(value=str(uuid.uuid4()))
