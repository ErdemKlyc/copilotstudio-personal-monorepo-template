---
last_edited: 2026-06-15
---

# Agent Assets

This directory holds the Microsoft Copilot Studio configuration for this vault's "Assistant" agent: maker-facing config, agent-level instructions, repo-local Topics, and the MCP tool wrapper for the bundled Python scripts.

It replaces the original template's `.codex/` directory (built for OpenAI Codex CLI). See `../MIGRATION.md` at the repo root for what changed and why.

## Layout

- `agent/agent.yaml` — maker checklist for setting up the agent in Copilot Studio (Overview, Knowledge, Tools, Triggers, publish channels). Not an importable solution file.
- `agent/instructions.md` — the agent-level system prompt. Paste into Agent > Overview > Instructions.
- `agent/assets/` — icon assets.
- `topics/` — one folder per Topic, each with a `TOPIC.md` (the maker-facing spec: trigger phrases, description, instructions) and `agents/copilotstudio.yaml` (compact UI metadata: display name, starter prompt, trigger phrases). Some also ship `references/`, `scripts/`, or `assets/`.
- `tools/` — a small MCP server that exposes the bundled Python scripts (`new_person.py`, `new_project.py`, `fetch_comments.py`, `inspect_pr_checks.py`, and the onboarding scripts) as callable tools, so they can be registered as a Copilot Studio Tool.

## The create-vault-file / create-vault-folder Tools

`new-person` and `new-project` need to write files into the vault. In an enterprise tenant where **Flow, MCP, Custom connector, and REST API tool types are all disabled** and only prebuilt **Connector** actions are available under Tools > Add a tool, the way to do this with zero custom hosting is to add a specific connector action directly as a Tool — no flow in between (confirmed against [Add tools to custom agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-tools-custom-agent)).

Set these up once; every write-back topic reuses them.

**`create-vault-file`** — SharePoint or OneDrive for Business's **"Create file"** action:

1. Agent > **Tools** page > **Add a tool**.
2. Pick **Connector**, search for **SharePoint** (or **OneDrive for Business**, matching whichever you used to sync this vault in "Connect The Vault").
3. Select the **Create file** action > **Add and configure**.
4. On the tool's configuration page:
   - **Name**: `create-vault-file`.
   - **Description**: something specific, e.g. "Creates a new file at a given folder path and file name in the vault, with given text content. Use for person notes, project READMEs, AGENTS.md files, and other single-file vault writes." — the orchestrator uses this to decide when to call it.
   - **Inputs**: set **Site Address** to **Custom value**, fixed to your vault's SharePoint site (or leave as the OneDrive default if using OneDrive for Business). Leave **Folder Path**, **File Name**, and **File Content** as **Dynamically fill with AI** — the agent computes these per call from the relevant `TOPIC.md`'s instructions (it already has the vault's folder conventions from `instructions.md` and Knowledge).
   - **Completion**: **Don't respond** (default) is fine — let the calling topic/orchestrator report the result.
5. **Save**, confirm **Enabled** is on.

**`create-vault-folder`** — SharePoint or OneDrive's **"Create new folder"** action. Same steps, same fixed Site Address, **Parent Folder** and **Folder Name** left dynamic. Needed because "Create file" does **not** auto-create missing parent folders (it fails with `NotFound` if the target folder doesn't exist) — so `new-project` calls this first, then `create-vault-file` for each file inside the new folder.

Test each Tool from the agent's Test panel with a concrete example (e.g. ask it to create a person note) before trusting it end to end — connector authentication (End user vs. Maker-provided credentials, in the tool's **Additional details**) affects whether it can actually write, and that's worth confirming empirically rather than assuming.

## GitHub Topics (gh-address-comments, gh-fix-ci, gh-commit, yeet)

- `gh-address-comments` and `gh-fix-ci` only work if a **GitHub** connector is available under Tools > Add a tool > Connector *and* it exposes the needed actions (listing PR review/issue comments; getting check-runs for a commit). This isn't guaranteed — search for "GitHub" in the Connector picker and check what actions it actually offers before assuming these topics are usable. If it's missing or doesn't cover what's needed, these topics are blocked in a Flow/MCP/REST-API-disabled tenant; there's no other route available.
- `gh-commit` and `yeet` need a live git working tree (staging, diffing, committing) that no Copilot Studio Tool can provide regardless of tenant configuration — kept for reference only, not expected to run in this agent. See their own Platform Notes.

## Setting Up A Topic In Copilot Studio

Copilot Studio Topics are authored in the maker portal, not imported from a markdown file. For each folder under `topics/`:

1. In Copilot Studio, create a new Topic with the same name.
2. Copy the `description` from the Topic's frontmatter into the Topic's own description field (the generative orchestrator uses this to decide when to route to it).
3. Copy the "Trigger Phrases" list into the Topic's trigger phrases field.
4. Either let generative orchestration handle the conversation using the rest of `TOPIC.md` as grounding context (simplest, works well for most of these Topics), or hand-build a classic Topic conversation flow if you need deterministic steps.
5. Wire up any Tools the Topic's "Platform Notes" section calls out (shell/code execution, GitHub connector, browser automation, messaging connectors) before relying on it end to end.

## Keep Frontmatter Limited

Keep `TOPIC.md` frontmatter limited to:

- `name`
- `description`
- `last_edited`

Use natural trigger phrases in the description because the description is the recall surface for Copilot Studio's generative orchestrator, the same way it was the recall surface for Codex's skill router.
