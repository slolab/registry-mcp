import pytest
from fastmcp import Client

import registry_mcp


def test_package_has_version():
    """Testing package version exist."""
    assert registry_mcp.__version__ is not None


@pytest.mark.asyncio
async def test_mcp_server():
    """Testing MCP server."""
    async with Client(registry_mcp.mcp) as client:
        result = await client.call_tool("greet", {"name": "test"})
        assert result.data == "Hello, test!"
