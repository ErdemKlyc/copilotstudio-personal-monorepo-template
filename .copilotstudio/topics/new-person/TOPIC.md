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
3. Run the helper when possible:

```sh
python .copilotstudio/topics/new-person/scripts/new_person.py "Person Name" --role "Role or context"
```

4. Edit the generated note with only useful, non-sensitive context.
5. Keep private facts, secrets, health details, account data, and confidential content out of the note.
6. Add or update `Last Verified` when facts may go stale.

## Output

Report the created or updated path and summarize any fields still needing human input.

## Platform Notes

This topic assumes a shell/code-execution Action is available to run the bundled Python script against the vault repo (for example, a knowledge source synced to a repo the agent can also write back to, or a code-execution connector). If no such Action is registered, write the note by hand from the template instead.
