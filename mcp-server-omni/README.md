# MCP Server for Omni

[![CI](https://github.com/ivnvxd/mcp-server-omni/actions/workflows/ci.yml/badge.svg)](https://github.com/ivnvxd/mcp-server-omni/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ivnvxd/mcp-server-omni/branch/main/graph/badge.svg)](https://codecov.io/gh/ivnvxd/mcp-server-omni)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL_2.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)

An MCP server that enables AI assistants like Claude to interact with Omni ERP systems. Access business data, search records, create new entries, update existing data, and manage your Omni instance through natural language.

## Features

- 🔍 **Search and retrieve** any Omni record (customers, products, invoices, etc.)
- ✨ **Create new records** with field validation and permission checks
- ✏️ **Update existing data** with smart field handling
- 🗑️ **Delete records** respecting model-level permissions
- 📊 **Browse multiple records** and get formatted summaries
- 🔢 **Count records** matching specific criteria
- 📋 **Inspect model fields** to understand data structure
- 🔐 **Secure access** with API key or username/password authentication
- 🎯 **Smart pagination** for large datasets
- 💬 **LLM-optimized output** with hierarchical text formatting

## Installation

### Prerequisites

- Python 3.10 or higher
- Access to an Omni instance (version 17.0+)
- The [Omni MCP module](https://apps.omni.com/apps/modules/18.0/mcp_server) installed on your Omni server
- (optional) An API key generated in Omni (Settings > Users > API Keys)

### Install UV First

The MCP server runs on your **local computer** (where Claude Desktop is installed), not on your Omni server. You need to install UV on your local machine:

<details>
<summary>macOS/Linux</summary>

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
</details>

<details>
<summary>Windows</summary>

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
</details>

After installation, restart your terminal to ensure UV is in your PATH.

### Installing via MCP Settings (Recommended)

Add this configuration to your MCP settings:

```json
{
  "mcpServers": {
    "omni": {
      "command": "uvx",
      "args": ["mcp-server-omni"],
      "env": {
        "OMNI_URL": "https://your-omni-instance.com",
        "OMNI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

<details>
<summary>Claude Desktop</summary>

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "omni": {
      "command": "uvx",
      "args": ["mcp-server-omni"],
      "env": {
        "OMNI_URL": "https://your-omni-instance.com",
        "OMNI_API_KEY": "your-api-key-here",
        "OMNI_DB": "your-database-name"
      }
    }
  }
}
```
</details>

<details>
<summary>Cursor</summary>

Add to `~/.cursor/mcp_settings.json`:

```json
{
  "mcpServers": {
    "omni": {
      "command": "uvx",
      "args": ["mcp-server-omni"],
      "env": {
        "OMNI_URL": "https://your-omni-instance.com",
        "OMNI_API_KEY": "your-api-key-here",
        "OMNI_DB": "your-database-name"
      }
    }
  }
}
```
</details>

<details>
<summary>VS Code (with GitHub Copilot)</summary>

Add to your VS Code settings (`~/.vscode/mcp_settings.json` or workspace settings):

```json
{
  "github.copilot.chat.mcpServers": {
    "omni": {
      "command": "uvx",
      "args": ["mcp-server-omni"],
      "env": {
        "OMNI_URL": "https://your-omni-instance.com",
        "OMNI_API_KEY": "your-api-key-here",
        "OMNI_DB": "your-database-name"
      }
    }
  }
}
```
</details>

<details>
<summary>Zed</summary>

Add to `~/.config/zed/settings.json`:

```json
{
  "context_servers": {
    "omni": {
      "command": "uvx",
      "args": ["mcp-server-omni"],
      "env": {
        "OMNI_URL": "https://your-omni-instance.com",
        "OMNI_API_KEY": "your-api-key-here",
        "OMNI_DB": "your-database-name"
      }
    }
  }
}
```
</details>

### Alternative Installation Methods

<details>
<summary>Using pip</summary>

```bash
# Install globally
pip install mcp-server-omni

# Or use pipx for isolated environment
pipx install mcp-server-omni
```

Then use `mcp-server-omni` as the command in your MCP configuration.
</details>

<details>
<summary>From source</summary>

```bash
git clone https://github.com/ivnvxd/mcp-server-omni.git
cd mcp-server-omni
pip install -e .
```

Then use the full path to the package in your MCP configuration.
</details>

## Configuration

### Environment Variables

The server requires the following environment variables:

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `OMNI_URL` | Yes | Your Omni instance URL | `https://mycompany.omni.com` |
| `OMNI_API_KEY` | Yes* | API key for authentication | `0ef5b399e9ee9c11b053dfb6eeba8de473c29fcd` |
| `OMNI_USER` | Yes* | Username (if not using API key) | `admin` |
| `OMNI_PASSWORD` | Yes* | Password (if not using API key) | `admin` |
| `OMNI_DB` | No | Database name (auto-detected if not set) | `mycompany` |

*Either `OMNI_API_KEY` or both `OMNI_USER` and `OMNI_PASSWORD` are required.

**Notes:**
- If database listing is restricted on your server, you must specify `OMNI_DB`
- API key authentication is recommended for better security

### Transport Options

The server supports multiple transport protocols for different use cases:

#### 1. **stdio** (Default)
Standard input/output transport - used by desktop AI applications like Claude Desktop.

```bash
# Default transport - no additional configuration needed
uvx mcp-server-omni
```

#### 2. **streamable-http**
Standard HTTP transport for REST API-style access and remote connectivity.

```bash
# Run with HTTP transport
uvx mcp-server-omni --transport streamable-http --host 0.0.0.0 --port 8000

# Or use environment variables
export OMNI_MCP_TRANSPORT=streamable-http
export OMNI_MCP_HOST=0.0.0.0
export OMNI_MCP_PORT=8000
uvx mcp-server-omni
```

The HTTP endpoint will be available at: `http://localhost:8000/mcp/`

> **Note**: SSE (Server-Sent Events) transport has been deprecated in MCP protocol version 2025-03-26. Use streamable-http transport instead for HTTP-based communication. Requires MCP library v1.9.4 or higher for proper session management.

#### Transport Configuration

| Variable/Flag | Description | Default |
|--------------|-------------|---------|
| `OMNI_MCP_TRANSPORT` / `--transport` | Transport type: stdio, streamable-http | `stdio` |
| `OMNI_MCP_HOST` / `--host` | Host to bind for HTTP transports | `localhost` |
| `OMNI_MCP_PORT` / `--port` | Port to bind for HTTP transports | `8000` |

<details>
<summary>Running streamable-http transport for remote access</summary>

```json
{
  "mcpServers": {
    "omni-remote": {
      "command": "uvx",
      "args": ["mcp-server-omni", "--transport", "streamable-http", "--port", "8080"],
      "env": {
        "OMNI_URL": "https://your-omni-instance.com",
        "OMNI_API_KEY": "your-api-key-here",
        "OMNI_DB": "your-database-name"
      }
    }
  }
}
```
</details>

### Setting up Omni

1. **Install the MCP module**:
   - Download the [mcp_server](https://apps.omni.com/apps/modules/18.0/mcp_server) module
   - Install it in your Omni instance
   - Navigate to Settings > MCP Server

2. **Enable models for MCP access**:
   - Go to Settings > MCP Server > Enabled Models
   - Add models you want to access (e.g., res.partner, product.product)
   - Configure permissions (read, write, create, delete) per model

3. **Generate an API key**:
   - Go to Settings > Users & Companies > Users
   - Select your user
   - Under the "API Keys" tab, create a new key
   - Copy the key for your MCP configuration

## Usage Examples

Once configured, you can ask Claude:

**Search & Retrieve:**
- "Show me all customers from Spain"
- "Find products with stock below 10 units"
- "List today's sales orders over $1000"
- "Search for unpaid invoices from last month"
- "Count how many active employees we have"
- "Show me the contact information for Microsoft"

**Create & Manage:**
- "Create a new customer contact for Acme Corporation"
- "Add a new product called 'Premium Widget' with price $99.99"
- "Create a calendar event for tomorrow at 2 PM"
- "Update the phone number for customer John Doe to +1-555-0123"
- "Change the status of order SO/2024/001 to confirmed"
- "Delete the test contact we created earlier"

## Available Tools

### `search_records`
Search for records in any Omni model with filters.

```json
{
  "model": "res.partner",
  "domain": [["is_company", "=", true], ["country_id.code", "=", "ES"]],
  "fields": ["name", "email", "phone"],
  "limit": 10
}
```

**Field Selection Options:**
- Omit `fields` or set to `null`: Returns smart selection of common fields
- Specify field list: Returns only those specific fields
- Use `["__all__"]`: Returns all fields (use with caution)

### `get_record`
Retrieve a specific record by ID.

```json
{
  "model": "res.partner",
  "record_id": 42,
  "fields": ["name", "email", "street", "city"]
}
```

**Field Selection Options:**
- Omit `fields` or set to `null`: Returns smart selection of common fields with metadata
- Specify field list: Returns only those specific fields
- Use `["__all__"]`: Returns all fields without metadata

### `list_models`
List all models enabled for MCP access.

```json
{}
```

### `create_record`
Create a new record in Omni.

```json
{
  "model": "res.partner",
  "values": {
    "name": "New Customer",
    "email": "customer@example.com",
    "is_company": true
  }
}
```

### `update_record`
Update an existing record.

```json
{
  "model": "res.partner",
  "record_id": 42,
  "values": {
    "phone": "+1234567890",
    "website": "https://example.com"
  }
}
```

### `delete_record`
Delete a record from Omni.

```json
{
  "model": "res.partner",
  "record_id": 42
}
```

## Resources

The server also provides direct access to Omni data through resource URIs:

- `omni://res.partner/record/1` - Get partner with ID 1
- `omni://product.product/search?domain=[["qty_available",">",0]]` - Search products in stock
- `omni://sale.order/browse?ids=1,2,3` - Browse multiple sales orders
- `omni://res.partner/count?domain=[["customer_rank",">",0]]` - Count customers
- `omni://product.product/fields` - List available fields for products

## Security

- Always use HTTPS in production environments
- Keep your API keys secure and rotate them regularly
- Configure model access carefully - only enable necessary models
- The MCP module respects Omni's built-in access rights and record rules
- Each API key is linked to a specific user with their permissions

## Troubleshooting

<details>
<summary>Connection Issues</summary>

If you're getting connection errors:
1. Verify your Omni URL is correct and accessible
2. Check that the MCP module is installed: visit `https://your-omni.com/mcp/health`
3. Ensure your firewall allows connections to Omni
</details>

<details>
<summary>Authentication Errors</summary>

If authentication fails:
1. Verify your API key is active in Omni
2. Check that the user has appropriate permissions
3. Try regenerating the API key
4. For username/password auth, ensure 2FA is not enabled
</details>

<details>
<summary>Model Access Errors</summary>

If you can't access certain models:
1. Go to Settings > MCP Server > Enabled Models in Omni
2. Ensure the model is in the list and has appropriate permissions
3. Check that your user has access to that model in Omni's security settings
</details>

<details>
<summary>"spawn uvx ENOENT" Error</summary>

This error means UV is not installed or not in your PATH:

**Solution 1: Install UV** (see Installation section above)

**Solution 2: macOS PATH Issue**
Claude Desktop on macOS doesn't inherit your shell's PATH. Try:
1. Quit Claude Desktop completely (Cmd+Q)
2. Open Terminal
3. Launch Claude from Terminal:
   ```bash
   open -a "Claude"
   ```

**Solution 3: Use Full Path**
Find UV location and use full path:
```bash
which uvx
# Example output: /Users/yourname/.local/bin/uvx
```

Then update your config:
```json
{
  "command": "/Users/yourname/.local/bin/uvx",
  "args": ["mcp-server-omni"]
}
```
</details>

<details>
<summary>Database Configuration Issues</summary>

If you see "Access Denied" when listing databases:
- This is normal - some Omni instances restrict database listing for security
- Make sure to specify `OMNI_DB` in your configuration
- The server will use your specified database without validation

Example configuration:
```json
{
  "env": {
    "OMNI_URL": "https://your-omni.com",
    "OMNI_API_KEY": "your-key",
    "OMNI_DB": "your-database-name"
  }
}
```
Note: `OMNI_DB` is required if database listing is restricted on your server.
</details>

<details>
<summary>"SSL: CERTIFICATE_VERIFY_FAILED" Error</summary>

This error occurs when Python cannot verify SSL certificates, often on macOS or corporate networks.

**Solution**: Add SSL certificate path to your environment configuration:

```json
{
  "env": {
    "OMNI_URL": "https://your-omni.com",
    "OMNI_API_KEY": "your-key",
    "SSL_CERT_FILE": "/etc/ssl/cert.pem"
  }
}
```

This tells Python where to find the system's SSL certificate bundle for HTTPS connections. The path `/etc/ssl/cert.pem` is the standard location on most systems.
</details>

<details>
<summary>Debug Mode</summary>

Enable debug logging for more information:

```json
{
  "env": {
    "OMNI_URL": "https://your-omni.com",
    "OMNI_API_KEY": "your-key",
    "OMNI_MCP_LOG_LEVEL": "DEBUG"
  }
}
```
</details>

## Development

<details>
<summary>Running from source</summary>

```bash
# Clone the repository
git clone https://github.com/ivnvxd/mcp-server-omni.git
cd mcp-server-omni

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest --cov

# Run the server
python -m mcp_server_omni
```
</details>

<details>
<summary>Testing with MCP Inspector</summary>

```bash
# Using uvx
npx @modelcontextprotocol/inspector uvx mcp-server-omni

# Using local installation
npx @modelcontextprotocol/inspector python -m mcp_server_omni
```
</details>

## Testing

### Transport Tests

You can test both stdio and streamable-http transports to ensure they're working correctly:

```bash
# Run comprehensive transport tests
python tests/run_transport_tests.py
```

This will test:
- **stdio transport**: Basic initialization and communication
- **streamable-http transport**: HTTP endpoint, session management, and tool calls

### Unit Tests

For complete testing including unit and integration tests:

```bash
# Run all tests
uv run pytest --cov

# Run specific test categories
uv run pytest tests/test_tools.py -v
uv run pytest tests/test_server_foundation.py -v
```

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0) - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are very welcome! Please see the [CONTRIBUTING](CONTRIBUTING.md) guide for details.

## Support

Thank you for using this project! If you find it helpful and would like to support my work, kindly consider buying me a coffee. Your support is greatly appreciated!

<a href="https://www.buymeacoffee.com/ivnvxd" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

And do not forget to give the project a star if you like it! :star: