# Installation Guide

This guide provides comprehensive instructions for installing and using the Registry MCP server locally to annotate and submit components to the BioContextAI registry.

## Prerequisites

- Python 3.11 or newer
- Git (for cloning the repository)
- Basic familiarity with command line tools

## Installation Methods

### Method 1: Install from PyPI (Recommended)

```bash
# Install using pip
pip install registry-mcp

# Or using uv (faster)
uv add registry-mcp
```

### Method 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/slolab/registry-mcp.git
cd registry-mcp

# Install in development mode
pip install -e .

# Or using uv
uv sync
```

### Method 3: Run Directly (Development)

```bash
# Run from source without installation
uv run registry_mcp

# Or with specific options
uv run registry_mcp --help
uv run registry_mcp --version
```

## Verification

After installation, verify the MCP server is working:

```bash
# Test the installation
uv run registry_mcp --version

# Run the MCP server
uv run registry_mcp

# Or if installed via pip
registry_mcp --version
registry_mcp
```

## MCP Client Configuration

To use the Registry MCP with an MCP client, you need to configure the client to connect to your locally running MCP server. Here are the configurations for different clients:

### For Cursor

Cursor uses a configuration file at `~/.cursor/mcp.json` (macOS/Linux) or `%APPDATA%\.cursor\mcp.json` (Windows).

**Important**: You must use the full path to the Python executable from your `uv` virtual environment.

```json
{
  "mcpServers": {
    "registry-mcp": {
      "command": "/path/to/your/registry-mcp/.venv/bin/python",
      "args": ["-u", "-m", "registry_mcp.main"],
      "workingDirectory": "/path/to/your/registry-mcp",
      "env": { "PYTHONUNBUFFERED": "1" }
    }
  }
}
```

**Example for macOS:**
```json
{
  "mcpServers": {
    "registry-mcp": {
      "command": "/Users/username/GitHub/registry-mcp/.venv/bin/python",
      "args": ["-u", "-m", "registry_mcp.main"],
      "workingDirectory": "/Users/username/GitHub/registry-mcp",
      "env": { "PYTHONUNBUFFERED": "1" }
    }
  }
}
```

**Finding the correct Python path:**
```bash
# In your registry-mcp directory
uv run which python
# This will show the path to use in the configuration
```

### For Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "registry-mcp": {
      "command": "/path/to/your/registry-mcp/.venv/bin/python",
      "args": ["-u", "-m", "registry_mcp.main"],
      "cwd": "/path/to/your/registry-mcp",
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### For Other MCP Clients

Most MCP clients support stdio transport. Use this configuration:

```json
{
  "mcpServers": {
    "registry-mcp": {
      "command": "/path/to/your/registry-mcp/.venv/bin/python",
      "args": ["-u", "-m", "registry_mcp.main"],
      "cwd": "/path/to/your/registry-mcp",
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### For Published Package (Future)

Once the package is published to PyPI, you can use:

```json
{
  "mcpServers": {
    "registry-mcp": {
      "command": "uvx",
      "args": ["registry-mcp"],
      "env": {
        "UV_PYTHON": "3.11"
      }
    }
  }
}
```

## Troubleshooting MCP Connection

### Common Issues

1. **"No module named registry_mcp"**
   - **Cause**: Using system Python instead of the `uv` virtual environment Python
   - **Solution**: Use the full path to the Python executable from your `.venv/bin/python`

2. **"Command not found"**
   - **Cause**: Using relative paths instead of absolute paths
   - **Solution**: Use full absolute paths in the configuration

3. **"Permission denied"**
   - **Cause**: Python executable doesn't have execute permissions
   - **Solution**: Ensure the virtual environment is properly set up with `uv sync`

### Finding the Correct Paths

```bash
# Find the Python executable path
cd /path/to/registry-mcp
uv run which python

# Test the command manually
/path/to/registry-mcp/.venv/bin/python -u -m registry_mcp.main --help
```

### Testing the Configuration

After updating your MCP client configuration:

1. **Restart the MCP client** completely
2. **Test the connection** by asking the client to:
   - "Analyze my current project directory"
   - "Get registry workflow guidance"
   - "Show me example submissions"

If the connection works, you should see the Registry MCP tools available in your client.

## Next Steps

After installation, proceed to the [Usage Guide](usage.md) to learn how to use the Registry MCP to annotate and submit your components.
