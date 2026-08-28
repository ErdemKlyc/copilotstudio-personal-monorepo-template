from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TEMPLATES = ROOT / "templates"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "new-project"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a project or experiment.")
    parser.add_argument("name")
    parser.add_argument("--type", choices=["project", "experiment"], default="project")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--slug", default="")
    parser.add_argument("--no-agents", action="store_true")
    args = parser.parse_args()

    today = date.today().isoformat()
    base_slug = args.slug or slugify(args.name)
    if args.type == "experiment":
        entry_id = base_slug
        if not entry_id.startswith("exp-"):
            entry_id = f"exp-{entry_id}-{today}"
        root_dir = ROOT / "experiments"
        template = TEMPLATES / "experiment_README.md"
    else:
        entry_id = base_slug
        root_dir = ROOT / "projects"
        template = TEMPLATES / "project_README.md"

    project_dir = root_dir / entry_id
    readme_path = project_dir / "README.md"
    agents_path = project_dir / "AGENTS.md"
    rel_path = project_dir.relative_to(ROOT).as_posix()

    if project_dir.exists():
        raise FileExistsError(f"path already exists: {rel_path}")

    project_dir.mkdir(parents=True)
    readme = template.read_text().replace("<Project Name>", args.name)
    readme = readme.replace("<Experiment Name>", args.name)
    readme = readme.replace("<Summary>", args.summary)
    readme_path.write_text(readme)
    if not args.no_agents:
        agents_path.write_text((TEMPLATES / "PROJECT_AGENTS.md").read_text())

    print(f"created: {rel_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
