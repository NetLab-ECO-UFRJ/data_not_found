"""
Add `notes_pt:` stubs alongside every `notes:` field across platform YAML files.

The Quarto profile-aware renderer reads `notes_pt` when the active profile is
`pt` and falls back to `notes` otherwise. Stubbing the PT field with the EN
text keeps the PT build from going blank while incremental translation
proceeds.

Idempotent: skips entries that already have `notes_pt`.
"""

from __future__ import annotations

import sys
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"


def find_target_files() -> list[Path]:
    files = []
    for sub in ("global", "regional"):
        root = DATA_DIR / sub
        if root.exists():
            files.extend(p for p in root.rglob("*.yml") if p.is_file())
    return sorted(files)


def stub_file(path: Path, yaml: YAML) -> tuple[int, int]:
    """Return (notes_added, notes_skipped) for a single YAML file."""
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.load(fh)

    if data is None:
        return 0, 0

    added = 0
    skipped = 0

    for key, value in data.items():
        if not key.endswith("_answers") or not isinstance(value, list):
            continue
        for entry in value:
            if not isinstance(entry, CommentedMap):
                continue
            if "notes" not in entry:
                continue
            if "notes_pt" in entry:
                skipped += 1
                continue
            notes_value = entry["notes"]
            keys = list(entry.keys())
            insert_at = keys.index("notes") + 1
            entry.insert(insert_at, "notes_pt", notes_value)
            added += 1

    if added:
        with path.open("w", encoding="utf-8") as fh:
            yaml.dump(data, fh)
    return added, skipped


def main() -> int:
    files = find_target_files()
    if not files:
        print("No YAML files found under data/global or data/regional", file=sys.stderr)
        return 1

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000  # avoid auto-wrapping long note strings
    yaml.indent(mapping=2, sequence=2, offset=0)

    total_added = 0
    total_skipped = 0
    for path in files:
        added, skipped = stub_file(path, yaml)
        total_added += added
        total_skipped += skipped
        rel = path.relative_to(REPO_ROOT)
        if added:
            print(f"  {rel}: +{added}{' (skipped ' + str(skipped) + ')' if skipped else ''}")
        elif skipped:
            print(f"  {rel}: already stubbed ({skipped})")

    print(f"\nTotal: {total_added} notes_pt stubs added, {total_skipped} entries already had notes_pt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
