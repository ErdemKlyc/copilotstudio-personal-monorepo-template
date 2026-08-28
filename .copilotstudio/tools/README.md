---
last_edited: 2026-06-15
---

# Vault Tools (MCP Server)

Several Topics in `.copilotstudio/topics/` (`new-person`, `new-project`, `gh-address-comments`, `gh-fix-ci`, `onboarding`) shell out to Python scripts to actually write files or call `gh`. Copilot Studio agents don't run local processes on their own, so `mcp_server.py` wraps those scripts as MCP tools you register as a Copilot Studio Action.

## Local test

```sh
pip install -r requirements.txt
python mcp_server.py
```

This runs the server over stdio so you can smoke-test it with any MCP-compatible client before deploying it anywhere.

## Deploying

Copilot Studio's MCP Action needs an HTTPS endpoint it can reach — running this script over stdio on your laptop is only good for local testing. Host it on infrastructure your organization already uses for internal services (an Azure Container App, App Service, Azure Function with an HTTP-triggered MCP adapter, or any other reachable host), with the same working directory layout as this repo so the relative script paths in `mcp_server.py` resolve correctly. Mount or clone this vault repo onto that host so the scripts and the `people/`, `projects/`, `templates/` folders they write to are all present.

## Registering in Copilot Studio

1. Agent > Actions > Add an action > Add an MCP server (naming may vary by tenant/version).
2. Point it at your deployed server's URL.
3. Copilot Studio will discover the tools (`new_person`, `new_project`, `fetch_pr_comments`, `inspect_pr_checks`, `setup_shared_memory_vault`, `new_person_note`, `new_project_note`) and let you enable them per-Topic.
4. Enable the relevant tools on each Topic that needs them (see each `TOPIC.md`'s Platform Notes section for which Action it expects).

## Why not just re-implement these as Power Automate flows?

You can — Power Automate flows are Copilot Studio's other native Action type and are a reasonable alternative if your team already standardizes on them. MCP was chosen here because it lets these scripts run unmodified instead of being rewritten as flow steps, and because Copilot Studio's 2025 MCP support makes this the more direct port of "a CLI agent that can run local scripts."

## `gh` authentication

`fetch_pr_comments` and `inspect_pr_checks` shell out to `gh`. Wherever you deploy this server, `gh auth login` must already be set up for the identity that should read/act on your repos — treat that credential with the same care as any other service credential, not as something Copilot Studio itself manages.
