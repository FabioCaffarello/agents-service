from agents_core.model_config import ModelConfig
from langchain_openai import ChatOpenAI


class BaseOrchestrator:
    def __init__(self, model_config: ModelConfig):
        self.llm = self._instantiate_llm(model_config)

    def _instantiate_llm(self, model_config: ModelConfig):
        if model_config.provider == "openai":
            return ChatOpenAI(
                model=model_config.model_name, temperature=model_config.temperature
            )
        else:
            raise ValueError(f"Unsupported model provider: {model_config.provider}")
