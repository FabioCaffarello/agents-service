from agents_core.registry import AgentRegistry
from application.dtos.agent_dto import AgentDTO, CreateAgentDTO
from application.usecases.create_agent import CreateAgentUseCase
from application.usecases.get_agent import GetAgentUseCase
from application.usecases.protocols import UseCaseProtocol


class AgentService:
    """Service that depends on protocol-based use cases."""

    def __init__(
        self,
        create_agent_use_case: UseCaseProtocol[CreateAgentDTO, AgentDTO],
        get_agent_use_case: UseCaseProtocol[str, AgentDTO],
    ):
        self.create_agent_use_case = create_agent_use_case
        self.get_agent_use_case = get_agent_use_case

    def create_agent(self, dto: CreateAgentDTO) -> AgentDTO:
        """Creates an agent via the use case."""
        return self.create_agent_use_case.execute(dto)

    def get_agent(self, agent_id: str) -> AgentDTO:
        """Retrieves an agent via the use case."""
        return self.get_agent_use_case.execute(agent_id)


def get_agent_service() -> AgentService:
    """Provides an instance of AgentService with injected dependencies."""
    registry = AgentRegistry()
    return AgentService(
        CreateAgentUseCase(registry),  # Inject CreateAgentUseCase
        GetAgentUseCase(registry),  # Inject GetAgentUseCase
    )
