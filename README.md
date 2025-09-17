# registry-mcp

[![BioContextAI - Registry](https://img.shields.io/badge/Registry-package?style=flat&label=BioContextAI&labelColor=%23fff&color=%233555a1&link=https%3A%2F%2Fbiocontext.ai%2Fregistry)](https://biocontext.ai/registry)
[![Tests][badge-tests]][tests]
[![Documentation][badge-docs]][documentation]

[badge-tests]: https://img.shields.io/github/actions/workflow/status/slolab/registry-mcp/test.yaml?branch=main
[badge-docs]: https://img.shields.io/readthedocs/registry-mcp

MCP server for supporting registry submissions

## Getting started

Please refer to the [documentation][],
in particular, the [API documentation][].

You can also find the project on [BioContextAI](https://biocontext.ai), the community-hub for biomedical MCP servers: [registry-mcp on BioContextAI](https://biocontext.ai/registry/slolab/registry-mcp).

## Installation

You need to have Python 3.10 or newer installed on your system.
If you don't have Python installed, we recommend installing [uv][].

There are several alternative options to install registry-mcp:

1. Use `uvx` to run it immediately:

```bash
uvx registry_mcp
```

2. Include it in one of various clients that supports the `mcp.json` standard, please use:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "uvx",
      "args": ["registry_mcp"],
      "env": {
        "UV_PYTHON": "3.12" // or required version
      }
    }
  }
}
```

3. Install it through `pip`:

```bash
pip install --user registry_mcp
```

4. Install the latest development version:

```bash
pip install git+https://github.com/slolab/registry-mcp.git@main
```

## Contact

If you found a bug, please use the [issue tracker][].

## Citation

> t.b.a

[uv]: https://github.com/astral-sh/uv
[issue tracker]: https://github.com/slolab/registry-mcp/issues
[tests]: https://github.com/slolab/registry-mcp/actions/workflows/test.yaml
[documentation]: https://registry-mcp.readthedocs.io
[changelog]: https://registry-mcp.readthedocs.io/en/latest/changelog.html
[api documentation]: https://registry-mcp.readthedocs.io/en/latest/api.html
[pypi]: https://pypi.org/project/registry-mcp
