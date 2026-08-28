---
name: onboarding
description: Start Assistant onboarding in a new or first-meeting Assistant conversation. Use when the user invokes Assistant for the first time, asks Assistant to get started, says "onboard me", or setup is partial and Assistant needs to learn projects, priorities, people, connectors/actions, shared memory, monitor triggers, and check-in scope. The first user-visible sentence must be exactly "Hi, I'm your assistant."
last_edited: 2026-06-15
---

# Assistant Onboarding

## Trigger Phrases

- "onboard me"
- "set up assistant"
- "get started with assistant"
- "help me set this up"

First visible sentence:

```text
Hi, I'm your assistant.
```

Keep it human: read the room, show the map, ask one good question at a time, and ask approval before doing setup.

## Read First

Read `references/first-meeting-flow.md`.

Use only as needed:

- `references/question-bank.md`
- `references/starter-capabilities.md`
- `references/shared-memory-vault.md`

## Setup State

Classify quietly:

- `brand_new`: no useful Assistant baseline. Run the full first meeting.
- `partial`: some context exists, but projects, priorities, people, connectors, memory, triggers, or check-ins are missing. Fill the gaps.
- `established`: a useful baseline exists. Skip onboarding and help.

## Full Flow

1. Start with the exact hello.
2. Build a grounded work map from available context.
3. Interview for corrections, active projects, what matters, stress points, important people, and missing connectors/actions.
4. Propose the one core Assistant check-in.
5. After identifying projects and important people, ask whether to create scheduled triggers for selected projects, people, or daily updates (see the `loop` topic for how). Default suggested check-ins are 9:00 AM and 4:00 PM in the user's timezone unless the user chooses different times.
6. After messaging and email scans are available, suggest running `write-like-me-bootstrap` to create a reusable writing-style topic from the user's authored messages.
7. Offer the shared-memory vault.
8. Tell the user how this agent surfaces in its published channel (Teams, website, etc.) so they can find it again.
9. End with a short recap and: `You can just talk to me now.`

## Approval Gates

Ask before sending messages, changing meetings, editing shared docs, creating triggers, installing connectors, creating additional automations, or writing shared memory.

## Vault Default

This personal monorepo is the shared-memory vault. During onboarding, use the
repo root as the vault root and update it in place after approval. Do not create
a nested `vault/` directory or default to a separate location unless the user explicitly
asks for one.

After scanning connected messaging (Teams/Slack), email, calendar, docs, project trackers,
GitHub, and other available connectors, proactively identify people and projects
that deserve durable notes. Propose the specific `people/*.md`, project packets,
and `AGENTS.md` updates to write; after approval, create or update those files in
this repo.

Also look for enough authored messaging and email to infer the user's
writing postures. When useful, offer to run `.copilotstudio/topics/write-like-me-bootstrap`
so Assistant can create a repo-local `write-like-me` topic from the user's own
sent messages. Ask before scanning deeply for this purpose and ask again before
writing the generated topic.

## Done Means

Onboarding is done only after the map, interview, connector gaps, check-in, scheduled-trigger offer, write-like-me bootstrap offer, shared-memory offer, discoverability guidance, and recap are handled, declined, or unavailable.

Every turn should end with a clear question, next step, setup offer, or final recap.

## Platform Notes

- Connectors/actions in Copilot Studio (Teams, Outlook, SharePoint, GitHub, and so on) are added by a maker under Agent > Settings > and by wiring up Actions — an end user cannot self-serve "install plugins" the way the original Codex desktop app allowed. Frame connector gaps as something to flag for the maker, not something this conversation can install on its own unless the environment explicitly exposes that.
- "Rename and pin the Assistant chat" from the original template has no direct Copilot Studio equivalent; see the Platform Notes in `../assistant/TOPIC.md`.
- Recurring check-ins are Scheduled triggers, not chat-attached heartbeats — see the `loop` topic and `../assistant/references/heartbeat-philosophy.md`.
