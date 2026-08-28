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

Ask for the repo (`owner/repo`) and PR number, then fetch and address its review comments.

## 1) Inspect comments needing attention
- Call the `fetch-pr-comments` Tool (see Platform Notes) with the repo and PR number.

## 2) Ask the user for clarification
- Number all the review threads and comments and provide a short summary of what would be required to apply a fix for it
- Ask the user which numbered comments should be addressed

## 3) If user chooses comments
- Apply fixes for the selected comments

## Platform Notes

**"Current branch" has no meaning here.** The original Codex CLI version of this topic resolved the PR from a local git checkout's current branch, and shelled out to `gh` (or a Codex-sandbox-specific `oai_gh` wrapper, dropped here since it has no Copilot Studio equivalent). Copilot Studio agents have no working tree at all, so this topic always asks for an explicit `owner/repo` and PR number instead of trying to infer either.

**This one depends on your tenant's connector catalog, unlike `new-person`/`new-project`.** Fetching comments needs a `fetch-pr-comments` Tool, and how you build it depends on what's available under Tools > Add a tool:

- **If Agent flow, custom REST API, or a GitHub connector with the needed actions is available**: build `fetch-pr-comments` calling `GET /repos/{owner}/{repo}/pulls/{pr}/comments` (review comments) and `GET /repos/{owner}/{repo}/issues/{pr}/comments` (issue-level comments), combine and number the results.
- **If only prebuilt Connector actions are available (Flow/MCP/REST API disabled — the common enterprise-lockdown case)**: search "GitHub" in the Connector picker and check what actions it actually exposes. There is no guarantee it covers PR/issue comments specifically — if it doesn't, this topic is blocked in your tenant with no other route available, and that's worth telling the user plainly rather than pretending a workaround exists.

Applying fixes (step 3) still requires a real code-editing capability on the actual repo checkout — this topic can plan the fix and describe it, but committing it back is `gh-commit`'s job, which has its own, more fundamental platform limitation (see its Platform Notes).

<details>
<summary>Legacy option: the bundled Python script</summary>

`scripts/fetch_comments.py` shells out to `gh api graphql` and assumes a local checkout on the current branch. Only useful with a genuine persistently-hosted, git-checked-out environment to run it in — see `.copilotstudio/tools/README.md` for the MCP-server option and why it's no longer the recommended default.

</details>
