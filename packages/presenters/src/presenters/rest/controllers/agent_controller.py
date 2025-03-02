from fastapi import APIRouter, Depends, HTTPException
from application.dtos.agent_dto import CreateAgentDTO, AgentDTO
from presenters.rest.dependencies import get_agent_service, AgentService
from security.dependencies import get_current_user

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/", response_model=AgentDTO, status_code=201)
def create_agent(
    dto: CreateAgentDTO,
    service: AgentService = Depends(get_agent_service),
    user: dict = Depends(get_current_user),  # 🔒 Require authentication
):
    """
    Creates a new agent using DTOs.
    Only authenticated users with 'admin' or 'agent' roles can create an agent.
    """
    if user["role"] not in ["admin", "agent"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    try:
        return service.create_agent(dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{agent_id}", response_model=AgentDTO)
def get_agent(
    agent_id: str,
    service: AgentService = Depends(get_agent_service),
    user: dict = Depends(get_current_user),  # 🔒 Require authentication
):
    """
    Retrieves an agent by ID using DTOs.
    Only authenticated users can retrieve agents.
    """
    try:
        return service.get_agent(agent_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Agent not found")
