"""Run Ruff when the optional dev dependency is installed."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys


def main() -> int:
    if importlib.util.find_spec("ruff") is None:
        message = "ruff is not installed; skipping optional lint"
        if os.environ.get("REQUIRE_RUFF") == "1":
            print(f"{message}. Install with: python3 -m pip install -e '.[dev]'")
            return 1
        print(f"{message}. Install with: python3 -m pip install -e '.[dev]'")
        return 0

    return subprocess.call([sys.executable, "-m", "ruff", "check", "."])


if __name__ == "__main__":
    raise SystemExit(main())
