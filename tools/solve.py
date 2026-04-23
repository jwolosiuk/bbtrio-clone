#!/usr/bin/env python3
"""
Blueberry Trio solver and difficulty rater.

Usage:
  tools/solve.py                       # use ../puzzle.txt
  tools/solve.py path/to/puzzle.txt
  tools/solve.py --count               # just count solutions (cap 50)
  tools/solve.py --depth N             # run Nishio BFS up to depth N (default 3)

Rules (from https://circle9puzzle.com/bbtrio/):
  - Place exactly 3 berries in each row, column, and region.
  - Each numbered clue cell equals the number of berries in its 8 neighbors.

Puzzle format (two grids, blank-line separated):
  Cells:  '.' open, '0'-'9' clue, 'x' pre-placed berry
  Groups: any letter, same letter = same region (each must have SIZE cells)
  Decoration (|, _, -, +, whitespace) is ignored. '#' starts a comment.

Difficulty metric: minimum Nishio-style lookahead depth needed to solve.
  depth 0: pure deduction (forced moves in row/col/region/clue).
  depth D: for some undecided cell, BOTH assignments lead to contradiction
           via lookahead of depth D-1. Pick the forced value. Repeat.
  "stuck at depth N" means either the puzzle has multiple solutions or
  needs deeper lookahead than N.
"""
from __future__ import annotations
import argparse, sys, time
from collections import defaultdict
from pathlib import Path

PER = 3  # berries per row/column/region (classic "Trio")


def parse(text: str):
    raw = text.splitlines()
    blocks: list[list[str]] = []
    cur: list[str] = []
    for ln in raw:
        trimmed = ln.strip()
        if trimmed.startswith("#"):
            continue
        if trimmed == "":
            if cur:
                blocks.append(cur)
                cur = []
            continue
        stripped = "".join(ch for ch in ln if ch not in " |_-+\t")
        if not stripped:
            continue
        cur.append(stripped)
    if cur:
        blocks.append(cur)
    if len(blocks) < 2:
        raise ValueError("puzzle needs a cells grid and a groups grid separated by a blank line")
    cell_lines, group_lines = blocks[0], blocks[1]
    n = len(cell_lines)
    if len(group_lines) != n:
        raise ValueError(f"cell grid has {n} rows, groups grid has {len(group_lines)}")
    for r in range(n):
        if len(cell_lines[r]) != n:
            raise ValueError(f"cells row {r} has width {len(cell_lines[r])}, expected {n}")
        if len(group_lines[r]) != n:
            raise ValueError(f"groups row {r} has width {len(group_lines[r])}, expected {n}")
    clues: dict[tuple[int, int], int] = {}
    givens: set[tuple[int, int]] = set()
    for r in range(n):
        for c in range(n):
            ch = cell_lines[r][c]
            if ch == ".":
                continue
            if ch in "xX":
                givens.add((r, c))
            elif ch.isdigit():
                clues[(r, c)] = int(ch)
            else:
                raise ValueError(f"unknown cell char '{ch}' at ({r},{c})")
    group_of = [[group_lines[r][c] for c in range(n)] for r in range(n)]
    counts: dict[str, int] = defaultdict(int)
    for row in group_of:
        for g in row:
            counts[g] += 1
    for g, k in counts.items():
        if k != n:
            raise ValueError(f"group '{g}' has {k} cells, expected {n}")
    return n, clues, givens, group_of


def neighbors8(r: int, c: int, n: int):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                yield nr, nc


class Solver:
    def __init__(self, size, clues, givens, group_of):
        self.N = size
        self.clues = clues
        self._clue_cells = set(clues)
        self.is_clue = lambda r, c: (r, c) in self._clue_cells
        self.initial = [[0] * size for _ in range(size)]
        for r, c in givens:
            self.initial[r][c] = 1
        groups: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for r in range(size):
            for c in range(size):
                groups[group_of[r][c]].append((r, c))
        lines = []
        for r in range(size):
            lines.append([(r, c) for c in range(size) if not self.is_clue(r, c)])
        for c in range(size):
            lines.append([(r, c) for r in range(size) if not self.is_clue(r, c)])
        for cells in groups.values():
            lines.append([(r, c) for (r, c) in cells if not self.is_clue(r, c)])
        self.lines = lines
        self.clue_ns = {
            (cr, cc): [(nr, nc) for (nr, nc) in neighbors8(cr, cc, size) if not self.is_clue(nr, nc)]
            for (cr, cc) in clues
        }

    def propagate(self, s):
        changed = True
        while changed:
            changed = False
            for cells in self.lines:
                b = o = 0
                for r, c in cells:
                    v = s[r][c]
                    if v == 1:
                        b += 1
                    elif v == 0:
                        o += 1
                need = PER - b
                if need < 0 or need > o:
                    return False
                if o == 0:
                    continue
                if need == 0:
                    for r, c in cells:
                        if s[r][c] == 0:
                            s[r][c] = 2
                            changed = True
                elif need == o:
                    for r, c in cells:
                        if s[r][c] == 0:
                            s[r][c] = 1
                            changed = True
            for (cr, cc), want in self.clues.items():
                ns = self.clue_ns[(cr, cc)]
                b = o = 0
                for nr, nc in ns:
                    v = s[nr][nc]
                    if v == 1:
                        b += 1
                    elif v == 0:
                        o += 1
                need = want - b
                if need < 0 or need > o:
                    return False
                if o == 0:
                    continue
                if need == 0:
                    for nr, nc in ns:
                        if s[nr][nc] == 0:
                            s[nr][nc] = 2
                            changed = True
                elif need == o:
                    for nr, nc in ns:
                        if s[nr][nc] == 0:
                            s[nr][nc] = 1
                            changed = True
        return True

    def is_complete(self, s):
        for r in range(self.N):
            for c in range(self.N):
                if not self.is_clue(r, c) and s[r][c] == 0:
                    return False
        return True

    def clone(self, s):
        return [row[:] for row in s]

    def count_solutions(self, cap=50):
        sols = 0

        def rec(s):
            nonlocal sols
            cp = self.clone(s)
            if not self.propagate(cp):
                return
            if self.is_complete(cp):
                sols += 1
                return
            if sols >= cap:
                return
            for r in range(self.N):
                for c in range(self.N):
                    if self.is_clue(r, c) or cp[r][c] != 0:
                        continue
                    for v in (1, 2):
                        t = self.clone(cp)
                        t[r][c] = v
                        rec(t)
                        if sols >= cap:
                            return
                    return
        rec(self.clone(self.initial))
        return sols

    def is_contradictory(self, s, depth):
        cp = self.clone(s)
        if not self.propagate(cp):
            return True
        if depth <= 0 or self.is_complete(cp):
            return False
        for r in range(self.N):
            for c in range(self.N):
                if self.is_clue(r, c) or cp[r][c] != 0:
                    continue
                both_fail = True
                for v in (1, 2):
                    t = self.clone(cp)
                    t[r][c] = v
                    if not self.is_contradictory(t, depth - 1):
                        both_fail = False
                        break
                if both_fail:
                    return True
        return False

    def solve_bfs(self, max_depth):
        """Nishio BFS: iteratively deepen contradiction lookahead. Returns (solved, max_used, forced_count)."""
        state = self.clone(self.initial)
        max_used = 0
        forced = 0
        while True:
            if not self.propagate(state):
                return False, max_used, forced
            if self.is_complete(state):
                return True, max_used, forced
            progress = False
            for depth in range(1, max_depth + 1):
                for r in range(self.N):
                    for c in range(self.N):
                        if self.is_clue(r, c) or state[r][c] != 0:
                            continue
                        for v in (1, 2):
                            t = self.clone(state)
                            t[r][c] = v
                            if self.is_contradictory(t, depth - 1):
                                state[r][c] = 2 if v == 1 else 1
                                max_used = max(max_used, depth)
                                progress = True
                                forced += 1
                                break
                        if progress:
                            break
                    if progress:
                        break
                if progress:
                    break
            if not progress:
                return False, max_used, forced


LABELS = ["Trivial", "Easy", "Medium", "Hard", "Expert"]


def rate(depth: int | None) -> str:
    if depth is None:
        return "Unrated (stuck)"
    return LABELS[min(depth, len(LABELS) - 1)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=None, help="puzzle.txt (default: ../puzzle.txt)")
    ap.add_argument("--count", action="store_true", help="only count solutions (cap 50)")
    ap.add_argument("--depth", type=int, default=3, help="max Nishio depth to try (default 3)")
    args = ap.parse_args()

    path = Path(args.path) if args.path else Path(__file__).resolve().parent.parent / "puzzle.txt"
    text = path.read_text()
    n, clues, givens, group_of = parse(text)
    solver = Solver(n, clues, givens, group_of)

    print(f"Puzzle: {path}")
    print(f"  size {n}x{n}, {len(clues)} clue(s), {len(givens)} given berry(ies)")
    t0 = time.time()
    sols = solver.count_solutions(cap=50)
    print(f"  solutions (cap 50): {sols}" + ("+" if sols == 50 else "") + f" [{time.time()-t0:.2f}s]")
    if args.count:
        return
    for d in range(0, args.depth + 1):
        t0 = time.time()
        ok, used, forced = solver.solve_bfs(d)
        dt = time.time() - t0
        status = "solved" if ok else "stuck"
        print(f"  Nishio depth<={d}: {status} (max_used={used}, forced={forced}) [{dt:.2f}s]")
        if ok:
            print(f"  Difficulty: {rate(used)} (min depth {used})")
            return
    print(f"  Difficulty: {rate(None)} — needs deeper lookahead or puzzle is non-unique")


if __name__ == "__main__":
    main()
