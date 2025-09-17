# Usage Guide

This guide walks you through using the Registry MCP to annotate and submit an arbitrary component to the BioContextAI registry.

## Overview

The Registry MCP provides 10 tools to help you:
1. **Analyze** your project directory to extract existing metadata
2. **Generate** schema.org-compatible YAML specifications
3. **Validate** submissions against the registry schema
4. **Submit** to the BioContextAI registry API
5. **Get guidance** and troubleshoot issues

## Step-by-Step Tutorial

### Step 1: Prepare Your Project

Navigate to your component's project directory:

```bash
cd /path/to/your/component
```

Ensure your project has:
- A clear name and purpose
- A README.md file (recommended)
- A LICENSE file (recommended)
- Source code in a supported language

### Step 2: Analyze Your Project

Use the MCP to analyze your project directory and extract existing metadata:

**Tool**: `analyze_project_directory_tool`

```python
# Example usage in MCP client
result = await client.call_tool("analyze_project_directory_tool", {
    "project_path": "."
})
```

This will:
- Detect configuration files (pyproject.toml, package.json, etc.)
- Extract metadata from existing files
- Provide suggestions and recommendations
- Identify missing information

**Example Output**:
```json
{
  "project_path": "/path/to/your/component",
  "detected_files": ["pyproject.toml", "README.md", "LICENSE"],
  "suggested_metadata": {
    "name": "your-component",
    "description": "Extracted from README.md",
    "programming_language": ["Python"]
  },
  "warnings": [],
  "recommendations": [
    "Please provide a GitHub repository URL to automatically extract the identifier"
  ]
}
```

### Step 3: Gather Required Information

Based on the analysis, collect the following required information:

#### Required Fields
- **name**: Clear, descriptive name for your component
- **description**: Detailed description (10-1000 characters)
- **codeRepository**: GitHub/GitLab/Bitbucket repository URL
- **maintainer**: Your information (Person or Organization)
- **license**: SPDX license identifier (e.g., `https://spdx.org/licenses/MIT.html`)
- **applicationCategory**: Type of application
- **keywords**: 1-10 relevant keywords
- **programmingLanguage**: Programming languages used

#### Optional Fields
- **url**: Remote hosting URL (if applicable)
- **softwareHelp**: Documentation URL
- **featureList**: List of features/capabilities
- **operatingSystem**: Supported operating systems

### Step 4: Get Field Guidance

Use the field guidance tool to understand specific requirements:

**Tool**: `get_field_guidance_tool`

```python
# Get guidance for specific fields
name_guidance = await client.call_tool("get_field_guidance_tool", {
    "field_name": "name"
})

identifier_guidance = await client.call_tool("get_field_guidance_tool", {
    "field_name": "identifier"
})

maintainer_guidance = await client.call_tool("get_field_guidance_tool", {
    "field_name": "maintainer"
})
```

### Step 5: Generate YAML Specification

Create your metadata dictionary and generate the YAML specification:

**Tool**: `generate_yaml_template_tool`

```python
# Prepare your metadata
metadata = {
    "identifier": "your-username/your-component",
    "name": "Your Component Name",
    "description": "A detailed description of your component's functionality, use cases, and target audience.",
    "codeRepository": "https://github.com/your-username/your-component",
    "url": "https://your-component.example.com",  # Optional
    "softwareHelp": {  # Optional
        "url": "https://your-component.example.com/docs",
        "name": "Your Component Documentation"
    },
    "maintainer": [
        {
            "@type": "Person",
            "name": "Your Name",
            "identifier": "GitHub: your-username",
            "url": "https://github.com/your-username"
        }
    ],
    "license": "https://spdx.org/licenses/MIT.html",
    "applicationCategory": "HealthApplication",  # or DeveloperApplication, etc.
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "operatingSystem": ["Cross-platform"],
    "programmingLanguage": ["Python"],
    "featureList": ["Feature 1", "Feature 2", "Feature 3"]
}

# Generate YAML
yaml_content = await client.call_tool("generate_yaml_template_tool", {
    "metadata": metadata
})
```

### Step 6: Validate Your Specification

Validate the generated YAML against the registry schema:

**Tool**: `validate_yaml_specification_tool`

```python
validation_result = await client.call_tool("validate_yaml_specification_tool", {
    "yaml_content": yaml_content
})

print(f"Valid: {validation_result['valid']}")
print(f"Errors: {validation_result['errors']}")
print(f"Warnings: {validation_result['warnings']}")
print(f"Suggestions: {validation_result['suggestions']}")
```

**Example Output**:
```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "suggestions": [
    "Consider adding 'softwareHelp' with documentation URL"
  ]
}
```

### Step 7: Fix Any Issues

If validation fails, use the troubleshooting guide:

**Tool**: `get_troubleshooting_guide_tool`

```python
troubleshooting = await client.call_tool("get_troubleshooting_guide_tool", {})
```

Common issues and solutions:
- **Invalid identifier**: Use format `owner/repository`
- **Missing required fields**: Ensure all required fields are present
- **Invalid license**: Use SPDX format (e.g., `https://spdx.org/licenses/MIT.html`)
- **Unsupported repository**: Use GitHub, GitLab, Bitbucket, or Codeberg

### Step 8: Submit to Registry (File-Based Confirmation)

The registry submission process now uses a robust file-based confirmation system to prevent accidental submissions:

**Tool**: `submit_to_registry_tool`

```python
# Step 8a: Create YAML file and request confirmation
submission_result = await client.call_tool("submit_to_registry_tool", {
    "yaml_content": yaml_content
})

print(f"Success: {submission_result['success']}")
print(f"Message: {submission_result['message']}")
print(f"Requires confirmation: {submission_result.get('requires_confirmation', False)}")

if submission_result.get('requires_confirmation'):
    print(f"YAML file created: {submission_result['yaml_file']}")
    print("Confirmation message:")
    print(submission_result['confirmation_message'])
```

**Example Output**:
```json
{
  "success": true,
  "message": "YAML file created successfully. User confirmation required before submission.",
  "requires_confirmation": true,
  "yaml_file": "/path/to/registry_submission_your-username_your-component.yaml",
  "submission_preview": {
    "identifier": "your-username/your-component",
    "name": "Your Component Name",
    "code_repository": "https://github.com/your-username/your-component"
  },
  "confirmation_message": "📄 YAML file created: registry_submission_your-username_your-component.yaml\n\n..."
}
```

**Step 8b: Confirm and Submit**

After reviewing the YAML file and confirming you want to proceed:

**Tool**: `confirm_and_submit_to_registry_tool`

```python
# Only call this after user confirmation
if user_confirmed:
    final_result = await client.call_tool("confirm_and_submit_to_registry_tool", {
        "yaml_file_path": submission_result['yaml_file']
    })
    
    print(f"Final submission success: {final_result['success']}")
    print(f"Final message: {final_result['message']}")
    if final_result.get('submission_id'):
        print(f"Submission ID: {final_result['submission_id']}")
```

**Step 8c: Check File Status (Optional)**

You can check the status of any YAML file at any time:

**Tool**: `check_yaml_file_status_tool`

```python
status_result = await client.call_tool("check_yaml_file_status_tool", {
    "yaml_file_path": submission_result['yaml_file']
})

print(f"File exists: {status_result['file_exists']}")
print(f"User confirmed: {status_result['user_confirmed']}")
print(f"Ready for submission: {status_result['ready_for_submission']}")
```

## Complete Example

Here's a complete example for a hypothetical MCP server:

```python
# 1. Analyze project
analysis = await client.call_tool("analyze_project_directory_tool", {"project_path": "."})

# 2. Prepare metadata
metadata = {
    "identifier": "johndoe/awesome-mcp",
    "name": "Awesome Biomedical MCP",
    "description": "A Model Context Protocol server that provides access to biomedical databases and analysis tools. Supports protein sequence analysis, pathway enrichment, and literature mining.",
    "codeRepository": "https://github.com/johndoe/awesome-mcp",
    "url": "https://awesome-mcp.example.com",
    "softwareHelp": {
        "url": "https://awesome-mcp.example.com/docs",
        "name": "Awesome MCP Documentation"
    },
    "maintainer": [
        {
            "@type": "Person",
            "name": "John Doe",
            "identifier": "GitHub: johndoe",
            "url": "https://github.com/johndoe"
        }
    ],
    "license": "https://spdx.org/licenses/MIT.html",
    "applicationCategory": "HealthApplication",
    "keywords": ["biomedical", "protein-analysis", "pathways", "literature-mining"],
    "operatingSystem": ["Cross-platform"],
    "programmingLanguage": ["Python"],
    "featureList": [
        "Protein Sequence Analysis",
        "Pathway Enrichment",
        "Literature Mining",
        "Database Integration"
    ]
}

# 3. Generate YAML
yaml_content = await client.call_tool("generate_yaml_template_tool", {"metadata": metadata})

# 4. Validate
validation = await client.call_tool("validate_yaml_specification_tool", {"yaml_content": yaml_content})

if validation["valid"]:
    # 5. Submit (with file-based confirmation)
    submission = await client.call_tool("submit_to_registry_tool", {"yaml_content": yaml_content})
    
    if submission.get('requires_confirmation'):
        print(f"YAML file created: {submission['yaml_file']}")
        print("Please review the YAML file and confirm submission.")
        print(submission['confirmation_message'])
        
        # After user confirmation:
        if user_confirmed:
            final_submission = await client.call_tool("confirm_and_submit_to_registry_tool", {
                "yaml_file_path": submission['yaml_file']
            })
            print(f"Final submission successful: {final_submission['success']}")
    else:
        print(f"Submission failed: {submission['message']}")
else:
    print(f"Validation failed: {validation['errors']}")
```

## Getting Help

### Available Tools

- `analyze_project_directory_tool`: Analyze project directory to extract metadata
- `generate_yaml_template_tool`: Generate YAML template from metadata
- `validate_yaml_specification_tool`: Validate YAML against registry schema
- `submit_to_registry_tool`: Create YAML file and request confirmation
- `confirm_and_submit_to_registry_tool`: Confirm and submit to registry API
- `check_yaml_file_status_tool`: Check status of YAML file
- `get_registry_workflow_guidance_tool`: Complete workflow guidance
- `get_example_submissions_tool`: Example YAML submissions
- `get_troubleshooting_guide_tool`: Comprehensive troubleshooting
- `get_field_guidance_tool`: Field-specific guidance
- `get_registry_schema_tool`: Complete schema definition

### Common Commands

```python
# Get workflow guidance
workflow = await client.call_tool("get_registry_workflow_guidance_tool", {})

# Get examples
examples = await client.call_tool("get_example_submissions_tool", {})

# Get troubleshooting help
troubleshooting = await client.call_tool("get_troubleshooting_guide_tool", {})

# Get schema
schema = await client.call_tool("get_registry_schema_tool", {})
```

## Best Practices

1. **Use descriptive names** that clearly indicate your component's purpose
2. **Write comprehensive descriptions** that explain functionality and use cases
3. **Include relevant keywords** to improve discoverability
4. **Provide clear documentation URLs** in softwareHelp
5. **Use SPDX license identifiers** for proper licensing
6. **Test your component** before submission
7. **Keep metadata up-to-date** with your project

## Troubleshooting

### Common Issues

- **"Identifier must be in format 'owner/repository'"**: Use your GitHub username and repository name
- **"Missing required fields"**: Ensure all required fields are present and non-empty
- **"License should use SPDX format"**: Use format like `https://spdx.org/licenses/MIT.html`
- **"Repository URL not supported"**: Use GitHub, GitLab, Bitbucket, or Codeberg URLs

### Getting Help

1. Use the troubleshooting guide tool
2. Check the example submissions
3. Review the field guidance for specific requirements
4. Validate your YAML before submission
5. Check the [GitHub issues](https://github.com/slolab/registry-mcp/issues) for known problems

## Next Steps

After successful submission:
1. Your component will be processed by the BioContextAI registry
2. The YAML file will be stored in the registry's GitHub repository
3. Your component will be discoverable through the registry
4. You can update your submission by resubmitting with the same identifier
