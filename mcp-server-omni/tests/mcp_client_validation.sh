#!/bin/bash
# Script to run MCP client validation tests with proper setup

echo "MCP Client Validation Test Runner"
echo "================================="
echo ""
echo "Prerequisites:"
echo "1. Omni server must be running at localhost:8069"
echo "2. MCP module must be installed in Omni"
echo "3. API key must be valid"
echo ""

# Find the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# If script is in tests directory, go up one level, otherwise use current directory
if [[ "$SCRIPT_DIR" == */tests ]]; then
    PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
else
    PROJECT_ROOT="$SCRIPT_DIR"
fi

# Check if Omni is running
echo -n "Checking Omni server... "
if curl -s http://localhost:8069/mcp/health > /dev/null; then
    echo "✓ OK"
else
    echo "✗ FAILED"
    echo "Error: Omni server is not running or MCP module is not installed"
    echo "Please start Omni with: "
    echo "  /Users/ve/dev/src/tmp/omni/omni/.venv/bin/python /Users/ve/dev/src/tmp/omni/omni/omni-bin \\"
    echo "    --config=/Users/ve/dev/src/code/omni_mcp_server/omni.conf \\"
    echo "    -d mcp -u mcp_server --dev=all"
    exit 1
fi

# Set up environment
# Look for .env file in the project root
ENV_FILE="$PROJECT_ROOT/.env"
if [ -f "$ENV_FILE" ]; then
    echo "Loading configuration from: $ENV_FILE"
    export $(grep -v '^#' "$ENV_FILE" | xargs)
else
    echo "ERROR: No .env file found at $ENV_FILE!"
    echo "Please create a .env file based on .env.example"
    echo "Run: cp $PROJECT_ROOT/.env.example $PROJECT_ROOT/.env"
    echo "Then update it with your test configuration"
    exit 1
fi

# Verify required variables are set
if [ -z "$OMNI_URL" ]; then
    echo "ERROR: OMNI_URL not set in .env file"
    exit 1
fi

if [ -z "$OMNI_API_KEY" ]; then
    echo "ERROR: OMNI_API_KEY not set in .env file"
    exit 1
fi

export OMNI_URL
export OMNI_DB
export OMNI_API_KEY
export OMNI_MCP_LOG_LEVEL

# Enable MCP tests by setting environment variable
export RUN_MCP_TESTS=1

echo ""
echo "Configuration:"
echo "  OMNI_URL: $OMNI_URL"
echo "  OMNI_DB: $OMNI_DB"
echo "  OMNI_API_KEY: ${OMNI_API_KEY:0:10}..."
echo "  RUN_MCP_TESTS: $RUN_MCP_TESTS"
echo ""

# Run tests from the project root directory
echo "Running MCP client validation tests..."
echo ""

cd "$PROJECT_ROOT" || exit 1
uv run pytest tests/test_mcp_client_validation.py -v -s -x --tb=short

echo ""
echo "To test with MCP Inspector instead, run:"
echo "  npx @modelcontextprotocol/inspector python -m mcp_server_omni"