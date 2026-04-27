#!/usr/bin/env python3
"""
Analyze a Blueberry Trio session: classify each good move by the minimum
number of constraints needed to derive it from the state before the move.

Usage:
    tools/analyze_session.py path/to/session.json
    tools/analyze_session.py --device DEVICE_ID         # fetch from Supabase
    tools/analyze_session.py --device DEVICE_ID --date 2026-04-24

Reads:
    config.json  for Supabase URL + anon key
    puzzles.json for the puzzle definition by (puzzle_date, category)

Constraint types considered:
    row(N), col(L), block(...), clue(LN=V)
A move is 'single-constraint' iff applying ONE constraint's standard
fill-or-mark rule to the state-just-before-the-move forces the move.
Otherwise we search for the smallest combination (chain) of constraints
that together force it.
"""
from __future__ import annotations
import argparse, json, sys, urllib.request, datetime as dt
from pathlib import Path
from collections import defaultdict, Counter
from itertools import combinations

# Re-use the cyrb53 hash and puzzle-pool parser used by the in-game JS
# selector and the daily fetcher.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_daily import cyrb53  # noqa: E402

PER = 3


def load_puzzles_json(repo_root: Path) -> dict:
    """Return the same {S, A, E} structure shipped to the browser."""
    return json.loads((repo_root / "puzzles.json").read_text())


def short_cat(cat: str) -> str:
    return {"Standard": "S", "Advanced": "A", "Expert": "E"}[cat]


def pick_puzzle(pool: dict, puzzle_date: dt.date, category: str) -> dict:
    """Replicate the client's daily picker."""
    ds = f"{puzzle_date.day} {puzzle_date.month} {puzzle_date.year}"
    h = cyrb53(f"{ds} {category} Daily 0")
    lst = pool[short_cat(category)]
    entry = lst[h % len(lst)]
    blocks_str, clues_str = entry.split("|")
    n = 9
    clues = {}
    blocks_grid = []
    cells_grid = []
    for r in range(n):
        cells_grid.append([clues_str[r * n + c] for c in range(n)])
        blocks_grid.append([int(blocks_str[r * n + c]) for c in range(n)])
        for c in range(n):
            ch = clues_str[r * n + c]
            if ch != ".":
                clues[(r, c)] = int(ch)
    return {"size": n, "clues": clues, "blocks": blocks_grid}


# --- chess coordinates ---
def row_label(r): return str(r + 1)
def col_label(c): return chr(ord("a") + c)
def cell_label(r, c): return f"{col_label(c)}{row_label(r)}"


def block_label(blocks, bid):
    cells = []
    for r in range(9):
        for c in range(9):
            if blocks[r][c] == bid:
                cells.append((r, c))
    rows = sorted({r for r, _ in cells})
    cols = sorted({c for _, c in cells})
    if (max(rows) - min(rows) + 1) * (max(cols) - min(cols) + 1) == len(cells):
        rr = row_label(min(rows)) if len(rows) == 1 else f"{row_label(min(rows))}-{row_label(max(rows))}"
        cc = col_label(min(cols)) if len(cols) == 1 else f"{col_label(min(cols))}-{col_label(max(cols))}"
        return f"block({rr}, {cc})"
    # irregular: anchor at top-left
    top = min(rows)
    left = min(c for r, c in cells if r == top)
    return f"block(containing {cell_label(top, left)})"


# --- constraint definitions ---
def all_constraints(puzzle):
    """Return list of (label, cell_list, target_count, is_clue).
    For row/col/block target_count == 3 (PER). For clues, target_count is the value."""
    n = puzzle["size"]
    clues = puzzle["clues"]
    blocks = puzzle["blocks"]
    out = []
    for r in range(n):
        cells = [(r, c) for c in range(n) if (r, c) not in clues]
        out.append((f"row({row_label(r)})", cells, PER, False))
    for c in range(n):
        cells = [(r, c) for r in range(n) if (r, c) not in clues]
        out.append((f"col({col_label(c)})", cells, PER, False))
    bids = sorted({blocks[r][c] for r in range(n) for c in range(n)})
    for bid in bids:
        cells = [(r, c) for r in range(n) for c in range(n)
                 if blocks[r][c] == bid and (r, c) not in clues]
        out.append((block_label(blocks, bid), cells, PER, False))
    for (cr, cc), want in clues.items():
        ns = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in clues:
                    ns.append((nr, nc))
        out.append((f"clue({cell_label(cr, cc)}={want})", ns, want, True))
    return out


def apply_constraint_once(state, cells, target):
    """One pass of the standard 'fill-with-berries-or-marks' rule for a single
    constraint. Mutates `state` in place. Returns True if anything changed."""
    berries = sum(1 for r, c in cells if state[r][c] == 1)
    open_cells = [(r, c) for r, c in cells if state[r][c] == 0]
    need = target - berries
    if need < 0 or need > len(open_cells):
        return False
    if not open_cells:
        return False
    if need == 0:
        for r, c in open_cells:
            state[r][c] = 2
        return True
    if need == len(open_cells):
        for r, c in open_cells:
            state[r][c] = 1
        return True
    return False


def clone(state):
    return [row[:] for row in state]


def empty_state(n=9):
    return [[0] * n for _ in range(n)]


def replay_to_click(move_log, target_index):
    """Replay events up to (but not including) move_log[target_index].
    Returns the state at that moment."""
    s = empty_state()
    stack = []
    for i in range(target_index):
        e = move_log[i]
        t = e.get("type")
        if t == "click":
            stack.append(clone(s))
            s[e["r"]][e["c"]] = e["to"]
        elif t == "undo":
            if stack:
                s = stack.pop()
        elif t == "reset":
            stack.append(clone(s))
            s = empty_state()
    return s


def classify_move(state_before, click, constraints):
    """Find the minimum-size constraint chain that forces this click.
    Returns (size, [labels]) or (None, []) if no chain up to size 3 works."""
    r, c, target_v = click["r"], click["c"], click["to"]

    # Single constraint
    for label, cells, tgt, _is_clue in constraints:
        if (r, c) not in cells:
            continue
        s2 = clone(state_before)
        if apply_constraint_once(s2, cells, tgt) and s2[r][c] == target_v:
            return (1, [label])

    # Pairs (A then B)
    for (la, ca, ta, _), (lb, cb, tb, _) in combinations(
            [c for c in constraints if (r, c[1])], 2):
        pass  # placeholder; replaced below

    relevant = [c for c in constraints]  # consider all
    for la, ca, ta, _ in relevant:
        s_after_a = clone(state_before)
        if not apply_constraint_once(s_after_a, ca, ta):
            continue
        # If A already forces it, skip (already caught above)
        if s_after_a[r][c] == target_v:
            continue
        for lb, cb, tb, _ in relevant:
            if lb == la:
                continue
            if (r, c) not in cb:
                continue
            s_after_b = clone(s_after_a)
            if apply_constraint_once(s_after_b, cb, tb) and s_after_b[r][c] == target_v:
                return (2, [la, lb])

    # Triples (apply A → B → C)
    for la, ca, ta, _ in relevant:
        sA = clone(state_before)
        if not apply_constraint_once(sA, ca, ta):
            continue
        if sA[r][c] == target_v:
            continue
        for lb, cb, tb, _ in relevant:
            if lb == la:
                continue
            sB = clone(sA)
            if not apply_constraint_once(sB, cb, tb):
                continue
            if sB[r][c] == target_v:
                continue
            for lc, cc, tc, _ in relevant:
                if lc in (la, lb):
                    continue
                if (r, c) not in cc:
                    continue
                sC = clone(sB)
                if apply_constraint_once(sC, cc, tc) and sC[r][c] == target_v:
                    return (3, [la, lb, lc])

    return (None, [])


def is_good_click(state_before, click, solution):
    """A click is 'good' if its target value matches the unique solution OR
    a same-cell follow-up within 2s reaches the solution value (cycle through ×)."""
    r, c, to = click["r"], click["c"], click["to"]
    return solution[r][c] == to


def solve_unique(puzzle):
    """Backtracking solver returning the unique state."""
    n = puzzle["size"]
    clues = puzzle["clues"]
    constraints = all_constraints(puzzle)

    def propagate(s):
        changed = True
        while changed:
            changed = False
            for label, cells, tgt, _ in constraints:
                berries = sum(1 for r, c in cells if s[r][c] == 1)
                opens = [(r, c) for r, c in cells if s[r][c] == 0]
                need = tgt - berries
                if need < 0 or need > len(opens):
                    return False
                if not opens:
                    continue
                if need == 0:
                    for r, c in opens:
                        s[r][c] = 2
                    changed = True
                elif need == len(opens):
                    for r, c in opens:
                        s[r][c] = 1
                    changed = True
        return True

    def is_complete(s):
        for r in range(n):
            for c in range(n):
                if (r, c) in clues:
                    continue
                if s[r][c] == 0:
                    return False
        return True

    def rec(s):
        cp = clone(s)
        if not propagate(cp):
            return None
        if is_complete(cp):
            return cp
        target = next(((r, c) for r in range(n) for c in range(n)
                       if (r, c) not in clues and cp[r][c] == 0), None)
        if not target:
            return cp
        for v in (1, 2):
            t = clone(cp)
            t[target[0]][target[1]] = v
            res = rec(t)
            if res is not None:
                return res
        return None

    s0 = empty_state()
    return rec(s0)


def analyze_session(session: dict, pool: dict):
    """Yield analysis lines for a single session row from the DB."""
    cat = session["category"]
    date = dt.date.fromisoformat(session["puzzle_date"])
    data = session.get("data") or {}
    cat_state = (data.get("categories") or {}).get(cat) or {}
    move_log = cat_state.get("moveLog") or []

    puzzle = pick_puzzle(pool, date, cat)
    constraints = all_constraints(puzzle)
    solution = solve_unique(puzzle)
    if solution is None:
        return [f"  could not solve puzzle for {date} {cat}; skipping"]

    out = []
    out.append(f"Session {date} {cat} ({len(move_log)} events)")
    counts = Counter()
    by_label = Counter()
    total_thinking_ms = 0
    last_t = 0
    for i, e in enumerate(move_log):
        if e.get("type") != "click":
            continue
        if not is_good_click(None, e, solution):
            continue
        s_before = replay_to_click(move_log, i)
        size, labels = classify_move(s_before, e, constraints)
        elapsed = e["t"] - last_t
        last_t = e["t"]
        total_thinking_ms += elapsed
        if size is None:
            tag = "deeper"
            counts["deeper"] += 1
        elif size == 1:
            tag = f"single via {labels[0]}"
            counts["single"] += 1
            by_label[labels[0]] += 1
        else:
            tag = f"cross-{size} via {' → '.join(labels)}"
            counts[f"cross-{size}"] += 1
            for l in labels:
                by_label[l] += 1
        out.append(f"  {e['t']/1000:6.1f}s  ({cell_label(e['r'], e['c'])}={e['to']})  {tag}")

    out.append("")
    out.append(f"  Totals: {dict(counts)}")
    if by_label:
        out.append(f"  Most-leveraged constraints (top 8):")
        for label, n in by_label.most_common(8):
            out.append(f"    {n}× {label}")
    return out


def fetch_from_supabase(url: str, key: str, device_id: str, date: str | None = None) -> list[dict]:
    base = url.rstrip("/")
    q = f"device_id=eq.{device_id}&order=created_at.desc"
    if date:
        q += f"&puzzle_date=eq.{date}"
    req = urllib.request.Request(
        f"{base}/rest/v1/sessions?{q}",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "x-device-id": device_id,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", help="local session JSON (file or directory)")
    ap.add_argument("--device", help="device_id to fetch sessions from Supabase")
    ap.add_argument("--date", help="puzzle_date filter (YYYY-MM-DD)")
    ap.add_argument("--config", default="config.json")
    ap.add_argument("--puzzles", default="puzzles.json")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    pool = load_puzzles_json(repo_root)

    sessions: list[dict] = []
    if args.device:
        cfg = json.loads((repo_root / args.config).read_text())
        sessions = fetch_from_supabase(cfg["supabase_url"], cfg["supabase_anon_key"], args.device, args.date)
    elif args.path:
        p = Path(args.path)
        if p.is_dir():
            files = sorted(p.glob("*.json"))
        else:
            files = [p]
        for f in files:
            j = json.loads(f.read_text())
            if isinstance(j, list):
                sessions.extend(j)
            elif "categories" in j:
                # Snapshot from ⬇ log — emit one pseudo-row per category
                for cat, cs in (j.get("categories") or {}).items():
                    sessions.append({
                        "puzzle_date": j["date"],
                        "category": cat,
                        "data": j,
                    })
            else:
                sessions.append(j)
    else:
        sys.exit("provide a session file or --device DEVICE_ID")

    if not sessions:
        print("no sessions found")
        return
    for s in sessions:
        for line in analyze_session(s, pool):
            print(line)
        print()


if __name__ == "__main__":
    main()
