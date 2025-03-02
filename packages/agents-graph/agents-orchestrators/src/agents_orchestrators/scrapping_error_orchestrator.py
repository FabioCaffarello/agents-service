import asyncio
from agents_workflows.scraping_error_workflow import ScrapingErrorWorkflow
from agents_orchestrators.base_orchestrator import BaseOrchestrator
from agents_core.model_config import ModelConfig
from logger.log import get_logger_from_env
from application.dtos.agent_dto import ScrapingErrorPayloadDTO


log = get_logger_from_env(__file__)


class ScrapingErrorOrchestrator(BaseOrchestrator):
    def __init__(self, model_config: ModelConfig):
        super().__init__(model_config)

    async def process_payload(self, payload: dict) -> dict:
        """
        A stub orchestrator for scraping usage.
        """
        payload_dto = ScrapingErrorPayloadDTO.from_dict(payload)

        workflow = ScrapingErrorWorkflow(self.llm, payload_dto)
        result = await workflow.run()
        log.info(f"Processed payload: {result}")

        await asyncio.sleep(0.5)  # Simulate processing delay.
        return {
            "status": "scheduled",
            "usage": "scraping",
        }
