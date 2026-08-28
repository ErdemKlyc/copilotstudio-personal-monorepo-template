---
name: new-person
description: Create or update a public-safe person note under `people/` from the repository's `people/person.md` template. Use when the user asks to add a collaborator, create a person profile, remember someone's preferences, make a people note, or bootstrap `people/<name>.md`.
last_edited: 2026-06-15
---

# New Person

## Trigger Phrases

- "add a person note"
- "create a profile for this collaborator"
- "remember this person's preferences"

Create a durable, public-safe note for a human collaborator.

## Workflow

1. Read `people/README.md` and `people/person.md`.
2. Choose a lowercase hyphenated slug from the person's name.
3. Build the note content from the template, then call the `create-vault-file` Tool (see Platform Notes) to write it.
4. Edit the generated note with only useful, non-sensitive context.
5. Keep private facts, secrets, health details, account data, and confidential content out of the note.
6. Add or update `Last Verified` when facts may go stale.

## Output

Report the created or updated path and summarize any fields still needing human input.

## Platform Notes

Write-back for this topic uses the shared **`create-vault-file`** Tool (see `.copilotstudio/README.md` > "The create-vault-file Tool" for full setup — it's a single prebuilt-connector Tool reused by `new-person`, `new-project`, and any other topic that needs to write one file into the vault). No Flow, no server, no custom code: it's the SharePoint (or OneDrive for Business) **"Create file"** connector action, added directly as a Tool.

To create a person note: build the content by reading `people/person.md` from Knowledge, replacing `<Person Name>` with the given name, the role placeholder line with the given role (or "TBD"), and `YYYY-MM-DD` with today's date, and building the slug (lowercase, letters/numbers/hyphens only) from the name — then call `create-vault-file` with folder path `people` and file name `<slug>.md`.

If `create-vault-file` isn't registered yet, write the note by hand from the template instead of guessing at file access you don't have.

<details>
<summary>Legacy option: the bundled Python script</summary>

`scripts/new_person.py` implements the same logic and is still in this folder. It only helps if you have a genuine, persistently-hosted way to run it against a live copy of this vault (see `.copilotstudio/tools/README.md` for the MCP-server option) — in a locked-down enterprise tenant where only prebuilt connectors are available as Tools (no Flow, no MCP, no custom REST API), `create-vault-file` is the one that actually works.

</details>
