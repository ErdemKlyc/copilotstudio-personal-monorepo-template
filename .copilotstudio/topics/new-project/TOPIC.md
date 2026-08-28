---
name: new-project
description: Bootstrap a new project or experiment directory with README and optional `AGENTS.md` files. Use when the user asks to create a new project, start an experiment, add a workspace entry, scaffold a project folder, or bootstrap durable work in this personal monorepo.
last_edited: 2026-06-15
---

# New Project

## Trigger Phrases

- "start a new project"
- "create a new experiment"
- "bootstrap a project folder"

Create a project or experiment that agents can discover later.

## Workflow

1. Read root `AGENTS.md` and `README.md`.
2. Decide whether the work is a long-lived `project` or short-lived `experiment`.
3. Use a lowercase hyphenated slug. Experiments must use `exp-<topic>-YYYY-MM-DD`.
4. Call `create-vault-folder` for the new project folder, then `create-vault-file` twice for its `README.md` and `AGENTS.md` (see Platform Notes).
5. Add project-specific commands, data sources, and safety gates to the generated `AGENTS.md` if they matter.

## Output

Report the created folder and any missing fields that need human input.

## Platform Notes

Write-back for this topic uses two shared prebuilt-connector Tools (see `.copilotstudio/README.md` for full setup): **`create-vault-folder`** (SharePoint/OneDrive "Create new folder" action) and **`create-vault-file`** (the same "Create file" Tool `new-person` uses). SharePoint's "Create file" action does **not** auto-create missing folders — it fails if the target folder doesn't exist yet — so the folder must be created first, as a separate Tool call:

1. Build the slug (lowercase, hyphenated). For an experiment, prefix with `exp-` and suffix with today's date as `YYYY-MM-DD`.
2. Call `create-vault-folder` with parent folder `projects` (or `experiments`) and the slug as the new folder name.
3. Build `README.md` content from `templates/project_README.md` (or `templates/experiment_README.md`) — replace `<Project Name>`/`<Experiment Name>` with the given name and `<Summary>` with the given summary — then call `create-vault-file` with that folder path and file name `README.md`.
4. Call `create-vault-file` again with the same folder path, file name `AGENTS.md`, and `templates/PROJECT_AGENTS.md`'s content as-is.

If these Tools aren't registered yet, create the folder and files by hand from `templates/project_README.md`, `templates/experiment_README.md`, and `templates/PROJECT_AGENTS.md` instead of guessing at file access you don't have.

<details>
<summary>Legacy option: the bundled Python script</summary>

`scripts/new_project.py` implements the same logic. Only useful with a genuine persistently-hosted way to run it against a live copy of this vault — see `.copilotstudio/tools/README.md` for the MCP-server option. In a locked-down enterprise tenant where only prebuilt connectors are available as Tools (no Flow, no MCP, no custom REST API), `create-vault-folder`/`create-vault-file` are what actually work.

</details>
