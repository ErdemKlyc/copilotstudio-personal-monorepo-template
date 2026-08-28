---
name: "yeet"
description: "Use only when the user explicitly asks to stage, commit, push, and open a GitHub pull request in one flow using the GitHub CLI (`gh`)."
last_edited: 2026-06-15
---

# Yeet

## Trigger Phrases

- "yeet this"
- "stage, commit, push, and open a PR"
- "ship this as a PR"

## Prerequisites

- Require GitHub CLI `gh`. Check `gh --version`. If missing, ask the user to install `gh` and stop.
- Require authenticated `gh` session. Run `gh auth status`. If not authenticated, ask the user to run `gh auth login` (and re-run `gh auth status`) before continuing.

## Naming conventions

- Branch: `copilot/{description}` when starting from main/master/default.
- Commit: `{description}` (terse).
- PR title: `[copilot] {description}` summarizing the full diff.

## Workflow

- If on main/master/default, create a branch: `git checkout -b "copilot/{description}"`
- Otherwise stay on the current branch.
- Confirm status, then stage everything: `git status -sb` then `git add -A`.
- Commit tersely with the description: `git commit -m "{description}"`
- Run checks if not already. If checks fail due to missing deps/tools, install dependencies and rerun once.
- Push with tracking: `git push -u origin $(git branch --show-current)`
- If git push fails due to workflow auth errors, pull from master and retry the push.
- Open a PR and edit title/body to reflect the description and the deltas: `GH_PROMPT_DISABLED=1 GIT_TERMINAL_PROMPT=0 gh pr create --draft --fill --head $(git branch --show-current)`
- Write the PR description to a temp file with real newlines (e.g. pr-body.md ... EOF) and run pr-body.md to avoid \\n-escaped markdown.
- PR description (markdown) must be detailed prose covering the issue, the cause and effect on users, the root cause, the fix, and any tests or checks used to validate.

## Platform Notes

**Same fundamental gap as `gh-commit`, plus more of it.** This entire flow — creating a branch, staging a working tree, running local checks, pushing, opening a PR — assumes a live local git checkout with a shell to run commands in. Copilot Studio agents have neither. There is no Tool or Agent flow that reasonably substitutes for "run the project's test suite against a working copy" from inside a knowledge-vault chatbot.

Keep this topic for reference, but run it from somewhere with actual repo/shell access — a coding agent (for example GitHub Copilot's coding agent) or a human's local git client — not this vault assistant. The `codex/...` branch/PR-title convention from the original template is renamed to `copilot/...` here; change it back if your team uses a different prefix, wherever you actually run this.
