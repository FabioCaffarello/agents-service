from logger.log import get_logger_from_env
from agents_orchestrators.scrapping_orchestrator import ScrapingOrchestrator
from agents_core.model_config import ModelConfig

log = get_logger_from_env(__file__)


class OrchestratorUseCase:
    def __init__(self):
        # The router decides which orchestrator should handle the payload.
        self.model_config = self._get_model_config()
        self.router = OrchestratorRouter(self.model_config)

    def _get_model_config(self):
        return ModelConfig(provider="openai", model_name="gpt-3.5-turbo")

    async def process_bot_payload(self, bot_name: str, payload: dict) -> dict:
        """
        Processes the payload from a given bot.
        Recognizes the usage context and delegates the payload to the appropriate orchestrator.
        """
        payload["bot_name"] = bot_name  # Attach bot name to payload.
        # log.info(f"Processing payload from bot '{bot_name}': {payload}")

        # Determine the usage context (defaulting to "scraping" for now).
        usage_context = payload.get("usage_context", "scraping")

        # Get the appropriate orchestrator.
        orchestrator = self.router.get_orchestrator(usage_context)
        result = await orchestrator.process_payload(payload)
        log.info(f"Processed payload: {result}")
        return result


class OrchestratorRouter:
    """
    Decides which orchestrator instance should handle a given payload based on its usage context.
    """

    def __init__(self, model_config: ModelConfig):
        # Pre-instantiate orchestrator variants or use lazy instantiation.
        self.orchestrators = {
            "scraping": ScrapingOrchestrator(model_config),
            # Additional contexts can be added here.
        }

    def get_orchestrator(self, usage_context: str):
        # Return the orchestrator that matches the usage context, defaulting to "generic".
        log.debug(f"Routing payload to orchestrator for usage context: {usage_context}")
        orchestrator = self.orchestrators.get(usage_context)
        if orchestrator is None:
            log.warning(f"No orchestrator found for usage context '{usage_context}'.")
            raise ValueError(
                f"No orchestrator found for usage context '{usage_context}'."
            )
        return orchestrator
