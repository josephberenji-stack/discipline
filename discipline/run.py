"""run.py -- run every check with each one scoped correctly.  Rows, not counts.

    python3 -m discipline.run FILE_OR_DIR [...] --names NAMES.md
                              [--corpus ROOT ...] [--floor=N] [--baseline=2,3,...]

Ten checks are FILE-LEVEL and run on the paths you give.  The eleventh, ledger,
is CORPUS-LEVEL: it needs the roots where the numbering lives, given with
--corpus.  Without --corpus it is skipped and says so, rather than reporting
every number below the file's highest as a gap (#109).

  #126 (found by Joseph, PROMPT-thread2.md:81-84, 6 Sep run).  forced.py was never
    imported nor in FILE_LEVEL, so it reported nothing and read as clean; wired in.
  #138 (found by Joseph, 8 Sep, stating the rule: "when a framework theorem is cited,
    ask what it adds beyond the plain statement.  If the argument survives deleting
    the citation, the citation was decoration and no map was ever needed.  If it
    collapses, the map has to be exhibited.").  reindex.sh checked that a citation
    RESOLVES and nothing checked that anything READS it; cited.py added and wired in
    as the eighth file-level check.
  #143 (found by Joseph, 8 Sep, setting the rule: "you, 'the builder', are no longer
    allowed to reference anything across files.  YOU are to cite it in a comment at
    the top that there are pieces of math contained that mirror a theorem or idea or
    variable or term or whatever the mathematical object may be, BUT you build out
    the math in file from the ground up, EVERY SINGLE TIME.").  ground.py added and
    wired in as the ninth file-level check.  It rows on every claim-bearing file in
    the space as of this run -- 25 corpus imports, 13 third-party, 22 files with no
    MIRRORS block -- because the rule is new and nothing was built under it yet.
  #145 (found by Joseph, 8 Sep, in the same breath as #143: "if something is VALUE
    dependent or value representative, it should now be built out in individual
    files that depend on it.  I suggest creating a log space, so that you can
    copy/paste the math once its correct and still know all the places that depend
    on that specific function/value/variable").  primitive.py and primitives/ added
    and wired in as the tenth file-level check.  Building from the ground up in
    every file removes the shared premise and creates N copies that can drift; the
    register is what makes the duplication checkable.
"""
import sys, io, contextlib
from pathlib import Path
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
import predeclare, rowsplit, guard, withdraw, ledger, noliteral, names, forced, cited
import ground, primitive

FILE_LEVEL = ["predeclare", "rowsplit", "guard", "withdraw", "noliteral", "names",
              "forced", "cited", "ground", "primitive"]


def main(argv):
    reg, corpus, ledger_opts = None, [], []
    argv = list(argv)
    if "--names" in argv:
        i = argv.index("--names"); reg = argv[i + 1]; del argv[i:i + 2]
    while "--corpus" in argv:
        i = argv.index("--corpus"); corpus.append(argv[i + 1]); del argv[i:i + 2]
    for a in list(argv):
        if a.startswith(("--max=", "--floor=", "--baseline=")):
            ledger_opts.append(a); argv.remove(a)

    checks = [("predeclare", lambda: predeclare.check(argv)),
              ("rowsplit", lambda: rowsplit.lint(argv)),
              ("guard", lambda: guard.lint(argv)),
              ("withdraw", lambda: withdraw.check(argv)),
              ("noliteral", lambda: noliteral.main(argv)),
              ("names", lambda: names.main((["--names", reg] if reg else []) + argv)),
              ("forced", lambda: forced.check(argv)),
              ("cited", lambda: cited.check(argv)),
              ("ground", lambda: ground.check(argv)),
              ("primitive", lambda: primitive.check(argv)),
              ("ledger", lambda: ledger.main(ledger_opts + (corpus or argv)))]

    report, total, file_rows = ["# discipline report", ""], 0, 0
    for title, fn in checks:
        if title == "ledger" and not corpus:
            print("== ledger: skipped (corpus-level; pass --corpus ROOT)")
            report += ["## ledger — skipped", "", "corpus-level check; pass --corpus ROOT", ""]
            continue
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            res = fn()
        n = len(res) if hasattr(res, "__len__") else int(res)
        total += n
        if title in FILE_LEVEL:
            file_rows += n
        print(f"== {title}: {n} rows")
        report += [f"## {title} — {n} rows", "", "```", buf.getvalue().rstrip(), "```", ""]
    Path("discipline-report.md").write_text("\n".join(report))
    print(f"\n  discipline: {file_rows} file-level rows"
          f"{f', {total - file_rows} ledger gaps' if corpus else ''}"
          f"; report in discipline-report.md")
    return total


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1:]) else 0)
