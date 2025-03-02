from dataclasses import dataclass, field
import os


@dataclass
class Config:
    """Central configuration for the agents-service.

    Attributes:
        log_level (str): The log level for the application. It is obtained from
            the environment variable 'LOG_LEVEL' (default is 'INFO') and converted to uppercase.
        verbose (bool): If True, enables verbose output. Defaults to False.
        debug (bool): If True, activates debug mode with detailed logging. Defaults to False.
    """

    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO").upper()
    )
    verbose: bool = field(default=False)
    debug: bool = field(default=False)

    def __post_init__(self):
        """Validates the configuration after initialization.

        Raises:
            ValueError: If the log_level is not one of the valid options.
        """
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level not in valid_levels:
            raise ValueError(
                f"Invalid log level: {self.log_level}. Must be one of {valid_levels}"
            )
