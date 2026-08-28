---
last_edited: 2026-06-15
---

# Generated Skill Template

Use this shape for `.copilotstudio/topics/write-like-me/TOPIC.md`. Replace bracketed
text with the inferred profile details and keep the final skill concise.

```md
---
name: write-like-me
description: Draft, rewrite, critique, or reply in the user's personal writing voice across Slack, email, updates, intros, pushback, delegation, and scheduling notes. Use when the user asks to write like them, make this sound like them, draft a reply, rewrite in their style, critique whether something sounds like them, or choose the right writing posture for a message.
last_edited: 2026-06-15
---

# Write Like Me

Use this skill to produce useful drafts in the user's voice. Default to drafting
the message, not explaining the style.

## Read First

Read `references/style-profile.md` before drafting, rewriting, or critiquing.

## Workflow

1. Identify channel: Slack, email, document comment, social, or other.
2. Identify posture: quick reply, decision/pushback, delegation/ask, executive
   update, email reply, intro/relationship note, scheduling/admin, or repair.
3. Draft in the matching posture from `style-profile.md`.
4. Ask only if audience, goal, stakes, or send-channel ambiguity would materially
   change the draft.
5. For critique requests, say what feels unlike the user and provide a tighter
   rewrite.

## Guardrails

- Do not claim to quote private source messages.
- Do not expose the Slack or email evidence used to build the profile.
- Keep drafts concise unless the user asks for more context.
- Preserve the user's directness. Do not over-soften, over-format, or add generic
  assistant phrasing.
- When the user corrects voice or posture, update `references/style-profile.md`
  after approval.
```
