import asyncio
from typing_extensions import TypedDict
from logger.log import get_logger_from_env
from application.dtos.agent_dto import ScrapingPayloadDTO
from agents_core.dynamic_agent_factory import DynamicAgentFactory

log = get_logger_from_env(__file__)


class State(TypedDict):
    topic: str


class ScrapingErrorWorkflow:
    def __init__(self, llm, payload: ScrapingPayloadDTO):
        self.llm = llm
        self.payload = payload
        self.agent_factory = DynamicAgentFactory(llm)

    async def run(self):
        """
        Runs the scraping workflow.
        """
        await asyncio.sleep(0.5)

        return {
            "usage": "scraping",
            "bot_name": self.payload.bot_name,
            "processed_data": self.payload,
        }
