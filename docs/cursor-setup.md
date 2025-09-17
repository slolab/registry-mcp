# Cursor MCP Setup Guide

This guide provides step-by-step instructions for setting up the Registry MCP with Cursor.

## Quick Setup

### Step 1: Install Dependencies

```bash
# Clone and setup the repository
git clone https://github.com/slolab/registry-mcp.git
cd registry-mcp

# Install dependencies with uv
uv sync

# Install the package in development mode
uv pip install -e .
```

### Step 2: Find Your Python Path

```bash
# Get the Python executable path
uv run which python
```

This will output something like: `/Users/username/GitHub/registry-mcp/.venv/bin/python`

### Step 3: Configure Cursor

Create or edit your Cursor MCP configuration file:

**macOS/Linux:** `~/.cursor/mcp.json`
**Windows:** `%APPDATA%\.cursor\mcp.json`

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

**Important:** Replace `/Users/username/GitHub/registry-mcp` with your actual path.

### Step 4: Test the Configuration

```bash
# Test the command manually
/path/to/your/registry-mcp/.venv/bin/python -u -m registry_mcp.main --help
```

### Step 5: Restart Cursor

Close and restart Cursor completely for the changes to take effect.

## Automated Setup Script

You can use this script to automate the setup:

```bash
#!/bin/bash
# setup-cursor-mcp.sh

# Get the current directory (should be registry-mcp)
REGISTRY_MCP_DIR="$(pwd)"
PYTHON_PATH="$REGISTRY_MCP_DIR/.venv/bin/python"
CURSOR_CONFIG_DIR="$HOME/.cursor"

# Create Cursor config directory if it doesn't exist
mkdir -p "$CURSOR_CONFIG_DIR"

# Create the configuration
cat > "$CURSOR_CONFIG_DIR/mcp.json" << EOF
{
  "mcpServers": {
    "registry-mcp": {
      "command": "$PYTHON_PATH",
      "args": ["-u", "-m", "registry_mcp.main"],
      "workingDirectory": "$REGISTRY_MCP_DIR",
      "env": { "PYTHONUNBUFFERED": "1" }
    }
  }
}
EOF

echo "✅ MCP configuration created at: $CURSOR_CONFIG_DIR/mcp.json"
echo "📝 Configuration:"
echo "   Command: $PYTHON_PATH"
echo "   Working Directory: $REGISTRY_MCP_DIR"
echo ""
echo "🔄 Please restart Cursor to apply the changes."
echo ""
echo "🧪 Test the configuration:"
echo "   $PYTHON_PATH -u -m registry_mcp.main --help"
```

Save this as `setup-cursor-mcp.sh`, make it executable, and run it:

```bash
chmod +x setup-cursor-mcp.sh
./setup-cursor-mcp.sh
```

## Testing the Connection

After restarting Cursor, test the connection by asking Cursor to:

1. **"Analyze my current project directory"**
2. **"Get registry workflow guidance"**
3. **"Show me example submissions"**
4. **"Help me create a YAML specification for my component"**

If the connection works, Cursor should be able to use the Registry MCP tools to help you with registry submissions.

## Troubleshooting

### Common Issues

1. **"No module named registry_mcp"**
   - Make sure you're using the Python from the `.venv/bin/python` path
   - Verify the package is installed with `uv pip install -e .`

2. **"Command not found"**
   - Use absolute paths in the configuration
   - Check that the Python executable exists at the specified path

3. **"Permission denied"**
   - Ensure the virtual environment is properly set up
   - Run `uv sync` to recreate the environment if needed

4. **Cursor doesn't recognize the MCP**
   - Restart Cursor completely
   - Check the configuration file syntax (valid JSON)
   - Verify the file is in the correct location

### Debugging Steps

1. **Test the command manually:**
   ```bash
   /path/to/registry-mcp/.venv/bin/python -u -m registry_mcp.main --help
   ```

2. **Check the configuration file:**
   ```bash
   cat ~/.cursor/mcp.json
   ```

3. **Verify the Python path:**
   ```bash
   cd /path/to/registry-mcp
   uv run which python
   ```

4. **Check Cursor's logs** for MCP-related errors

## Next Steps

Once the MCP is connected, you can:

1. Follow the [Usage Guide](usage.md) for step-by-step instructions
2. Use the [Quick Reference](quick-reference.md) for tool parameters
3. Start annotating your components for registry submission

The Registry MCP provides 10 specialized tools to help you create, validate, and submit schema.org-compatible specifications to the BioContextAI registry.
