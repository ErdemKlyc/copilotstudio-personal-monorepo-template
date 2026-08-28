---
last_edited: 2026-06-15
---

# Migration Notes: OpenAI Codex CLI to Microsoft Copilot Studio

This repo is a port of a personal-monorepo vault template from OpenAI Codex CLI to Microsoft Copilot Studio. The vault structure (`projects/`, `experiments/`, `people/`, `templates/`) carried over unchanged — it's just markdown. Everything under `.codex/` needed a real rethink because the two platforms have different building blocks, not just different names for the same thing.

## What mapped cleanly

| Codex CLI | Copilot Studio |
|---|---|
| `SKILL.md` (frontmatter + trigger-cued description) | `TOPIC.md` (same frontmatter shape, plus an explicit Trigger Phrases list, since Studio has a dedicated trigger-phrase field separate from the description) |
| `.codex/skills/<name>/agents/openai.yaml` (display metadata) | `.copilotstudio/topics/<name>/agents/copilotstudio.yaml` |
| `.codex/AGENTS.md`, root `AGENTS.md` | `.copilotstudio/agent/instructions.md` (paste into Agent > Overview > Instructions) + root `AGENTS.md` kept as the human/contributor doc |
| `references/`, `scripts/`, `assets/` per skill | Copied through unchanged; scripts are now called via the MCP tool wrapper in `.copilotstudio/tools/` instead of being run directly by the agent |

## What genuinely doesn't map

- **`create_goal` / `update_goal` (Codex's native persistent-goal tools).** No Copilot Studio equivalent exists. The `ultragoal` topic now treats "activate a goal" as "write `GOAL.md`/`WORKLOG.md` and, if unattended continuation is needed, set up a Scheduled trigger" — durable files plus a real trigger, not a magic tool call.
- **Chat-attached heartbeats and thread renaming.** Codex's `loop` skill could attach an automation to the live thread and rename it (`loop: ...` / `done: ...`). Copilot Studio has no per-conversation heartbeat or rename API exposed to the agent. The `loop` topic now points at Copilot Studio's **Scheduled trigger** (Agent > Overview > Triggers), which runs independently of any open conversation, and tracks status in a durable file instead of a thread title.
- **`$command` slash-trigger convention.** Codex skills are invoked with `$skill-name`. Copilot Studio Topics use a **trigger phrases** list of natural-language utterances plus a description the generative orchestrator matches against — there's no slash-command syntax. Every ported topic has a "Trigger Phrases" section with the `$` dropped.
- **Bundled `$playwright` / `$playwright-interactive` skills.** Codex CLI ships these; Copilot Studio has no built-in browser tool. `audit-ai-frontend` now expects a Playwright-based MCP tool or custom connector to be registered as an Action, and falls back to screenshot-only review if none is registered.
- **`oai_gh` CLI wrapper.** A Codex-sandbox-specific convenience wrapper around `gh`. Dropped in favor of plain `gh` everywhere (`gh-commit`, `gh-address-comments`, `gh-fix-ci`, `yeet`).
- **Local shell/filesystem execution.** Codex CLI runs scripts and git commands directly. Copilot Studio agents have zero ambient capability — every topic that shells out (`new-person`, `new-project`, `gh-*`, `yeet`, onboarding's helper scripts) now depends on an explicit Action: either the MCP server in `.copilotstudio/tools/` (wraps the existing Python scripts unmodified) or a GitHub connector.
- **Reading the repo as a local filesystem.** Codex reads this repo directly off disk. Copilot Studio reads Knowledge sources (SharePoint, OneDrive, Dataverse, public websites) — it does not clone or mount a git repo. See the root `README.md`'s "Connect The Vault" section for the sync step this requires.
- **Cross-conversation memory.** Codex CLI has its own local Memories concept that the original `assistant` topic explicitly said not to use as a vault substitute. Copilot Studio has no equivalent native memory feature for a maker-built agent, so that caution became moot — this vault (via a connected Knowledge source) is now unambiguously the only durable-memory surface.
- **"Rename/pin the chat" onboarding step.** No Copilot Studio equivalent for an agent to rename its own conversation surface. Onboarding now just explains how to find the agent again in its published channel.
- **Branch/PR naming (`codex/...`, `[codex] ...`).** Cosmetic only — renamed to `copilot/...` and `[copilot] ...` in `gh-commit` and `yeet`. Change it if your team uses something else.

## Design choices worth knowing about

- **`agent.yaml` is not an importable Studio solution file.** Copilot Studio's real machine-importable format (via `pac solution unpack`/`pack`) requires solution GUIDs specific to a live environment, which can't be fabricated ahead of time. `agent.yaml` is a maker checklist kept in source control instead — see `.copilotstudio/agent/agent.yaml`'s header comment.
- **MCP over Power Automate for the bundled scripts.** Either is a valid Copilot Studio Action type. MCP was chosen so the existing Python scripts could be wrapped unmodified rather than rewritten as flow steps — see `.copilotstudio/tools/README.md` for the tradeoff and the Power Automate alternative.
- **`write-like-me-bootstrap` defaults shifted toward Teams/Outlook**, with Slack kept as a secondary option, since this is now a Microsoft-first template. Swap the emphasis back if your organization is Slack-first.

## What to verify before you trust this for real work

This port was written from a static read of the source repo, not validated against a live Copilot Studio tenant. Before relying on it:

- Confirm the current Copilot Studio UI still exposes **Triggers > Scheduled** the way described here — this is a newer (2024/2025-era) feature and naming/placement can shift between releases.
- Confirm your tenant's MCP Action support and the exact registration flow in `.copilotstudio/tools/README.md` against the current portal, since MCP support in Copilot Studio is still evolving.
- Confirm the Instructions field's length limit in your tenant version; trim `.copilotstudio/agent/instructions.md` if Studio truncates or warns on save.
