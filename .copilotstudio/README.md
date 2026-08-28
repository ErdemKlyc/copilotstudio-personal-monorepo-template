---
last_edited: 2026-06-15
---

# Agent Assets

This directory holds the Microsoft Copilot Studio configuration for this vault's "Assistant" agent: maker-facing config, agent-level instructions, repo-local Topics, and the MCP tool wrapper for the bundled Python scripts.

It replaces the original template's `.codex/` directory (built for OpenAI Codex CLI). See `../MIGRATION.md` at the repo root for what changed and why.

## Layout

- `agent/agent.yaml` — maker checklist for setting up the agent in Copilot Studio (Overview, Knowledge, Actions, Triggers, publish channels). Not an importable solution file.
- `agent/instructions.md` — the agent-level system prompt. Paste into Agent > Overview > Instructions.
- `agent/assets/` — icon assets.
- `topics/` — one folder per Topic, each with a `TOPIC.md` (the maker-facing spec: trigger phrases, description, instructions) and `agents/copilotstudio.yaml` (compact UI metadata: display name, starter prompt, trigger phrases). Some also ship `references/`, `scripts/`, or `assets/`.
- `tools/` — a small MCP server that exposes the bundled Python scripts (`new_person.py`, `new_project.py`, `fetch_comments.py`, `inspect_pr_checks.py`, and the onboarding scripts) as callable tools, so they can be registered as a Copilot Studio Action.

## Setting Up A Topic In Copilot Studio

Copilot Studio Topics are authored in the maker portal, not imported from a markdown file. For each folder under `topics/`:

1. In Copilot Studio, create a new Topic with the same name.
2. Copy the `description` from the Topic's frontmatter into the Topic's own description field (the generative orchestrator uses this to decide when to route to it).
3. Copy the "Trigger Phrases" list into the Topic's trigger phrases field.
4. Either let generative orchestration handle the conversation using the rest of `TOPIC.md` as grounding context (simplest, works well for most of these Topics), or hand-build a classic Topic conversation flow if you need deterministic steps.
5. Wire up any Actions the Topic's "Platform Notes" section calls out (shell/code execution, GitHub connector, browser automation, messaging connectors) before relying on it end to end.

## Keep Frontmatter Limited

Keep `TOPIC.md` frontmatter limited to:

- `name`
- `description`
- `last_edited`

Use natural trigger phrases in the description because the description is the recall surface for Copilot Studio's generative orchestrator, the same way it was the recall surface for Codex's skill router.
