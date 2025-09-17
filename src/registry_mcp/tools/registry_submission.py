"""
Registry submission tools for MCP servers and other components.

This module provides tools to help users create, validate, and submit
schema.org-compatible YAML specifications to the BioContextAI registry.
"""

import os
import re
import yaml
from typing import Any
import requests
from registry_mcp.mcp import mcp


def get_registry_schema() -> dict[str, Any]:
    """
    Get the registry schema definition for validation.
    
    Returns:
        Dict containing the JSON schema for registry submissions
    """
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://raw.githubusercontent.com/biocontext-ai/registry-dev/main/schema.json",
        "title": "BioContextAI Registry",
        "description": "Schema.org SoftwareApplication compliant registry for biomedical MCP servers",
        "type": "object",
        "properties": {
            "@context": {
                "description": "JSON-LD context",
                "type": "string",
                "const": "https://schema.org"
            },
            "@type": {
                "description": "Primary Schema.org type",
                "type": "string",
                "const": "SoftwareApplication"
            },
            "@id": {
                "description": "Unique identifier URI for this MCP server",
                "type": "string",
                "format": "uri"
            },
            "identifier": {
                "description": "Unique identifier in format 'owner/repository'",
                "type": "string",
                "pattern": "^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$"
            },
            "name": {
                "description": "The name of the MCP server",
                "type": "string",
                "minLength": 1,
                "maxLength": 100
            },
            "description": {
                "description": "A description of the MCP server",
                "type": "string",
                "minLength": 10,
                "maxLength": 1000
            },
            "codeRepository": {
                "description": "URL of the source code repository",
                "type": "string",
                "format": "uri",
                "pattern": "^https://(github.com|gitlab.com|bitbucket.org|codeberg.com)(/[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+|/record/[0-9]+)(/.*)?$"
            },
            "url": {
                "description": "URL of the remotely hosted MCP server (if available)",
                "type": "string",
                "format": "uri"
            },
            "softwareHelp": {
                "description": "Documentation/help resource for the MCP server",
                "type": "object",
                "properties": {
                    "@type": {
                        "type": "string",
                        "const": "CreativeWork"
                    },
                    "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 100
                    },
                    "url": {
                        "type": "string",
                        "format": "uri"
                    }
                },
                "required": ["@type", "url"],
                "additionalProperties": False
            },
            "maintainer": {
                "description": "A maintainer of the MCP server",
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "@type": {
                            "type": "string",
                            "enum": ["Person", "Organization"]
                        },
                        "name": {
                            "type": "string"
                        },
                        "identifier": {
                            "description": "GitHub username, ORCID, or other identifier",
                            "type": "string"
                        },
                        "url": {
                            "description": "GitHub user profile or ORCID profile",
                            "type": "string",
                            "format": "uri"
                        }
                    },
                    "required": ["@type", "name"],
                    "additionalProperties": False
                }
            },
            "license": {
                "description": "Link to an OSI-approved license",
                "type": "string",
                "format": "uri"
            },
            "keywords": {
                "description": "Keywords or tags used to describe the MCP server",
                "type": "array",
                "items": {
                    "type": "string",
                    "minLength": 2,
                    "maxLength": 30
                },
                "minItems": 1,
                "maxItems": 10,
                "uniqueItems": True
            },
            "applicationCategory": {
                "description": "Type of software application",
                "type": "string",
                "enum": [
                    "HealthApplication",
                    "EducationApplication",
                    "ReferenceApplication",
                    "DeveloperApplication",
                    "UtilitiesApplication"
                ],
                "default": "HealthApplication"
            },
            "operatingSystem": {
                "description": "Operating systems supported",
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["Windows", "macOS", "Linux", "Unix", "Cross-platform"]
                },
                "default": ["Cross-platform"],
                "uniqueItems": True
            },
            "programmingLanguage": {
                "description": "The computer programming language",
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "Python",
                        "TypeScript",
                        "JavaScript",
                        "R",
                        "Julia",
                        "Java",
                        "Go",
                        "Rust",
                        "C#",
                        "C++",
                        "Other"
                    ]
                },
                "uniqueItems": True
            },
            "featureList": {
                "description": "Features provided by this MCP server",
                "type": "array",
                "items": {
                    "type": "string"
                },
                "uniqueItems": True
            }
        },
        "required": [
            "@context",
            "@type",
            "@id",
            "identifier",
            "name",
            "description",
            "codeRepository",
            "maintainer",
            "license",
            "applicationCategory",
            "keywords",
            "programmingLanguage"
        ],
        "additionalProperties": False
    }


def analyze_project_directory(project_path: str = ".") -> dict[str, Any]:
    """
    Analyze the current project directory to extract metadata for registry submission.
    
    Args:
        project_path: Path to the project directory (defaults to current directory)
        
    Returns:
        Dict containing extracted project metadata
    """
    analysis = {
        "project_path": os.path.abspath(project_path),
        "detected_files": [],
        "suggested_metadata": {},
        "warnings": [],
        "recommendations": []
    }
    
    # Check for common project files
    common_files = [
        "pyproject.toml", "package.json", "Cargo.toml", "go.mod", 
        "requirements.txt", "setup.py", "README.md", "LICENSE"
    ]
    
    for file in common_files:
        if os.path.exists(os.path.join(project_path, file)):
            analysis["detected_files"].append(file)
    
    # Try to extract metadata from pyproject.toml
    pyproject_path = os.path.join(project_path, "pyproject.toml")
    if os.path.exists(pyproject_path):
        try:
            import tomllib
            with open(pyproject_path, "rb") as f:
                pyproject_data = tomllib.load(f)
            
            project_data = pyproject_data.get("project", {})
            if project_data:
                analysis["suggested_metadata"]["name"] = project_data.get("name", "")
                analysis["suggested_metadata"]["description"] = project_data.get("description", "")
                analysis["suggested_metadata"]["license"] = project_data.get("license", {})
                analysis["suggested_metadata"]["authors"] = project_data.get("authors", [])
                analysis["suggested_metadata"]["keywords"] = project_data.get("keywords", [])
                analysis["suggested_metadata"]["programming_language"] = ["Python"]
                
                # Extract repository URL
                urls = project_data.get("urls", {})
                if "Homepage" in urls:
                    repo_url = urls["Homepage"]
                    if "github.com" in repo_url:
                        analysis["suggested_metadata"]["codeRepository"] = repo_url
                        # Extract identifier from GitHub URL
                        match = re.search(r"github\.com/([^/]+/[^/]+)", repo_url)
                        if match:
                            analysis["suggested_metadata"]["identifier"] = match.group(1)
        except Exception as e:
            analysis["warnings"].append(f"Could not parse pyproject.toml: {e}")
    
    # Check for README.md
    readme_path = os.path.join(project_path, "README.md")
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                readme_content = f.read()
                # Extract first paragraph as description if not found in pyproject.toml
                if not analysis["suggested_metadata"].get("description"):
                    lines = readme_content.split("\n")
                    description_lines = []
                    for line in lines:
                        if line.strip() and not line.startswith("#"):
                            description_lines.append(line.strip())
                        elif description_lines:
                            break
                    if description_lines:
                        analysis["suggested_metadata"]["description"] = " ".join(description_lines[:3])
        except Exception as e:
            analysis["warnings"].append(f"Could not read README.md: {e}")
    
    # Check for LICENSE file
    license_files = ["LICENSE", "LICENSE.txt", "LICENSE.md"]
    for license_file in license_files:
        if os.path.exists(os.path.join(project_path, license_file)):
            analysis["suggested_metadata"]["has_license_file"] = True
            break
    
    # Generate recommendations
    if not analysis["suggested_metadata"].get("identifier"):
        analysis["recommendations"].append("Please provide a GitHub repository URL to automatically extract the identifier")
    
    if not analysis["suggested_metadata"].get("description"):
        analysis["recommendations"].append("Please provide a description of your MCP server")
    
    if not analysis["suggested_metadata"].get("has_license_file"):
        analysis["recommendations"].append("Consider adding a LICENSE file to your project")
    
    return analysis


def generate_yaml_template(metadata: dict[str, Any]) -> str:
    """
    Generate a YAML template based on provided metadata.
    
    Args:
        metadata: Dictionary containing metadata for the MCP server
        
    Returns:
        YAML string representing the registry submission
    """
    # Start with required fields
    yaml_data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication"
    }
    
    # Add identifier and @id
    if "identifier" in metadata:
        yaml_data["@id"] = f"https://github.com/{metadata['identifier']}"
        yaml_data["identifier"] = metadata["identifier"]
    
    # Add basic information
    if "name" in metadata:
        yaml_data["name"] = metadata["name"]
    
    if "description" in metadata:
        yaml_data["description"] = metadata["description"]
    
    if "codeRepository" in metadata:
        yaml_data["codeRepository"] = metadata["codeRepository"]
    
    if "url" in metadata:
        yaml_data["url"] = metadata["url"]
    
    # Add software help if provided
    if "softwareHelp" in metadata:
        yaml_data["softwareHelp"] = {
            "@type": "CreativeWork",
            "url": metadata["softwareHelp"]["url"],
            "name": metadata["softwareHelp"].get("name", "Documentation")
        }
    
    # Add maintainer information
    if "maintainer" in metadata:
        yaml_data["maintainer"] = []
        for maintainer in metadata["maintainer"]:
            maintainer_data = {
                "@type": maintainer.get("@type", "Person"),
                "name": maintainer["name"]
            }
            if "identifier" in maintainer:
                maintainer_data["identifier"] = maintainer["identifier"]
            if "url" in maintainer:
                maintainer_data["url"] = maintainer["url"]
            yaml_data["maintainer"].append(maintainer_data)
    
    # Add license
    if "license" in metadata:
        yaml_data["license"] = metadata["license"]
    
    # Add application category
    yaml_data["applicationCategory"] = metadata.get("applicationCategory", "HealthApplication")
    
    # Add keywords
    if "keywords" in metadata:
        yaml_data["keywords"] = metadata["keywords"]
    
    # Add operating system
    yaml_data["operatingSystem"] = metadata.get("operatingSystem", ["Cross-platform"])
    
    # Add programming language
    if "programmingLanguage" in metadata:
        yaml_data["programmingLanguage"] = metadata["programmingLanguage"]
    
    # Add feature list if provided
    if "featureList" in metadata:
        yaml_data["featureList"] = metadata["featureList"]
    
    return yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)


def validate_yaml_specification(yaml_content: str) -> dict[str, Any]:
    """
    Validate a YAML specification against the registry schema.
    
    Args:
        yaml_content: YAML content as string
        
    Returns:
        Dict containing validation results
    """
    try:
        from jsonschema import validate, ValidationError
    except ImportError:
        return {
            "valid": False,
            "errors": ["jsonschema package not available for validation"],
            "warnings": []
        }
    
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "suggestions": []
    }
    
    try:
        # Parse YAML
        yaml_data = yaml.safe_load(yaml_content)
        if not yaml_data:
            result["valid"] = False
            result["errors"].append("YAML content is empty or invalid")
            return result
        
        # Get schema
        schema = get_registry_schema()
        
        # Validate against schema
        validate(instance=yaml_data, schema=schema)
        
        # Additional custom validations
        # Check license format
        if "license" in yaml_data:
            license_url = yaml_data["license"]
            if not license_url.startswith("https://spdx.org/licenses/"):
                result["warnings"].append("License should use SPDX format (https://spdx.org/licenses/...)")
        
        # Check identifier format
        if "identifier" in yaml_data:
            identifier = yaml_data["identifier"]
            if not re.match(r"^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$", identifier):
                result["errors"].append("Identifier must be in format 'owner/repository'")
                result["valid"] = False
        
        # Check repository URL format
        if "codeRepository" in yaml_data:
            repo_url = yaml_data["codeRepository"]
            if not re.match(r"^https://(github\.com|gitlab\.com|bitbucket\.org|codeberg\.com)(/[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+|/record/[0-9]+)(/.*)?$", repo_url):
                result["warnings"].append("Repository URL should be from a supported platform (GitHub, GitLab, Bitbucket, Codeberg)")
        
        # Suggest improvements
        if not yaml_data.get("url"):
            result["suggestions"].append("Consider adding a 'url' field if your MCP server is remotely hosted")
        
        if not yaml_data.get("softwareHelp"):
            result["suggestions"].append("Consider adding 'softwareHelp' with documentation URL")
        
        if not yaml_data.get("featureList"):
            result["suggestions"].append("Consider adding 'featureList' to describe your MCP server's capabilities")
        
    except yaml.YAMLError as e:
        result["valid"] = False
        result["errors"].append(f"YAML parsing error: {e}")
    except ValidationError as e:
        result["valid"] = False
        result["errors"].append(f"Schema validation error: {e.message}")
        if e.path:
            result["errors"].append(f"  at path: {'/'.join(str(p) for p in e.path)}")
    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"Unexpected error: {e}")
    
    return result


def submit_to_registry(yaml_content: str, api_endpoint: str = "https://api.biocontext.ai/registry/submit") -> dict[str, Any]:
    """
    Submit a YAML specification to the registry API.
    
    Args:
        yaml_content: YAML content as string
        api_endpoint: Registry API endpoint URL
        
    Returns:
        Dict containing submission results
    """
    result = {
        "success": False,
        "message": "",
        "submission_id": None,
        "errors": []
    }
    
    try:
        # First validate the YAML
        validation_result = validate_yaml_specification(yaml_content)
        if not validation_result["valid"]:
            result["errors"] = validation_result["errors"]
            result["message"] = "Validation failed before submission"
            return result
        
        # Prepare submission data
        yaml_data = yaml.safe_load(yaml_content)
        
        # Submit to API
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.post(
            api_endpoint,
            json=yaml_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200 or response.status_code == 201:
            result["success"] = True
            result["message"] = "Successfully submitted to registry"
            try:
                response_data = response.json()
                result["submission_id"] = response_data.get("id")
            except:
                pass
        else:
            result["message"] = f"API request failed with status {response.status_code}"
            try:
                error_data = response.json()
                result["errors"].append(error_data.get("message", "Unknown error"))
            except:
                result["errors"].append(response.text)
    
    except requests.exceptions.RequestException as e:
        result["errors"].append(f"Network error: {e}")
        result["message"] = "Failed to connect to registry API"
    except Exception as e:
        result["errors"].append(f"Unexpected error: {e}")
        result["message"] = "Submission failed due to unexpected error"
    
    return result


# Register tools with MCP
@mcp.tool
def analyze_project_directory_tool(project_path: str = ".") -> dict[str, Any]:
    """
    Analyze the current project directory to extract metadata for registry submission.
    
    This tool examines common project files (pyproject.toml, README.md, etc.) to
    automatically extract metadata that can be used for registry submission.
    
    Args:
        project_path: Path to the project directory (defaults to current directory)
        
    Returns:
        Dict containing extracted project metadata, detected files, and recommendations
    """
    return analyze_project_directory(project_path)


@mcp.tool
def generate_yaml_template_tool(metadata: dict[str, Any]) -> str:
    """
    Generate a YAML template based on provided metadata.
    
    This tool creates a schema.org-compatible YAML specification that can be
    submitted to the BioContextAI registry.
    
    Args:
        metadata: Dictionary containing metadata for the MCP server
        
    Returns:
        YAML string representing the registry submission
    """
    return generate_yaml_template(metadata)


@mcp.tool
def validate_yaml_specification_tool(yaml_content: str) -> dict[str, Any]:
    """
    Validate a YAML specification against the registry schema.
    
    This tool checks if a YAML specification conforms to the BioContextAI
    registry schema and provides detailed feedback on any issues.
    
    Args:
        yaml_content: YAML content as string
        
    Returns:
        Dict containing validation results, errors, warnings, and suggestions
    """
    return validate_yaml_specification(yaml_content)


@mcp.tool
def submit_to_registry_tool(yaml_content: str, api_endpoint: str = "https://api.biocontext.ai/registry/submit") -> dict[str, Any]:
    """
    Submit a YAML specification to the registry API.
    
    This tool validates and submits a YAML specification to the BioContextAI
    registry API for processing and storage.
    
    Args:
        yaml_content: YAML content as string
        api_endpoint: Registry API endpoint URL (optional, defaults to BioContextAI API)
        
    Returns:
        Dict containing submission results and any errors encountered
    """
    return submit_to_registry(yaml_content, api_endpoint)


@mcp.tool
def get_registry_schema_tool() -> dict[str, Any]:
    """
    Get the registry schema definition for validation.
    
    This tool returns the complete JSON schema used by the BioContextAI
    registry for validating submissions.
    
    Returns:
        Dict containing the JSON schema for registry submissions
    """
    return get_registry_schema()
