# Roadmap

The work that is left, and the gaps that are known. It orders that work into chunks small enough to
review individually — a *sequence*, not a schedule, and any chunk may be reordered once the one
before it has been read.

**What this document admits.** Work not done, and gaps. The test is whether an entry names something
that will change; if it describes the present, it belongs in [design.md](./design.md), and if it
explains why the present is as it is, it belongs in [decisions.md](./decisions.md). What has been
built is described in exactly one place, and this is not it. The landed index below names chunks; it
does not describe the project.

Ground rules, house style and the commit-message convention are in [AGENTS.md](../AGENTS.md); they
are about the work rather than about the project. Ground rule 5 is the one this document is built
around: nothing outstanding may be left without a destination, which is a chunk here or a gated
entry in [deferred.md](./deferred.md).

**How a chunk is written.** A `###` heading reading `### <n>. <title> · E[<level>]`, the level from
G7. Its body says what changes, in sentences that assume nothing, then bullets: the decisions the
chunk makes or leaves to itself, **Not doing:** for what it deliberately omits (ground rule 4), and
**Verified by:** for how it will be shown to work (ground rule 2). A requirement below `MUST` is
cited with its level, as `R<s>.<n> (MAY)`, so the chunk does not read as an obligation (G13). A
chunk that takes on an issue carries what the issue knew, and the issue leaves
[issues.md](./issues.md); references to it are rewritten to the chunk.

**Numbering.** A chunk's number is a permanent identity, taken from the counter below and never
reused; its position in the sequence is separate and changes freely. Lettered parts (`12a`, `12b`)
share their parent's number.

**Next: 1.**

---

## Where this stands

[design.md](./design.md) is what the project does today, [issues.md](./issues.md) is what is known
to be wrong and not yet routed, and [deferred.md](./deferred.md) is what was decided against for
now, each with the gate that reopens it. The chunks below are the rest of the delta.

<!-- Fill in: the target the sequence aims at — the first thing someone could run and judge — and
why it is a better acceptance test than a synthetic one. -->

---

## What has landed

An index, not a description. Chunk numbers are stable identities cited in commit messages and in
code comments, so the sequence stays recoverable; what each chunk delivered is in git.

| #   | Chunk |
| --- | ----- |

---

## Next

The author's shortlist, in order.

---

<!-- Chunks go below, grouped under `##` headings by area. Two groups recur in every project and are
worth keeping from the start: -->

## Sweeps

Each of these passes over a whole document or module. A sweep lands a unit at a time, as a lettered
chunk small enough to finish in one session, and a unit is never left half done. A unit starts and
ends with `scripts/growth.py`, so its effect is measured rather than asserted, and its section's
**Done** line records it.

## Tooling

Tools the project runs on itself, under `tools/` and `scripts/`, rather than anything the project
ships.
