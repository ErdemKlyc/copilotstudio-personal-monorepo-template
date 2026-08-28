---
last_edited: 2026-06-15
---

# Personal Copilot Studio Vault

Starter workspace for giving a Microsoft Copilot Studio agent durable context: projects, people, topics,
onboarding, recurring checks, and writing-style memory.

This started as a port of a personal-monorepo template originally built for OpenAI Codex CLI. See [`MIGRATION.md`](MIGRATION.md) for what changed and why — the two platforms have genuinely different building blocks (Topics vs. slash-command skills, Scheduled triggers vs. chat heartbeats, Knowledge sources vs. a locally-readable git repo), so this isn't a drop-in reskin.

This template gives your Copilot Studio agent a place to look before it acts and a place to write
important context after you approve it:

- `projects/` for active work
- `experiments/` for short spikes
- `people/` for collaborators and agents
- `.copilotstudio/topics/` for repo-local Topics

This repo is the Assistant shared-memory vault. Onboarding should update this
repo in place; it should not create a nested `vault/` directory unless you
explicitly choose a different location.

## Prerequisites

- A Microsoft 365 tenant with access to [Copilot Studio](https://copilotstudio.microsoft.com).
- Maker permissions to create an agent, add Knowledge sources, add Actions, and add Triggers.
- A place this repo can live that Copilot Studio can read as Knowledge — see **Connect The Vault** below.

## Fast Start

1. Clone this template and push it to your own repo (or a SharePoint/OneDrive-synced folder — see below).
2. Open [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com) and create a new agent named "Assistant".
3. Follow **Set Up The Agent** below to wire up instructions, knowledge, actions, and triggers.
4. Publish the agent to a channel (Teams is the easiest starting point) and start a conversation with: `onboard me`.

There is no single-command "set me up" flow the way a local CLI agent can offer — Copilot Studio setup is a maker task done once in the portal, not something an end user's first message can trigger unattended.

## Connect The Vault

Copilot Studio does not read a git repository directly. Pick one:

- **SharePoint or OneDrive (recommended):** sync this repo (or mirror its contents) into a SharePoint document library or OneDrive folder, then add that folder as a Knowledge source (Agent > Knowledge > Add knowledge). This is what makes `projects/`, `experiments/`, `people/`, and `templates/` readable by the agent.
- **Public website:** if this vault is published as a static site (for example GitHub Pages), add it as a website Knowledge source. Read-only — the agent can't write back through this path.
- **Dataverse:** for a more structured setup, mirror `people/*.md` and project packets into Dataverse tables instead of files, and add those tables as Knowledge sources.

Writing back to the vault (new project folders, updated `people/*.md`, `GOAL.md` files) requires an Action that can actually write to wherever you synced this repo — see `.copilotstudio/tools/README.md` for the MCP-server option that lets the agent run the bundled Python scripts, or use a Power Automate flow with a SharePoint/OneDrive connector.

## Set Up The Agent

1. Open Copilot Studio and create (or open) the "Assistant" agent.
2. Paste `.copilotstudio/agent/instructions.md` into Agent > Overview > Instructions.
3. Add the Knowledge source(s) from **Connect The Vault** above.
4. Register the Actions this template needs before relying on the topics that use them:
   - The vault-tools MCP server (`.copilotstudio/tools/`) for `new-person`, `new-project`, `gh-address-comments`, `gh-fix-ci`, and onboarding's helper scripts.
   - A GitHub connector or `gh`-capable Action for `gh-commit`, `gh-address-comments`, `gh-fix-ci`, and `yeet`.
   - A browser-automation MCP tool or connector, only if you want `audit-ai-frontend`'s browser-QA steps to run rather than fall back to screenshot-only review.
5. For each folder under `.copilotstudio/topics/`, create a matching Topic using that folder's `TOPIC.md` — see `.copilotstudio/README.md` for the exact steps.
6. Publish to at least one channel: Microsoft Teams, a custom website, or Microsoft 365 Copilot (if licensed).
7. Once a conversation is running, say `onboard me` to start first-meeting onboarding, which will offer to set up a recurring check-in as a Scheduled trigger (Agent > Overview > Triggers > Add trigger > Scheduled).

## What Onboarding Does

Onboarding should explain what it is checking before it checks it.

It should:

- read the workspace (via whatever Knowledge source you connected)
- ask what projects exist and what matters
- ask who Assistant should know about
- check whether useful connectors/Actions are missing
- offer a Scheduled trigger for a daily update check-in, a people-monitor, and project monitors, defaulting to 9:00 AM and 4:00 PM check-ins in your timezone
- offer to bootstrap a `write-like-me` topic from your sent Teams/Slack and email writing
- offer shared-memory setup by using this repo as the vault
- proactively propose `people/*.md`, project packets, and `AGENTS.md` updates after scanning connected Teams/Slack, email, calendar, docs, project trackers, and GitHub context

Assistant should ask before sending messages, changing meetings, editing shared docs, creating triggers, adding connectors/Actions, or writing shared memory.

## Topics

Repo-local Topics live under `.copilotstudio/topics/`.

Useful starting points:

- `onboarding`: first setup
- `assistant`: ongoing work support after onboarding
- `loop`: recurring checks via a Scheduled trigger
- `new-project`: create a project or experiment
- `new-person`: create a person note
- `write-like-me-bootstrap`: create a personal writing-style topic from Teams/Slack and email

## Structure

- `projects/`: long-lived work
- `experiments/`: short-lived spikes
- `people/`: notes about people or agents
- `.copilotstudio/`: agent config, Topics, and the MCP tool server
- `templates/`: starter files
- `tests/`: checks for template integrity
