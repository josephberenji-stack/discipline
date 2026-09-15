# discipline — the seven blockers as code

The five practices of the methodology paper, plus the two rules its audit added, as
checks that run over a project's files. Concept-first: each module is short, has no
dependencies beyond the standard library, and states in its docstring which failure in the
corpus it exists to catch. They are meant to be run as a pre-commit hook, a CI step, or a
background pass after every exchange with the model; nothing here needs to live inside the
model.

| module | rule | catches (corpus instance) |
|---|---|---|
| `predeclare.py` | a script that prints a verdict must carry a prediction block above the computation | a script whose "HOLDS/FAILS" has no declared failure condition |
| `rowsplit.py` | a kill-check reports the rows that violate and a witness, never a bare count | `attention.py` #63 (keys never collided); `definitions.py` #28 (filter hid the rows) |
| `guard.py` | a function whose domain is narrower than its signature asserts it | `height.py` k=8 (six-prime list sliced to eight, silently) |
| `withdraw.py` | a withdrawal is written above the result it withdraws, and every file carrying the withdrawn sentence carries the notice | `embedding.py`, `equilibrium.py`, `interaction.py` (ledger caught it; file never amended) |
| `ledger.py` | the consolidated ledger is regenerated from docstrings, with gaps listed | #23–#72 never consolidated; #49 missing |
| `noliteral.py` | no printed table column or verdict is a constant | `variants.py` λ = 2.0; `algebra.py` 'YES', 1.0; `measure.py` 0.0; `verify.py` True |
| `names.py` | every load-bearing word has one definition; the census of senses is generated, not remembered | "Grace" with four senses; three different "three seeds" |

Two more, added for Method B (`METHOD-B.md`, the builder's method):

| module | rule | catches (corpus instance) |
|---|---|---|
| `referee.py` | the runtime referee: `declare()` before `verdict()`; a verdict argument may not be a literal; at least one negative control must fail; a withdrawal may not follow its result; `rows()` behind every count | `values.py` W6, `exist.py` X7, `derive.py` E1 (typed verdicts); `selfpres.py` C3 (failed prediction printed HOLDS); `exist.out:193` (withdrawal below result) |
| `index.py` | the results index: every theorem, axiom, section verdict, docstring claim, ledger entry and Lean declaration, with file:line — so "it would require …" is a search, not a memory | register rows V7, V9, V10 (T9's halves unjoined for six versions; a run summarised and missed; "nobody has asked") |

Run everything:

    python -m discipline.run PATH [PATH ...] --names NAMES.md
    python3 discipline/index.py PATH [PATH ...] > RESULTS-INDEX.md

Each check prints rows, not counts, and exits non-zero on any finding, so it composes
with a CI runner. `run.py` also writes `discipline-report.md`. `referee.py` is imported by
the computation file itself and exits non-zero from `close()` when the run does not count;
what it cannot catch — an identity that is computed rather than typed — is what the
negative-control requirement is for: if no case can be named that must fail, the check is
not a check.

## Enterprise shape

The checks are file-level and language-level, so they scale by being placed where files
are already gated: a pre-commit hook for the human, a CI job for the team, and a
post-turn pass for an agent. The only piece that needs the model is the one that writes
the files; the checks are the same for every model. A team that adopts them adopts one
`NAMES.md` per project, one ledger, one rule that a script without a transcript has no
result — and inherits the negative controls (`rowsplit` on a check that cannot fail,
`noliteral` on a column that cannot move).
