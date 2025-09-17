"""
Tests for registry guidance tools.
"""

import pytest

from registry_mcp.tools.registry_guidance import (
    get_registry_workflow_guidance,
    get_example_submissions,
    get_troubleshooting_guide,
    get_field_guidance,
)


class TestWorkflowGuidance:
    """Test workflow guidance functionality."""

    def test_get_workflow_guidance(self):
        """Test getting workflow guidance."""
        guidance = get_registry_workflow_guidance()
        
        assert "workflow_overview" in guidance
        assert "workflow_steps" in guidance
        assert "best_practices" in guidance
        assert "common_issues" in guidance
        
        # Check workflow overview
        overview = guidance["workflow_overview"]
        assert "name" in overview
        assert "description" in overview
        assert "estimated_time" in overview
        assert "prerequisites" in overview
        
        # Check workflow steps
        steps = guidance["workflow_steps"]
        assert len(steps) == 5
        assert all("step" in step for step in steps)
        assert all("name" in step for step in steps)
        assert all("description" in step for step in steps)
        
        # Check step numbers
        step_numbers = [step["step"] for step in steps]
        assert step_numbers == [1, 2, 3, 4, 5]

    def test_workflow_step_content(self):
        """Test workflow step content."""
        guidance = get_registry_workflow_guidance()
        steps = guidance["workflow_steps"]
        
        # Test first step (Project Analysis)
        step1 = steps[0]
        assert step1["name"] == "Project Analysis"
        assert "activities" in step1
        assert "outputs" in step1
        assert "tool" in step1
        
        # Test last step (Submission)
        step5 = steps[4]
        assert step5["name"] == "Submission"
        assert "activities" in step5
        assert "outputs" in step5
        assert "tool" in step5

    def test_best_practices(self):
        """Test best practices content."""
        guidance = get_registry_workflow_guidance()
        best_practices = guidance["best_practices"]
        
        assert isinstance(best_practices, list)
        assert len(best_practices) > 0
        assert all(isinstance(practice, str) for practice in best_practices)

    def test_common_issues(self):
        """Test common issues content."""
        guidance = get_registry_workflow_guidance()
        common_issues = guidance["common_issues"]
        
        assert isinstance(common_issues, list)
        assert len(common_issues) > 0
        
        for issue in common_issues:
            assert "issue" in issue
            assert "solution" in issue
            # Check for either example, required, or supported fields
            assert any(field in issue for field in ["example", "required", "supported"])


class TestExampleSubmissions:
    """Test example submissions functionality."""

    def test_get_example_submissions(self):
        """Test getting example submissions."""
        examples = get_example_submissions()
        
        assert "mcp_server_example" in examples
        assert "biomedical_tool_example" in examples
        assert "data_analysis_tool_example" in examples

    def test_mcp_server_example(self):
        """Test MCP server example."""
        examples = get_example_submissions()
        mcp_example = examples["mcp_server_example"]
        
        assert "name" in mcp_example
        assert "description" in mcp_example
        assert "yaml_content" in mcp_example
        
        # Check YAML content contains expected fields
        yaml_content = mcp_example["yaml_content"]
        assert "@context" in yaml_content
        assert "@type" in yaml_content
        assert "identifier" in yaml_content
        assert "name" in yaml_content
        assert "description" in yaml_content

    def test_biomedical_tool_example(self):
        """Test biomedical tool example."""
        examples = get_example_submissions()
        bio_example = examples["biomedical_tool_example"]
        
        assert "name" in bio_example
        assert "description" in bio_example
        assert "yaml_content" in bio_example
        
        # Check it's a biomedical tool
        assert "PubMed" in bio_example["name"]
        assert "biomedical" in bio_example["description"].lower()

    def test_data_analysis_tool_example(self):
        """Test data analysis tool example."""
        examples = get_example_submissions()
        data_example = examples["data_analysis_tool_example"]
        
        assert "name" in data_example
        assert "description" in data_example
        assert "yaml_content" in data_example
        
        # Check it's a data analysis tool
        assert "Genomics" in data_example["name"]
        assert "analysis" in data_example["description"].lower()


class TestTroubleshootingGuide:
    """Test troubleshooting guide functionality."""

    def test_get_troubleshooting_guide(self):
        """Test getting troubleshooting guide."""
        guide = get_troubleshooting_guide()
        
        assert "troubleshooting_overview" in guide
        assert "validation_errors" in guide
        assert "submission_errors" in guide
        assert "common_warnings" in guide
        assert "best_practices" in guide

    def test_validation_errors(self):
        """Test validation errors section."""
        guide = get_troubleshooting_guide()
        validation_errors = guide["validation_errors"]
        
        assert "invalid_identifier" in validation_errors
        assert "missing_required_fields" in validation_errors
        assert "invalid_license_format" in validation_errors
        assert "invalid_repository_url" in validation_errors
        
        # Test invalid identifier error
        invalid_id = validation_errors["invalid_identifier"]
        assert "error" in invalid_id
        assert "causes" in invalid_id
        assert "solutions" in invalid_id
        assert "example_fix" in invalid_id

    def test_submission_errors(self):
        """Test submission errors section."""
        guide = get_troubleshooting_guide()
        submission_errors = guide["submission_errors"]
        
        assert "api_connection_failed" in submission_errors
        assert "authentication_failed" in submission_errors
        assert "duplicate_submission" in submission_errors
        
        # Test API connection error
        api_error = submission_errors["api_connection_failed"]
        assert "error" in api_error
        assert "causes" in api_error
        assert "solutions" in api_error

    def test_common_warnings(self):
        """Test common warnings section."""
        guide = get_troubleshooting_guide()
        warnings = guide["common_warnings"]
        
        assert "missing_optional_fields" in warnings
        assert "generic_keywords" in warnings
        assert "short_description" in warnings

    def test_best_practices(self):
        """Test best practices section."""
        guide = get_troubleshooting_guide()
        best_practices = guide["best_practices"]
        
        assert "metadata_quality" in best_practices
        assert "testing" in best_practices
        assert "documentation" in best_practices
        
        # Check each section is a list
        for section in best_practices.values():
            assert isinstance(section, list)
            assert len(section) > 0


class TestFieldGuidance:
    """Test field guidance functionality."""

    def test_get_field_guidance_valid_field(self):
        """Test getting guidance for valid field."""
        guidance = get_field_guidance("name")
        
        assert "description" in guidance
        assert "requirements" in guidance
        assert "examples" in guidance
        assert "tips" in guidance

    def test_get_field_guidance_invalid_field(self):
        """Test getting guidance for invalid field."""
        guidance = get_field_guidance("invalid_field")
        
        assert "error" in guidance
        assert "available_fields" in guidance
        assert "invalid_field" in guidance["error"]

    def test_name_field_guidance(self):
        """Test name field guidance."""
        guidance = get_field_guidance("name")
        
        assert "The name of your MCP server or component" in guidance["description"]
        assert "Must be 1-100 characters long" in guidance["requirements"]
        assert isinstance(guidance["examples"], list)
        assert len(guidance["examples"]) > 0

    def test_identifier_field_guidance(self):
        """Test identifier field guidance."""
        guidance = get_field_guidance("identifier")
        
        assert "owner/repository" in guidance["description"]
        assert "pattern" in guidance["requirements"][0]
        assert isinstance(guidance["examples"], list)
        assert all("/" in example for example in guidance["examples"])

    def test_maintainer_field_guidance(self):
        """Test maintainer field guidance."""
        guidance = get_field_guidance("maintainer")
        
        assert "maintainer" in guidance["description"].lower()
        assert "types" in guidance
        assert "Person" in guidance["types"]
        assert "Organization" in guidance["types"]
        
        # Check Person type example
        person_example = guidance["types"]["Person"]["example"]
        assert person_example["@type"] == "Person"
        assert "name" in person_example

    def test_license_field_guidance(self):
        """Test license field guidance."""
        guidance = get_field_guidance("license")
        
        assert "SPDX" in guidance["description"]
        assert "common_licenses" in guidance
        assert "MIT" in guidance["common_licenses"]
        assert "Apache-2.0" in guidance["common_licenses"]

    def test_keywords_field_guidance(self):
        """Test keywords field guidance."""
        guidance = get_field_guidance("keywords")
        
        assert "keywords" in guidance["description"].lower()
        assert "Must be 1-10 keywords" in guidance["requirements"]
        assert "examples" in guidance
        assert isinstance(guidance["examples"], list)

    def test_application_category_guidance(self):
        """Test application category guidance."""
        guidance = get_field_guidance("applicationCategory")
        
        assert "options" in guidance
        assert "HealthApplication" in guidance["options"]
        assert "DeveloperApplication" in guidance["options"]
        assert "guidance" in guidance
        assert "HealthApplication" in guidance["guidance"]

    def test_programming_language_guidance(self):
        """Test programming language guidance."""
        guidance = get_field_guidance("programmingLanguage")
        
        assert "supported_languages" in guidance
        assert "Python" in guidance["supported_languages"]
        assert "TypeScript" in guidance["supported_languages"]
        assert "tips" in guidance
