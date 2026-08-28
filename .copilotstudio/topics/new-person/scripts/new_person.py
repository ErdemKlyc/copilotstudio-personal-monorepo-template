from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PEOPLE_DIR = ROOT / "people"
TEMPLATE = PEOPLE_DIR / "person.md"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "new-person"


def build_note(name: str, role: str) -> str:
    template = TEMPLATE.read_text()
    today = date.today().isoformat()
    note = template.replace("<Person Name>", name)
    note = note.replace(
        "What this person does or how they relate to this workspace.",
        role or "TBD",
    )
    note = note.replace("YYYY-MM-DD", today)
    return note


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a people note.")
    parser.add_argument("name")
    parser.add_argument("--role", default="")
    parser.add_argument("--slug", default="")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    slug = args.slug or slugify(args.name)
    path = PEOPLE_DIR / f"{slug}.md"
    if path.exists() and not args.force:
        print(f"exists: {path.relative_to(ROOT)}")
        return 0

    PEOPLE_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(build_note(args.name, args.role))
    print(f"created: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
