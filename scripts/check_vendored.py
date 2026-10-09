#!/usr/bin/env python3
"""Check the vendored reference RTL matches the hashes in VENDORED.md.

``third_party/CORDIC/`` is a verbatim copy of part of the reference repo at a
pinned commit. This script recomputes every file's SHA-256 and compares it
with the table in ``VENDORED.md``, so an accidental edit (or a partial
update) fails CI instead of silently changing the hardware the golden model
is checked against. Exit status 0 = all match.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parents[1] / "third_party" / "CORDIC"
ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`\s*\|\s*$")


def main() -> int:
    rows = [m.groups() for line in (DIR / "VENDORED.md").read_text().splitlines() if (m := ROW.match(line))]
    if not rows:
        print("no hash rows found in VENDORED.md")
        return 1
    bad = 0
    for name, want in rows:
        got = hashlib.sha256((DIR / name).read_bytes()).hexdigest() if (DIR / name).exists() else "missing"
        ok = got == want
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} {name} {got[:16]}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
