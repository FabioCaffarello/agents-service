from pydantic import BaseModel
from dataclasses import dataclass
from typing import Dict, Any
from application.value_objects.agent_id import AgentID


@dataclass(frozen=True)
class AgentDTO:
    """Data Transfer Object representing an agent."""

    id: AgentID
    name: str


class CreateAgentDTO(BaseModel):
    """DTO for creating an agent."""

    name: str


@dataclass
class RequestDTO:
    url: str
    headers: Dict[str, Any]
    method: str


@dataclass
class ResponseDTO:
    url: str
    status: int
    body: str
    headers: Dict[str, Any]


@dataclass
class ScrapingPayloadDTO:
    usage_context: str
    request: RequestDTO
    response: ResponseDTO
    bot_name: str

    @classmethod
    def from_dict(cls, payload: dict) -> "ScrapingPayloadDTO":
        request_data = payload.get("request", {})
        response_data = payload.get("response", {})
        return cls(
            usage_context=payload.get("usage_context", "scraping"),
            request=RequestDTO(**request_data),
            response=ResponseDTO(**response_data),
            bot_name=payload.get("bot_name", ""),
        )
