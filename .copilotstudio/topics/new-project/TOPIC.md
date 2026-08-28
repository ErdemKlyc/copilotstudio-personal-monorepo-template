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
4. Run the helper when possible:

```sh
python .copilotstudio/topics/new-project/scripts/new_project.py "Project Name" --summary "One-line summary"
```

For an experiment:

```sh
python .copilotstudio/topics/new-project/scripts/new_project.py "Experiment Name" --type experiment --summary "One-line summary"
```

5. Add project-specific commands, data sources, and safety gates to the generated `AGENTS.md` if they matter.

## Output

Report the created folder and any missing fields that need human input.

## Platform Notes

This topic assumes a shell/code-execution Tool is available to run the bundled Python script against the vault repo. If no such Tool is registered, create the folder and files by hand from `templates/project_README.md`, `templates/experiment_README.md`, and `templates/PROJECT_AGENTS.md`.
