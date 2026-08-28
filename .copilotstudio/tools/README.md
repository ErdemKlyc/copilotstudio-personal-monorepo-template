---
last_edited: 2026-06-15
---

# Vault Write-Back: What's Available Varies By Tenant

Several Topics in `.copilotstudio/topics/` (`new-person`, `new-project`, `gh-address-comments`, `gh-fix-ci`) need to write files into the vault or read state from GitHub. Copilot Studio agents have no ambient file or shell access, so this needs to be wired up explicitly — and *how* depends entirely on what your tenant's Tools > Add a tool page actually offers. Check before picking one:

1. **Prebuilt Connector actions added directly as a Tool (no flow, no server)** — works even in the most locked-down enterprise tenants, where Flow, MCP, Custom connector, and REST API tool types are all disabled and only the Connector picker remains. This is the path `new-person`/`new-project` are built around by default: see `.copilotstudio/README.md` > "The create-vault-file / create-vault-folder Tools" for exact setup.
2. **Agent flow**, if your tenant allows it — built inside Copilot Studio via natural language, still no server to host. Equally valid for the same logic; see each topic's Platform Notes for the flow-description version if you'd rather use this than a bare connector action.
3. **This folder's `mcp_server.py`** — kept as an **optional** last resort for organizations that already have persistent, IT-approved hosting (an Azure Container App or App Service with a mounted, synced volume — not a free-tier or ephemeral host, which loses every write on restart) *and* a tenant where MCP tool registration is actually enabled. Read the rest of this file only if that's genuinely your situation and you'd rather reuse the bundled Python scripts than rebuild the logic as a Tool/flow.

## MCP server: local test

```sh
pip install -r requirements.txt
python mcp_server.py
# serves http://127.0.0.1:8000/mcp
```

Pinned to `mcp<2.0.0` — the package had a breaking API rename (FastMCP → MCPServer) after this was written; see the comment in `requirements.txt` before upgrading. This serves over **Streamable HTTP** (not stdio) at `/mcp`, because that's the only transport Copilot Studio's MCP integration supports — it dropped SSE after August 2025. Point any MCP-compatible HTTP client at `http://127.0.0.1:8000/mcp` to smoke-test.

A quick local tunnel (ngrok, cloudflared) can expose that for a one-off test, but treat it as throwaway: the URL isn't stable, your machine has to stay on, and some corporate antivirus/EDR software flags the ngrok binary itself as unwanted software (a known false positive) — don't try to work around your organization's security tooling to make this work; if it's blocked, that's a signal to use the Agent flow path instead, not to find a bypass.

## MCP server: deploying for real

This only makes sense with **persistent, non-ephemeral storage** mounted at the same path structure as this repo (so `people/`, `projects/`, `templates/` are present relative to `mcp_server.py`), and ideally a mechanism to sync that storage back to wherever your Knowledge source reads from (SharePoint, OneDrive) — otherwise writes the server makes are invisible to the agent's own Knowledge search. An Azure Container App or App Service with a mounted Azure Files share (itself synced to SharePoint via Azure File Sync, or simply the same OneDrive-synced folder if running on a domain-joined VM) is the realistic shape of this. Set `MCP_HOST=0.0.0.0` and either `MCP_PORT` or `PORT` (both are read) to whatever the platform expects.

## Registering the MCP server in Copilot Studio

This is the **MCP onboarding wizard** (confirmed against the current [Copilot Studio MCP docs](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent) — MCP reached general availability in Copilot Studio on July 15, 2026):

1. Open your agent, go to the **Tools** page.
2. Select **Add a tool** > **New tool** > **Model Context Protocol**.
3. Fill in the wizard: **Server name**, **Server description**, and **Server URL** (your deployed `https://.../mcp` endpoint).
4. Choose authentication: **API key** or **OAuth 2.0** (strongly recommended over **None**, since this server can write files and shell out to `gh`).
5. Select **Create**. In the **Add tool** dialog, choose **Create a new connection**, then **Add to agent**.
6. Copilot Studio discovers the tools (`new_person`, `new_project`, `fetch_pr_comments`, `inspect_pr_checks`, `setup_shared_memory_vault`, `new_person_note`, `new_project_note`) automatically.

## `gh` authentication

`fetch_pr_comments` and `inspect_pr_checks` shell out to `gh`. Wherever you deploy this server, `gh auth login` must already be set up for the identity that should read/act on your repos — treat that credential with the same care as any other service credential.
