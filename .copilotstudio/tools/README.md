---
last_edited: 2026-06-15
---

# Vault Tools (MCP Server)

Several Topics in `.copilotstudio/topics/` (`new-person`, `new-project`, `gh-address-comments`, `gh-fix-ci`, `onboarding`) shell out to Python scripts to actually write files or call `gh`. Copilot Studio agents don't run local processes on their own, so `mcp_server.py` wraps those scripts as MCP tools you register as a Copilot Studio Tool.

## Local test

```sh
pip install -r requirements.txt
python mcp_server.py
# serves http://127.0.0.1:8000/mcp
```

This serves over **Streamable HTTP** (not stdio) at `/mcp`, because that's the only transport Copilot Studio's MCP integration supports — it dropped SSE after August 2025, and it always connects to a Server URL rather than spawning a local process. Point any MCP-compatible HTTP client at `http://127.0.0.1:8000/mcp` to smoke-test before deploying.

## Deploying

Copilot Studio needs an **HTTPS** URL it can reach from the internet — `127.0.0.1` only works for your own local testing. Host this on infrastructure your organization already uses for internal services (an Azure Container App, App Service, or similar), put TLS in front of it (a reverse proxy or the platform's built-in HTTPS), and set `MCP_HOST=0.0.0.0` plus whatever `MCP_PORT` that platform expects. Clone or mount this vault repo onto that host so the scripts and the `people/`, `projects/`, `templates/` folders they read/write are all present at the same relative paths `mcp_server.py` expects.

## Registering in Copilot Studio

This is the **MCP onboarding wizard**, Microsoft's recommended path (confirmed against the current [Copilot Studio MCP docs](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent) — MCP reached general availability in Copilot Studio on July 15, 2026):

1. Open your agent, go to the **Tools** page.
2. Select **Add a tool** > **New tool** > **Model Context Protocol**.
3. Fill in the wizard: **Server name**, **Server description** (the agent's orchestrator uses this to decide when to call the server — be specific, e.g. "Vault helper scripts: create person/project notes, fetch PR comments, inspect failing CI checks"), and **Server URL** (your deployed `https://.../mcp` endpoint).
4. Choose authentication: **None** if you're not putting anything in front of the server, or **API key** / **OAuth 2.0** if you added one (recommended for anything beyond a quick test, since this server can write files and shell out to `gh`).
5. Select **Create**. In the **Add tool** dialog, choose **Create a new connection** (or reuse an existing one), then **Add to agent**.
6. Copilot Studio discovers the tools (`new_person`, `new_project`, `fetch_pr_comments`, `inspect_pr_checks`, `setup_shared_memory_vault`, `new_person_note`, `new_project_note`) from the server automatically and adds each as an action inheriting its name/description/inputs/outputs — no manual mapping needed.
7. Reference the relevant tools from each Topic that needs them (see each `TOPIC.md`'s Platform Notes section for which one it expects), or let generative orchestration pick them up automatically from their descriptions.

Alternative: **Tools > Add a tool > New tool > Custom connector** lets you register the same server manually via an OpenAPI schema with `x-ms-agentic-protocol: mcp-streamable-1.0` on the path — useful if your organization already manages connectors through Power Apps rather than the wizard.

## Why not just re-implement these as Power Automate flows?

You can — Power Automate flows are Copilot Studio's other native tool type and are a reasonable alternative if your team already standardizes on them. MCP was chosen here because it lets these scripts run unmodified instead of being rewritten as flow steps.

## `gh` authentication

`fetch_pr_comments` and `inspect_pr_checks` shell out to `gh`. Wherever you deploy this server, `gh auth login` must already be set up for the identity that should read/act on your repos — treat that credential with the same care as any other service credential, not as something Copilot Studio itself manages.
