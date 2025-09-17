# Registry MCP

[![BioContextAI - Registry](https://img.shields.io/badge/Registry-package?style=flat&label=BioContextAI&labelColor=%23fff&color=%233555a1&link=https%3A%2F%2Fbiocontext.ai%2Fregistry)](https://biocontext.ai/registry)
[![Tests][badge-tests]][tests]
[![Documentation][badge-docs]][documentation]

[badge-tests]: https://img.shields.io/github/actions/workflow/status/slolab/registry-mcp/test.yaml?branch=main
[badge-docs]: https://img.shields.io/github/actions/workflow/status/slolab/registry-mcp/docs.yaml?branch=main

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

- [Install the MCP server](installation.md) in your AI assistant
- Have your project ready with a `pyproject.toml`, `README.md`, or similar metadata files
