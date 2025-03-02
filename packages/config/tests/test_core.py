import pytest
from config.core import Config


def test_default_log_level(monkeypatch):
    # Ensure the LOG_LEVEL environment variable is not set.
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    config = Config()
    # Default log level should be INFO.
    assert config.log_level == "INFO"


def test_env_log_level(monkeypatch):
    # Set the environment variable to 'debug' (lowercase) and check it becomes uppercase.
    monkeypatch.setenv("LOG_LEVEL", "debug")
    config = Config()
    assert config.log_level == "DEBUG"


def test_invalid_log_level():
    # Passing an invalid log level should raise a ValueError.
    with pytest.raises(ValueError) as excinfo:
        Config(log_level="INVALID")
    assert "Invalid log level: INVALID" in str(excinfo.value)
