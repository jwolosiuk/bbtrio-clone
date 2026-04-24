#!/usr/bin/env python3
"""
Build puzzles.json from circle9puzzle's bbtrio.puzzles.js.

Run this once to mirror their puzzle pool into our repo; the client picks
today's puzzle from it. No daily cron needed because their file is itself
pre-generated (6000 puzzles shipped statically; cycle repeats every ~5.5
years).

Usage:
    tools/build_puzzles.py                  # fetch from circle9puzzle.com
    tools/build_puzzles.py --in local.js    # use a local copy
    tools/build_puzzles.py --out puzzles.json
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

# Re-use the JS-string-list parser from fetch_daily.py.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_daily import fetch_puzzles  # noqa: E402


def compact(desc_json: str) -> str:
    """Encode a full desc JSON as 'blocks|cellClues' (163 chars for 9x9)."""
    d = json.loads(desc_json)
    blocks = "".join(str(b) for b in d["blocks"])  # 0-8 → single digit
    clues = "".join("." if v is None else str(v) for v in d["cellClues"])
    return f"{blocks}|{clues}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default="https://circle9puzzle.com/bbtrio/bbtrio.puzzles.js")
    ap.add_argument("--in", dest="inp", help="read from a local file instead of the URL")
    ap.add_argument("--out", default="puzzles.json")
    args = ap.parse_args()

    src = args.inp or args.url
    print(f"fetching puzzles from {src}", file=sys.stderr)
    puzzles = fetch_puzzles(src)
    out = {
        "S": [compact(p) for p in puzzles["Standard"]],
        "A": [compact(p) for p in puzzles["Advanced"]],
        "E": [compact(p) for p in puzzles["Expert"]],
    }
    Path(args.out).write_text(json.dumps(out, separators=(",", ":")))
    print(f"wrote {args.out}: S={len(out['S'])}, A={len(out['A'])}, E={len(out['E'])}", file=sys.stderr)


if __name__ == "__main__":
    main()
