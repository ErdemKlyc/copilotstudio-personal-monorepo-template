---
name: loop
description: "Set up a recurring scheduled trigger for this agent. Use when the user asks this agent to keep going, check again, follow up, retry, monitor, or resume on a recurring cadence."
last_edited: 2026-06-15
---

# Loop

## Trigger Phrases

- "keep checking on this"
- "loop this"
- "check again later"
- "follow up on this periodically"
- "monitor this and let me know"

Turn a plain-English request into a recurring check-in with as little ceremony as possible.

## Platform Notes (read first)

Codex CLI's original `loop` skill attached a "heartbeat" automation directly to the live chat thread and could rename that thread to reflect status. Copilot Studio agents do not have a native "attach a recurring job to this specific conversation and rename it" tool — the closest real building block is a **Scheduled trigger** on the agent itself:

- In Copilot Studio: Agent > Overview > Triggers > Add a trigger > Scheduled. A scheduled trigger fires independently of any open conversation and can start the agent on a topic/prompt on a cadence (for example, hourly, daily, or a custom recurrence).
- If your environment doesn't expose Triggers to makers yet, use a Power Automate recurrence trigger instead: have the flow call this agent's "Direct Line" / channel API or post to wherever the check-in should land (email, Teams channel, Dataverse row), on the desired schedule.
- There is no equivalent to renaming a chat thread to `loop: ...` / `done: ...` inside Copilot Studio. Track loop status durably instead — for example a row in a Dataverse table, a status field in a tracked file in this vault (`WORKLOG.md`), or a Teams message the trigger posts — and say plainly that thread-renaming isn't available in this environment.

Everything below is adapted to that model.

## Set Up The Loop

1. Infer the task from the request and current context. Infer the stop condition when one is clear.
2. Decide whether a scheduled trigger is useful. Use one when the work benefits from returning after time passes or external state may change; continue immediately instead when the task can simply be finished now.
3. Use the requested cadence when sensible. Otherwise choose a cadence from the task's expected feedback latency, urgency, cost, and risk of noisy empty runs. Do not poll faster than the underlying state can plausibly change.
4. Choose a short verb-led name and a self-contained prompt for the trigger to run. Put the work, its completion condition, and this terminal behavior in the prompt:
   - when the completion condition is met, update the durable status record (see Platform Notes) to reflect `done: <short task name>`;
   - report the completed result through whatever channel the trigger posts to, then disable or delete the trigger.
   Keep timing and destination details in the trigger's own configuration, not in the prompt text.
5. Create the trigger in Copilot Studio (Agent > Overview > Triggers > Add a trigger > Scheduled) with:
   - the inferred name
   - the self-contained prompt from step 4
   - the chosen recurrence
6. After creation succeeds, record the loop's status as `loop: <short task name>` in the durable status record.
7. Return only the trigger name, cadence, and what it will do, plus where its status/output will show up.

Do not invent a chat-thread-rename capability or a detached cron job outside Copilot Studio's Triggers (or an explicit Power Automate flow the user approved).

## Use Judgment

- Ask when the task, cadence, stop condition, deadline, or notification behavior is materially ambiguous. Offer a small set of task-appropriate cadence choices and recommend one; do not make the user translate the task into scheduling jargon (RRULE, cron) themselves.
- If the ambiguity is minor, make a reasonable assumption and state it instead of interrupting setup.
- Treat "loop," "keep going," and "check again" as authorization to create the scheduled trigger requested in that message.
- Preserve explicit deadlines, notification requirements, and stop conditions.
- Keep the lifecycle prefixes exact in the durable status record: `loop:` while active and `done:` after successful completion.
- Mark `done:` only after successful completion, not after a failed run, pause, or temporary retry.
- Prefer updating an existing matching trigger over creating a duplicate.
- For inspect, pause, resume, change, or delete requests, resolve the existing trigger in Copilot Studio's Triggers pane and update or disable it, preserving fields the user did not change. Restore the `loop:` status when resuming.
- If maker access to Triggers is unavailable in this environment, say so plainly. Never fabricate a scheduling mechanism as a workaround.
