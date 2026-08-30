---
last_edited: 2026-06-15
---

# Personal Copilot Studio Vault

Starter workspace for giving a Microsoft Copilot Studio agent durable context: projects, people, topics,
onboarding, recurring checks, and writing-style memory.

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
- Maker permissions to create an agent, add Knowledge sources, add Tools, and add Triggers.
- A place this repo can live that Copilot Studio can read as Knowledge — see **Connect The Vault** below.

## Fast Start

1. Clone this template and push it to your own repo (or a SharePoint/OneDrive-synced folder — see below).
2. Open [copilotstudio.microsoft.com](https://copilotstudio.microsoft.com) and create a new agent named "Assistant".
3. Follow **Set Up The Agent** below to wire up instructions, knowledge, Tools, and triggers.
4. Publish the agent to a channel (Teams is the easiest starting point) and start a conversation with: `onboard me`.

There is no single-command "set me up" flow the way a local CLI agent can offer — Copilot Studio setup is a maker task done once in the portal, not something an end user's first message can trigger unattended.

## Connect The Vault

Copilot Studio does not read a git repository directly. Pick one:

- **SharePoint or OneDrive (recommended):** sync this repo (or mirror its contents) into a SharePoint document library or OneDrive folder, then add that folder as a Knowledge source (Agent > Knowledge > Add knowledge). This is what makes `projects/`, `experiments/`, `people/`, and `templates/` readable by the agent.
- **Public website:** if this vault is published as a static site (for example GitHub Pages), add it as a website Knowledge source. Read-only — the agent can't write back through this path.
- **Dataverse:** for a more structured setup, mirror `people/*.md` and project packets into Dataverse tables instead of files, and add those tables as Knowledge sources.

Writing back to the vault (new project folders, updated `people/*.md`, `GOAL.md` files) requires a Tool that can actually write to wherever you synced this repo — see `.copilotstudio/tools/README.md` for the MCP-server option that lets the agent run the bundled Python scripts, or use a Power Automate flow with a SharePoint/OneDrive connector.

## Set Up The Agent

1. Open Copilot Studio and create (or open) the "Assistant" agent.
2. Paste `.copilotstudio/agent/instructions.md` into the agent's Overview page > Instructions section > Edit. New agents use **generative orchestration** by default — required later for the Recurrence trigger in step 7 — but confirm it's on at Settings page > Generative AI section > Orchestration > "Use generative AI orchestration for your agent's responses?" (should read Yes; if the setting isn't there at all, an environment admin has disabled it and needs to turn it on tenant-side).
3. Add the Knowledge source(s) from **Connect The Vault** above.
4. Set up the Tools this template's write-back topics need. What's available under Tools > Add a tool varies a lot by tenant — some enterprise environments disable Flow, MCP, Custom connector, and REST API entirely, leaving only prebuilt **Connector** actions. Check what you actually have before picking an approach:
   - **`create-vault-file` and `create-vault-folder`** (used by `new-person`/`new-project`) — in a Connector-only tenant, add SharePoint's (or OneDrive for Business's) **"Create file"** and **"Create new folder"** actions directly as Tools; no Flow needed. Full setup in `.copilotstudio/README.md` > "The create-vault-file / create-vault-folder Tools". If Agent flow *is* available to you, that's an equally valid way to build the same logic — see each topic's Platform Notes.
   - **`fetch-pr-comments` and `inspect-pr-checks`** (used by `gh-address-comments`/`gh-fix-ci`) — depend on whether a GitHub connector with the right actions exists in your tenant, or Agent flow/REST API tool types are available to call GitHub's REST API directly. Check both before assuming these topics work — see `.copilotstudio/README.md` > "GitHub Topics".
   - `gh-commit` and `yeet` can't run inside Copilot Studio at all, in any tenant (no working tree to act on) — kept for reference only; use a real coding agent or your own git client for those.
   - A browser-automation MCP tool or connector, only if you want `audit-ai-frontend`'s browser-QA steps to run rather than fall back to screenshot-only review.
   - Optional: `.copilotstudio/tools/mcp_server.py` is a fallback for the write-back/GitHub topics if you have genuine persistent, IT-approved hosting and prefer reusing the bundled Python scripts to rebuilding the logic as Tools — see `.copilotstudio/tools/README.md` for when that actually makes sense (and when it doesn't, e.g. free/ephemeral hosts, or a locked-down corporate device that also blocks the local tooling needed to test it).
5. For each folder under `.copilotstudio/topics/`, create a matching Topic using that folder's `TOPIC.md` — see `.copilotstudio/README.md` for the exact steps.
6. Publish to at least one channel: Microsoft Teams, a custom website, or Microsoft 365 Copilot (if licensed).
7. Once a conversation is running, say `onboard me` to start first-meeting onboarding, which will offer to set up a recurring check-in as a **Recurrence** trigger: on the agent's **Overview** page, **Triggers** section > **Add trigger** > select the Recurrence trigger and set the cadence. This needs generative orchestration turned on (step 2) and, in some tenants, an admin to turn on "solution-aware cloud flow sharing" for the environment before the Triggers option appears at all.

## What Onboarding Does

Onboarding should explain what it is checking before it checks it.

It should:

- read the workspace (via whatever Knowledge source you connected)
- ask what projects exist and what matters
- ask who Assistant should know about
- check whether useful connectors/Tools are missing
- offer a Recurrence trigger for a daily update check-in, a people-monitor, and project monitors, defaulting to 9:00 AM and 4:00 PM check-ins in your timezone
- offer to bootstrap a `write-like-me` topic from your sent Teams/Slack and email writing
- offer shared-memory setup by using this repo as the vault
- proactively propose `people/*.md`, project packets, and `AGENTS.md` updates after scanning connected Teams/Slack, email, calendar, docs, project trackers, and GitHub context

Assistant should ask before sending messages, changing meetings, editing shared docs, creating triggers, adding connectors/Tools, or writing shared memory.

## Topics

Repo-local Topics live under `.copilotstudio/topics/`.

Useful starting points:

- `onboarding`: first setup
- `assistant`: ongoing work support after onboarding
- `loop`: recurring checks via a Recurrence trigger
- `new-project`: create a project or experiment
- `new-person`: create a person note
- `write-like-me-bootstrap`: create a personal writing-style topic from Teams/Slack and email

## Example Prompts

Once the agent is set up, here's what you'd actually type. These map directly to the Topics under `.copilotstudio/topics/` — grouped the same way as the root `AGENTS.md`.

**Assistant (day-to-day)**
- "Onboard me." — first-time setup, or fills gaps if setup is partial.
- "What should I know today?" / "Catch me up."
- "Draft a reply for this." (paste the email/message thread first)
- "Keep an eye on this for me."

**Bootstrapping**
- "Start a new project called Q3 Vendor Review."
- "Create a new experiment for the pricing model spike."
- "Add a person note for Sarah, our new IT procurement lead."
- "Learn my writing style from my sent email and Teams chats."

**Goals**
- "Set a goal to get all open PRs merged by Friday, with tests passing as the verifier."
- "Start a persistent goal for the Q3 migration — track it in GOAL.md."
- "What's our leverage with this goal — activate it."

**Automations**
- "Keep checking on this and let me know when the vendor responds."
- "Loop this every morning until the deploy finishes."
- "Check again later — say, in a couple hours."

**Artifacts**
- "Build an HTML report summarizing this quarter's project status."
- "Make a static info page comparing these three vendor options."

**Audits**
- "Audit this code for AI-generated smells." (paste a diff or point at a PR)
- "De-slop this UI — review this React component for generic AI tells."
- "Does this sound like an AI chatbot wrote it? Check these citations too."

**GitHub workflows** (need the Tools/connector setup in Step 4 above)
- "Commit my changes — split this diff into semantic commits."
- "Address the PR comments on my current branch."
- "Fix the failing CI checks on this PR."
- "Yeet this — stage, commit, push, and open a PR." *(only works from a real coding agent/git client, not from inside Copilot Studio — see `gh-commit`/`yeet`'s Platform Notes)*

## Structure

- `projects/`: long-lived work
- `experiments/`: short-lived spikes
- `people/`: notes about people or agents
- `.copilotstudio/`: agent config, Topics, and the MCP tool server
- `templates/`: starter files
- `tests/`: checks for template integrity
