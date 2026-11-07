"""Download the package's stated public inputs and verify their SHA-256 hashes.

Python 3.10+ standard library only; no shell-specific commands are required.
URLs/hashes are inherited from the review package. Successful checksum checks
establish file identity with that package, not independent source provenance.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import tempfile
import urllib.request

DATA_ROOT = Path(__file__).resolve().parents[1] / "data"
BASE = "https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive"
FILES = {
    2023: ("results.csv", "828874a3cf0fa1bbb4c3da6a87e5822b8563bbc04b21f9869479480dbcff410c"),
    2024: ("results.csv", "7f2c2dbf6989d00b80a7351de4bb3af4b52b21cc52d5c947891bbc4f4e5cbe49"),
    2025: ("results.csv", "2d1f65308877282edfb4470520eabbc08cb499118432a3dcec6a66c086aa2baa"),
    2026: ("survey_results_public.csv", "ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c"),
}


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fetch_verified(url: str, destination: Path, expected: str, replace: bool) -> None:
    if destination.exists():
        if digest_file(destination) == expected:
            print(f"Already verified: {destination}")
            return
        if not replace:
            raise RuntimeError(
                f"Existing file has a different hash: {destination}. "
                "Preserved it. Use --replace only after reviewing that difference."
            )
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=".partial", delete=False) as handle:
            temporary = Path(handle.name)
            digest = hashlib.sha256()
            request = urllib.request.Request(url, headers={"User-Agent": "adoption-without-confidence-research"})
            with urllib.request.urlopen(request, timeout=120) as response:
                for block in iter(lambda: response.read(1024 * 1024), b""):
                    digest.update(block)
                    handle.write(block)
        actual = digest.hexdigest()
        if actual != expected:
            raise RuntimeError(f"Checksum mismatch for {url}: expected {expected}, got {actual}. No input file was replaced.")
        os.replace(temporary, destination)
        temporary = None
        print(f"Downloaded and verified: {destination}")
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--years", nargs="+", type=int, choices=sorted(FILES), default=sorted(FILES))
    parser.add_argument("--replace", action="store_true", help="Replace existing mismatched files only after the new download passes its checksum.")
    args = parser.parse_args()
    for year in args.years:
        filename, checksum = FILES[year]
        fetch_verified(f"{BASE}/{year}/{filename}", DATA_ROOT / str(year) / "survey_results_public.csv", checksum, args.replace)


if __name__ == "__main__":
    main()
