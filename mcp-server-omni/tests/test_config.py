"""Tests for the configuration module."""

import os
import tempfile
from pathlib import Path

import pytest

from mcp_server_omni.config import OmniConfig, get_config, load_config, reset_config, set_config


@pytest.fixture(autouse=True)
def reset_config_fixture():
    """Reset configuration before each test."""
    reset_config()
    yield
    reset_config()


class TestOmniConfig:
    """Test the OmniConfig dataclass."""

    def test_valid_config_with_api_key(self):
        """Test creating a valid configuration with API key."""
        config = OmniConfig(
            url=os.getenv("OMNI_URL", "http://localhost:8069"), api_key="test-api-key"
        )
        assert config.url == os.getenv("OMNI_URL", "http://localhost:8069")
        assert config.api_key == "test-api-key"
        assert config.uses_api_key is True
        assert config.uses_credentials is False
        assert config.log_level == "INFO"
        assert config.default_limit == 10
        assert config.max_limit == 100

    def test_valid_config_with_credentials(self):
        """Test creating a valid configuration with username/password."""
        config = OmniConfig(
            url="https://omni.example.com",
            username="testuser",
            password="testpass",
            database="test_db",
        )
        assert config.url == "https://omni.example.com"
        assert config.username == "testuser"
        assert config.password == "testpass"
        assert config.database == "test_db"
        assert config.uses_api_key is False
        assert config.uses_credentials is True

    def test_missing_url_raises_error(self):
        """Test that missing URL raises ValueError."""
        with pytest.raises(ValueError, match="OMNI_URL is required"):
            OmniConfig(url="", api_key="test-key")

    def test_invalid_url_format_raises_error(self):
        """Test that invalid URL format raises ValueError."""
        with pytest.raises(ValueError, match="OMNI_URL must start with http"):
            OmniConfig(url="invalid-url", api_key="test-key")

    def test_missing_authentication_raises_error(self):
        """Test that missing authentication raises ValueError."""
        with pytest.raises(ValueError, match="Authentication required"):
            OmniConfig(url="http://localhost:8069")

    def test_incomplete_credentials_raises_error(self):
        """Test that incomplete username/password raises ValueError."""
        with pytest.raises(ValueError, match="Authentication required"):
            OmniConfig(url="http://localhost:8069", username="user")

    def test_invalid_default_limit(self):
        """Test that invalid default limit raises ValueError."""
        with pytest.raises(ValueError, match="OMNI_MCP_DEFAULT_LIMIT must be positive"):
            OmniConfig(url="http://localhost:8069", api_key="test-key", default_limit=0)

    def test_invalid_max_limit(self):
        """Test that invalid max limit raises ValueError."""
        with pytest.raises(ValueError, match="OMNI_MCP_MAX_LIMIT must be positive"):
            OmniConfig(url="http://localhost:8069", api_key="test-key", max_limit=-1)

    def test_default_exceeds_max_limit(self):
        """Test that default exceeding max limit raises ValueError."""
        with pytest.raises(ValueError, match="cannot exceed OMNI_MCP_MAX_LIMIT"):
            OmniConfig(
                url="http://localhost:8069", api_key="test-key", default_limit=100, max_limit=50
            )

    def test_invalid_log_level(self):
        """Test that invalid log level raises ValueError."""
        with pytest.raises(ValueError, match="Invalid log level"):
            OmniConfig(url="http://localhost:8069", api_key="test-key", log_level="INVALID")

    def test_log_level_case_insensitive(self):
        """Test that log level is case insensitive."""
        config = OmniConfig(url="http://localhost:8069", api_key="test-key", log_level="debug")
        # Config should validate successfully
        assert config.log_level == "debug"


class TestLoadConfig:
    """Test the load_config function."""

    def test_load_config_from_env_vars(self, monkeypatch):
        """Test loading configuration from environment variables."""
        monkeypatch.setenv("OMNI_URL", "http://test.omni.com")
        monkeypatch.setenv("OMNI_API_KEY", "env-api-key")
        monkeypatch.setenv("OMNI_DB", "test_db")
        monkeypatch.setenv("OMNI_MCP_LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("OMNI_MCP_DEFAULT_LIMIT", "20")
        monkeypatch.setenv("OMNI_MCP_MAX_LIMIT", "200")

        config = load_config()

        assert config.url == "http://test.omni.com"
        assert config.api_key == "env-api-key"
        assert config.database == "test_db"
        assert config.log_level == "DEBUG"
        assert config.default_limit == 20
        assert config.max_limit == 200

    def test_load_config_from_env_file(self, monkeypatch):
        """Test loading configuration from .env file."""
        # Clear environment variables
        for key in [
            "OMNI_URL",
            "OMNI_API_KEY",
            "OMNI_USER",
            "OMNI_PASSWORD",
            "OMNI_MCP_DEFAULT_LIMIT",
            "OMNI_MCP_MAX_LIMIT",
        ]:
            monkeypatch.delenv(key, raising=False)

        # Create a temporary .env file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("OMNI_URL=http://file.omni.com\n")
            f.write("OMNI_USER=fileuser\n")
            f.write("OMNI_PASSWORD=filepass\n")
            f.write("OMNI_MCP_DEFAULT_LIMIT=30\n")
            env_file = f.name

        try:
            config = load_config(Path(env_file))

            assert config.url == "http://file.omni.com"
            assert config.username == "fileuser"
            assert config.password == "filepass"
            assert config.default_limit == 30
        finally:
            os.unlink(env_file)

    def test_env_vars_override_env_file(self, monkeypatch):
        """Test that environment variables override .env file."""
        # Set environment variable
        monkeypatch.setenv("OMNI_URL", "http://env.omni.com")
        monkeypatch.setenv("OMNI_API_KEY", "env-key")

        # Create a temporary .env file with different values
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("OMNI_URL=http://file.omni.com\n")
            f.write("OMNI_API_KEY=file-key\n")
            env_file = f.name

        try:
            config = load_config(Path(env_file))

            # Environment variables should take precedence
            assert config.url == "http://env.omni.com"
            assert config.api_key == "env-key"
        finally:
            os.unlink(env_file)

    def test_load_config_with_empty_strings(self, monkeypatch):
        """Test that empty strings are treated as None."""
        monkeypatch.setenv("OMNI_URL", "http://localhost:8069")
        monkeypatch.setenv("OMNI_API_KEY", "  ")  # Whitespace only
        monkeypatch.setenv("OMNI_USER", "user")
        monkeypatch.setenv("OMNI_PASSWORD", "pass")
        monkeypatch.setenv("OMNI_DB", "")  # Empty string

        config = load_config()

        assert config.api_key is None  # Whitespace stripped to empty
        assert config.database is None  # Empty string becomes None
        # Should use credentials since API key is empty
        assert config.uses_credentials is True

    def test_load_config_invalid_integer(self, monkeypatch):
        """Test that invalid integer values raise ValueError."""
        monkeypatch.setenv("OMNI_URL", "http://localhost:8069")
        monkeypatch.setenv("OMNI_API_KEY", "test-key")
        monkeypatch.setenv("OMNI_MCP_DEFAULT_LIMIT", "not-a-number")

        with pytest.raises(ValueError, match="must be a valid integer"):
            load_config()


class TestConfigSingleton:
    """Test the singleton configuration management."""

    def test_get_config_loads_config(self, monkeypatch):
        """Test that get_config loads configuration on first call."""
        reset_config()  # Ensure clean state

        monkeypatch.setenv("OMNI_URL", "http://singleton.omni.com")
        monkeypatch.setenv("OMNI_API_KEY", "singleton-key")

        config = get_config()

        assert config.url == "http://singleton.omni.com"
        assert config.api_key == "singleton-key"

        # Second call should return same instance
        config2 = get_config()
        assert config is config2

    def test_set_config(self):
        """Test setting a custom configuration."""
        reset_config()  # Ensure clean state

        custom_config = OmniConfig(url="http://custom.omni.com", api_key="custom-key")

        set_config(custom_config)

        config = get_config()
        assert config is custom_config
        assert config.url == "http://custom.omni.com"

    def test_reset_config(self, monkeypatch):
        """Test resetting the configuration."""
        # Set initial config
        monkeypatch.setenv("OMNI_URL", "http://first.omni.com")
        monkeypatch.setenv("OMNI_API_KEY", "first-key")

        config1 = get_config()
        assert config1.url == "http://first.omni.com"

        # Reset and change environment
        reset_config()
        monkeypatch.setenv("OMNI_URL", "http://second.omni.com")
        monkeypatch.setenv("OMNI_API_KEY", "second-key")

        config2 = get_config()
        assert config2.url == "http://second.omni.com"
        assert config1 is not config2
