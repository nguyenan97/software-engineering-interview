#!/usr/bin/env python3
"""Build/check a reproducible downloadable lab containing the checked-in source."""
import argparse
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
LABS = {
    "atomic-inbox": ("exercise.py", "solution.py", "verify.py", "README.md"),
    "department-headcount": (
        "setup.sql", "exercise.sql", "solution.sql", "all-departments.sql",
        "transfer.sql", "verify.py", "README.md",
    ),
}


def package(lab="atomic-inbox"):
    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive:
        for name in LABS[lab]:
            entry = ZipInfo(lab + "/" + name, (2020, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            archive.writestr(entry, (ROOT / "labs" / lab / name).read_bytes())
    return buffer.getvalue()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for lab in LABS:
        target = ROOT / "assets/labs" / (lab + ".zip")
        expected = package(lab)
        if args.check:
            if not target.exists() or target.read_bytes() != expected:
                raise SystemExit("Lab download is stale: run python scripts/package_labs.py")
            print(f"{lab}: download matches the exercise and reference sources.")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(expected)
            print(f"Built assets/labs/{lab}.zip")
