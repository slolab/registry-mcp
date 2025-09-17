"""
Registry guidance and troubleshooting tools.

This module provides guidance, examples, and troubleshooting assistance
for users submitting to the BioContextAI registry.
"""

from typing import Any
from registry_mcp.mcp import mcp


def get_registry_workflow_guidance() -> dict[str, Any]:
    """
    Get comprehensive guidance on the registry submission workflow.
    
    Returns:
        Dict containing step-by-step workflow guidance
    """
    return {
        "workflow_overview": {
            "name": "BioContextAI Registry Submission Workflow",
            "description": "Complete workflow for submitting MCP servers and other components to the BioContextAI registry",
            "estimated_time": "10-30 minutes",
            "prerequisites": [
                "MCP server or component ready for submission",
                "GitHub repository with your component",
                "Basic understanding of your component's functionality"
            ]
        },
        "workflow_steps": [
            {
                "step": 1,
                "name": "Project Analysis",
                "description": "Analyze your project directory to extract existing metadata",
                "tool": "analyze_project_directory_tool",
                "activities": [
                    "Run project analysis to detect existing metadata",
                    "Review detected files and suggested metadata",
                    "Note any warnings or recommendations"
                ],
                "outputs": [
                    "Project metadata analysis",
                    "Detected configuration files",
                    "Suggested metadata fields"
                ]
            },
            {
                "step": 2,
                "name": "Metadata Collection",
                "description": "Collect and prepare all required metadata for submission",
                "activities": [
                    "Review required fields from schema",
                    "Gather missing information",
                    "Prepare maintainer information",
                    "Select appropriate keywords and categories"
                ],
                "required_fields": [
                    "name", "description", "codeRepository", "maintainer",
                    "license", "applicationCategory", "keywords", "programmingLanguage"
                ],
                "optional_fields": [
                    "url", "softwareHelp", "featureList", "operatingSystem"
                ]
            },
            {
                "step": 3,
                "name": "YAML Generation",
                "description": "Generate schema.org-compatible YAML specification",
                "tool": "generate_yaml_template_tool",
                "activities": [
                    "Prepare metadata dictionary",
                    "Generate YAML template",
                    "Review generated YAML content"
                ],
                "outputs": [
                    "Complete YAML specification",
                    "Schema.org-compatible metadata"
                ]
            },
            {
                "step": 4,
                "name": "Validation",
                "description": "Validate YAML specification against registry schema",
                "tool": "validate_yaml_specification_tool",
                "activities": [
                    "Run schema validation",
                    "Review validation results",
                    "Fix any errors or warnings",
                    "Address suggestions for improvement"
                ],
                "outputs": [
                    "Validation report",
                    "Error and warning details",
                    "Improvement suggestions"
                ]
            },
            {
                "step": 5,
                "name": "Submission",
                "description": "Submit validated specification to registry API",
                "tool": "submit_to_registry_tool",
                "activities": [
                    "Submit YAML to registry API",
                    "Review submission results",
                    "Handle any submission errors"
                ],
                "outputs": [
                    "Submission confirmation",
                    "Registry entry creation",
                    "GitHub storage of YAML file"
                ]
            }
        ],
        "best_practices": [
            "Use descriptive names that clearly indicate the MCP server's purpose",
            "Write comprehensive descriptions that explain functionality and use cases",
            "Include relevant keywords to improve discoverability",
            "Provide clear documentation URLs in softwareHelp",
            "Use SPDX license identifiers for proper licensing",
            "Test your MCP server before submission",
            "Keep metadata up-to-date with your project"
        ],
        "common_issues": [
            {
                "issue": "Invalid identifier format",
                "solution": "Use format 'owner/repository' (e.g., 'biocypher/biocypher-mcp')",
                "example": "biocypher/biocypher-mcp"
            },
            {
                "issue": "Missing required fields",
                "solution": "Ensure all required fields are present and properly formatted",
                "required": ["@context", "@type", "@id", "identifier", "name", "description", "codeRepository", "maintainer", "license", "applicationCategory", "keywords", "programmingLanguage"]
            },
            {
                "issue": "Invalid license format",
                "solution": "Use SPDX license format: https://spdx.org/licenses/MIT.html",
                "example": "https://spdx.org/licenses/MIT.html"
            },
            {
                "issue": "Repository URL not supported",
                "solution": "Use GitHub, GitLab, Bitbucket, or Codeberg URLs",
                "supported": ["github.com", "gitlab.com", "bitbucket.org", "codeberg.com"]
            }
        ]
    }


def get_example_submissions() -> dict[str, Any]:
    """
    Get example YAML submissions for different types of components.
    
    Returns:
        Dict containing example submissions for various component types
    """
    return {
        "mcp_server_example": {
            "name": "BioCypher Knowledge Graph MCP",
            "description": "MCP server for BioCypher workflows and adapter creation",
            "yaml_content": '''"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/biocypher/biocypher-mcp

identifier: biocypher/biocypher-mcp

name: BioCypher Knowledge Graph MCP

description: >
  Knowledge curation, grounding, and harmonisation are complex processes. The BioCypher ecosystem (https://biocypher.org) supports the deterministic mapping of diverse inputs to harmonised graphs. To further simplify the creation and maintenance of BioCypher pipelines, we provide an MCP server with implementation guidelines and structured documentation for LLM co-programmers.

codeRepository: https://github.com/biocypher/biocypher-mcp

url: https://mcp.biocypher.org

softwareHelp:
  "@type": CreativeWork
  url: https://biocypher.org/BioCypher/llms/
  name: BioCypher LLM Documentation

maintainer:
  - "@type": Organization
    name: BioCypher
    identifier: "GitHub: biocypher"
    url: https://github.com/biocypher

license: https://spdx.org/licenses/MIT.html

applicationCategory: DeveloperApplication

keywords:
  - BioCypher
  - BioChatter
  - Knowledge Graph
  - Harmonisation
  - Adapter Design

operatingSystem:
  - Cross-platform

programmingLanguage:
  - Python

featureList:
  - Pipeline Setup
  - Pipeline Planning
  - Semantic Definition
  - Adapter Design
  - Adapter Implementation'''
        },
        "biomedical_tool_example": {
            "name": "PubMed Search MCP",
            "description": "MCP server for searching and retrieving biomedical literature from PubMed",
            "yaml_content": '''"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/example/pubmed-mcp

identifier: example/pubmed-mcp

name: PubMed Search MCP

description: >
  A Model Context Protocol server that provides access to PubMed database for searching and retrieving biomedical literature. Supports advanced search queries, article metadata extraction, and citation management.

codeRepository: https://github.com/example/pubmed-mcp

softwareHelp:
  "@type": CreativeWork
  url: https://github.com/example/pubmed-mcp/blob/main/README.md
  name: PubMed MCP Documentation

maintainer:
  - "@type": Person
    name: Jane Doe
    identifier: "GitHub: janedoe"
    url: https://github.com/janedoe

license: https://spdx.org/licenses/Apache-2.0.html

applicationCategory: HealthApplication

keywords:
  - PubMed
  - Biomedical Literature
  - Search
  - Citations
  - Research

operatingSystem:
  - Cross-platform

programmingLanguage:
  - Python

featureList:
  - PubMed Search
  - Article Retrieval
  - Citation Management
  - Metadata Extraction'''
        },
        "data_analysis_tool_example": {
            "name": "Genomics Analysis MCP",
            "description": "MCP server for genomic data analysis and visualization",
            "yaml_content": '''"@context": https://schema.org
"@type": SoftwareApplication
"@id": https://github.com/genomics/genomics-mcp

identifier: genomics/genomics-mcp

name: Genomics Analysis MCP

description: >
  A comprehensive MCP server for genomic data analysis, providing tools for sequence analysis, variant calling, and genomic visualization. Integrates with popular genomics databases and analysis pipelines.

codeRepository: https://github.com/genomics/genomics-mcp

url: https://genomics-mcp.example.com

softwareHelp:
  "@type": CreativeWork
  url: https://genomics-mcp.example.com/docs
  name: Genomics MCP Documentation

maintainer:
  - "@type": Organization
    name: Genomics Research Lab
    identifier: "GitHub: genomics-lab"
    url: https://github.com/genomics-lab

license: https://spdx.org/licenses/GPL-3.0.html

applicationCategory: HealthApplication

keywords:
  - Genomics
  - Sequence Analysis
  - Variant Calling
  - Bioinformatics
  - Data Visualization

operatingSystem:
  - Linux
  - macOS

programmingLanguage:
  - Python
  - R

featureList:
  - Sequence Analysis
  - Variant Calling
  - Genomic Visualization
  - Database Integration
  - Pipeline Management'''
        }
    }


def get_troubleshooting_guide() -> dict[str, Any]:
    """
    Get comprehensive troubleshooting guide for registry submissions.
    
    Returns:
        Dict containing troubleshooting information and solutions
    """
    return {
        "troubleshooting_overview": {
            "name": "Registry Submission Troubleshooting Guide",
            "description": "Common issues and solutions for BioContextAI registry submissions"
        },
        "validation_errors": {
            "invalid_identifier": {
                "error": "Identifier must be in format 'owner/repository'",
                "causes": [
                    "Missing owner/repository format",
                    "Invalid characters in identifier",
                    "Empty identifier field"
                ],
                "solutions": [
                    "Use format: 'your-username/your-repo-name'",
                    "Ensure only alphanumeric characters, hyphens, and underscores",
                    "Check that both owner and repository name are present"
                ],
                "example_fix": {
                    "wrong": "my-awesome-mcp",
                    "correct": "johndoe/my-awesome-mcp"
                }
            },
            "missing_required_fields": {
                "error": "Missing required fields",
                "causes": [
                    "Incomplete metadata dictionary",
                    "Missing schema.org required fields",
                    "Empty or null values for required fields"
                ],
                "solutions": [
                    "Check all required fields are present",
                    "Ensure no required fields are empty",
                    "Use the schema validation tool to identify missing fields"
                ],
                "required_fields": [
                    "@context", "@type", "@id", "identifier", "name",
                    "description", "codeRepository", "maintainer", "license",
                    "applicationCategory", "keywords", "programmingLanguage"
                ]
            },
            "invalid_license_format": {
                "error": "License should use SPDX format",
                "causes": [
                    "Using custom license text",
                    "Missing SPDX URL format",
                    "Invalid license URL"
                ],
                "solutions": [
                    "Use SPDX format: https://spdx.org/licenses/LICENSE-NAME.html",
                    "Find your license at https://spdx.org/licenses/",
                    "Common licenses: MIT, Apache-2.0, GPL-3.0, BSD-3-Clause"
                ],
                "examples": {
                    "MIT": "https://spdx.org/licenses/MIT.html",
                    "Apache": "https://spdx.org/licenses/Apache-2.0.html",
                    "GPL": "https://spdx.org/licenses/GPL-3.0.html"
                }
            },
            "invalid_repository_url": {
                "error": "Repository URL not supported",
                "causes": [
                    "Using unsupported repository platform",
                    "Invalid URL format",
                    "Missing repository path"
                ],
                "solutions": [
                    "Use supported platforms: GitHub, GitLab, Bitbucket, Codeberg",
                    "Ensure URL includes full repository path",
                    "Use HTTPS URLs"
                ],
                "supported_platforms": [
                    "https://github.com/owner/repo",
                    "https://gitlab.com/owner/repo",
                    "https://bitbucket.org/owner/repo",
                    "https://codeberg.org/owner/repo"
                ]
            }
        },
        "submission_errors": {
            "api_connection_failed": {
                "error": "Failed to connect to registry API",
                "causes": [
                    "Network connectivity issues",
                    "Invalid API endpoint",
                    "API server unavailable"
                ],
                "solutions": [
                    "Check internet connection",
                    "Verify API endpoint URL",
                    "Try again later if server is down",
                    "Check for API rate limiting"
                ]
            },
            "authentication_failed": {
                "error": "Authentication failed",
                "causes": [
                    "Missing or invalid API key",
                    "Insufficient permissions",
                    "Expired credentials"
                ],
                "solutions": [
                    "Check API key configuration",
                    "Verify account permissions",
                    "Refresh authentication credentials"
                ]
            },
            "duplicate_submission": {
                "error": "Component already exists in registry",
                "causes": [
                    "Identifier already registered",
                    "Repository URL already used",
                    "Previous submission not removed"
                ],
                "solutions": [
                    "Use unique identifier",
                    "Check existing registry entries",
                    "Contact registry administrators if needed"
                ]
            }
        },
        "common_warnings": {
            "missing_optional_fields": {
                "warning": "Consider adding optional fields for better discoverability",
                "fields": ["url", "softwareHelp", "featureList"],
                "benefits": [
                    "Improved searchability",
                    "Better user experience",
                    "More complete metadata"
                ]
            },
            "generic_keywords": {
                "warning": "Keywords may be too generic",
                "suggestion": "Use specific, descriptive keywords",
                "examples": {
                    "generic": ["tool", "server", "api"],
                    "specific": ["bioinformatics", "genomics", "protein-analysis"]
                }
            },
            "short_description": {
                "warning": "Description may be too brief",
                "suggestion": "Provide detailed description of functionality",
                "minimum_length": "At least 10 characters",
                "recommended_length": "50-200 characters"
            }
        },
        "best_practices": {
            "metadata_quality": [
                "Use clear, descriptive names",
                "Write comprehensive descriptions",
                "Include relevant keywords",
                "Provide accurate maintainer information",
                "Use proper license identifiers"
            ],
            "testing": [
                "Test MCP server before submission",
                "Validate YAML locally before API submission",
                "Check all URLs are accessible",
                "Verify repository is public and accessible"
            ],
            "documentation": [
                "Include clear README.md",
                "Provide usage examples",
                "Document installation requirements",
                "Include troubleshooting information"
            ]
        }
    }


def get_field_guidance(field_name: str) -> dict[str, Any]:
    """
    Get detailed guidance for a specific registry field.
    
    Args:
        field_name: Name of the field to get guidance for
        
    Returns:
        Dict containing detailed field guidance
    """
    field_guidance = {
        "name": {
            "description": "The name of your MCP server or component",
            "requirements": [
                "Must be 1-100 characters long",
                "Should be descriptive and clear",
                "Avoid generic names like 'MCP Server'"
            ],
            "examples": [
                "BioCypher Knowledge Graph MCP",
                "PubMed Search MCP",
                "Genomics Analysis MCP"
            ],
            "tips": [
                "Include the type of component (MCP, Server, etc.)",
                "Be specific about the domain or functionality",
                "Make it searchable and memorable"
            ]
        },
        "description": {
            "description": "A detailed description of your component's functionality",
            "requirements": [
                "Must be 10-1000 characters long",
                "Should explain what the component does",
                "Include use cases and target audience"
            ],
            "examples": [
                "Knowledge curation, grounding, and harmonisation are complex processes. The BioCypher ecosystem supports the deterministic mapping of diverse inputs to harmonised graphs.",
                "A Model Context Protocol server that provides access to PubMed database for searching and retrieving biomedical literature."
            ],
            "tips": [
                "Start with the main purpose",
                "Explain key features and capabilities",
                "Mention target users or use cases",
                "Include relevant URLs or references"
            ]
        },
        "identifier": {
            "description": "Unique identifier in format 'owner/repository'",
            "requirements": [
                "Must match pattern: ^[a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+$",
                "Should match your GitHub repository",
                "Must be unique across the registry"
            ],
            "examples": [
                "biocypher/biocypher-mcp",
                "johndoe/pubmed-mcp",
                "genomics-lab/analysis-tools"
            ],
            "tips": [
                "Use your GitHub username as owner",
                "Use repository name exactly as it appears on GitHub",
                "Avoid special characters except hyphens and underscores"
            ]
        },
        "codeRepository": {
            "description": "URL of the source code repository",
            "requirements": [
                "Must be a valid HTTPS URL",
                "Must be from supported platform",
                "Should point to the main repository"
            ],
            "supported_platforms": [
                "GitHub (github.com)",
                "GitLab (gitlab.com)",
                "Bitbucket (bitbucket.org)",
                "Codeberg (codeberg.com)"
            ],
            "examples": [
                "https://github.com/biocypher/biocypher-mcp",
                "https://gitlab.com/example/my-mcp",
                "https://bitbucket.org/team/project"
            ],
            "tips": [
                "Use HTTPS URLs",
                "Point to the main repository page",
                "Ensure repository is public and accessible"
            ]
        },
        "maintainer": {
            "description": "Information about the maintainer(s) of the component",
            "requirements": [
                "Must include @type (Person or Organization)",
                "Must include name",
                "Can include identifier and url"
            ],
            "types": {
                "Person": {
                    "description": "Individual maintainer",
                    "example": {
                        "@type": "Person",
                        "name": "Jane Doe",
                        "identifier": "GitHub: janedoe",
                        "url": "https://github.com/janedoe"
                    }
                },
                "Organization": {
                    "description": "Organization maintainer",
                    "example": {
                        "@type": "Organization",
                        "name": "BioCypher",
                        "identifier": "GitHub: biocypher",
                        "url": "https://github.com/biocypher"
                    }
                }
            },
            "tips": [
                "Use GitHub username as identifier",
                "Include GitHub profile URL",
                "For organizations, use organization name and GitHub"
            ]
        },
        "license": {
            "description": "License information using SPDX format",
            "requirements": [
                "Must use SPDX format: https://spdx.org/licenses/LICENSE.html",
                "Must be OSI-approved license",
                "Should match your repository license"
            ],
            "common_licenses": {
                "MIT": "https://spdx.org/licenses/MIT.html",
                "Apache-2.0": "https://spdx.org/licenses/Apache-2.0.html",
                "GPL-3.0": "https://spdx.org/licenses/GPL-3.0.html",
                "BSD-3-Clause": "https://spdx.org/licenses/BSD-3-Clause.html"
            },
            "tips": [
                "Check your repository's LICENSE file",
                "Use the exact SPDX identifier",
                "Ensure license is OSI-approved"
            ]
        },
        "keywords": {
            "description": "Keywords or tags for discoverability",
            "requirements": [
                "Must be 1-10 keywords",
                "Each keyword 2-30 characters",
                "Must be unique",
                "Should be relevant to your component"
            ],
            "examples": [
                ["BioCypher", "Knowledge Graph", "Harmonisation", "Adapter Design"],
                ["PubMed", "Biomedical Literature", "Search", "Citations"],
                ["Genomics", "Sequence Analysis", "Bioinformatics", "Data Visualization"]
            ],
            "tips": [
                "Use specific, descriptive terms",
                "Include domain-specific terminology",
                "Avoid overly generic terms",
                "Consider what users would search for"
            ]
        },
        "applicationCategory": {
            "description": "Type of software application",
            "options": [
                "HealthApplication",
                "EducationApplication", 
                "ReferenceApplication",
                "DeveloperApplication",
                "UtilitiesApplication"
            ],
            "default": "HealthApplication",
            "guidance": {
                "HealthApplication": "For biomedical, healthcare, or life sciences tools",
                "EducationApplication": "For educational or training tools",
                "ReferenceApplication": "For reference or lookup tools",
                "DeveloperApplication": "For development tools and frameworks",
                "UtilitiesApplication": "For general utility tools"
            }
        },
        "programmingLanguage": {
            "description": "Programming languages used in the component",
            "supported_languages": [
                "Python", "TypeScript", "JavaScript", "R", "Julia",
                "Java", "Go", "Rust", "C#", "C++", "Other"
            ],
            "tips": [
                "List all languages used",
                "Include primary language first",
                "Use 'Other' for unsupported languages"
            ]
        }
    }
    
    if field_name in field_guidance:
        return field_guidance[field_name]
    else:
        return {
            "error": f"Field '{field_name}' not found",
            "available_fields": list(field_guidance.keys())
        }


# Register tools with MCP
@mcp.tool
def get_registry_workflow_guidance_tool() -> dict[str, Any]:
    """
    Get comprehensive guidance on the registry submission workflow.
    
    This tool provides step-by-step guidance for submitting components
    to the BioContextAI registry, including best practices and common issues.
    
    Returns:
        Dict containing complete workflow guidance
    """
    return get_registry_workflow_guidance()


@mcp.tool
def get_example_submissions_tool() -> dict[str, Any]:
    """
    Get example YAML submissions for different types of components.
    
    This tool provides example YAML specifications for various types of
    components to help users understand the expected format and content.
    
    Returns:
        Dict containing example submissions for different component types
    """
    return get_example_submissions()


@mcp.tool
def get_troubleshooting_guide_tool() -> dict[str, Any]:
    """
    Get comprehensive troubleshooting guide for registry submissions.
    
    This tool provides detailed troubleshooting information for common
    issues encountered during registry submission, including validation
    errors, submission errors, and best practices.
    
    Returns:
        Dict containing troubleshooting information and solutions
    """
    return get_troubleshooting_guide()


@mcp.tool
def get_field_guidance_tool(field_name: str) -> dict[str, Any]:
    """
    Get detailed guidance for a specific registry field.
    
    This tool provides detailed information about specific fields in the
    registry schema, including requirements, examples, and best practices.
    
    Args:
        field_name: Name of the field to get guidance for
        
    Returns:
        Dict containing detailed field guidance
    """
    return get_field_guidance(field_name)
