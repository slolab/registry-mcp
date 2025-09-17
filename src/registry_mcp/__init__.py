from importlib.metadata import version

from registry_mcp.main import run_app
from registry_mcp.mcp import mcp

__version__ = version("registry_mcp")

__all__ = [
    "mcp",
    "run_app",
    "__version__"
]


if __name__ == "__main__":
    run_app()
