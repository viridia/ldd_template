# Recon prompt template

Copy this verbatim into an `Explore` agent, substituting the files for the group. It is long on
purpose: the agent starts cold, with no access to the conversation, to `AGENTS.md`, or to the dial.

Substitute `{{ROOT}}`, `{{LANGUAGE}}` and `{{FILES}}`, and delete this header before sending.

---

You are doing read-only reconnaissance for a comment-grooming pass on a {{LANGUAGE}} project at
`{{ROOT}}`. DO NOT EDIT ANY FILE. Your output is a ranked list of candidates for a human editor.

Scope: exactly these files — {{FILES}}. Read them fully.

## The project's house style

Comments divide by **who reads them**, which is not the same as which marker they carry.

- **Internal comments, and documentation on a private or internal item**, address a maintainer.
  Terse. They must not explain what a maintainer already knows (the language's semantics, the
  framework's standard behaviour). They comment the non-obvious decision — the thing that would
  break if someone changed it. They may detail an algorithm or a theory of operation where genuinely
  needed. They legitimately keep R-number and `docs/` references, and may use the project's own
  vocabulary freely.
- **Documentation on public items** is for someone using the code. Pedagogy rules: explain the
  concept, show the usage, say why it matters. It must NEVER cite a requirement number (R4.2), a
  design section (TD5.3), a decision (D22), an issue (I7), or a development chunk ("chunk 88") —
  wherever the documentation is published, those documents do not exist. It must also not explain
  *how the item is implemented*; that describes an internal choice to someone who cannot see it and
  freezes it into the public documentation.

**Check visibility before reporting a doc-comment violation.** Documentation on a private function
is maintainer-facing and is governed by the first bullet, not the second.

## What to find, ranked highest-value first

1. **Restatement across locations.** A comment saying something already said by its own adjacent doc
   comment, by another comment in these files, or by `docs/design.md`. This is the highest-value
   category — always report the other location. Consult `docs/design.md` where a comment cites a
   `TD` section or covers a topic it documents. The project's rule is that what has been built is
   described in exactly one place, so a second description anywhere is a real finding.
2. **Story rather than conclusion.** A comment narrating how the design was arrived at — what it
   used to do, what bug was hit, what was tried — where the conclusion alone would serve. Quote the
   narrating sentence. IMPORTANT: a bug story that stops a future maintainer re-introducing the bug
   is worth KEEPING in compressed form. Flag those "compress", not "cut".
3. **Doc-comment citations.** An R-number, TD section, D-number, I-number or "chunk N" inside
   documentation on a **public** item.
4. **"chunk" anywhere in a comment.** Development-methodology vocabulary with no referent in the
   project's design. Worse in public documentation, but wrong in an internal comment too.
5. **House-style tells**, in user-facing prose:
   - Retired metaphors — "load-bearing", "seam", "fold", "reach for" used *figuratively*. Domain
     vocabulary is not a metaphor: a type or function with one of these names is a real name. Do not
     report those.
   - Manufactured significance — "Crucially,", "Importantly,", "It's worth noting that", "Remember
     that".
   - Defending anything — a doc comment arguing for the design rather than describing it.
   - Hedges that gate no real exception — "simply", "just".
   - A constant diet of em-dash asides.
   - Unusual punctuation or phrasing.
   - "nothing" where a positive term exists ("later ticks take nothing" → "take none"). Most uses
     are ordinary English ("nothing fires it") and are fine — report only ones with a real positive
     alternative.
6. **Comments explaining the obvious** — restating the adjacent line, or enumerating what a reader
   can already see.

## Calibration

A real edit already accepted, so you can judge severity: a 36-line theory-of-operation block became
27 lines.

OUT: a parenthetical saying what the code "did originally"; a rationale already stated verbatim on
the function it described; the word "load-bearing"; "take nothing" → "take none"; and a "Theory of
operation. … Three rules keep those from interfering." preamble.

STAYED: every "this would fail silently" warning, every constraint on where code may move, a
paragraph defending a non-obvious design against a plausible simplification, and a link to an
upstream issue.

**The dial: keep every conclusion, cut history, restatement, scaffolding and tells.**

The counterweight matters as much: **concise is not thin.** Cut the padding around a parameter, an
error or an edge case, not the parameter, error or edge case itself. A block that is already
conclusion-first should shrink by nothing, and reporting that it cannot be cut is a useful answer.

## Output format

A flat ranked list. Each entry exactly one line:

`path/to/file:LINE` — CATEGORY — what to do, in one line — (for restatement: the other location)

At most 60 entries. **Prefer 25 excellent entries to 60 padded ones.** Omit any entry you are not
confident about — a noisy list is worse than a short one. Do NOT propose replacement prose; the
human editor writes that.

A warning that applies to you directly: *ask a model to find sixty problems and it will find sixty.
Some of what comes back is real and some is a rule nobody would ever violate.* Returning a list at
the cap will be read as evidence it was padded.

Finish with a two-sentence assessment of how much fat these files actually carry, so the caller can
decide whether the remaining groups are worth the same pass.
