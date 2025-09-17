# Registry MCP
[![BioContextAI - Registry](https://img.shields.io/badge/Registry-package?style=flat&label=BioContextAI&labelColor=%23fff&color=%233555a1&link=https%3A%2F%2Fbiocontext.ai%2Fregistry)](https://biocontext.ai/registry)
[![Tests][badge-tests]][tests]
[![Documentation][badge-docs]][documentation]

[badge-tests]: https://img.shields.io/github/actions/workflow/status/slolab/registry-mcp/test.yaml?branch=main
[badge-docs]: https://img.shields.io/readthedocs/registry-mcp
[tests]: https://github.com/slolab/registry-mcp/actions
[documentation]: https://slolab.github.io/registry-mcp/
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://slolab.github.io/registry-mcp/)
[![GitHub](https://img.shields.io/badge/GitHub-slolab%2Fregistry--mcp-blue.svg)](https://github.com/slolab/registry-mcp)

A Model Context Protocol (MCP) server for assisting users in registering their MCP servers, knowledge graph components, and other biomedical tools to the BioContextAI registry.

## 🚀 Quick Start

To use this MCP server to submit your project to the BioContext registry, simply ask your AI assistant:

> **"Help me submit this project to the BioContext registry"**

The MCP will automatically:
1. **Analyze your project** - Extract metadata from your project files
2. **Generate YAML** - Create a schema.org-compatible specification
3. **Validate** - Check the specification against registry requirements
4. **Request confirmation** - Ask you to review before submission
5. **Submit** - Send your project to the registry (after your confirmation)

### Prerequisites

- [Install the MCP server](https://slolab.github.io/registry-mcp/installation/) in your AI assistant
- Have your project ready with a `pyproject.toml`, `README.md`, or similar metadata files

## Overview

The Registry MCP provides a comprehensive set of tools to help users create, validate, and submit schema.org-compatible YAML specifications to the BioContextAI registry. It follows the same pattern as the [biocypher-mcp](https://github.com/biocypher/biocypher-mcp) repository, providing structured guidance and automation for registry submissions.

## Features

### Core Functionality

- **Project Analysis**: Automatically extract metadata from existing project files (pyproject.toml, README.md, etc.)
- **YAML Generation**: Create schema.org-compatible YAML specifications from user input
- **Validation**: Validate submissions against the registry schema with detailed feedback
- **API Submission**: Submit validated specifications to the registry REST API
- **Troubleshooting**: Comprehensive guidance and error resolution

### Available Tools

#### Registry Submission Tools

1. **`analyze_project_directory_tool`** - Analyze project directory to extract metadata
2. **`generate_yaml_template_tool`** - Generate YAML template from metadata
3. **`validate_yaml_specification_tool`** - Validate YAML against registry schema
4. **`submit_to_registry_tool`** - Request submission (requires user confirmation)
5. **`confirm_and_submit_to_registry_tool`** - Actually submit after user confirmation
6. **`get_registry_schema_tool`** - Get the complete registry schema

#### Guidance and Troubleshooting Tools

7. **`get_registry_workflow_guidance_tool`** - Get step-by-step submission workflow
8. **`get_example_submissions_tool`** - Get example YAML submissions
9. **`get_troubleshooting_guide_tool`** - Get comprehensive troubleshooting guide
10. **`get_field_guidance_tool`** - Get detailed guidance for specific fields

## Installation

```bash
# Clone the repository
git clone https://github.com/slolab/registry-mcp.git
cd registry-mcp

# Install dependencies
uv sync

# Run the MCP server
uv run registry_mcp

# Or test the installation
uv run registry_mcp --version
uv run registry_mcp --help
```

## Usage

### Basic Workflow

1. **Analyze your project**:
   ```python
   # Use the MCP tool to analyze your project directory
   result = analyze_project_directory_tool(".")
   ```

2. **Generate YAML template**:
   ```python
   # Create YAML from your metadata
   yaml_content = generate_yaml_template_tool({
       "identifier": "your-username/your-repo",
       "name": "Your MCP Server",
       "description": "Description of your MCP server",
       # ... other metadata
   })
   ```

3. **Validate specification**:
   ```python
   # Validate the YAML
   validation_result = validate_yaml_specification_tool(yaml_content)
   ```

4. **Submit to registry** (with file-based confirmation):
   ```python
   # First, create YAML file and request confirmation
   # Specify project_path to save meta.yaml in the project directory
   submission_request = submit_to_registry_tool(yaml_content, project_path=".")
   
   # The tool will create a YAML file and return confirmation request
   if submission_request.get("requires_confirmation"):
       print(submission_request["confirmation_message"])
       yaml_file_path = submission_request["yaml_file"]
       
       # User must explicitly confirm before actual submission
       # After user confirms, call:
       submission_result = confirm_and_submit_to_registry_tool(yaml_file_path)
   ```

### File-Based User Confirmation Workflow

The registry submission process now uses a robust file-based confirmation system to prevent accidental submissions:

1. **YAML File Creation**: `submit_to_registry_tool()` validates the YAML and creates a `meta.yaml` file with `user_confirmed: false` in the specified project directory (defaults to current directory)
2. **User Review**: The tool displays submission details and asks for confirmation
3. **User Decision**: User must explicitly confirm with "Yes, submit to registry" or "Confirm submission"
4. **Confirmation Update**: `confirm_and_submit_to_registry_tool()` sets `user_confirmed: true` and performs the submission
5. **Status Checking**: `check_yaml_file_status_tool()` allows checking the current status of any YAML file

**Important**: The `meta.yaml` file will be created in the specified project directory. Use the `project_path` parameter to ensure it's saved in the correct location.

This ensures users have full control over when their MCP servers are submitted to the public registry, with a persistent record of the confirmation state.

### Example YAML Structure

Based on the [BioCypher MCP example](https://raw.githubusercontent.com/biocontext-ai/registry/refs/heads/main/servers/biocypher-mcp/meta.yaml):

```yaml
"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/your-username/your-mcp

identifier: your-username/your-mcp

name: Your MCP Server Name

description: >
  A detailed description of your MCP server's functionality,
  use cases, and target audience.

codeRepository: https://github.com/your-username/your-mcp

url: https://your-mcp.example.com  # Optional

softwareHelp:
  "@type": CreativeWork
  url: https://your-mcp.example.com/docs
  name: Your MCP Documentation

maintainer:
  - "@type": Person
    name: Your Name
    identifier: "GitHub: your-username"
    url: https://github.com/your-username

license: https://spdx.org/licenses/MIT.html

applicationCategory: HealthApplication

keywords:
  - keyword1
  - keyword2
  - keyword3

operatingSystem:
  - Cross-platform

programmingLanguage:
  - Python

featureList:
  - Feature 1
  - Feature 2
  - Feature 3

user_confirmed: false  # Set to true only after user confirmation
```

## Schema Requirements

The registry uses a schema.org-compatible specification with the following required fields:

### Required Fields
- `@context`: Must be "https://schema.org"
- `@type`: Must be "SoftwareApplication"
- `@id`: Unique identifier URI (typically GitHub URL)
- `identifier`: Repository identifier in format "owner/repository"
- `name`: Component name (1-100 characters)
- `description`: Detailed description (10-1000 characters)
- `codeRepository`: Repository URL (GitHub, GitLab, Bitbucket, or Codeberg)
- `maintainer`: Maintainer information (Person or Organization)
- `license`: SPDX license URL
- `applicationCategory`: Application type
- `keywords`: 1-10 relevant keywords
- `programmingLanguage`: Programming languages used

### Optional Fields
- `url`: Remote hosting URL
- `softwareHelp`: Documentation/help resource
- `featureList`: List of features/capabilities
- `operatingSystem`: Supported operating systems
- `user_confirmed`: User confirmation flag (boolean, defaults to false)

## Registry Schema

The registry follows a strict JSON schema for validation. You can retrieve the complete schema using:

```python
schema = get_registry_schema_tool()
```

## Troubleshooting

### Common Issues

1. **Invalid identifier format**: Use "owner/repository" format
2. **Missing required fields**: Ensure all required fields are present
3. **Invalid license format**: Use SPDX format (https://spdx.org/licenses/LICENSE.html)
4. **Unsupported repository**: Use GitHub, GitLab, Bitbucket, or Codeberg

### Getting Help

Use the troubleshooting tools for detailed guidance:

```python
# Get comprehensive troubleshooting guide
troubleshooting = get_troubleshooting_guide_tool()

# Get guidance for specific fields
field_help = get_field_guidance_tool("identifier")

# Get workflow guidance
workflow = get_registry_workflow_guidance_tool()
```

## Development

### Running Tests

```bash
# Run the test suite
uv run python test_registry_mcp.py
```

### Project Structure

```
src/registry_mcp/
├── __init__.py
├── main.py              # CLI entry point
├── mcp.py               # MCP server configuration
└── tools/
    ├── __init__.py
    ├── _greet.py        # Example tool
    ├── registry_submission.py  # Core submission tools
    └── registry_guidance.py    # Guidance and troubleshooting
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [BioCypher MCP](https://github.com/biocypher/biocypher-mcp) - MCP server for BioCypher workflows
- [BioContextAI Registry](https://github.com/biocontext-ai/registry) - The registry this MCP submits to
- [Model Context Protocol](https://modelcontextprotocol.io/) - The MCP specification

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting guide
- Review the example submissions
- Use the field guidance tools