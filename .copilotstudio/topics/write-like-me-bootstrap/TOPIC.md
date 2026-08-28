---
name: write-like-me-bootstrap
description: Bootstrap a durable "write like me" topic from the user's own messaging and email writing. Use during Assistant onboarding, after messaging/email connectors are available, or when the user asks to learn their voice, infer writing style, create a personal writing persona, generate a write-like-me topic, analyze sent messages, or capture different writing postures across email and chat.
last_edited: 2026-06-15
---

# Write Like Me Bootstrap

## Trigger Phrases

- "learn my writing style"
- "create a write like me topic"
- "analyze my sent messages"
- "capture my writing voice"

Create or update a repo-local writing-style topic from the user's real authored
messages. The output should help future assistants draft in the user's voice
without copying raw private messages into durable files.

## Default Output

Write the generated topic to `.copilotstudio/topics/write-like-me/` unless the user asks
for a different name. Use:

- `.copilotstudio/topics/write-like-me/TOPIC.md` for the durable drafting workflow
- `.copilotstudio/topics/write-like-me/references/style-profile.md` for compact voice, posture, and examples
- `.copilotstudio/topics/write-like-me/agents/copilotstudio.yaml` if the repo uses topic UI metadata

Use `references/style-profile-template.md` as the target shape.
Use `references/generated-skill-template.md` as the starting shape for the
generated `TOPIC.md`.

## Source Scan

Use connected messaging and email sources when available — in a Microsoft-first environment that typically means Outlook and Microsoft Teams connectors, plus Slack if it is also connected. Prefer authored messages:

- Teams or Slack messages sent by the user in channels, DMs, and group chats
- sent email, replies, follow-ups, scheduling notes, intros, escalations, and updates
- recent enough writing to reflect the current voice, usually the last 90-180 days
- older writing only when it clarifies stable style or an important posture

If a connector is unavailable, say what is missing and proceed with available
sources or ask whether to retry later.

## Privacy Boundary

Do not save raw Teams, Slack, or email excerpts in durable files. Use short synthetic
examples that preserve style without exposing private content, names, deals,
secrets, or account details. Keep source evidence as compact descriptors such as
`sent email follow-ups, March-June 2026` or `Teams replies in project channels`.

Ask before writing or updating the generated topic. Reading connected context for
this bootstrap is allowed only when the user has asked for onboarding or this
topic, and writing still requires explicit approval.

## Analysis Workflow

1. Identify the user's authored messages and separate them by channel and intent.
2. Cluster writing into postures rather than one generic voice. Useful default
   postures:
   - quick chat reply
   - decision or pushback
   - delegation or ask
   - executive/status update
   - email reply
   - intro or relationship note
   - scheduling/admin note
   - apology, correction, or repair
3. For each posture, infer:
   - when to use it
   - sentence length and pacing
   - directness, warmth, humor, and formality
   - how the user frames asks, tradeoffs, disagreement, and urgency
   - phrases or moves to reuse as patterns, not verbatim quotes
   - things the user avoids
4. Compare chat and email. Preserve differences instead of flattening them.
5. Draft the generated `write-like-me` topic and profile.
6. Present a concise preview of the inferred postures and ask for approval before
   writing files.
7. After approval, create or update the generated topic in this repo.

## Generated Topic Requirements

The generated `write-like-me` topic should:

- trigger for drafting, rewriting, critiquing, or replying in the user's voice
- route by channel and posture before drafting
- ask only when audience, channel, or goal would materially change the draft
- default to concise, useful drafts rather than style analysis
- include a critique mode that says what feels unlike the user
- preserve privacy by never revealing the source messages used for bootstrapping
- tell future assistants to update the profile when the user corrects voice,
  posture, or audience assumptions

## Onboarding Behavior

During Assistant onboarding, suggest this bootstrap after the first connected
messaging/email scan finds enough authored writing to infer voice. The offer should
be concrete:

```text
I can also bootstrap a write-like-me topic from your sent email and chat messages, split by posture like quick replies, pushback, delegation, intros, and status updates. Want me to do that?
```

If the user says yes, run the source scan, show the posture preview, and ask
before writing the generated topic.

## Platform Notes

This assumes at least one messaging/email Tool or knowledge connector is registered on the agent (Outlook, Teams, or Slack). If none is connected, say so and offer to proceed once one is available, per the Source Scan section above.
