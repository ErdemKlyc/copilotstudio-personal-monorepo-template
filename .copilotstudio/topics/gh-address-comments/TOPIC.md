---
name: gh-address-comments
description: Help address review/issue comments on the open GitHub PR for the current branch using `gh`; verify auth first and prompt the user to authenticate if not logged in.
last_edited: 2026-06-15
---

# PR Comment Handler

## Trigger Phrases

- "address the PR comments"
- "handle the review feedback"
- "respond to reviewer comments on this PR"

Guide to find the open PR for the current branch and address its comments with `gh`.

Prereq: ensure the GitHub CLI is installed and authenticated. Run `gh auth status`. If it is not available or auth is missing, ask the user to install/authenticate before continuing.

## 1) Inspect comments needing attention
- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR

## 2) Ask the user for clarification
- Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it
- Ask the user which numbered comments should be addressed

## 3) If user chooses comments
- Apply fixes for the selected comments

Notes:
- If GitHub auth/rate issues appear mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.

## Platform Notes

The original Codex CLI version of this skill preferred an internal `oai_gh` CLI wrapper over plain `gh`, falling back to `gh` when it was not present. That wrapper is a Codex-sandbox-specific convenience and has no Copilot Studio equivalent, so this topic uses plain `gh` throughout. This topic also assumes the agent has a shell/code-execution Action available to actually run `gh` and the bundled script — Copilot Studio does not run local processes by default, so wire that Action (or an equivalent GitHub connector) up before relying on this topic end to end.
