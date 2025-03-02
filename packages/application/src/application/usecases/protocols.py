from typing import Protocol, TypeVar, Generic

InputDTO = TypeVar("InputDTO")  # Input type
OutputDTO = TypeVar("OutputDTO")  # Output type


class UseCaseProtocol(Protocol, Generic[InputDTO, OutputDTO]):
    """Defines a protocol for all use cases."""

    def execute(self, input_dto: InputDTO) -> OutputDTO:
        """Executes the use case with an input DTO and returns an output DTO."""
        pass
