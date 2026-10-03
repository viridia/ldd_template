#!/usr/bin/env python3
"""Report how much there is to read, against a base commit.

Nothing here passes or fails. The numbers are for a reviewer accepting a change, who knows what the
change was for and so whether its growth was earned.

    scripts/growth.py              the working tree against HEAD
    scripts/growth.py <ref>        the working tree against <ref>

Three measures are the same for every project: words per document, the count and size of each
ledger's entries, and how much a session reads before it starts. The fourth, `complexity`, is the
project's own, and is empty until written: what makes a project harder to hold in mind is different
for each one. A library might count its public types and functions, a compiler its grammar
productions, a game its systems and the components they touch. Whatever it counts should grow only
when the project does something new.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

from xref import DESIGN, LEDGERS, REQUIREMENTS, ROADMAP, ROOT

MEMORY_INDEX = (
    Path.home() / ".claude/projects" / re.sub(r"[^A-Za-z0-9]", "-", str(ROOT)) / "memory/MEMORY.md"
)

# Where a document's entries start, keyed by path relative to the root. Requirements are list items,
# and run until the next line that is neither blank nor indented.
ENTRIES = {
    **{
        str(path.relative_to(ROOT)): (prefix, re.compile(rf"^### ({prefix}\d+)\b"))
        for prefix, path, _ in LEDGERS
    },
    str(DESIGN.relative_to(ROOT)): ("TD", re.compile(r"^#{2,3} (\d+(?:\.\d+)?)\.? ")),
    str(REQUIREMENTS.relative_to(ROOT)): ("R", re.compile(r"^- \*\*(R\d+\.\d+[a-z]?) ")),
}
LIST_ENTRY = {"R"}


def git(*args):
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        check=True,
    ).stdout


class Tree:
    """Files as they are at a commit, or in the working tree when `ref` is None."""

    def __init__(self, ref):
        self.ref = ref

    def paths(self, *patterns):
        if self.ref:
            listed = git("ls-tree", "-r", "--name-only", self.ref).split("\n")
        else:
            listed = git("ls-files", "--cached", "--others", "--exclude-standard").split("\n")
            listed = [p for p in listed if (ROOT / p).exists()]
        return sorted(p for p in listed if p and any(re.fullmatch(pat, p) for pat in patterns))

    def read(self, path):
        if self.ref:
            try:
                return git("show", f"{self.ref}:{path}")
            except subprocess.CalledProcessError:
                return ""
        p = ROOT / path
        return p.read_text(encoding="utf-8") if p.exists() else ""


def words(text):
    return len(text.split())


def documents(tree):
    return {p: words(tree.read(p)) for p in tree.paths(r"(?!archive/).*\.md")}


def entries(tree):
    """Per scheme: a list of (id, words) for each entry."""
    out = {}
    for path, (scheme, start) in ENTRIES.items():
        found, current, body = [], None, []

        def close():
            if current:
                found.append((current, words("\n".join(body))))

        fenced = False
        for line in tree.read(path).split("\n"):
            # A fenced block is an example, such as a ledger's "shape of an entry", not an entry.
            if line.lstrip().startswith("```"):
                fenced = not fenced
            if fenced:
                continue
            m = start.match(line)
            if m:
                close()
                current, body = m.group(1), [line]
            elif current and scheme in LIST_ENTRY and line and not line[0].isspace():
                close()
                current, body = None, []
            elif current and line.startswith("#"):
                close()
                current, body = None, []
            elif current:
                body.append(line)
        close()
        out[scheme] = found
    return out


def section(text, heading):
    """A `## ` section's text, up to the next `## ` heading."""
    lines = text.split("\n")
    try:
        i = lines.index(heading)
    except ValueError:
        return ""
    end = next((j for j in range(i + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
    return "\n".join(lines[i:end])


def bootstrap(tree):
    """What a session reads before it starts: CLAUDE.md, the memory index, and the orientation
    sequence CLAUDE.md gives. The memory index is not versioned, so it is today's on both sides."""
    roadmap = str(ROADMAP.relative_to(ROOT))
    parts = {
        "CLAUDE.md": words(tree.read("CLAUDE.md")),
        f"{roadmap}, Where this stands": words(section(tree.read(roadmap), "## Where this stands")),
        "docs/issues.md": words(tree.read("docs/issues.md")),
    }
    if MEMORY_INDEX.exists():
        parts["memory index (unversioned)"] = words(MEMORY_INDEX.read_text(encoding="utf-8"))
    return parts


def complexity(tree):
    """The project's own measure of how much there is to hold in mind, as {label: count}.

    Read files through `tree`, so the same count runs against the base and the working tree:
    `tree.paths(r"src/.*\\.cpp")` lists them and `tree.read(path)` returns one's text. A line scan
    is close enough; the numbers are read as deltas, not as truth.
    """
    return {}


def row(label, before, after, width):
    delta = after - before
    sign = f"{delta:+d}" if delta else "."
    print(f"  {label:<{width}} {before:>8} {after:>8} {sign:>8}")


def table(title, before, after, total=True):
    keys = list(dict.fromkeys([*before, *after]))
    width = max(map(len, keys), default=0)
    print(f"\n{title}\n  {'':<{width}} {'base':>8} {'now':>8} {'delta':>8}")
    for k in keys:
        row(k, before.get(k, 0), after.get(k, 0), width)
    if total:
        row("total", sum(before.values()), sum(after.values()), width)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("base", nargs="?", default="HEAD")
    args = ap.parse_args()

    base, now = Tree(args.base), Tree(None)
    short = git("rev-parse", "--short", args.base).strip()
    print(f"Base: {args.base} ({short}). Now: the working tree.")

    table("Markdown words, by document", documents(base), documents(now))

    print("\nEntries: count, mean words, largest (base -> now)")
    b, n = entries(base), entries(now)
    for scheme, _ in ENTRIES.values():

        def summary(found):
            if not found:
                return "-"
            big = max(found, key=lambda e: e[1])
            return f"{len(found)}, {sum(w for _, w in found) // len(found)}, {big[0]} {big[1]}"

        print(f"  {scheme:<6} {summary(b[scheme]):>22} -> {summary(n[scheme])}")

    table("Bootstrap reading, in words", bootstrap(base), bootstrap(now))

    before, after = complexity(base), complexity(now)
    if before or after:
        table("Complexity", before, after, total=False)
    else:
        print("\nComplexity: not yet defined; see complexity() in scripts/growth.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
