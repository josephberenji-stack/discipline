"""
cited.py -- a citation that nothing reads is decoration, and the space had no
check for it.

WHY THIS EXISTS.  RULE (Joseph, 2026-09-08): "when a framework theorem is cited,
ask what it adds beyond the plain statement.  If the argument survives deleting
the citation, the citation was decoration and no map was ever needed.  If it
collapses, the map has to be exhibited."

  reindex.sh already checks that every citation RESOLVES -- the file is there and
  the line is there.  Nothing checked that a citation DOES anything.  A
  requires-list entry that resolves and is never read passes every check in the
  space, and nothing on the page distinguishes it from one the file depends on.
  That is #121's shape again, one level up: this time in the evidence rather
  than in the machinery.

WHAT IT CHECKS.  Every `requires=[...]` entry of every `declare()`.

  RESOLUTION.  "file.md:LINE label", "file.py:LINE", "file.out LABEL" and bare
  "file.out" are all in use.  The file is found by name under the corpus roots;
  the line is taken as given, or found from the label; the BLOCK at that line is
  the line plus what follows it up to the next header, because a citation that
  names a section header points at the section, not at the header text.

  LOAD-BEARING, three kinds, none of them a threshold:
    import        the cited module is imported by the citing file.
    runtime-read  the citing file opens the cited file while running.
    copy          the citing file contains >= COPY_RUN consecutive non-trivial
                  lines verbatim from the cited file.  Load-bearing for
                  PROVENANCE, not for the argument: deleting the citation leaves
                  the argument standing and the borrowing unattributed.

  ROWS.
    no-such-file       the cited file is not under the corpus roots.
    label-not-at-line  a line and a label are given and the label is not in the
                       block at that line.  The citation resolves and points at
                       the wrong place.
    label-not-in-file  no line given, and the label is nowhere in the file.
    bare-file          neither line nor label: there is nothing to test.
    not-load-bearing   it resolves, the label is where it says, and the citing
                       file has no import, no runtime read and no copy.  Deleting
                       this citation cannot break the file.  The deletion test's
                       decidable half; whether the ARGUMENT survives is the half
                       a parser cannot see, and the row is where a human looks.
    prose-citation     it resolves and the label is where it says, and the cited
                       file is a .md or .out.  No prose citation can be an import,
                       a runtime read or a copy, so its outcome is forced by the
                       citation's file type.  Reported apart from the row count so
                       the headline is a measurement and not a restatement of how
                       many citations name the axiom set (#139).

WHAT IT DOES NOT CHECK.  Whether a not-load-bearing citation is decoration.  A
theorem can be the reason a computation is correct without being imported.  The
row says the machine cannot tell, not that the citation is wrong.  Token overlap
between the citing file's code and the cited block was tried and DISCARDED: the
answer moved with the block window (line-only: 37 rows; 45-line block: 2), so it
was a threshold, and a threshold that can be tuned to any answer is not a
measurement.  Only the dependency tiers are reported, and they need no window.

CONTROLS.  `python3 discipline/cited.py --self` plants two citations in a scratch
file: one naming a module the file imports (must not row) and one naming a file
it never touches (must row).  Both are asserted.

LEDGER.
  #147 (found by the referee while checking IDEA-014-lambdaindex-1.py, which
    declares in its MIRRORS block that it reuses nothing).  copies_from counted a
    run of lines that were consecutive in the CITED file and merely PRESENT
    somewhere in the citing one, so four shared lines plus a fifth appearing
    elsewhere read as a five-line copy.  The longest run actually consecutive in
    both files is 4.  The run must now be consecutive in BOTH files.
  #141 (found by Joseph, 8 Sep, on being handed 11 label-not-at-line rows as
    defects: "go back and ensure none of them exists across any of the other
    project files").  Five of those eleven were this module's own false positives,
    reported without being read one at a time.  label_re took the label's FIRST
    whitespace token, so "[OPEN] the assignment lattice" was located by "[OPEN]"
    -- a status marker, not a locator -- and AXIOMS-v10-CLEAN.md:631 rowed twice
    although it is exactly the assignment-lattice bullet.  "T30 (iii)" was located
    by "T30" although :485 is T30's own clause (iii).  And "T7''" was located by an
    ASCII spelling of a file that writes the Unicode double prime.  Status markers
    are now stripped, every locator word is tried, "/" is a word break so that "the
    level/hexagon sentence" locates by "level" or "hexagon", and both sides are
    ASCII-folded for primes and smart quotes.  Six of the eleven were this module
    misreading a correct citation; five were real and are corrected in their files.
  #139 (found by Joseph, on being told the first run's headline: "im just confused
    because i feel like theres been several points where i stoped the progression of
    the thread to investigate the computability of files.  now we are seeing that
    pretty much none of them are computable").  The first run reported 171 rows of
    201 requires entries and let that stand as the finding.  110 of the 201 cite a
    .md and 22 cite a .out, and NO prose citation can be an import, a runtime read
    or a copy -- so 132 of those rows were determined by the citation's file type
    before any file was read.  That is the forced-quantity failure, in the module
    written to catch decoration.  The unforced number is 30 of 69 .py citations
    load-bearing; prose citations are now counted apart and named prose-citation.
    Separately: cited.py measures the CITATION, never the computation.  Whether a
    result was ever at risk is forced.py, noliteral.py, predeclare.py and audit.py,
    and a cited row says nothing about any of them.

Rows, not counts.
"""
import ast, os, re, sys, collections
from pathlib import Path

COPY_RUN = 5
SKIP = {"Resource_Material", "hallucinated_papers", "paper1_methodology", ".git",
        "__pycache__"}
CITE = re.compile(r"^(?:.*/)?([^/:\s]+\.(?:py|md|out|lean))(?::(\d+))?(?:[\s,]+(.*))?$")
HEADER = re.compile(r'^\s*(print\(\s*f?["\']\s*[A-Z]|#{1,4} |\*\*[A-Z]|={8,}|-{8,})')
TRIVIAL = re.compile(r'^\s*(#|$|\)|\]|\}|else:|try:|pass$)')


def corpus_roots(start):
    """bookstuff by name, walking up from the checked file; lean beside it."""
    roots, p = [], Path(start).resolve()
    for anc in [p] + list(p.parents):
        if anc.name == "bookstuff":
            roots.append(anc); break
        cand = anc / "bookstuff"
        if cand.is_dir():
            roots.append(cand); break
    for anc in list(Path(start).resolve().parents) + [Path(os.environ.get("HOME", "/")) / "mnt"]:
        cand = anc / "lean_verification_engV7"
        if cand.is_dir():
            roots.append(cand); break
    return roots


def build_index(roots):
    idx = collections.defaultdict(list)
    for root in roots:
        for f in root.rglob("*"):
            if f.is_file() and f.suffix in (".py", ".md", ".out", ".lean") \
               and not any(s in f.parts for s in SKIP):
                idx[f.name].append(f)
    for k in idx:
        idx[k].sort(key=lambda f: (0 if "testcases" in f.parts else 1, len(str(f))))
    return idx


def block_at(lines, ln, cap=45):
    out, i = [lines[ln - 1]], ln
    while i < len(lines) and len(out) < cap:
        if len(out) > 2 and HEADER.match(lines[i]):
            break
        out.append(lines[i]); i += 1
    return "\n".join(out)


STATUS = re.compile(r"\[(OPEN|PROVED|DEF|CITED|AXIOM|WITHDRAWN)\]", re.I)


def norm(t):
    """ASCII a citation's primes so T7'' and T7-double-prime are one label (#141)."""
    return (t.replace("\u2033", "''").replace("\u2032", "'")
             .replace("\u201c", '"').replace("\u201d", '"')
             .replace("\u2018", "'").replace("\u2019", "'"))


def label_keys(label):
    """The locator tokens of a citation label, best first.  A status marker is
    not a locator: '[OPEN] the assignment lattice' locates by 'assignment', not
    by '[OPEN]' (#141)."""
    cleaned = STATUS.sub(" ", norm(label)).replace("/", " ")
    words = [w.strip("(),.:;") for w in cleaned.split()]
    words = [w for w in words if len(w) > 1 and w.lower() not in
             ("the", "a", "an", "of", "on", "in", "and", "its")]
    return words


def label_re(label):
    keys = label_keys(label)
    if not keys:
        return None
    return re.compile("|".join(r"(?<![A-Za-z0-9_])" + re.escape(k) + r"(?![A-Za-z0-9_])"
                               for k in keys))


def declares(tree, src):
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and (getattr(n.func, "attr", "") == "declare"
                                        or getattr(n.func, "id", "") == "declare"):
            claim = (n.args[0].value if n.args and isinstance(n.args[0], ast.Constant)
                     else "?")
            for kw in n.keywords:
                if kw.arg == "requires" and isinstance(kw.value, ast.List):
                    for e in kw.value.elts:
                        if isinstance(e, ast.Constant) and isinstance(e.value, str):
                            yield claim, e.value, getattr(e, "lineno", 0)


def imports_of(tree):
    got = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                got.add(a.name.split(".")[0])
        elif isinstance(n, ast.ImportFrom) and n.module:
            got.add(n.module.split(".")[0])
    return got


def copies_from(src_lines, cited_lines):
    """>= COPY_RUN consecutive non-trivial lines that are consecutive in BOTH
    files.  Membership alone is not a copy (#147)."""
    want = [l.rstrip() for l in cited_lines if not TRIVIAL.match(l)]
    mine = [l.rstrip() for l in src_lines if not TRIVIAL.match(l)]
    if len(want) < COPY_RUN or len(mine) < COPY_RUN:
        return False
    index = {}
    for i, l in enumerate(mine):
        index.setdefault(l, []).append(i)
    for j in range(len(want) - COPY_RUN + 1):
        for i in index.get(want[j], ()):
            if i + COPY_RUN > len(mine):
                continue
            if all(mine[i + k] == want[j + k] for k in range(COPY_RUN)):
                return True
    return False


def check(paths):
    rows, kinds, seen = [], collections.Counter(), collections.Counter()
    idx, roots = None, []
    for p in paths:
        p = Path(p)
        files = [p] if p.is_file() else sorted(f for f in p.rglob("*.py")
                                               if not any(s in f.parts for s in SKIP))
        for f in files:
            if idx is None:
                roots = corpus_roots(f)
                idx = build_index(roots)
            src = f.read_text(errors="replace")
            try:
                tree = ast.parse(src)
            except SyntaxError:
                continue
            src_lines = src.splitlines()
            imported = imports_of(tree)
            for claim, entry, at in declares(tree, src):
                m = CITE.match(entry.strip())
                if not m:
                    rows.append(("bare-file", str(f), at, claim, entry,
                                 "no file name in the citation")); continue
                base, line, label = m.group(1), m.group(2), (m.group(3) or "").strip()
                cands = idx.get(base, [])
                if not cands:
                    rows.append(("no-such-file", str(f), at, claim, entry,
                                 "no file of that name under " +
                                 ", ".join(r.name for r in roots))); continue
                cf = cands[0]
                seen["py" if cf.suffix == ".py" else "prose"] += 1
                clines = cf.read_text(errors="replace").splitlines()

                if line is None and not label:
                    rows.append(("bare-file", str(f), at, claim, entry,
                                 "names a file and nothing in it")); continue
                if line is not None:
                    ln = int(line)
                    if not 1 <= ln <= len(clines):
                        rows.append(("no-such-file", str(f), at, claim, entry,
                                     f"line {ln} past EOF ({len(clines)} lines)")); continue
                    if label:
                        rx = label_re(label)
                        if rx and not rx.search(norm(block_at(clines, ln))):
                            rows.append(("label-not-at-line", str(f), at, claim, entry,
                                         f"'{label.split()[0]}' is not in the block at "
                                         f"{cf.name}:{ln}")); continue
                else:
                    rx = label_re(label)
                    if rx is None or not any(rx.search(norm(l)) for l in clines):
                        rows.append(("label-not-in-file", str(f), at, claim, entry,
                                     f"'{label}' is nowhere in {cf.name}")); continue

                if cf.suffix == ".py" and cf.stem in imported:
                    kinds["import"] += 1; continue
                if re.search(r'open\(\s*[^)]*' + re.escape(cf.name), src):
                    kinds["runtime-read"] += 1; continue
                if cf.suffix == ".py" and copies_from(src_lines, clines):
                    kinds["copy"] += 1; continue
                if cf.suffix != ".py":
                    rows.append(("prose-citation", str(f), at, claim, entry,
                                 "a .md/.out citation can never be an import or a "
                                 "copy: the deletion test has no mechanical purchase "
                                 "here and a human applies the rule (#139)"))
                    continue
                rows.append(("not-load-bearing", str(f), at, claim, entry,
                             "no import, no runtime read, no copy: deleting this "
                             "citation cannot break the file"))

    for kind, f, at, claim, entry, why in rows:
        print(f"  {kind:<18} {f}:{at}  [{claim}]  {entry}")
        print(f"  {'':<18}   {why}")
    tot = sum(kinds.values()) + len(rows)
    lb = sum(kinds.values())
    n_py = seen["py"]
    n_prose = tot - n_py
    prose_rows = sum(1 for r in rows if r[0] == "prose-citation")
    print(f"\n  load-bearing: " +
          ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())))
    print(f"  requires entries: {tot}.  {n_prose} name a .md or .out and CANNOT be an "
          f"import, a runtime read or a copy;")
    print(f"  that count is forced by the citation's file type and is not a "
          f"measurement (#139).")
    print(f"  Of the {n_py} that name a .py, {lb} are load-bearing and "
          f"{n_py - lb} are not.")
    print(f"  cited: {len(rows)} rows ({len(rows) - prose_rows} on .py citations and "
          f"malformed ones, {prose_rows} prose)")
    return rows


def _self_test():
    import tempfile, textwrap
    d = Path(tempfile.mkdtemp()) / "bookstuff" / "testcases"
    d.mkdir(parents=True)
    (d / "referee.py").write_text("def declare(*a, **k):\n    pass\n")
    (d / "faraway.py").write_text('print("Z9.  A SECTION THIS FILE NEVER TOUCHES")\n'
                                  'X = 41\n')
    (d / "probe.py").write_text(textwrap.dedent('''\
        """probe."""
        import referee as R
        R.declare("C1", requires=["referee.py:1 declare"])
        R.declare("C2", requires=["faraway.py:1 Z9"])
        '''))
    got = collections.Counter(r[0] for r in check([d / "probe.py"]))
    assert got["not-load-bearing"] == 1, got
    assert sum(got.values()) == 1, got
    print("\n  self-test: the imported citation does not row; the untouched one does.")
    return 0


if __name__ == "__main__":
    if "--self" in sys.argv:
        sys.exit(_self_test())
    sys.exit(1 if check(sys.argv[1:] or ["."]) else 0)
