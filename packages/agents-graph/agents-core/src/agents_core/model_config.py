from dataclasses import dataclass


@dataclass
class ModelConfig:
    provider: str  # e.g., "openai" or "anthropic"
    model_name: str  # e.g., "gpt-3.5-turbo" or "claude-v1"
    temperature: float = 0
