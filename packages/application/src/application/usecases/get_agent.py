from application.dtos.agent_dto import AgentDTO
from application.value_objects.agent_id import AgentID
from agents_core.registry_protocol import AgentRegistryProtocol
from application.usecases.protocols import UseCaseProtocol


class GetAgentUseCase(UseCaseProtocol[str, AgentDTO]):
    """Handles retrieving an agent by ID using an abstract registry."""

    def __init__(self, registry: AgentRegistryProtocol):
        self.registry = registry

    def execute(self, agent_id: str) -> AgentDTO:
        """Retrieve an agent by ID."""
        agent = self.registry.get_agent(agent_id)
        return AgentDTO(id=AgentID(agent_id), name=agent.name)
