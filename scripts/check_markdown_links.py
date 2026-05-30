"""Check local Markdown links in the repository."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    missing: list[str] = []
    for markdown_path in sorted(ROOT.rglob("*.md")):
        if ".git" in markdown_path.parts:
            continue
        text = markdown_path.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            clean_target = target.strip()
            if _is_external_or_anchor(clean_target):
                continue
            target_without_anchor = clean_target.split("#", 1)[0]
            resolved = (markdown_path.parent / target_without_anchor).resolve()
            if not resolved.exists():
                rel_markdown = markdown_path.relative_to(ROOT)
                missing.append(f"{rel_markdown}: {clean_target}")

    if missing:
        print("Missing local Markdown links:")
        print("\n".join(missing))
        return 1

    print("Markdown links OK")
    return 0


def _is_external_or_anchor(target: str) -> bool:
    return (
        target.startswith("#")
        or target.startswith("http://")
        or target.startswith("https://")
        or target.startswith("mailto:")
    )


if __name__ == "__main__":
    raise SystemExit(main())
