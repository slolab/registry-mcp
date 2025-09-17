# Quick Reference

This page provides a quick reference for all Registry MCP tools and their usage.

## Available Tools

### Registry Submission Tools

#### `analyze_project_directory_tool`
Analyze project directory to extract existing metadata.

**Parameters:**
- `project_path` (str, optional): Path to project directory (defaults to ".")

**Returns:**
- Project metadata analysis with detected files, suggestions, and recommendations

**Example:**
```python
result = await client.call_tool("analyze_project_directory_tool", {"project_path": "."})
```

#### `generate_yaml_template_tool`
Generate schema.org-compatible YAML specification from metadata.

**Parameters:**
- `metadata` (dict): Dictionary containing component metadata

**Returns:**
- YAML string representing the registry submission

**Example:**
```python
yaml_content = await client.call_tool("generate_yaml_template_tool", {
    "metadata": {
        "identifier": "user/repo",
        "name": "Component Name",
        "description": "Component description",
        # ... other metadata
    }
})
```

#### `validate_yaml_specification_tool`
Validate YAML specification against registry schema.

**Parameters:**
- `yaml_content` (str): YAML content as string

**Returns:**
- Validation results with errors, warnings, and suggestions

**Example:**
```python
result = await client.call_tool("validate_yaml_specification_tool", {
    "yaml_content": yaml_string
})
```

#### `submit_to_registry_tool`
Create YAML file and request user confirmation for registry submission.

**Parameters:**
- `yaml_content` (str): YAML content as string
- `api_endpoint` (str, optional): Registry API endpoint URL

**Returns:**
- File creation results with confirmation request and YAML file path

**Example:**
```python
result = await client.call_tool("submit_to_registry_tool", {
    "yaml_content": yaml_string
})

if result.get('requires_confirmation'):
    print(f"YAML file created: {result['yaml_file']}")
    print(result['confirmation_message'])
```

#### `confirm_and_submit_to_registry_tool`
Confirm and submit YAML file to registry API after user confirmation.

**Parameters:**
- `yaml_file_path` (str): Path to the YAML file to submit
- `api_endpoint` (str, optional): Registry API endpoint URL

**Returns:**
- Submission results with success status and any errors

**Example:**
```python
result = await client.call_tool("confirm_and_submit_to_registry_tool", {
    "yaml_file_path": "/path/to/registry_submission_file.yaml"
})
```

#### `check_yaml_file_status_tool`
Check the status of a YAML file for registry submission.

**Parameters:**
- `yaml_file_path` (str): Path to the YAML file to check

**Returns:**
- File status information including confirmation state and validation results

**Example:**
```python
result = await client.call_tool("check_yaml_file_status_tool", {
    "yaml_file_path": "/path/to/registry_submission_file.yaml"
})

print(f"User confirmed: {result['user_confirmed']}")
print(f"Ready for submission: {result['ready_for_submission']}")
```

#### `get_registry_schema_tool`
Get the complete registry schema definition.

**Parameters:**
- None

**Returns:**
- JSON schema for registry submissions

**Example:**
```python
schema = await client.call_tool("get_registry_schema_tool", {})
```

### Guidance and Troubleshooting Tools

#### `get_registry_workflow_guidance_tool`
Get step-by-step submission workflow guidance.

**Parameters:**
- None

**Returns:**
- Complete workflow guidance with steps, best practices, and common issues

**Example:**
```python
guidance = await client.call_tool("get_registry_workflow_guidance_tool", {})
```

#### `get_example_submissions_tool`
Get example YAML submissions for different component types.

**Parameters:**
- None

**Returns:**
- Example submissions for MCP servers, biomedical tools, and data analysis tools

**Example:**
```python
examples = await client.call_tool("get_example_submissions_tool", {})
```

#### `get_troubleshooting_guide_tool`
Get comprehensive troubleshooting guide.

**Parameters:**
- None

**Returns:**
- Troubleshooting information for validation errors, submission errors, and common warnings

**Example:**
```python
troubleshooting = await client.call_tool("get_troubleshooting_guide_tool", {})
```

#### `get_field_guidance_tool`
Get detailed guidance for specific registry fields.

**Parameters:**
- `field_name` (str): Name of the field to get guidance for

**Returns:**
- Detailed field guidance with requirements, examples, and tips

**Example:**
```python
guidance = await client.call_tool("get_field_guidance_tool", {
    "field_name": "identifier"
})
```

## Required Metadata Fields

### Core Fields
- `identifier`: Repository identifier in format "owner/repository"
- `name`: Component name (1-100 characters)
- `description`: Detailed description (10-1000 characters)
- `codeRepository`: Repository URL (GitHub, GitLab, Bitbucket, or Codeberg)
- `maintainer`: Maintainer information (Person or Organization)
- `license`: SPDX license URL (e.g., `https://spdx.org/licenses/MIT.html`)
- `applicationCategory`: Application type
- `keywords`: 1-10 relevant keywords
- `programmingLanguage`: Programming languages used

### Optional Fields
- `url`: Remote hosting URL
- `softwareHelp`: Documentation/help resource
- `featureList`: List of features/capabilities
- `operatingSystem`: Supported operating systems

## Application Categories

- `HealthApplication`: For biomedical, healthcare, or life sciences tools
- `EducationApplication`: For educational or training tools
- `ReferenceApplication`: For reference or lookup tools
- `DeveloperApplication`: For development tools and frameworks
- `UtilitiesApplication`: For general utility tools

## Supported Programming Languages

- Python, TypeScript, JavaScript, R, Julia
- Java, Go, Rust, C#, C++
- Other

## Supported Operating Systems

- Windows, macOS, Linux, Unix
- Cross-platform

## Common License URLs

- MIT: `https://spdx.org/licenses/MIT.html`
- Apache 2.0: `https://spdx.org/licenses/Apache-2.0.html`
- GPL 3.0: `https://spdx.org/licenses/GPL-3.0.html`
- BSD 3-Clause: `https://spdx.org/licenses/BSD-3-Clause.html`

## Maintainer Types

### Person
```json
{
  "@type": "Person",
  "name": "John Doe",
  "identifier": "GitHub: johndoe",
  "url": "https://github.com/johndoe"
}
```

### Organization
```json
{
  "@type": "Organization",
  "name": "Organization Name",
  "identifier": "GitHub: orgname",
  "url": "https://github.com/orgname"
}
```

## Common Error Messages

- **"Identifier must be in format 'owner/repository'"**: Use format like `username/repository-name`
- **"Missing required fields"**: Ensure all required fields are present and non-empty
- **"License should use SPDX format"**: Use format like `https://spdx.org/licenses/MIT.html`
- **"Repository URL not supported"**: Use GitHub, GitLab, Bitbucket, or Codeberg URLs
- **"Schema validation error"**: Check field formats and required properties

## Workflow Summary

1. **Analyze** your project directory
2. **Gather** required metadata
3. **Generate** YAML specification
4. **Validate** against schema
5. **Fix** any issues
6. **Submit** to registry

## Getting Help

- Use `get_troubleshooting_guide_tool` for error resolution
- Use `get_field_guidance_tool` for field-specific help
- Use `get_example_submissions_tool` for examples
- Use `get_registry_workflow_guidance_tool` for complete workflow
