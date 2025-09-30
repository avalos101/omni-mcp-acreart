"""Entry point for the mcp-server-omni package.

This module provides the command-line interface for running the
Omni MCP server via uvx or direct execution.
"""

import argparse
import asyncio
import logging
import os
import sys
from typing import Optional

from dotenv import load_dotenv

from .config import load_config
from .server import SERVER_VERSION, OmniMCPServer


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point for the MCP server.

    This function handles command-line arguments, loads configuration,
    and runs the MCP server with the specified transport.

    Args:
        argv: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    # Load environment variables from .env file
    load_dotenv()

    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Omni MCP Server - Model Context Protocol server for Omni ERP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Environment variables:
  OMNI_URL           Omni server URL (required)
  OMNI_API_KEY       Omni API key (preferred authentication)
  OMNI_USER          Omni username (fallback if no API key)
  OMNI_PASSWORD      Omni password (required with username)
  OMNI_DB            Omni database name (auto-detected if not set)

Optional environment variables:
  OMNI_MCP_LOG_LEVEL    Log level (DEBUG, INFO, WARNING, ERROR)
  OMNI_MCP_DEFAULT_LIMIT Default record limit (default: 10)
  OMNI_MCP_MAX_LIMIT     Maximum record limit (default: 100)
  OMNI_MCP_TRANSPORT     Transport type: stdio or streamable-http (default: stdio)
  OMNI_MCP_HOST          Server host for HTTP transports (default: localhost)
  OMNI_MCP_PORT          Server port for HTTP transports (default: 8000)

For more information, visit: https://github.com/ivnvxd/mcp-server-omni""",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"omni-mcp-server v{SERVER_VERSION}",
    )

    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default=os.getenv("OMNI_MCP_TRANSPORT", "stdio"),
        help="Transport type to use (default: stdio)",
    )

    parser.add_argument(
        "--host",
        default=os.getenv("OMNI_MCP_HOST", "localhost"),
        help="Server host for HTTP transports (default: localhost)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("OMNI_MCP_PORT", "8000")),
        help="Server port for HTTP transports (default: 8000)",
    )

    # Parse arguments
    args = parser.parse_args(argv)

    try:
        # Override environment variables with CLI arguments
        if args.transport:
            os.environ["OMNI_MCP_TRANSPORT"] = args.transport
        if args.host:
            os.environ["OMNI_MCP_HOST"] = args.host
        if args.port:
            os.environ["OMNI_MCP_PORT"] = str(args.port)

        # Load configuration from environment
        config = load_config()

        # Create server instance
        server = OmniMCPServer(config)

        # Run the server with the specified transport
        if config.transport == "stdio":
            asyncio.run(server.run_stdio())
        elif config.transport == "streamable-http":
            asyncio.run(server.run_http(host=config.host, port=config.port))
        else:
            raise ValueError(f"Unsupported transport: {config.transport}")

        return 0

    except KeyboardInterrupt:
        # Handle graceful shutdown on Ctrl+C
        print("\nServer stopped by user", file=sys.stderr)
        return 0

    except ValueError as e:
        # Configuration errors
        print(f"Configuration error: {e}", file=sys.stderr)
        print("\nPlease check your environment variables or .env file", file=sys.stderr)
        return 1

    except Exception as e:
        # Other errors
        logging.error(f"Server error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        return 1


# Entry point for module execution
if __name__ == "__main__":
    sys.exit(main())
