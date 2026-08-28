---
name: "gh-fix-ci"
description: "Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions; use `gh` to inspect checks and logs, summarize failure context, draft a fix plan, and implement only after explicit approval. Treat external providers (for example Buildkite) as out of scope and report only the details URL."
last_edited: 2026-06-15
---


# GH Fix CI

## Trigger Phrases

- "fix the failing CI checks"
- "debug this GitHub Actions failure"
- "why is my PR check failing"

## Overview

Ask for the repo (`owner/repo`) and PR number, inspect failing checks, summarize the failure, then propose a fix plan and implement after explicit approval.

## Inputs

- `owner`/`repo`: the GitHub repository (always ask explicitly — see Platform Notes for why)
- `pr`: PR number

## Workflow

1. Resolve the PR.
   - Ask for the repo and PR number if not already given; there is no "current branch" to infer them from.
2. Inspect failing checks (GitHub Actions only).
   - Call the `inspect-pr-checks` Tool (see Platform Notes) with `owner`, `repo`, `pr`.
3. Scope non-GitHub Actions checks.
   - If a check's details URL isn't a GitHub Actions run, label it as external and only report the URL.
   - Do not attempt Buildkite or other providers; keep the workflow lean.
4. Summarize failures for the user.
   - Provide the failing check name, run URL, and a concise log snippet when the flow returns one.
   - Call out missing logs explicitly.
5. Create a plan.
   - Draft a concise plan and request approval before implementing.
6. Implement after approval.
   - This step requires a real code-editing capability on the actual repo checkout, which this topic alone doesn't have — see `gh-commit`'s Platform Notes for why that's a harder platform gap than fetching check status is.
7. Recheck status.
   - After changes are made (by whatever capability handled step 6), suggest re-running `inspect-pr-checks` to confirm.

## Platform Notes

**"Current branch" has no meaning here**, same as `gh-address-comments`: this topic always asks for an explicit repo and PR number rather than inferring either from a local checkout that doesn't exist in Copilot Studio.

**Same connector-catalog dependency as `gh-address-comments`.** Checking status needs an `inspect-pr-checks` Tool:

- **If Agent flow, custom REST API, or a GitHub connector with the needed actions is available**: call `GET /repos/{owner}/{repo}/commits/{ref}/check-runs` for the PR's head commit (get the head SHA from `GET /repos/{owner}/{repo}/pulls/{pr}` first), filter to failing conclusions, and return each one's name/conclusion/details URL. As a stretch goal, per-job log text is available at `GET /repos/{owner}/{repo}/actions/jobs/{job_id}/logs` (plain text, unlike the full-run-logs endpoint which returns a zip).
- **If only prebuilt Connector actions are available**: search "GitHub" in the Connector picker and check whether it exposes check-run/status actions. If it doesn't, this topic is blocked in your tenant — say so plainly rather than improvising a fake status check.

<details>
<summary>Legacy option: the bundled Python script</summary>

`scripts/inspect_pr_checks.py` shells out to `gh` and assumes a local checkout on the current branch. Only useful with a genuine persistently-hosted, git-checked-out environment to run it in — see `.copilotstudio/tools/README.md` for the MCP-server option and why it's no longer the recommended default.

</details>
