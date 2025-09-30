"""Tests for basic Omni XML-RPC connection infrastructure.

These tests use a real Omni server at localhost:8069 to test
connection management and error handling.
"""

import os
import socket
from unittest.mock import MagicMock, patch

import pytest

from mcp_server_omni.config import OmniConfig
from mcp_server_omni.omni_connection import OmniConnection, OmniConnectionError, create_connection


@pytest.fixture
def test_config():
    """Create test configuration."""
    return OmniConfig(
        url=os.getenv("OMNI_URL", "http://localhost:8069"),
        api_key="test_api_key",
        database=os.getenv("OMNI_DB"),
        log_level="INFO",
        default_limit=10,
        max_limit=100,
    )


@pytest.fixture
def invalid_config():
    """Create configuration with invalid URL."""
    return OmniConfig(
        url="http://invalid.host.nowhere:9999",
        api_key="test_api_key",
        database=os.getenv("OMNI_DB"),
        log_level="INFO",
        default_limit=10,
        max_limit=100,
    )


class TestOmniConnectionInit:
    """Test OmniConnection initialization."""

    def test_init_valid_config(self, test_config):
        """Test initialization with valid configuration."""
        conn = OmniConnection(test_config)

        assert conn.config == test_config
        assert conn.timeout == OmniConnection.DEFAULT_TIMEOUT
        assert not conn.is_connected

        # Parse expected values from config URL
        from urllib.parse import urlparse

        parsed = urlparse(test_config.url)
        expected_host = parsed.hostname or "localhost"
        expected_port = parsed.port or (443 if parsed.scheme == "https" else 80)

        assert conn._url_components["host"] == expected_host
        assert conn._url_components["port"] == expected_port
        assert conn._url_components["scheme"] == parsed.scheme

    def test_init_custom_timeout(self, test_config):
        """Test initialization with custom timeout."""
        conn = OmniConnection(test_config, timeout=60)
        assert conn.timeout == 60

    def test_parse_url_https(self):
        """Test URL parsing for HTTPS URLs."""
        config = OmniConfig(
            url="https://omni.example.com", api_key="test", database=os.getenv("OMNI_DB")
        )
        conn = OmniConnection(config)

        assert conn._url_components["scheme"] == "https"
        assert conn._url_components["host"] == "omni.example.com"
        assert conn._url_components["port"] == 443

    def test_parse_url_with_path(self):
        """Test URL parsing with path."""
        config = OmniConfig(
            url="http://localhost:8069/custom/path", api_key="test", database=os.getenv("OMNI_DB")
        )
        conn = OmniConnection(config)

        assert conn._url_components["path"] == "/custom/path"
        assert conn._url_components["base_url"] == "http://localhost:8069/custom/path"

    def test_parse_url_invalid_scheme(self):
        """Test URL parsing with invalid scheme."""
        with pytest.raises(ValueError, match="OMNI_URL must start with http:// or https://"):
            config = OmniConfig(
                url="ftp://localhost:8069", api_key="test", database=os.getenv("OMNI_DB")
            )
            OmniConnection(config)

    def test_build_endpoint_url(self, test_config):
        """Test endpoint URL building."""
        conn = OmniConnection(test_config)

        db_url = conn._build_endpoint_url(OmniConnection.MCP_DB_ENDPOINT)
        # Build expected URL from config
        from urllib.parse import urlparse

        parsed = urlparse(test_config.url)
        expected_url = f"{parsed.scheme}://{parsed.netloc}{OmniConnection.MCP_DB_ENDPOINT}"
        assert db_url == expected_url

        common_url = conn._build_endpoint_url(OmniConnection.MCP_COMMON_ENDPOINT)
        expected_common_url = (
            f"{parsed.scheme}://{parsed.netloc}{OmniConnection.MCP_COMMON_ENDPOINT}"
        )
        assert common_url == expected_common_url

        object_url = conn._build_endpoint_url(OmniConnection.MCP_OBJECT_ENDPOINT)
        expected_object_url = (
            f"{parsed.scheme}://{parsed.netloc}{OmniConnection.MCP_OBJECT_ENDPOINT}"
        )
        assert object_url == expected_object_url


class TestOmniConnectionConnect:
    """Test connection establishment."""

    @pytest.mark.omni_required
    def test_connect_success(self, test_config):
        """Test successful connection to real Omni server."""
        conn = OmniConnection(test_config)

        try:
            conn.connect()
            assert conn.is_connected
            assert conn._db_proxy is not None
            assert conn._common_proxy is not None
            assert conn._object_proxy is not None
        finally:
            conn.disconnect()

    @pytest.mark.omni_required
    def test_connect_already_connected(self, test_config, caplog):
        """Test connecting when already connected."""
        conn = OmniConnection(test_config)

        try:
            conn.connect()
            assert conn.is_connected

            # Try to connect again
            conn.connect()
            assert "Already connected to Omni" in caplog.text
        finally:
            conn.disconnect()

    def test_connect_invalid_host(self, invalid_config):
        """Test connection to invalid host."""
        conn = OmniConnection(invalid_config)

        with pytest.raises(OmniConnectionError) as exc_info:
            conn.connect()

        assert "Connection failed" in str(exc_info.value)

    def test_connect_timeout(self, test_config):
        """Test connection timeout handling."""
        # Use very short timeout
        conn = OmniConnection(test_config, timeout=0.001)

        # Mock socket to simulate timeout
        with patch("socket.socket") as mock_socket:
            mock_socket.side_effect = socket.timeout("Timeout")

            with pytest.raises(OmniConnectionError) as exc_info:
                conn.connect()

            assert "Connection failed" in str(exc_info.value)


class TestOmniConnectionDisconnect:
    """Test connection cleanup."""

    @pytest.mark.omni_required
    def test_disconnect_when_connected(self, test_config):
        """Test normal disconnect."""
        conn = OmniConnection(test_config)

        conn.connect()
        assert conn.is_connected

        conn.disconnect()
        assert not conn.is_connected
        assert conn._db_proxy is None
        assert conn._common_proxy is None
        assert conn._object_proxy is None

    def test_disconnect_when_not_connected(self, test_config, caplog):
        """Test disconnect when not connected."""
        conn = OmniConnection(test_config)

        conn.disconnect()
        assert "Not connected to Omni" in caplog.text

    @pytest.mark.omni_required
    def test_disconnect_cleanup_on_del(self, test_config):
        """Test cleanup on object deletion."""
        conn = OmniConnection(test_config)
        conn.connect()

        # Delete should trigger disconnect
        del conn


class TestOmniConnectionHealth:
    """Test health checking."""

    @pytest.mark.omni_required
    def test_check_health_connected(self, test_config):
        """Test health check when connected."""
        conn = OmniConnection(test_config)

        try:
            conn.connect()
            is_healthy, message = conn.check_health()

            assert is_healthy
            assert "Connected to Omni" in message
        finally:
            conn.disconnect()

    def test_check_health_not_connected(self, test_config):
        """Test health check when not connected."""
        conn = OmniConnection(test_config)

        is_healthy, message = conn.check_health()

        assert not is_healthy
        assert message == "Not connected"

    @pytest.mark.omni_required
    def test_check_health_error(self, test_config):
        """Test health check with connection error."""
        conn = OmniConnection(test_config)
        conn.connect()

        # Mock common proxy to simulate error
        conn._common_proxy = MagicMock()
        conn._common_proxy.version.side_effect = Exception("Server error")

        is_healthy, message = conn.check_health()

        assert not is_healthy
        assert "Health check failed" in message

        conn.disconnect()


class TestOmniConnectionProxies:
    """Test proxy access."""

    @pytest.mark.omni_required
    def test_proxy_access_when_connected(self, test_config):
        """Test accessing proxies when connected."""
        conn = OmniConnection(test_config)

        try:
            conn.connect()

            # Should not raise
            db_proxy = conn.db_proxy
            common_proxy = conn.common_proxy
            object_proxy = conn.object_proxy

            assert db_proxy is not None
            assert common_proxy is not None
            assert object_proxy is not None
        finally:
            conn.disconnect()

    def test_proxy_access_when_not_connected(self, test_config):
        """Test accessing proxies when not connected."""
        conn = OmniConnection(test_config)

        with pytest.raises(OmniConnectionError, match="Not connected"):
            _ = conn.db_proxy

        with pytest.raises(OmniConnectionError, match="Not connected"):
            _ = conn.common_proxy

        with pytest.raises(OmniConnectionError, match="Not connected"):
            _ = conn.object_proxy


class TestOmniConnectionContext:
    """Test context manager functionality."""

    @pytest.mark.omni_required
    def test_context_manager_success(self, test_config):
        """Test using connection as context manager."""
        with OmniConnection(test_config) as conn:
            assert conn.is_connected

            # Test that we can use the connection
            is_healthy, _ = conn.check_health()
            assert is_healthy

        # Should be disconnected after context
        assert not conn.is_connected

    @pytest.mark.omni_required
    def test_context_manager_with_error(self, test_config):
        """Test context manager with error in context."""
        conn = OmniConnection(test_config)

        try:
            with conn:
                assert conn.is_connected
                raise ValueError("Test error")
        except ValueError:
            pass

        # Should still be disconnected
        assert not conn.is_connected

    @pytest.mark.omni_required
    def test_create_connection_helper(self, test_config):
        """Test create_connection helper function."""
        with create_connection(test_config) as conn:
            assert conn.is_connected
            assert isinstance(conn, OmniConnection)

        assert not conn.is_connected


class TestOmniConnectionIntegration:
    """Integration tests with real Omni server."""

    @pytest.mark.integration
    def test_real_server_version(self, test_config):
        """Test getting version from real server."""
        with create_connection(test_config) as conn:
            version = conn.common_proxy.version()

            assert isinstance(version, dict)
            assert "server_version" in version
            assert "protocol_version" in version

    @pytest.mark.integration
    def test_real_server_db_list(self, test_config):
        """Test listing databases from real server."""
        with create_connection(test_config) as conn:
            # Note: This might fail if db listing is disabled
            try:
                db_list = conn.db_proxy.list()
                assert isinstance(db_list, list)
            except Exception as e:
                # DB listing might be disabled for security
                assert "Access Denied" in str(e) or "not allowed" in str(e)
