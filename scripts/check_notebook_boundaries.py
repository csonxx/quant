"""Keep notebooks exploratory by blocking reusable logic definitions."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_ROOT = ROOT / "notebooks"
LOGIC_RE = re.compile(r"^\s*(def|class)\s+\w+")
PATH_HACK_RE = re.compile(r"sys\.path\.(append|insert)|PYTHONPATH")


def main() -> int:
    notebooks = sorted(NOTEBOOK_ROOT.rglob("*.ipynb"))
    if not notebooks:
        print("No notebooks found")
        return 0

    violations: list[str] = []
    for notebook in notebooks:
        with notebook.open(encoding="utf-8") as handle:
            payload = json.load(handle)
        for cell_index, cell in enumerate(payload.get("cells", []), start=1):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            for line_number, line in enumerate(source.splitlines(), start=1):
                if LOGIC_RE.search(line):
                    violations.append(
                        _format_violation(
                            notebook,
                            cell_index,
                            line_number,
                            "move reusable def/class logic to src/ and tests/",
                        )
                    )
                if PATH_HACK_RE.search(line):
                    violations.append(
                        _format_violation(
                            notebook,
                            cell_index,
                            line_number,
                            "do not patch import paths inside notebooks",
                        )
                    )

    if violations:
        print("Notebook boundary violations:")
        print("\n".join(violations))
        return 1

    print("Notebook boundaries OK")
    return 0


def _format_violation(notebook: Path, cell_index: int, line_number: int, message: str) -> str:
    return f"{notebook.relative_to(ROOT)} cell {cell_index} line {line_number}: {message}"


if __name__ == "__main__":
    raise SystemExit(main())
