#!/usr/bin/env python3
"""Check that the documents' cross-references resolve.

Numbering schemes tie the documents and the source comments together: `R<section>.<n>` for
requirements, `D<n>` for decisions, `TD<n>` for design sections, and one prefix for each counted
ledger. Nothing else validates them, so they stay correct only because people are careful. This
reports every reference that points nowhere.

    scripts/xref.py             every check; exit 1 if any fails
    scripts/xref.py --report    also list requirements nothing cites
    scripts/xref.py --quiet     failures only, no summary

Each numbered document owns a prefix, so a reference resolves without knowing where it is written:
`R4` is a section of `docs/requirements.md` and `R4.2` a requirement inside it, `TD5.3` a subsection
of `docs/design.md`, `X12` an entry in `docs/deferred.md`, `I7` one in `docs/issues.md`.

A document whose entries are numbered from a counter carries its `**Next: <n>.**` line, and the
counter must exceed every number the document has ever used, read from its git history as well as
the working tree: an entry routed out leaves a gap that must not be reissued.

Two checks guard the requirements themselves. Every requirement carries a `_(from: …)_` provenance
tag naming where it came from, and a survey it names must exist under `docs/sources/`. And in the
documents read out of the requirements' context (`LEVEL_CITED`), a requirement below MUST is cited
with its level, as `R4.2 (MAY)`.

The tables below are this script's configuration, and `show.py` and `growth.py` read them too. A new
ledger is a row in `LEDGERS`; a source tree whose comments cite anchors is a row in `CODE`.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

REQUIREMENTS = DOCS / "requirements.md"
DESIGN = DOCS / "design.md"
ROADMAP = DOCS / "roadmap.md"

# Ledgers whose entries are `### <prefix><n>` headings, numbered from a counter. Each row is
# (prefix, file, whether it carries a `**Next: <n>.**` counter).
LEDGERS = [
    ("D", DOCS / "decisions.md", False),
    ("X", DOCS / "deferred.md", True),
    ("G", DOCS / "guidelines.md", True),
    ("I", DOCS / "issues.md", True),
]

# Source files whose comments cite anchors, as (directory, glob). Empty until the project has
# source. A short prefix can collide with an identifier (`X11`, `D3D`), so check the first run's
# failures for false hits before trusting a clean one.
CODE = [
    # ("src", "*.cpp"),
    # ("include", "*.h"),
]

# Where a requirement's provenance tag may name a survey, as `sources/<name>`.
SOURCES = DOCS / "sources"

# Documents read out of the requirements' context, where a requirement below MUST is cited with its
# level so a chunk built on a MAY does not read as an obligation.
LEVEL_CITED = [ROADMAP, DOCS / "issues.md", DOCS / "deferred.md"]

R_DEF = re.compile(r"^\s*- \*\*(R\d+\.\d+[a-z]?) \((MUST|SHOULD|MAY|WITHDRAWN|BLOCKED)\)\*\*")
FROM = re.compile(r"_\(from: ([^)]*)\)_")
FROM_ITEM = re.compile(r"author|unrecorded|R\d+\.\d+[a-z]?|D\d+|sources/([\w.-]+)")
R_CITE = re.compile(r"\bR\d+\.\d+[a-z]?\b")
R_STAR = re.compile(r"\*\*R\d+\.\d+[a-z]?")
R_SECTION = re.compile(r"\bR(\d+)\b(?!\.\d)")
TD_SECTION = re.compile(r"\bTD(\d+(?:\.\d+)?)\b")
H2_NUM = re.compile(r"^## (\d+)\.")
H3_NUM = re.compile(r"^### (\d+\.\d+)\b")
NEXT = re.compile(r"^\*\*Next: (\d+)\.\*\*")
# A chunk is spent by its roadmap heading, and its number is never reissued after it lands.
CHUNK_DEF = re.compile(r"^### (\d+)[a-z]?\.")


def entry_def(prefix):
    return re.compile(rf"^### ({prefix}\d+)\b")


def entry_cite(prefix):
    return re.compile(rf"\b{prefix}\d+\b")


def sources():
    md = sorted(ROOT.glob("*.md")) + sorted(DOCS.glob("*.md"))
    code = sorted(p for d, pattern in CODE for p in (ROOT / d).rglob(pattern))
    return md, code


def prose(path):
    """Yield (line number, text), skipping fenced code blocks."""
    fenced = False
    for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            yield n, line


def headings(path, pattern):
    return {m.group(1) for _, l in prose(path) for m in [pattern.match(l)] if m}


def highest_ever(path, pattern):
    """The highest number `pattern` has matched in `path`, in the working tree or any commit."""
    lines = path.read_text(encoding="utf-8").split("\n")
    log = subprocess.run(
        ["git", "log", "-p", "--format=", "--", str(path.relative_to(ROOT))],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    # A diff line carries a one-character prefix, so the heading starts at column 1.
    lines += [l[1:] for l in log.stdout.split("\n") if l[:1] in "+- " and l[1:4] == "###"]
    return max((int(m.group(1)) for l in lines for m in [pattern.match(l)] if m), default=0)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--report", action="store_true", help="list requirements nothing cites")
    ap.add_argument("--quiet", action="store_true", help="failures only")
    args = ap.parse_args()

    md, code = sources()

    fails, cited = [], set()

    def fail(path, n, msg):
        fails.append(f"{path.relative_to(ROOT)}:{n}  {msg}")

    # Definitions, and where each one lives, so a definition is not counted as a citation of itself.
    r_defined, r_level, r_dupes = {}, {}, []
    for n, line in prose(REQUIREMENTS):
        m = R_DEF.match(line)
        if not m:
            continue
        rid = m.group(1)
        if rid in r_defined:
            r_dupes.append((REQUIREMENTS, n, rid))
        r_defined.setdefault(rid, n)
        r_level.setdefault(rid, m.group(2))
        # R and D items are checked below with every other citation; only the rest are checked here.
        tag = FROM.search(line)
        if tag is None:
            fail(REQUIREMENTS, n, f"{rid} has no _(from: …)_ provenance tag on its first line")
            continue
        for item in (i.strip() for i in tag.group(1).split(",")):
            source = FROM_ITEM.fullmatch(item)
            if source is None:
                fail(REQUIREMENTS, n, f"{rid}'s provenance {item!r} is not a recognized source")
            elif source.group(1) and not (SOURCES / f"{source.group(1)}.md").exists():
                fail(REQUIREMENTS, n, f"{rid} cites {item}, and docs/{item}.md does not exist")
    req_sections = headings(REQUIREMENTS, H2_NUM)
    des_sections = headings(DESIGN, H2_NUM) | headings(DESIGN, H3_NUM)
    ledgers = [
        (prefix, path, entry_cite(prefix), headings(path, entry_def(prefix)))
        for prefix, path, _ in LEDGERS
    ]

    for path in md + code:
        is_req = path == REQUIREMENTS
        for n, line in prose(path):
            defines_here = is_req and R_DEF.match(line)

            for m in R_CITE.finditer(line):
                rid = m.group()
                if defines_here and r_defined.get(rid) == n:
                    continue  # the definition itself
                cited.add(rid)
                if rid not in r_defined:
                    fail(path, n, f"{rid} has no definition in docs/requirements.md")
                elif path in LEVEL_CITED and r_level[rid] != "MUST":
                    level = r_level[rid]
                    if not line[m.end() :].startswith(f" ({level})"):
                        fail(path, n, f"{rid} is a {level}; cite it here as `{rid} ({level})`")

            for prefix, ledger, cite, defined in ledgers:
                for m in cite.finditer(line):
                    if m.group() not in defined:
                        fail(path, n, f"{m.group()} has no entry in {ledger.relative_to(ROOT)}")

            for m in R_STAR.finditer(line):
                if not R_DEF.match(line):
                    fail(path, n, f"{m.group()} is bold but is not a definition")

            # Markdown only: a bare R-number in source is indistinguishable from any other short
            # identifier. Requirement citations are dotted, so they stay checked everywhere; only
            # the section form is narrowed.
            if path in md:
                for m in R_SECTION.finditer(line):
                    if m.group(1) not in req_sections:
                        fail(path, n, f"R{m.group(1)} is not a section of docs/requirements.md")

            for m in TD_SECTION.finditer(line):
                if m.group(1) not in des_sections:
                    fail(path, n, f"TD{m.group(1)} is not a section of docs/design.md")

    for path, n, rid in r_dupes:
        fail(path, n, f"{rid} is defined more than once")

    counted = [(path, re.compile(rf"^### {prefix}(\d+)\b")) for prefix, path, c in LEDGERS if c]
    counted.append((ROADMAP, CHUNK_DEF))
    for path, pattern in counted:
        counter = next(
            ((n, int(m.group(1))) for n, l in prose(path) for m in [NEXT.match(l)] if m), None
        )
        if counter is None:
            fail(path, 1, "has no **Next: <n>.** counter")
            continue
        n, value = counter
        used = highest_ever(path, pattern)
        if value <= used:
            fail(path, n, f"Next: {value} is stale; {used} has been used, so it should be {used + 1}")

    for line in fails:
        print(line)

    if args.report:
        uncited = sorted(set(r_defined) - cited, key=lambda r: [int(x) for x in re.findall(r"\d+", r)])
        print(f"\nRequirements nothing cites ({len(uncited)}) -- a traceability signal, not a failure:")
        print("  " + ", ".join(uncited) if uncited else "  none")

    if not args.quiet:
        entries = ", ".join(f"{len(defined)} {prefix}" for prefix, _, _, defined in ledgers)
        print(
            f"\n{len(md)} documents, {len(code)} source files | "
            f"{len(r_defined)} requirements, {entries}, "
            f"{len(req_sections) + len(des_sections)} sections | "
            f"{len(fails)} problem(s)"
        )
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
