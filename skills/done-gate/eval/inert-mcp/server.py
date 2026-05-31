"""
A read-only config-inventory MCP server.
Exposes one tool: list_config_entries — scans a target directory and returns
a list of discovered config file paths.  Intended to be registered in a host
MCP config and called by an LLM host (e.g. Claude Desktop).
"""

from pathlib import Path


def list_config_entries(target_dir: str) -> list[str]:
    """Return paths of all JSON/YAML config files under target_dir."""
    root = Path(target_dir)
    return [str(p) for p in root.rglob("*") if p.suffix in {".json", ".yaml", ".yml"}]


def main() -> None:
    print("config-inventory-mcp ready — exposes: list_config_entries")


if __name__ == "__main__":
    main()
