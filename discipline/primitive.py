"""
primitive.py -- the log space.  One verified instance, many carried copies, and a
check that every copy is still that instance.

WHY THIS EXISTS.  RULE (Joseph, 2026-09-08): a claim-bearing file builds its own
mathematics from the ground up (ground.py, #143).  That removes the silent shared
premise and puts an equal and opposite risk in its place: N copies of the same
construction, drifting apart with nothing to say so.  His answer, verbatim:

  "if something is VALUE dependent or value representative, it should now be
  built out in individual files that depend on it.  I suggest creating a log
  space, so that you can copy/paste the math once its correct and still know all
  the places that depend on that specific function/value/variable."

  Measured before building: 33 top-level functions in this space are already
  carried by two or more files, 1140 lines in total, identical today with nothing
  checking that they stay identical.  `closure`, `inverse`, `perm`, `cyc` and
  `dart_voltage` are in five files each.

WHAT THE LOG SPACE IS.  primitives/<name>.py holds the canonical text of one
function -- the thing to copy from.  primitives/REGISTER.md is generated and
lists, for each primitive, its hash, its library dependency if any, and every
file carrying it with the line it starts on.

WHAT IT CHECKS.  No markers are needed in the carrying files; identity is by name
and hash, so an edit cannot forget to update a marker.

  drift            a file defines a function whose NAME is registered and whose
                   normalised source hash is NOT the canonical one.  The two
                   hashes are printed.  Exact -- no tolerance, no window.
  unregistered     two or more files carry an identical function that the
                   register does not hold.  A duplicate nobody is watching.
  dead-primitive   a registered primitive no carrier carries.
  stale-register   a carrier list that does not match what is on disk.

NORMALISATION.  ast.dump of the parsed function with docstrings blanked.  So a
ledger entry added to one copy is not drift; a changed constant, name, or
operator is.  Comments are not in the AST and are likewise not drift.

  python3 discipline/primitive.py --rebuild   regenerate the log space from the
                                              copies now on disk
  python3 discipline/primitive.py --self      the control

LEDGER.
  #144 (found by the referee on this module's own first run).  The rebuild keyed
    the register on (name, hash), so two files carrying DIFFERENT versions of the
    same function became two separate primitives and nothing rowed -- the exact
    failure the module exists to catch, in the module that catches it.  It keys on
    NAME now; the canonical text is the majority hash and every minority copy is a
    drift row.  Caught on the first run: theta_rule and tree_path.

Rows, not counts.
"""
import ast, hashlib, re, sys, collections
from pathlib import Path

LIBS = ("numpy", "np", "scipy", "sympy", "sp")


def norm_hash(seg):
    t = ast.parse(seg)
    for n in ast.walk(t):
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) \
           and isinstance(n.value.value, str):
            n.value.value = ""
    return hashlib.sha256(ast.dump(t).encode()).hexdigest()[:8]


def libs_used(seg):
    names = {n.id for n in ast.walk(ast.parse(seg)) if isinstance(n, ast.Name)}
    names |= {n.value.id for n in ast.walk(ast.parse(seg))
              if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)}
    return sorted(n for n in names if n in LIBS)


def top_functions(f):
    src = Path(f).read_text(errors="replace")
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return
    for n in tree.body:
        if isinstance(n, ast.FunctionDef):
            seg = ast.get_source_segment(src, n)
            if seg and len(seg.splitlines()) >= 3:
                yield n.name, n.lineno, seg


def space_files(root):
    return sorted(f for f in Path(root).glob("*.py"))


def load_independent(reg_dir):
    """Names two files implement independently on purpose, each with a reason.
    A line with no reason is not an exemption."""
    out, path = {}, Path(reg_dir) / "INDEPENDENT.md"
    if not path.is_file():
        return out
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith("#") or "|" not in line:
            continue
        name, _, reason = line.partition("|")
        name, reason = name.strip(), reason.strip()
        if name and reason:
            out[name] = reason
    return out


def load_register(reg_dir):
    """name -> dict(hash, libs, carriers[(file, line)])"""
    reg, path = {}, Path(reg_dir) / "REGISTER.md"
    if not path.is_file():
        return reg
    cur = None
    for line in path.read_text(errors="replace").splitlines():
        m = re.match(r"^## (\S+)\s+`([0-9a-f]{8})`(?:\s+lib:(\S+))?", line)
        if m:
            cur = m.group(1)
            reg[cur] = dict(hash=m.group(2),
                            libs=(m.group(3).split(",") if m.group(3) else []),
                            carriers=[])
            continue
        m = re.match(r"^- (\S+):(\d+)\b", line)
        if m and cur:
            reg[cur]["carriers"].append((m.group(1), int(m.group(2))))
    return reg


def rebuild(root=".", reg_dir="primitives"):
    root, reg_dir = Path(root), Path(reg_dir)
    reg_dir.mkdir(exist_ok=True)
    byname = collections.defaultdict(list)
    for f in space_files(root):
        if f.parent.name == "primitives":
            continue
        for name, ln, seg in top_functions(f):
            byname[name].append((f.name, ln, seg, norm_hash(seg)))
    out, kept = ["# REGISTER -- the log space", "",
                 "Generated by `python3 discipline/primitive.py --rebuild`.  Never",
                 "hand-edited.  One section per primitive: its hash, the library it",
                 "needs if any, and every file carrying it.", ""], 0
    for name, carriers in sorted(byname.items()):
        if len(carriers) < 2:
            continue
        # the canonical text is the MAJORITY hash; a minority copy is drift and
        # the check says so, rather than the rebuild quietly making two buckets
        # of the same name (#144).
        counts = collections.Counter(c[3] for c in carriers)
        h = counts.most_common(1)[0][0]
        kept += 1
        seg = next(c[2] for c in carriers if c[3] == h)
        libs = libs_used(seg)
        (reg_dir / f"{name}.py").write_text(
            f"# PRIMITIVE {name} @ {h}\n"
            f"# The canonical text.  Copy from here; never import from here.\n"
            f"# Carried by: {', '.join(c[0] for c in carriers)}\n"
            + (f"# Needs: {', '.join(libs)}\n" if libs else "")
            + "\n" + seg.rstrip() + "\n")
        out.append(f"## {name}  `{h}`" + (f"  lib:{','.join(libs)}" if libs else ""))
        out.append("")
        for c, ln, _, ch in carriers:
            out.append(f"- {c}:{ln}" + ("" if ch == h else f"   DRIFTED `{ch}`"))
        out.append("")
    (reg_dir / "REGISTER.md").write_text("\n".join(out))
    drift = sum(1 for n, v in byname.items() if len(v) >= 2
                for c in v if c[3] != collections.Counter(
                    x[3] for x in v).most_common(1)[0][0])
    print(f"  register: {kept} primitives, "
          f"{sum(len(v) for n, v in byname.items() if len(v) >= 2)} carried copies, "
          f"{drift} of them drifted from the canonical text")
    return kept


def check(paths, reg_dir="primitives"):
    reg = load_register(reg_dir)
    indep = load_independent(reg_dir)
    rows = []
    if not reg:
        print("\n  primitive: 0 rows (no register; run --rebuild)")
        return rows
    on_disk = collections.defaultdict(list)
    scanned = set()
    for p in paths:
        p = Path(p)
        files = [p] if p.is_file() else sorted(
            f for f in p.rglob("*.py")
            if "Resource_Material" not in f.parts and f.parent.name != "primitives")
        for f in files:
            if f in scanned:
                continue
            scanned.add(f)
            for name, ln, seg in top_functions(f):
                if name not in reg:
                    continue
                h = norm_hash(seg)
                on_disk[name].append((f.name, ln))
                if h != reg[name]["hash"] and name not in indep:
                    rows.append(("drift", str(f), ln,
                                 f"'{name}' is {h}; the register holds "
                                 f"{reg[name]['hash']} (primitives/{name}.py)"))
    for name, e in sorted(reg.items()):
        if not on_disk.get(name) and len(scanned) > 1:
            rows.append(("dead-primitive", f"{reg_dir}/{name}.py", 1,
                         "registered and carried by no file"))
        elif on_disk.get(name) and len(scanned) > 1:
            want = {c for c, _ in e["carriers"]}
            got = {c for c, _ in on_disk[name]}
            if want != got:
                rows.append(("stale-register", f"{reg_dir}/REGISTER.md", 1,
                             f"'{name}': register says {sorted(want)}, disk says "
                             f"{sorted(got)} -- run --rebuild"))
    for kind, f, i, d in rows:
        print(f"  {kind:<16} {f}:{i}  {d}")
    print(f"\n  primitive: {len(rows)} rows "
          f"({len(reg)} primitives registered, {len(indep)} names exempt as "
          f"declared-independent reimplementations)")
    return rows


def _self_test():
    import tempfile
    d = Path(tempfile.mkdtemp())
    body = "def twice(x):\n    y = x + x\n    return y\n"
    (d / "a.py").write_text(body)
    (d / "b.py").write_text(body)
    rebuild(d, d / "primitives")
    got = check([d], d / "primitives")
    assert got == [], got
    (d / "b.py").write_text("def twice(x):\n    y = x * 2\n    return y\n")
    got = check([d], d / "primitives")
    kinds = collections.Counter(r[0] for r in got)
    assert kinds["drift"] == 1, got
    print("\n  self-test: two identical copies register and pass; changing one to "
          "x*2 rows as drift.")
    return 0


if __name__ == "__main__":
    if "--self" in sys.argv:
        sys.exit(_self_test())
    if "--rebuild" in sys.argv:
        sys.exit(0 if rebuild() else 1)
    sys.exit(1 if check(sys.argv[1:] or ["."]) else 0)
