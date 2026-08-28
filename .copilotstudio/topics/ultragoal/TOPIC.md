---
name: ultragoal
description: Design, critique, set, create, activate, or run durable goals for persistent or long-running objectives. Use when the user says "set a goal", "start a goal", "activate goal mode", "persistent goal", "long-running objective", "goal tree", or asks for a goal with verifiers, durable state, approval gates, completion proof, bounded delegation, or parent/child subagent goals.
last_edited: 2026-06-15
---

# Ultragoal

## Trigger Phrases

- "set a goal"
- "start a persistent goal"
- "activate goal mode"
- "track this as a long running objective"

Use this topic when a user wants a persistent goal, not just a longer task. A good goal has an observable finish line, a verifier that can fail, and enough context for the agent to recover after interruptions.

Do not activate a goal from vague planning language. Activate only when the user explicitly asks to start, set, activate, create, or run a goal. Never set a token or run budget unless the user explicitly requests one.

## Platform Notes (read first)

Codex CLI ships native `create_goal` / `update_goal` tools that track a persistent goal's state across sessions and can autonomously resume work. **Copilot Studio has no built-in equivalent** — there is no native "activate this as a tracked goal" call. This topic replaces that mechanism with two things this vault already supports:

1. **Durable files**, exactly as described below (`GOAL.md`, `WORKLOG.md`, `RESULT.md`) — these are the actual source of truth for goal state, not a chat-session memory.
2. **A scheduled trigger from the `loop` topic** when the goal needs to resume without a human re-opening the conversation: the trigger's prompt should read `GOAL.md`/`WORKLOG.md`, do the next safe step, update `WORKLOG.md`, and stop or mark `RESULT.md` complete per the verifier.

Wherever the text below says "call `create_goal`" or "call `update_goal`", read that as: write/update the corresponding durable file and, if unattended continuation is needed, ensure a scheduled trigger exists per the `loop` topic. There is no separate activation API call to make.

## Modes

- **Design:** research and return a goal packet. Do not write `GOAL.md` yet.
- **Critique:** inspect an existing goal or draft and tighten it.
- **Activate:** design and critique the goal, then write `GOAL.md` (and set up a scheduled trigger if unattended continuation is needed) as the final activation step.
- **Goal tree:** only when the user explicitly authorizes goal-backed subagents. Give each child one bounded objective and verifier, tracked in its own durable file.

## Default Activation Rule

When the user explicitly invokes this topic for a concrete work objective and asks the agent to build, complete, run, pursue, or "do it", treat the request as **Activate** by default.

Do not stop after drafting a goal packet. After grounding, write `GOAL.md` (and `WORKLOG.md` if useful) before continuing task work.

Only stay in **Design** mode when the user asks to draft, design, critique, or discuss a goal without starting it.

## Workflow

### 1. Ground the Outcome

Find the intended result, audience, destination, constraints, and why persistence helps. Inspect named files, repos, conversations, artifacts, and live systems before drafting.

Ask only when the missing answer changes the finish line, grants consequential approval, or chooses between incompatible goals. Otherwise state the assumption and continue.

### 2. Research Enough

Gather the smallest useful evidence set:

1. Read the canonical local source and applicable instructions.
2. Inspect the baseline, prior attempts, tests, benchmarks, reproductions, or acceptance criteria.
3. Refresh volatile facts from primary or live sources when they matter.
4. Stop once the finish line and verifier are grounded.

Separate observed facts, user requirements, and inferred choices.

### 3. Check Goal Fit

Recommend Goal mode only when most are true:

- progress needs repeated attempts, waiting, recovery, or long feedback cycles;
- success can be measured by a test, benchmark, workflow, artifact inspection, screenshot, readback, or other external signal;
- the agent can respond to the next failure without another preference decision;
- completion evidence is stronger than the agent saying "done."

Prefer an ordinary task or plan when the work is one-shot, taste-dependent, blocked on repeated human choices, lacks a credible verifier, or risks unbounded external action.

### 4. Define the Loop

Specify:

- **Outcome:** one observable result.
- **Baseline:** current state, failure, or starting metric.
- **Primary verifier:** strongest independent success check.
- **Supporting checks:** regression, quality, safety, or durability checks.
- **Iteration loop:** inspect, change one meaningful thing, run verifier, record evidence, choose next action.
- **Anti-cheating rules:** do not weaken tests, narrow scope, hide failures, swap in mocks, or change benchmarks without approval.
- **Approval gates:** irreversible, public, shared, or costly actions need separate user approval.
- **Blocker standard:** external blocker plus smallest next action; difficulty or uncertainty is not enough.
- **Completion proof:** exact commands, outputs, paths, screenshots, or readbacks required before marking `RESULT.md` complete.

For flaky or stateful checks, require clean-state reproduction and enough consecutive passes to rule out luck.

### 5. Keep State Durable

Keep the active goal objective compact. Put supporting context in the nearest durable file when it exceeds a few paragraphs.

Prefer project conventions. Otherwise propose:

```text
GOAL.md      outcome, baseline, constraints, success and blocker criteria
WORKLOG.md   attempts, evidence, current state, next action
RESULT.md    final change, verification, remaining risks
```

Do not create files in Design mode unless the user asked for a durable artifact or the repo convention makes it obvious. Preserve dirty work and read existing goal files before editing them.

### 6. Delegate Carefully

When subagents are authorized, the parent keeps scope, integration, conflict resolution, and final completion. Delegate only separable lanes: environment discovery, source research, alternative approaches, or independent verification.

For each lane, name the objective, non-goals, ownership boundary, verifier, stop condition, and returned evidence. Give each child its own durable file (a scoped `GOAL.md`/`WORKLOG.md` pair) since there is no built-in goal-tree tool to track parent/child state for you.

### 7. Activate Last

Before activation, red-team the draft:

- Can success be faked by weakening the verifier?
- Could the words be satisfied while missing the user's real outcome?
- Are approval gates explicit?
- Does the loop say what to do after a failed attempt or wait?
- Is completion observable outside the running agent?

If activation was requested, or the Default Activation Rule applies, write `GOAL.md` only after the goal packet is grounded and red-teamed. This is the final action of activation; do not write it early, and do not merely say a goal should be set. If the goal needs to progress without an open conversation, set up the scheduled trigger described in the `loop` topic now, pointed at this goal's durable files.

If task work should continue after activation, write the goal files first and then resume under Active Goal Discipline.

Use a compact objective, recorded at the top of `GOAL.md`:

```text
Complete and verify the objective defined in <path-to-GOAL.md>.
```

For a self-contained goal, put the observable outcome and strongest verifier directly in the objective. After writing `GOAL.md` (and the trigger, if any), report the exact active objective and continue from there.

## Goal Packet

Return:

1. **Fit:** Goal mode or better alternative, with one-sentence rationale.
2. **Grounding:** current state, assumptions, evidence gaps.
3. **Goal brief:** outcome, baseline, constraints, non-goals, verifier, loop, approval gates, blocker standard, completion proof.
4. **Delegation map:** only when useful and authorized.
5. **Exact objective:** concise text for the top of `GOAL.md`.
6. **Activation state:** `drafted`, `active`, or `not recommended`.

If activated, include the exact active objective and whether a scheduled trigger was created. If not, say no goal was created.

## Active Goal Discipline

When operating an active goal:

- inspect `GOAL.md`/`WORKLOG.md` when resuming or after material steering;
- continue while a safe, relevant next step remains;
- mark `RESULT.md` complete only after the objective and completion proof are satisfied;
- mark blocked only after the required repeated external blocker threshold is met and no meaningful progress remains;
- preserve partial results and next action in `WORKLOG.md` when stopping.
