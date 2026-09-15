"""
withdraw.py -- a withdrawal is written above the result, and propagates.

WHY THIS EXISTS.  The ledger recorded #10, #11, #8 as wrong; embedding.py,
equilibrium.py and interaction.py still carry the wrong sentence with no
notice, because they have no transcript and were never re-run.  RESULTS.md
section 12 was withdrawn by section 13 -- correctly, above -- but the
scripts named in section 12 were not touched.

WHAT IT CHECKS.

  1. Position.  In every file that contains WITHDRAWN / RETRACTED / WITHDRAWAL,
     the first such word must occur before the first result-section header
     (a line of '=' or '-' rules, or a markdown '## ' heading after the first).
     A withdrawal below the result is a row.

  2. Propagation.  Every file name mentioned within 3 lines of a withdrawal
     (foo.py, foo.out, foo.md) is opened; if it does not itself contain
     WITHDRAWN / RETRACTED / superseded / overturned, that is a row: the
     withdrawal names a file that does not know it was withdrawn.

Rows, not counts.
"""
import re, sys
from pathlib import Path

WD = re.compile(r"\b(WITHDRAWN|RETRACTED|WITHDRAWAL|RETRACTION)\b")
KNOWS = re.compile(r"\b(WITHDRAWN|RETRACTED|withdrawn|retracted|superseded|overturned|Superseded)\b")
FILE = re.compile(r"\b([A-Za-z0-9_]+\.(?:py|out|md|lean))\b")
HEADER = re.compile(r"^\s*(={8,}|-{8,}|## )")

def check(paths):
    rows = []
    for p in paths:
        p = Path(p)
        files = [p] if p.is_file() else sorted(f for f in p.rglob("*") if f.suffix in (".py", ".md", ".out"))
        index = {f.name: f for f in files}
        for f in files:
            lines = f.read_text(errors="replace").splitlines()
            wd_lines = [i for i, l in enumerate(lines) if WD.search(l)]
            if not wd_lines:
                continue
            headers = [i for i, l in enumerate(lines) if HEADER.match(l)]
            first_result = headers[1] if len(headers) > 1 else (headers[0] if headers else len(lines))
            if wd_lines[0] > first_result:
                rows.append(("withdrawal-below-result", str(f), wd_lines[0] + 1,
                             f"first withdrawal at line {wd_lines[0]+1}, first result section at {first_result+1}"))
            for i in wd_lines:
                ctx = " ".join(lines[max(0, i - 3): i + 4])
                for name in set(FILE.findall(ctx)):
                    if name == f.name or name not in index:
                        continue
                    if not KNOWS.search(index[name].read_text(errors="replace")):
                        rows.append(("unpropagated", str(f), i + 1, f"withdraws {name}, which carries no notice"))
    for kind, f, i, d in rows:
        print(f"  {kind:<24} {f}:{i}  {d}")
    print(f"\n  withdraw: {len(rows)} rows")
    return rows

if __name__ == "__main__":
    sys.exit(1 if check(sys.argv[1:]) else 0)
