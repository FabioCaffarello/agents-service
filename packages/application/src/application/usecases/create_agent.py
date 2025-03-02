from application.dtos.agent_dto import CreateAgentDTO, AgentDTO
from application.value_objects.agent_id import AgentID
from agents_core.registry_protocol import AgentRegistryProtocol
from application.usecases.protocols import UseCaseProtocol


class CreateAgentUseCase(UseCaseProtocol[CreateAgentDTO, AgentDTO]):
    """Handles agent creation logic using dependency inversion."""

    def __init__(self, registry: AgentRegistryProtocol):
        self.registry = registry

    def execute(self, dto: CreateAgentDTO) -> AgentDTO:
        """Creates and registers an agent, returning a DTO."""
        agent_class = self.registry.get_agent("base")  # Defaulting to BaseAgent
        agent = agent_class(dto.name)  # Instantiate agent
        agent_id = AgentID.generate()  # Generate a new AgentID

        return AgentDTO(id=agent_id, name=agent.name)
