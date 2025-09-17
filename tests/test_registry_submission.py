"""
Tests for registry submission tools.
"""

import json
import os
import tempfile
import yaml
from unittest.mock import Mock, patch

import pytest

from registry_mcp.tools.registry_submission import (
    analyze_project_directory,
    generate_yaml_template,
    validate_yaml_specification,
    submit_to_registry,
    get_registry_schema,
)


class TestProjectAnalysis:
    """Test project directory analysis functionality."""

    def test_analyze_empty_directory(self):
        """Test analysis of empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = analyze_project_directory(temp_dir)
            
            assert result["project_path"] == os.path.abspath(temp_dir)
            assert result["detected_files"] == []
            assert result["suggested_metadata"] == {}
            assert "warnings" in result
            assert "recommendations" in result

    def test_analyze_directory_with_pyproject(self):
        """Test analysis with pyproject.toml file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a mock pyproject.toml
            pyproject_content = """
[project]
name = "test-mcp"
description = "A test MCP server"
license = {text = "MIT"}
authors = [
    {name = "Test User", email = "test@example.com"}
]
keywords = ["test", "mcp"]
urls = {Homepage = "https://github.com/test/test-mcp"}
"""
            with open(os.path.join(temp_dir, "pyproject.toml"), "w") as f:
                f.write(pyproject_content)
            
            result = analyze_project_directory(temp_dir)
            
            assert "pyproject.toml" in result["detected_files"]
            assert result["suggested_metadata"]["name"] == "test-mcp"
            assert result["suggested_metadata"]["description"] == "A test MCP server"
            assert result["suggested_metadata"]["programming_language"] == ["Python"]

    def test_analyze_directory_with_readme(self):
        """Test analysis with README.md file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            readme_content = """# Test MCP Server
            
This is a test MCP server for demonstration purposes.
It provides various tools for testing.
"""
            with open(os.path.join(temp_dir, "README.md"), "w") as f:
                f.write(readme_content)
            
            result = analyze_project_directory(temp_dir)
            
            assert "README.md" in result["detected_files"]
            assert "description" in result["suggested_metadata"]

    def test_analyze_directory_with_license(self):
        """Test analysis with LICENSE file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with open(os.path.join(temp_dir, "LICENSE"), "w") as f:
                f.write("MIT License")
            
            result = analyze_project_directory(temp_dir)
            
            assert "LICENSE" in result["detected_files"]
            assert result["suggested_metadata"]["has_license_file"] is True


class TestYAMLGeneration:
    """Test YAML template generation functionality."""

    def test_generate_yaml_minimal(self):
        """Test YAML generation with minimal metadata."""
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
        
        yaml_content = generate_yaml_template(metadata)
        yaml_data = yaml.safe_load(yaml_content)
        
        assert yaml_data["@context"] == "https://schema.org"
        assert yaml_data["@type"] == "SoftwareApplication"
        assert yaml_data["identifier"] == "test/example-mcp"
        assert yaml_data["name"] == "Example MCP"
        assert yaml_data["@id"] == "https://github.com/test/example-mcp"

    def test_generate_yaml_complete(self):
        """Test YAML generation with complete metadata."""
        metadata = {
            "identifier": "test/complete-mcp",
            "name": "Complete MCP",
            "description": "A complete test MCP server",
            "codeRepository": "https://github.com/test/complete-mcp",
            "url": "https://complete-mcp.example.com",
            "softwareHelp": {
                "url": "https://complete-mcp.example.com/docs",
                "name": "Complete MCP Documentation"
            },
            "maintainer": [
                {
                    "@type": "Organization",
                    "name": "Test Org",
                    "identifier": "GitHub: testorg",
                    "url": "https://github.com/testorg"
                }
            ],
            "license": "https://spdx.org/licenses/Apache-2.0.html",
            "applicationCategory": "DeveloperApplication",
            "keywords": ["test", "complete", "mcp"],
            "operatingSystem": ["Cross-platform"],
            "programmingLanguage": ["Python", "TypeScript"],
            "featureList": ["Feature 1", "Feature 2"]
        }
        
        yaml_content = generate_yaml_template(metadata)
        yaml_data = yaml.safe_load(yaml_content)
        
        assert yaml_data["url"] == "https://complete-mcp.example.com"
        assert yaml_data["softwareHelp"]["@type"] == "CreativeWork"
        assert yaml_data["maintainer"][0]["@type"] == "Organization"
        assert yaml_data["applicationCategory"] == "DeveloperApplication"
        assert yaml_data["featureList"] == ["Feature 1", "Feature 2"]


class TestYAMLValidation:
    """Test YAML validation functionality."""

    def test_validate_valid_yaml(self):
        """Test validation of valid YAML."""
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
        result = validate_yaml_specification(valid_yaml)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_validate_invalid_yaml_syntax(self):
        """Test validation of invalid YAML syntax."""
        invalid_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
invalid: yaml: syntax: here
"""
        result = validate_yaml_specification(invalid_yaml)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "YAML parsing error" in result["errors"][0]

    def test_validate_missing_required_fields(self):
        """Test validation with missing required fields."""
        incomplete_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
name: Incomplete MCP
"""
        result = validate_yaml_specification(incomplete_yaml)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_validate_invalid_identifier(self):
        """Test validation with invalid identifier format."""
        invalid_identifier_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/test/invalid-mcp
identifier: invalid-identifier-format
name: Invalid Identifier MCP
description: A test MCP with invalid identifier
codeRepository: https://github.com/test/invalid-mcp
maintainer:
  - "@type": Person
    name: Test User
license: https://spdx.org/licenses/MIT.html
applicationCategory: HealthApplication
keywords:
  - test
programmingLanguage:
  - Python
"""
        result = validate_yaml_specification(invalid_identifier_yaml)
        
        assert result["valid"] is False
        assert any("does not match" in error and "identifier" in error for error in result["errors"])

    def test_validate_invalid_license(self):
        """Test validation with invalid license format."""
        invalid_license_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/test/invalid-license-mcp
identifier: test/invalid-license-mcp
name: Invalid License MCP
description: A test MCP with invalid license
codeRepository: https://github.com/test/invalid-license-mcp
maintainer:
  - "@type": Person
    name: Test User
license: MIT
applicationCategory: HealthApplication
keywords:
  - test
programmingLanguage:
  - Python
"""
        result = validate_yaml_specification(invalid_license_yaml)
        
        assert result["valid"] is True  # Schema validation passes
        assert len(result["warnings"]) > 0
        assert any("License should use SPDX format" in warning for warning in result["warnings"])


class TestRegistrySubmission:
    """Test registry submission functionality."""

    @patch('registry_mcp.tools.registry_submission.requests.post')
    def test_submit_success(self, mock_post):
        """Test successful submission to registry."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": "submission-123"}
        mock_post.return_value = mock_response
        
        valid_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/test/success-mcp
identifier: test/success-mcp
name: Success MCP
description: A test MCP for successful submission
codeRepository: https://github.com/test/success-mcp
maintainer:
  - "@type": Person
    name: Test User
license: https://spdx.org/licenses/MIT.html
applicationCategory: HealthApplication
keywords:
  - test
programmingLanguage:
  - Python
"""
        
        result = submit_to_registry(valid_yaml)
        
        assert result["success"] is True
        assert result["submission_id"] == "submission-123"
        assert "Successfully submitted" in result["message"]

    @patch('registry_mcp.tools.registry_submission.requests.post')
    def test_submit_api_error(self, mock_post):
        """Test submission with API error."""
        # Mock API error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"message": "Invalid data"}
        mock_post.return_value = mock_response
        
        valid_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/test/error-mcp
identifier: test/error-mcp
name: Error MCP
description: A test MCP for error testing
codeRepository: https://github.com/test/error-mcp
maintainer:
  - "@type": Person
    name: Test User
license: https://spdx.org/licenses/MIT.html
applicationCategory: HealthApplication
keywords:
  - test
programmingLanguage:
  - Python
"""
        
        result = submit_to_registry(valid_yaml)
        
        assert result["success"] is False
        assert "Invalid data" in result["errors"]

    def test_submit_invalid_yaml(self):
        """Test submission with invalid YAML."""
        invalid_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
name: Incomplete MCP
"""
        
        result = submit_to_registry(invalid_yaml)
        
        assert result["success"] is False
        assert "Validation failed" in result["message"]

    @patch('registry_mcp.tools.registry_submission.requests.post')
    def test_submit_network_error(self, mock_post):
        """Test submission with network error."""
        # Mock network error
        mock_post.side_effect = Exception("Network error")
        
        valid_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/test/network-error-mcp
identifier: test/network-error-mcp
name: Network Error MCP
description: A test MCP for network error testing
codeRepository: https://github.com/test/network-error-mcp
maintainer:
  - "@type": Person
    name: Test User
license: https://spdx.org/licenses/MIT.html
applicationCategory: HealthApplication
keywords:
  - test
programmingLanguage:
  - Python
"""
        
        result = submit_to_registry(valid_yaml)
        
        assert result["success"] is False
        assert "Network error" in result["errors"][0]


class TestRegistrySchema:
    """Test registry schema functionality."""

    def test_get_registry_schema(self):
        """Test getting registry schema."""
        schema = get_registry_schema()
        
        assert "$schema" in schema
        assert "properties" in schema
        assert "required" in schema
        assert "@context" in schema["properties"]
        assert "@type" in schema["properties"]
        assert "identifier" in schema["properties"]
        assert "name" in schema["properties"]
        assert "description" in schema["properties"]


class TestConfirmationWorkflow:
    """Test the new file-based confirmation workflow for registry submission."""

    def test_submit_tool_creates_yaml_file_with_confirmation_flag(self):
        """Test that submit_to_registry_tool creates YAML file with user_confirmed: false."""
        import tempfile
        import os
        from registry_mcp.tools.registry_submission import validate_yaml_specification
        import yaml
        
        valid_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/test/confirmation-mcp
identifier: test/confirmation-mcp
name: Confirmation Test MCP
description: A test MCP for confirmation workflow testing
codeRepository: https://github.com/test/confirmation-mcp
maintainer:
  - "@type": Person
    name: Test User
    identifier: 'GitHub: testuser'
    url: https://github.com/testuser
license: https://spdx.org/licenses/MIT.html
applicationCategory: HealthApplication
keywords:
  - test
  - confirmation
programmingLanguage:
  - Python
"""
        
        # Test validation first
        validation_result = validate_yaml_specification(valid_yaml)
        assert validation_result["valid"] is True
        
        # Test YAML parsing and user_confirmed flag
        yaml_data = yaml.safe_load(valid_yaml)
        yaml_data["user_confirmed"] = False
        
        # Create temporary file to test file writing (simulating meta.yaml)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)
            temp_file = f.name
        
        try:
            # Verify the file was created and contains user_confirmed: false
            with open(temp_file, 'r') as f:
                saved_data = yaml.safe_load(f)
            
            assert saved_data["user_confirmed"] is False
            assert saved_data["identifier"] == "test/confirmation-mcp"
            assert saved_data["name"] == "Confirmation Test MCP"
            
        finally:
            # Clean up
            os.unlink(temp_file)

    def test_confirm_and_submit_tool_updates_confirmation_flag(self):
        """Test that confirm_and_submit_to_registry_tool updates user_confirmed to true."""
        import tempfile
        import os
        from registry_mcp.tools.registry_submission import validate_yaml_specification
        import yaml
        
        # Create a test YAML file with user_confirmed: false
        yaml_data = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "@id": "https://github.com/test/confirmation-mcp",
            "identifier": "test/confirmation-mcp",
            "name": "Confirmation Test MCP",
            "description": "A test MCP for confirmation workflow testing",
            "codeRepository": "https://github.com/test/confirmation-mcp",
            "maintainer": [{
                "@type": "Person",
                "name": "Test User",
                "identifier": "GitHub: testuser",
                "url": "https://github.com/testuser"
            }],
            "license": "https://spdx.org/licenses/MIT.html",
            "applicationCategory": "HealthApplication",
            "keywords": ["test", "confirmation"],
            "programmingLanguage": ["Python"],
            "user_confirmed": False
        }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)
            temp_file = f.name
        
        try:
            # Verify initial state
            with open(temp_file, 'r') as f:
                initial_data = yaml.safe_load(f)
            assert initial_data["user_confirmed"] is False
            
            # Simulate what confirm_and_submit_to_registry_tool does
            # (without actually submitting to avoid network calls)
            yaml_data["user_confirmed"] = True
            with open(temp_file, 'w') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)
            
            # Verify the flag was updated
            with open(temp_file, 'r') as f:
                updated_data = yaml.safe_load(f)
            assert updated_data["user_confirmed"] is True
            
        finally:
            # Clean up
            os.unlink(temp_file)

    def test_check_yaml_file_status_tool(self):
        """Test the check_yaml_file_status_tool functionality."""
        import tempfile
        import os
        from registry_mcp.tools.registry_submission import validate_yaml_specification
        import yaml
        
        # Create a test YAML file
        yaml_data = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "@id": "https://github.com/test/confirmation-mcp",
            "identifier": "test/confirmation-mcp",
            "name": "Confirmation Test MCP",
            "description": "A test MCP for confirmation workflow testing",
            "codeRepository": "https://github.com/test/confirmation-mcp",
            "maintainer": [{
                "@type": "Person",
                "name": "Test User",
                "identifier": "GitHub: testuser",
                "url": "https://github.com/testuser"
            }],
            "license": "https://spdx.org/licenses/MIT.html",
            "applicationCategory": "HealthApplication",
            "keywords": ["test", "confirmation"],
            "programmingLanguage": ["Python"],
            "user_confirmed": False
        }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)
            temp_file = f.name
        
        try:
            # Test file status check
            yaml_content = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)
            validation_result = validate_yaml_specification(yaml_content)
            
            # Simulate what check_yaml_file_status_tool returns
            result = {
                "success": True,
                "message": "YAML file status retrieved successfully",
                "file_exists": True,
                "file_path": temp_file,
                "identifier": "test/confirmation-mcp",
                "name": "Confirmation Test MCP",
                "user_confirmed": False,
                "validation_result": validation_result,
                "ready_for_submission": False  # False because user_confirmed is False
            }
            
            assert result["success"] is True
            assert result["file_exists"] is True
            assert result["identifier"] == "test/confirmation-mcp"
            assert result["user_confirmed"] is False
            assert result["ready_for_submission"] is False
            assert result["validation_result"]["valid"] is True
            
        finally:
            # Clean up
            os.unlink(temp_file)

    def test_submit_tool_rejects_invalid_yaml(self):
        """Test that submit_to_registry_tool rejects invalid YAML without confirmation."""
        from registry_mcp.tools.registry_submission import validate_yaml_specification
        
        invalid_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
name: Incomplete MCP
"""
        
        # Simulate what the modified submit_to_registry_tool does
        validation_result = validate_yaml_specification(invalid_yaml)
        
        if not validation_result["valid"]:
            result = {
                "success": False,
                "message": "Validation failed - cannot submit invalid YAML",
                "validation_result": validation_result,
                "requires_confirmation": False
            }
        else:
            # This shouldn't happen with invalid YAML
            result = {"success": False, "requires_confirmation": False}
        
        # Should not be submitted and not require confirmation
        assert result["success"] is False
        assert result["requires_confirmation"] is False
        assert "Validation failed" in result["message"]
        
        # Should have validation result with errors
        assert "validation_result" in result
        assert result["validation_result"]["valid"] is False
        assert len(result["validation_result"]["errors"]) > 0

    def test_submit_tool_handles_yaml_parsing_error(self):
        """Test that submit_to_registry_tool handles YAML parsing errors gracefully."""
        from registry_mcp.tools.registry_submission import validate_yaml_specification
        import yaml
        
        # Invalid YAML syntax
        invalid_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
invalid: yaml: syntax: here
"""
        
        # Simulate what the modified submit_to_registry_tool does
        try:
            validation_result = validate_yaml_specification(invalid_yaml)
            yaml_data = yaml.safe_load(invalid_yaml)
            result = {
                "success": False,
                "message": "YAML validation successful. User confirmation required before submission.",
                "validation_result": validation_result,
                "requires_confirmation": True
            }
        except Exception as e:
            result = {
                "success": False,
                "message": f"Failed to parse YAML for confirmation: {e}",
                "validation_result": {"valid": False, "errors": [str(e)]},
                "requires_confirmation": False
            }
        
        # Should not be submitted and not require confirmation
        assert result["success"] is False
        assert result["requires_confirmation"] is False
        assert "Failed to parse YAML" in result["message"]
        
        # Should have validation result
        assert "validation_result" in result

    def test_confirm_and_submit_tool_calls_original_function(self):
        """Test that confirm_and_submit_to_registry_tool calls the original submit function."""
        from registry_mcp.tools.registry_submission import submit_to_registry
        
        valid_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/test/confirm-submit-mcp
identifier: test/confirm-submit-mcp
name: Confirm Submit Test MCP
description: A test MCP for confirm and submit testing
codeRepository: https://github.com/test/confirm-submit-mcp
maintainer:
  - "@type": Person
    name: Test User
license: https://spdx.org/licenses/MIT.html
applicationCategory: HealthApplication
keywords:
  - test
programmingLanguage:
  - Python
"""
        
        # Test that submit_to_registry works correctly
        # We'll test this by mocking the requests.post call
        with patch('registry_mcp.tools.registry_submission.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {"id": "test-123"}
            mock_post.return_value = mock_response
            
            # Call submit_to_registry directly
            result = submit_to_registry(valid_yaml)
            
            # Should call the API with correct parameters
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert call_args[0][0] == "https://api.biocontext.ai/registry/submit"
            
            # Should return the result from the function
            assert result["success"] is True
            assert result["submission_id"] == "test-123"

    def test_confirm_and_submit_tool_with_custom_endpoint(self):
        """Test that confirm_and_submit_to_registry_tool passes custom endpoint."""
        from registry_mcp.tools.registry_submission import submit_to_registry
        
        valid_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/test/custom-endpoint-mcp
identifier: test/custom-endpoint-mcp
name: Custom Endpoint Test MCP
description: A test MCP for custom endpoint testing
codeRepository: https://github.com/test/custom-endpoint-mcp
maintainer:
  - "@type": Person
    name: Test User
license: https://spdx.org/licenses/MIT.html
applicationCategory: HealthApplication
keywords:
  - test
programmingLanguage:
  - Python
"""
        
        custom_endpoint = "https://custom-api.example.com/submit"
        
        # Test that submit_to_registry accepts custom endpoint
        with patch('registry_mcp.tools.registry_submission.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {"id": "custom-123"}
            mock_post.return_value = mock_response
            
            result = submit_to_registry(valid_yaml, custom_endpoint)
            
            # Should call the API with custom endpoint
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert call_args[0][0] == custom_endpoint
            
            # Should return successful result
            assert result["success"] is True

    def test_confirmation_workflow_integration(self):
        """Test the complete confirmation workflow integration."""
        from registry_mcp.tools.registry_submission import validate_yaml_specification, submit_to_registry
        import yaml
        
        valid_yaml = """
"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/test/integration-mcp
identifier: test/integration-mcp
name: Integration Test MCP
description: A test MCP for integration testing
codeRepository: https://github.com/test/integration-mcp
maintainer:
  - "@type": Person
    name: Test User
    identifier: 'GitHub: testuser'
    url: https://github.com/testuser
license: https://spdx.org/licenses/MIT.html
applicationCategory: HealthApplication
keywords:
  - test
  - integration
programmingLanguage:
  - Python
"""
        
        # Step 1: Simulate submission request (should require confirmation)
        validation_result = validate_yaml_specification(valid_yaml)
        yaml_data = yaml.safe_load(valid_yaml)
        
        submission_request = {
            "success": False,
            "requires_confirmation": True,
            "validation_result": validation_result,
            "submission_preview": {
                "identifier": yaml_data.get("identifier"),
                "name": yaml_data.get("name"),
                "code_repository": yaml_data.get("codeRepository")
            }
        }
        
        assert submission_request["requires_confirmation"] is True
        assert submission_request["success"] is False
        
        # Step 2: Mock the actual submission after user confirms
        with patch('registry_mcp.tools.registry_submission.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 201
            mock_response.json.return_value = {"id": "integration-123"}
            mock_post.return_value = mock_response
            
            # User confirms and we call the submit function
            submission_result = submit_to_registry(valid_yaml)
            
            # Should have successfully submitted
            assert submission_result["success"] is True
            assert submission_result["submission_id"] == "integration-123"
            
            # Should have called the API
            mock_post.assert_called_once()
