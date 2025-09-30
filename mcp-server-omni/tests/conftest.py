"""Pytest configuration and fixtures for Omni MCP Server tests."""

import os
import socket
import xmlrpc.client

import pytest
from dotenv import load_dotenv

from mcp_server_omni.config import OmniConfig

# Load .env file for tests
load_dotenv()

# Import model discovery helper
try:
    from tests.helpers.model_discovery import ModelDiscovery

    MODEL_DISCOVERY_AVAILABLE = True
except ImportError:
    MODEL_DISCOVERY_AVAILABLE = False


def is_omni_server_available(host: str = "localhost", port: int = 8069) -> bool:
    """Check if Omni server is available at the given host and port."""
    try:
        # Try to connect to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()

        if result != 0:
            return False

        # Try to access the XML-RPC endpoint
        try:
            proxy = xmlrpc.client.ServerProxy(f"http://{host}:{port}/xmlrpc/2/common")
            proxy.version()
            return True
        except Exception:
            return False

    except Exception:
        return False


# Global flag for Omni server availability
OMNI_SERVER_AVAILABLE = is_omni_server_available()


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "omni_required: mark test as requiring a running Omni server"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to skip tests that require Omni when it's not available."""
    if OMNI_SERVER_AVAILABLE:
        # Server is available, don't skip anything
        return

    skip_omni = pytest.mark.skip(reason="Omni server not available at localhost:8069")

    for item in items:
        # Skip tests marked with 'integration' when server is not available
        if "integration" in item.keywords:
            item.add_marker(skip_omni)

        # Skip tests marked with 'omni_required' when server is not available
        if "omni_required" in item.keywords:
            item.add_marker(skip_omni)

        # Also check for specific test names that indicate they need a real server
        test_name = item.name.lower()
        if any(keyword in test_name for keyword in ["real_server", "integration"]):
            item.add_marker(skip_omni)


@pytest.fixture(autouse=True)
def rate_limit_delay(request):
    """Add a delay between tests to avoid rate limiting (only when needed)."""
    # Add delay BEFORE integration tests that hit the real server
    test_name = request.node.name.lower() if hasattr(request.node, "name") else ""
    class_name = request.cls.__name__ if request.cls else ""

    # Check if this is an integration test that needs rate limit protection
    if (
        "integration" in request.keywords
        or "Integration" in class_name
        or "integration" in test_name
        or "real_" in test_name
    ):
        import time

        time.sleep(2.0)  # 2 second delay BEFORE integration tests to avoid rate limiting

    yield


@pytest.fixture
def omni_server_required():
    """Fixture that skips test if Omni server is not available."""
    if not OMNI_SERVER_AVAILABLE:
        pytest.skip("Omni server not available at localhost:8069")


@pytest.fixture
def handle_rate_limit():
    """Fixture that handles rate limiting errors gracefully."""
    import urllib.error

    try:
        yield
    except Exception as e:
        # Check if this is a rate limit error
        if isinstance(e, urllib.error.HTTPError) and e.code == 429:
            pytest.skip("Skipping due to rate limiting")
        elif "429" in str(e) or "TOO MANY REQUESTS" in str(e):
            pytest.skip("Skipping due to rate limiting")
        else:
            raise


@pytest.fixture
def test_config_with_server_check(omni_server_required) -> OmniConfig:
    """Create test configuration, but skip if server not available."""
    # Require environment variables to be set
    if not os.getenv("OMNI_URL"):
        pytest.skip("OMNI_URL environment variable not set. Please configure .env file.")

    if not os.getenv("OMNI_API_KEY"):
        pytest.skip("OMNI_API_KEY environment variable not set. Please configure .env file.")

    return OmniConfig(
        url=os.getenv("OMNI_URL"),
        api_key=os.getenv("OMNI_API_KEY"),
        database=os.getenv("OMNI_DB"),  # DB can be auto-detected
        log_level=os.getenv("OMNI_MCP_LOG_LEVEL", "INFO"),
        default_limit=int(os.getenv("OMNI_MCP_DEFAULT_LIMIT", "10")),
        max_limit=int(os.getenv("OMNI_MCP_MAX_LIMIT", "100")),
    )


# MCP Model Discovery Fixtures
# These fixtures help make tests model-agnostic by discovering
# and adapting to whatever models are currently available


@pytest.fixture
def model_discovery():
    """Create a model discovery helper.

    Creates a fresh discovery instance for each test.
    """
    if not MODEL_DISCOVERY_AVAILABLE:
        pytest.skip("Model Discovery not available")

    if not OMNI_SERVER_AVAILABLE:
        pytest.skip("Omni server not available")

    # Create config for discovery
    config = OmniConfig(
        url=os.getenv("OMNI_URL"),
        api_key=os.getenv("OMNI_API_KEY"),
        database=os.getenv("OMNI_DB"),
    )

    discovery = ModelDiscovery(config)
    return discovery


@pytest.fixture
def readable_model(model_discovery):
    """Get a model with read permission.

    Skips test if no readable models are available.
    """
    return model_discovery.require_readable_model()


@pytest.fixture
def writable_model(model_discovery):
    """Get a model with write permission.

    Skips test if no writable models are available.
    """
    return model_discovery.require_writable_model()


@pytest.fixture
def disabled_model(model_discovery):
    """Get a model name that is NOT enabled.

    Returns a model that should fail access checks.
    """
    return model_discovery.get_disabled_model()


@pytest.fixture
def test_models(model_discovery):
    """Get commonly available models for testing.

    Returns a list of models that are commonly enabled,
    or skips if none are available.
    """
    models = model_discovery.get_common_models()
    if not models:
        models = [model_discovery.require_readable_model()]
    return models
