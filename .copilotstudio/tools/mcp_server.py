#!/usr/bin/env python3
"""MCP server exposing this vault's bundled Python scripts as tools.

Copilot Studio has no built-in shell/filesystem action, but it can call an
MCP server registered as a Tool (agent's Tools page > Add a tool > New tool
> Model Context Protocol). This server is the bridge: it runs the existing
new_person.py / new_project.py / fetch_comments.py / inspect_pr_checks.py
scripts as subprocesses and returns their output, so the Topics in
.copilotstudio/topics/ that reference those scripts can actually execute
when this agent calls them as a Tool.

Copilot Studio's MCP onboarding wizard only supports the Streamable HTTP
transport (it dropped SSE support after August 2025) and connects to a
Server URL, not a local stdio process — so this runs over streamable-http,
not the FastMCP default. Run it locally for testing:

    python mcp_server.py
    # serves http://127.0.0.1:8000/mcp

Deploy wherever your organization runs services reachable over HTTPS from
Copilot Studio (an Azure Container App, App Service, or similar), put a
reverse proxy/TLS in front of it, and register that HTTPS URL + /mcp path
as the Server URL in the MCP onboarding wizard. See README.md in this
folder for the exact registration steps.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

VAULT_ROOT = Path(__file__).resolve().parents[2]
TOPICS = VAULT_ROOT / ".copilotstudio" / "topics"

mcp = FastMCP(
    "vault-tools",
    host=os.environ.get("MCP_HOST", "127.0.0.1"),
    # Most free hosting platforms (Render, Railway, etc.) inject the port to
    # bind to as $PORT rather than a custom name; MCP_PORT wins if you set it.
    port=int(os.environ.get("MCP_PORT", os.environ.get("PORT", "8000"))),
    streamable_http_path="/mcp",
)


def _run(argv: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, *argv],
        cwd=VAULT_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    output = result.stdout.strip()
    if result.returncode != 0:
        error = result.stderr.strip() or f"exited with status {result.returncode}"
        return f"error: {error}\n{output}".strip()
    return output


@mcp.tool()
def new_person(name: str, role: str = "") -> str:
    """Create a public-safe people/<slug>.md note from the person.md template."""
    script = TOPICS / "new-person" / "scripts" / "new_person.py"
    argv = [str(script), name]
    if role:
        argv += ["--role", role]
    return _run(argv)


@mcp.tool()
def new_project(name: str, summary: str, project_type: str = "project") -> str:
    """Bootstrap a projects/<slug>/ or experiments/<slug>/ folder with README.md and AGENTS.md."""
    script = TOPICS / "new-project" / "scripts" / "new_project.py"
    argv = [str(script), name, "--summary", summary, "--type", project_type]
    return _run(argv)


@mcp.tool()
def fetch_pr_comments(repo_path: str = ".") -> str:
    """Fetch all comments, reviews, and review threads for the open PR on the current branch.

    Requires `gh auth login` to already be set up wherever this MCP server runs.
    """
    script = TOPICS / "gh-address-comments" / "scripts" / "fetch_comments.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=Path(repo_path).resolve(),
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        return f"error: {result.stderr.strip()}"
    return result.stdout


@mcp.tool()
def inspect_pr_checks(repo_path: str = ".", pr: str = "", as_json: bool = True) -> str:
    """Inspect failing GitHub Actions checks on a PR and pull a failure log snippet."""
    script = TOPICS / "gh-fix-ci" / "scripts" / "inspect_pr_checks.py"
    argv = [str(script), "--repo", repo_path]
    if pr:
        argv += ["--pr", pr]
    if as_json:
        argv += ["--json"]
    return _run(argv)


@mcp.tool()
def setup_shared_memory_vault(vault_dir: str = "", dry_run: bool = False) -> str:
    """Create the plain-file shared-memory vault scaffold (AGENTS.md, TODO.md, agent/, people/, projects/, notes/, sources/)."""
    script = TOPICS / "onboarding" / "scripts" / "setup_shared_memory_vault.py"
    argv = [str(script)]
    if vault_dir:
        argv += ["--vault-dir", vault_dir]
    if dry_run:
        argv += ["--dry-run"]
    return _run(argv)


@mcp.tool()
def new_person_note(name: str, key: str = "", dry_run: bool = False) -> str:
    """Create a richer person-note scaffold (used by onboarding, distinct from the plain new_person tool)."""
    script = TOPICS / "onboarding" / "scripts" / "new_person_note.py"
    argv = [str(script), "--name", name]
    if key:
        argv += ["--key", key]
    if dry_run:
        argv += ["--dry-run"]
    return _run(argv)


@mcp.tool()
def new_project_note(title: str, slug: str = "", dry_run: bool = False) -> str:
    """Create and index a project packet (used by onboarding, distinct from the plain new_project tool)."""
    script = TOPICS / "onboarding" / "scripts" / "new_project_note.py"
    argv = [str(script), "--title", title]
    if slug:
        argv += ["--slug", slug]
    if dry_run:
        argv += ["--dry-run"]
    return _run(argv)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
