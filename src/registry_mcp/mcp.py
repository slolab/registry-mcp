from fastmcp import FastMCP

mcp: FastMCP = FastMCP(
    name="registry-mcp",
    instructions="MCP server for supporting registry submissions",
    on_duplicate_tools="error",
)
