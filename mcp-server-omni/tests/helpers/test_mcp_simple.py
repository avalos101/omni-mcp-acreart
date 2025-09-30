#!/usr/bin/env python
"""Simple MCP server test script.

This script tests the MCP server by starting it and verifying basic functionality.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import the module
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server_omni import OmniConfig, OmniMCPServer


async def test_server():
    """Test the MCP server."""
    print("Testing Omni MCP Server")
    print("======================")
    print()

    # Check environment
    print("Environment Configuration:")
    print(f"  OMNI_URL: {os.getenv('OMNI_URL', 'Not set')}")
    print(f"  OMNI_DB: {os.getenv('OMNI_DB', 'Not set')}")
    print(
        f"  OMNI_API_KEY: {os.getenv('OMNI_API_KEY', 'Not set')[:10]}..."
        if os.getenv("OMNI_API_KEY")
        else "  OMNI_API_KEY: Not set"
    )
    print()

    # Create server
    try:
        config = OmniConfig.from_env()
        print("✓ Configuration loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load configuration: {e}")
        return 1

    # Create server instance
    server = OmniMCPServer(config)
    print(f"✓ Server created: {server.app.name}")

    # Test connection
    try:
        server._ensure_connection()
        print("✓ Connected to Omni successfully")
        print(f"  Database: {server.connection.database}")
        print(f"  User ID: {server.connection.uid}")
    except Exception as e:
        print(f"✗ Failed to connect to Omni: {e}")
        return 1

    # Test resource registration
    try:
        server._register_resources()
        print("✓ Resources registered successfully")

        # Get resource handler info
        if server.resource_handler and server.access_controller:
            models = server.access_controller.get_enabled_models()
            print(f"  Models available: {len(models)}")
            if models:
                # Models is a list of dicts with 'model' key
                model_names = [m["model"] for m in models[:3]]
                print(f"  Example models: {', '.join(model_names)}")
    except Exception as e:
        print(f"✗ Failed to register resources: {e}")
        return 1

    print()
    print("Server is ready to handle MCP requests!")
    print()
    print("To test with MCP Inspector:")
    print("  npx @modelcontextprotocol/inspector python -m mcp_server_omni")

    return 0


if __name__ == "__main__":
    # Set up test environment
    if not os.getenv("OMNI_URL"):
        os.environ["OMNI_URL"] = "http://localhost:8069"
    # OMNI_DB and OMNI_API_KEY should be set in environment

    # Run test
    exit_code = asyncio.run(test_server())
    sys.exit(exit_code)
