---
name: gh-commit
description: "Review git changes and split them into semantic commits with clear messages. Use when the user asks to commit work, clean up local history, or group a mixed diff into logical commits. Do not commit on main or master unless the user explicitly asks."
last_edited: 2026-06-15
---

# GH Commit

## Trigger Phrases

- "commit my changes"
- "split this diff into commits"
- "clean up my local history"
- "group these changes into commits"

## Goal

Turn the current working tree into a small set of clean commits without mixing unrelated changes.

## Workflow

1. Verify git context.
- Run `git rev-parse --show-toplevel` and `git status -sb`.
- Read the branch with `git branch --show-current`.
- If the branch is `main` or `master`, stop and ask the user to switch/create a branch (recommend `copilot/...`) unless they explicitly asked to commit on that branch.

2. Inspect all changes before staging anything.
- Run `git diff --stat` and `git diff --cached --stat`.
- List untracked files with `git ls-files --others --exclude-standard`.
- Read actual hunks with `git diff` and `git diff --cached`.
- Include untracked files in the review (read them if needed) so commit grouping decisions cover the full diff.

3. Propose semantic commit groups.
- Group by intent, not just file type (for example: bug fix, refactor, tests, docs).
- Keep user-authored unrelated work separate.
- Call out any files that need partial staging because they contain mixed concerns.

4. Create each commit group.
- Stage only the files or hunks for that group (`git add <paths>` or `git add -p`).
- Verify exactly what is staged with `git diff --cached --stat` and `git diff --cached`.
- Commit with a concise imperative message.
- Prefer `type(scope): summary` when the change has an obvious type/scope; otherwise use a clear plain-English summary.

5. Repeat until done.
- After each commit, re-check `git status -sb`.
- Continue until all intended changes are committed or intentionally left uncommitted.

6. Report the result.
- List the commit SHAs and messages in order.
- Note any remaining staged/unstaged/untracked files.

## Safety Rules

- Avoid `git add -A` unless the entire remaining diff belongs in one commit.
- Use partial staging when a file mixes multiple concerns.
- Do not rewrite or discard user changes unless explicitly asked.
- If grouping is ambiguous, ask before committing.

## Platform Notes

**This topic does not fit a Copilot Studio agent, and there is no Tool that fixes that.** Everything above assumes a live git working tree with a mix of staged/unstaged/untracked changes to inspect and group — that concept doesn't exist for a Copilot Studio agent, which has no working directory at all. Unlike `new-person`/`new-project` (which just need to create one known file, easy to replicate with a "Create file" flow action) or `gh-address-comments`/`gh-fix-ci` (which just need to read GitHub state given explicit repo/PR numbers), "split my mixed working-tree diff into semantic commits" is inherently an operation on a local checkout, not on a document library or a REST API response.

Keep this topic for reference, but expect to actually run it from somewhere that has real git access — a coding agent with shell access (for example GitHub Copilot's coding agent, or a human's local git client), not this vault assistant. If you want an agent-flow-only approximation, the closest honest option is the GitHub Contents API (`PUT /repos/{owner}/{repo}/contents/{path}`), which can commit a *single known file* with a given path and content — useful for "update one file" automation, not for "group an arbitrary diff into semantic commits."
