#!/usr/bin/env python3
"""
Fetch today's daily Blueberry Trio puzzle from circle9puzzle.com and write
it to puzzle.txt in our format.

Mirrors the site's selection logic exactly:
  - date key: "D M YYYY" (no zero padding)
  - hash string: f"{date_key} {category} {source} {set_number}"
  - hash function: cyrb53
  - index: hash % len(puzzles[category])
  - source puzzle JSON -> cells grid + groups grid in our format

Usage:
    tools/fetch_daily.py [--date YYYY-MM-DD] [--category Standard|Advanced|Expert]
                        [--source Daily|Plus] [--set N]
                        [--out puzzle.txt] [--archive-dir puzzles]
                        [--puzzles-url URL | --puzzles-file PATH]

Defaults: today (UTC), Standard, Daily, set 0.
"""
from __future__ import annotations
import argparse, datetime as dt, json, re, sys, urllib.request
from pathlib import Path

MASK = 0xFFFFFFFF

def to_i32(x: int) -> int:
    x &= MASK
    return x - 0x100000000 if x >= 0x80000000 else x

def to_u32(x: int) -> int:
    return x & MASK

def imul(a: int, b: int) -> int:
    return to_i32(((to_i32(a) * to_i32(b)) & MASK))

def ursh(x: int, n: int) -> int:
    return to_u32(x) >> n

def cyrb53(s: str, seed: int = 0) -> int:
    h1 = to_i32(0xdeadbeef ^ seed)
    h2 = to_i32(0x41c6ce57 ^ seed)
    for ch in s:
        c = ord(ch)
        h1 = imul(h1 ^ c, 2654435761)
        h2 = imul(h2 ^ c, 1597334677)
    h1 = imul(h1 ^ ursh(h1, 16), 2246822507)
    h1 = to_i32(h1 ^ imul(h2 ^ ursh(h2, 13), 3266489909))
    h2 = imul(h2 ^ ursh(h2, 16), 2246822507)
    h2 = to_i32(h2 ^ imul(h1 ^ ursh(h1, 13), 3266489909))
    return 4294967296 * (to_u32(h2) & 2097151) + to_u32(h1)


def date_key(d: dt.date) -> str:
    return f"{d.day} {d.month} {d.year}"


def fetch_puzzles(source: str) -> dict:
    """Return {category: [desc_json_string, ...]} from circle9puzzle.com/bbtrio/bbtrio.puzzles.js."""
    if source.startswith("http"):
        req = urllib.request.Request(source, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) bbtrio-clone-updater"
        })
        with urllib.request.urlopen(req, timeout=30) as r:
            text = r.read().decode("utf-8")
    else:
        text = Path(source).read_text()
    # The file defines BBTRIO.puzzles = {}; and then entries like
    # BBTRIO.puzzles["Standard"] = [ '...', '...', ... ];
    out: dict[str, list[str]] = {}
    for cat in ("Standard", "Advanced", "Expert"):
        m = re.search(
            rf'BBTRIO\.puzzles\["{cat}"\]\s*=\s*\[(.*?)\];',
            text,
            re.S,
        )
        if not m:
            continue
        body = m.group(1)
        # Entries are single-quoted strings separated by commas+whitespace.
        # The JSON inside uses double quotes, so splitting on lines is safe
        # enough but we be pedantic and strip trailing comma / whitespace.
        items = re.findall(r"'((?:\\'|[^'])*)'", body)
        out[cat] = items
    return out


def select_puzzle(puzzles: dict, date: dt.date, category: str, source: str, set_number: int) -> str:
    lst = puzzles[category]
    s = f"{date_key(date)} {category} {source} {set_number}"
    h = cyrb53(s)
    i = h % len(lst)
    return lst[i]


def desc_to_our_format(desc_json: str) -> str:
    desc = json.loads(desc_json)
    rows = desc["size"]["rows"]
    cols = desc["size"]["columns"]
    assert rows == cols, f"expected square grid, got {rows}x{cols}"
    n = rows
    blocks = desc["blocks"]
    cells = desc["cellClues"]
    assert len(blocks) == n * n and len(cells) == n * n

    # Groups: block index -> letter. 9 blocks typical -> A..I.
    unique = []
    for b in blocks:
        if b not in unique:
            unique.append(b)
    letters = {b: chr(ord("A") + i) for i, b in enumerate(unique)}

    out_lines = []
    out_lines.append("# Blueberry Trio — fetched from circle9puzzle.com")
    out_lines.append(f"# Generated {dt.datetime.utcnow().isoformat(timespec='seconds')}Z")
    out_lines.append("# Cells: '.' open, '0'-'9' clue, 'x' pre-placed berry")
    out_lines.append("# Groups: matching letters = same region (each region has N cells)")
    out_lines.append("")
    out_lines.append("# Cells")
    for r in range(n):
        row = []
        for c in range(n):
            v = cells[r * n + c]
            row.append("." if v is None else str(v))
        out_lines.append(" ".join(row))
    out_lines.append("")
    out_lines.append("# Groups")
    for r in range(n):
        row = []
        for c in range(n):
            row.append(letters[blocks[r * n + c]])
        out_lines.append(" ".join(row))
    out_lines.append("")
    return "\n".join(out_lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="YYYY-MM-DD (default: today UTC)")
    ap.add_argument("--category", default=None, choices=["Standard", "Advanced", "Expert"],
                    help="single category; default is to emit all three")
    ap.add_argument("--source", default="Daily", choices=["Daily", "Plus"])
    ap.add_argument("--set", dest="set_number", default=0, type=int)
    ap.add_argument("--out", default=None, help="override single-category output path")
    ap.add_argument("--archive-dir", default="puzzles", help="mirror the daily file into this dir")
    ap.add_argument("--puzzles-url", default="https://circle9puzzle.com/bbtrio/bbtrio.puzzles.js")
    ap.add_argument("--puzzles-file", help="read puzzles.js from local file instead of URL")
    args = ap.parse_args()

    if args.date:
        today = dt.date.fromisoformat(args.date)
    else:
        today = dt.datetime.utcnow().date()

    src = args.puzzles_file or args.puzzles_url
    print(f"fetching puzzles from {src}", file=sys.stderr)
    puzzles = fetch_puzzles(src)
    counts = {k: len(v) for k, v in puzzles.items()}
    print(f"available categories: {counts}", file=sys.stderr)

    categories = [args.category] if args.category else ["Standard", "Advanced", "Expert"]
    for cat in categories:
        if cat not in puzzles:
            sys.exit(f"category {cat!r} not in {list(puzzles)}")
        desc = select_puzzle(puzzles, today, cat, args.source, args.set_number)
        print(f"selected {today.isoformat()} / {cat} / {args.source} / set {args.set_number}", file=sys.stderr)
        out_text = desc_to_our_format(desc)

        if args.out and args.category:
            out = Path(args.out)
        else:
            out = Path(f"puzzle-{cat.lower()}.txt")
        out.write_text(out_text)
        print(f"wrote {out}", file=sys.stderr)

        if args.archive_dir:
            arch = Path(args.archive_dir) / f"{today.isoformat()}_{cat}.txt"
            arch.parent.mkdir(parents=True, exist_ok=True)
            arch.write_text(out_text)
            print(f"wrote {arch}", file=sys.stderr)


if __name__ == "__main__":
    main()
