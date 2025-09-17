"""
Tests for MCP tool integration.
"""

import pytest
from fastmcp import Client

import registry_mcp


class TestMCPTools:
    """Test MCP tool integration."""

    @pytest.mark.asyncio
    async def test_analyze_project_directory_tool(self):
        """Test analyze_project_directory_tool via MCP."""
        async with Client(registry_mcp.mcp) as client:
            result = await client.call_tool("analyze_project_directory_tool", {"project_path": "."})
            
            assert "project_path" in result.data
            assert "detected_files" in result.data
            assert "suggested_metadata" in result.data
            assert "warnings" in result.data
            assert "recommendations" in result.data

    @pytest.mark.asyncio
    async def test_generate_yaml_template_tool(self):
        """Test generate_yaml_template_tool via MCP."""
        async with Client(registry_mcp.mcp) as client:
            metadata = {
                "identifier": "test/example-mcp",
                "name": "Example MCP",
                "description": "A test MCP server",
                "codeRepository": "https://github.com/test/example-mcp",
                "maintainer": [
                    {
                        "@type": "Person",
                        "name": "Test User"
                    }
                ],
                "license": "https://spdx.org/licenses/MIT.html",
                "keywords": ["test", "example"],
                "programmingLanguage": ["Python"]
            }
            
            result = await client.call_tool("generate_yaml_template_tool", {"metadata": metadata})
            
            assert isinstance(result.data, str)
            assert "@context" in result.data
            assert "@type" in result.data
            assert "identifier" in result.data
            assert "test/example-mcp" in result.data

    @pytest.mark.asyncio
    async def test_validate_yaml_specification_tool(self):
        """Test validate_yaml_specification_tool via MCP."""
        async with Client(registry_mcp.mcp) as client:
            valid_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/test/valid-mcp
identifier: test/valid-mcp
name: Valid MCP
description: A valid MCP server for testing
codeRepository: https://github.com/test/valid-mcp
maintainer:
  - "@type": Person
    name: Test User
license: https://spdx.org/licenses/MIT.html
applicationCategory: HealthApplication
keywords:
  - test
  - valid
programmingLanguage:
  - Python
"""
            
            result = await client.call_tool("validate_yaml_specification_tool", {"yaml_content": valid_yaml})
            
            assert "valid" in result.data
            assert "errors" in result.data
            assert "warnings" in result.data
            assert "suggestions" in result.data

    @pytest.mark.asyncio
    async def test_get_registry_schema_tool(self):
        """Test get_registry_schema_tool via MCP."""
        async with Client(registry_mcp.mcp) as client:
            result = await client.call_tool("get_registry_schema_tool", {})
            
            assert "$schema" in result.data
            assert "properties" in result.data
            assert "required" in result.data
            assert "@context" in result.data["properties"]
            assert "@type" in result.data["properties"]

    @pytest.mark.asyncio
    async def test_get_registry_workflow_guidance_tool(self):
        """Test get_registry_workflow_guidance_tool via MCP."""
        async with Client(registry_mcp.mcp) as client:
            result = await client.call_tool("get_registry_workflow_guidance_tool", {})
            
            assert "workflow_overview" in result.data
            assert "workflow_steps" in result.data
            assert "best_practices" in result.data
            assert "common_issues" in result.data

    @pytest.mark.asyncio
    async def test_get_example_submissions_tool(self):
        """Test get_example_submissions_tool via MCP."""
        async with Client(registry_mcp.mcp) as client:
            result = await client.call_tool("get_example_submissions_tool", {})
            
            assert "mcp_server_example" in result.data
            assert "biomedical_tool_example" in result.data
            assert "data_analysis_tool_example" in result.data

    @pytest.mark.asyncio
    async def test_get_troubleshooting_guide_tool(self):
        """Test get_troubleshooting_guide_tool via MCP."""
        async with Client(registry_mcp.mcp) as client:
            result = await client.call_tool("get_troubleshooting_guide_tool", {})
            
            assert "troubleshooting_overview" in result.data
            assert "validation_errors" in result.data
            assert "submission_errors" in result.data
            assert "common_warnings" in result.data
            assert "best_practices" in result.data

    @pytest.mark.asyncio
    async def test_get_field_guidance_tool(self):
        """Test get_field_guidance_tool via MCP."""
        async with Client(registry_mcp.mcp) as client:
            result = await client.call_tool("get_field_guidance_tool", {"field_name": "name"})
            
            assert "description" in result.data
            assert "requirements" in result.data
            assert "examples" in result.data
            assert "tips" in result.data

    @pytest.mark.asyncio
    async def test_get_field_guidance_tool_invalid_field(self):
        """Test get_field_guidance_tool with invalid field via MCP."""
        async with Client(registry_mcp.mcp) as client:
            result = await client.call_tool("get_field_guidance_tool", {"field_name": "invalid_field"})
            
            assert "error" in result.data
            assert "available_fields" in result.data

    @pytest.mark.asyncio
    async def test_greet_tool_still_works(self):
        """Test that the original greet tool still works."""
        async with Client(registry_mcp.mcp) as client:
            result = await client.call_tool("greet", {"name": "test"})
            assert result.data == "Hello, test!"

    @pytest.mark.asyncio
    async def test_all_tools_registered(self):
        """Test that all expected tools are registered."""
        # Test that we can call each expected tool without errors
        expected_tools = [
            "greet",
            "analyze_project_directory_tool",
            "generate_yaml_template_tool",
            "validate_yaml_specification_tool",
            "submit_to_registry_tool",
            "get_registry_schema_tool",
            "get_registry_workflow_guidance_tool",
            "get_example_submissions_tool",
            "get_troubleshooting_guide_tool",
            "get_field_guidance_tool"
        ]
        
        async with Client(registry_mcp.mcp) as client:
            # Test that we can call each tool (this will fail if tool doesn't exist)
            for tool_name in expected_tools:
                try:
                    if tool_name == "greet":
                        await client.call_tool(tool_name, {"name": "test"})
                    elif tool_name == "get_field_guidance_tool":
                        await client.call_tool(tool_name, {"field_name": "name"})
                    elif tool_name == "generate_yaml_template_tool":
                        await client.call_tool(tool_name, {"metadata": {"name": "test"}})
                    elif tool_name == "validate_yaml_specification_tool":
                        await client.call_tool(tool_name, {"yaml_content": 'name: test'})
                    elif tool_name == "submit_to_registry_tool":
                        await client.call_tool(tool_name, {"yaml_content": 'name: test'})
                    else:
                        await client.call_tool(tool_name, {})
                except Exception as e:
                    pytest.fail(f"Tool {tool_name} failed to execute: {e}")
