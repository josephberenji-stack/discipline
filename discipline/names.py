"""
names.py -- one word, one definition; the census is generated, not remembered.

WHY THIS EXISTS.  The audit of the final axiom set found "Grace" naming four
objects (a section, flasqueness, an averaging idempotent, the element 0 of
Z/3), three different triples called "the three seeds", and two quantities
called "the magnitude" in two documents that do not cite each other.  Every
one of those is the shared-word trap the project has a standing rule against,
and every one got past the rule because the rule was applied to morphisms and
not to vocabulary.

WHAT IT DOES.  Given a registry NAMES.md (one word per line, optionally
followed by ' | ' and the canonical definition and file), it walks the tree
and prints every DEFINITIONAL line for each registered word -- a line where
the word is followed closely by ':=', '=', 'is the', 'is a', 'means', 'as the',
'--', ':' or is bolded as a definition.  It then groups the definitional lines
by the words that follow the name, so distinct senses fall into distinct rows.
The output is the census a taxonomy discussion starts from.  It exits non-zero
when a registered word has definitional lines in more than one sense-group,
which is the condition the taxonomy has to resolve.

Rows, not counts.
"""
import re, sys
from pathlib import Path

DEF_TAIL = r"(\s*(:=|=|\bis the\b|\bis an?\b|\bmeans\b|\bas the\b|--|—|:)\s*)"

def load_registry(path):
    words = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        words.append((parts[0], parts[1] if len(parts) > 1 else "", parts[2] if len(parts) > 2 else ""))
    return words

def sense_key(tail):
    toks = re.findall(r"[A-Za-z_][A-Za-z0-9_]*|[0-9]+|[|∅=]", tail)
    toks = [t.lower() for t in toks if t.lower() not in ("the", "a", "an", "of", "is", "to", "and", "in")]
    return " ".join(toks[:4])

def census(paths, words):
    out = {}
    for p in paths:
        p = Path(p)
        files = [p] if p.is_file() else sorted(f for f in p.rglob("*")
                                                 if f.suffix in (".py", ".md", ".out", ".lean"))
        for f in files:
            try:
                lines = f.read_text(errors="replace").splitlines()
            except Exception:
                continue
            for i, line in enumerate(lines, 1):
                for w, _, _ in words:
                    pat = re.compile(r"(\*\*)?\b" + re.escape(w) + r"(\*\*)?(\([^)]*\))?" + DEF_TAIL + r"(.{0,80})")
                    m = pat.search(line)
                    if m:
                        tail = m.group(len(m.groups()))
                        out.setdefault(w, []).append((str(f), i, sense_key(tail), line.strip()[:120]))
    return out

def main(argv):
    reg = None
    if argv and argv[0] == "--names":
        reg = argv[1]; argv = argv[2:]
    words = load_registry(reg) if reg else [(w, "", "") for w in
             ("Grace", "Attention", "Freedom", "Observer", "Witness", "seed", "magnitude",
              "presentation", "reach", "demand", "theta", "base", "incompleteness")]
    cen = census(argv, words)
    conflicts = 0
    for w, canon, cfile in words:
        rows = cen.get(w, [])
        senses = {}
        for f, i, k, line in rows:
            senses.setdefault(k, []).append((f, i, line))
        print(f"\n== {w}  ({len(rows)} definitional lines, {len(senses)} sense-groups)"
              + (f"   canonical: {canon} [{cfile}]" if canon else ""))
        for k, lst in sorted(senses.items(), key=lambda kv: -len(kv[1])):
            f, i, line = lst[0]
            print(f"   [{len(lst):>3}] {k:<28} e.g. {f.split('/')[-1]}:{i}  {line[:90]}")
        if len(senses) > 1:
            conflicts += 1
    print(f"\n  names: {conflicts} of {len(words)} registered words have more than one sense-group")
    return conflicts

if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1:]) else 0)
