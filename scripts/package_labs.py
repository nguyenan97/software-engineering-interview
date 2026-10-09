#!/usr/bin/env python3
"""Build/check a reproducible downloadable lab containing the checked-in source."""
import argparse
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]


def package():
    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive:
        for name in ("exercise.py", "solution.py", "verify.py", "README.md"):
            entry = ZipInfo("atomic-inbox/" + name, (2020, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            archive.writestr(entry, (ROOT / "labs/atomic-inbox" / name).read_bytes())
    return buffer.getvalue()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "assets/labs/atomic-inbox.zip"
    expected = package()
    if args.check:
        if not target.exists() or target.read_bytes() != expected:
            raise SystemExit("Lab download is stale: run python scripts/package_labs.py")
        print("Lab download matches the exercise and reference sources.")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(expected)
        print("Built assets/labs/atomic-inbox.zip")
