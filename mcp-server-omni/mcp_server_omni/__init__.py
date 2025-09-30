"""MCP Server for Omni - Model Context Protocol server for Omni ERP systems."""

__version__ = "0.1.0"
__author__ = "Andrey Ivanov"
__license__ = "MPL-2.0"

from .access_control import AccessControlError, AccessController, ModelPermissions
from .config import OmniConfig, load_config
from .omni_connection import OmniConnection, OmniConnectionError, create_connection
from .server import OmniMCPServer

__all__ = [
    "OmniMCPServer",
    "OmniConfig",
    "load_config",
    "OmniConnection",
    "OmniConnectionError",
    "create_connection",
    "AccessController",
    "AccessControlError",
    "ModelPermissions",
    "__version__",
]
