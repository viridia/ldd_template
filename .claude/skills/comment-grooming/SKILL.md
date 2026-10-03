---
name: comment-grooming
description: A whole-tree sweep of comments and doc comments for house-style violations and duplicated explanations, using read-only recon subagents to find candidates before editing anything by hand. Expensive; use only when the author asks for a comment sweep, typically after the house style in CLAUDE.md has changed and the tree must be brought into line. Not for routine compliance, which is the per-chunk second pass over changed comments that CLAUDE.md's house style asks for.
---

# Comment grooming

A sweep over the project's comments. Recon is delegated and parallel; **every edit is made by hand,
serially, in one voice**. The whole value of the sweep is that the code reads as though one
maintainer wrote it, and parallel editing agents destroy exactly that.

## When to run it

Rarely. Comments stay compliant through the second pass `CLAUDE.md` asks for at the end of each
chunk, over the comments that chunk changed; this skill is for the moment that stops being enough,
when the house style itself has changed and the existing tree predates it. It reads every comment in
scope, and a whole-tree run through parallel subagents once cost a week's token budget in two days.
Price it before starting (`CLAUDE.md`'s "Context" section), and prefer scoping it to the files the
change actually affects: the workflow below works the same over one directory as over the tree.

## What this is not

Not a bug hunt — use `/code-review`. Not a refactor. No line of code changes; if a comment is wrong
about what the code does, that is a finding for `docs/issues.md`, not a licence to fix the code in
the same pass.

## The dial

**Keep every conclusion. Cut history, restatement, scaffolding and tells.**

The worked example, from the sweep that produced this skill: a 36-line theory-of-operation block
became 27 lines.

Out: a parenthetical saying what the code "did originally"; a rationale already stated verbatim on
the function it described; the word "load-bearing"; "take nothing" → "take none"; and a "Theory of
operation. … Three rules keep those from interfering." preamble.

In: every "this would fail silently" warning, every constraint on where code may move, a paragraph
defending a non-obvious design against a plausible simplification, and a link to an upstream issue.

A block that is already conclusion-first shrinks by nothing, and that is a correct outcome. The real
yield is usually category 1 below, not length.

## Categories, in value order

1. **Restatement across locations.** A comment saying what is already said by its own adjacent doc
   comment, by another comment elsewhere, or by `docs/design.md`. This is the highest-value category
   and the one that justifies the recon cost, because it cannot be found by reading one file. It is
   also the project's named regression: what has been built is described in exactly one place, and a
   second description anywhere is the thing to watch for. The fix is to pick the canonical home and
   let the others cross-reference it, in a clause ("see the note on `X`").
2. **Story rather than conclusion.** Prose narrating how the design was reached — what it used to
   do, what bug was hit, what was tried. A bug story that stops a maintainer re-introducing the bug
   earns its place **compressed to the warning**; cut the narrative tense, not the trap.
3. **Doc-comment citations.** An `R`-number, a `TD` section, a `D`-number or an issue inside public
   API documentation. Wherever that documentation is published, the cited documents do not exist.
   The reasoning usually survives the edit: drop the parenthesis, keep the sentence. Internal
   comments keep their citations.
4. **"chunk" anywhere in a comment.** Development-methodology vocabulary with no referent in the
   project's design. Worse in public documentation, but wrong in an internal comment too.
5. **House-style tells.** Judge these by *reader*, not by comment marker — see "Which reader" below.
   - *Retired metaphors*: "load-bearing", "seam", "fold", "reach for" used figuratively, which ask
     the reader to learn what a word means here before the sentence parses. Domain vocabulary is not
     a metaphor: a type named `Fold` is a real name.
   - *Manufactured significance*: "Crucially,", "Importantly,", "It's worth noting that", "Remember
     that". If the sentence matters it matters without the announcement.
   - *Defending anything*: a doc comment arguing for the design rather than describing it. The
     argument belongs in `docs/decisions.md`, or in the chunk's review conversation.
   - *Hedges that gate no real exception*: "simply", "just".
   - *A constant diet of em-dash asides*, which reads as a fingerprint once noticed.
   - *Unusual punctuation or phrasing.*
   - *"nothing" where a positive term exists*: "later ticks take nothing" → "take none". Most uses
     are ordinary English ("nothing fires it") and stay.
6. **Comments explaining the obvious** — restating the adjacent line, enumerating what a reader can
   see, or explaining the language's semantics or the framework's standard behaviour to a maintainer
   who knows them.

## Which reader

The rules divide by who reads a comment, which is not the same as which marker it carries.

Documentation on a public item is public documentation: pedagogy rules, no citations, and every tell
in category 5 applies. It also must not explain *how the thing is implemented* — public
documentation describes what the item does and why it matters to a caller, and an implementation
detail there both misleads and freezes an internal choice into the API's documentation.
Documentation on a private or internal item has a maintainer as its reader, so it keeps its
citations, may use the project's own vocabulary freely, and may describe the implementation at
whatever length the algorithm needs. **Check visibility before reporting a doc-comment violation.**

And the counterweight, which matters as much as the dial: **concise is not thin.** Cut the padding
around a parameter, an error or an edge case — not the parameter, error or edge case itself. A doc
comment that loses a documented failure to brevity has been made worse.

## Workflow

### 1. Survey

Measure before planning, so the split is sized from the real numbers. Set `SRC` to the source
directories and `INC` to the `--include` globs for the project's language, and `C` to a regular
expression matching a comment line's start:

```sh
SRC="src/"; INC="--include=*.cpp --include=*.h"; C='^\s*//'
echo -n "doc-comment citations: "; grep -rnE "$C" $INC $SRC \
  | grep -cE 'R[0-9]+\.[0-9]+|\bTD[0-9]+|\bD[0-9]+\b|\bI[0-9]+\b|[Cc]hunk [0-9]+'
echo -n "chunk refs:            "; grep -rnE "$C.*\bchunks?\b" $INC $SRC | wc -l
echo -n "metaphors:             "; grep -rniE "$C.*(load-bearing|\bseams?\b|reach for)" $INC $SRC | wc -l
echo -n "hedges:                "; grep -rnE "$C.*\b(simply|just)\b" $INC $SRC | wc -l
echo -n "manufactured signif.:  "; grep -rnE \
  "$C.*(Crucially|Importantly|Notably|worth noting|Remember that|Keep in mind)" $INC $SRC | wc -l
echo -n "'nothing' in comments: "; grep -rnE "$C.*\bnothing\b" $INC $SRC | wc -l
echo "comment lines, per file, heaviest first:"
grep -rcE "$C" $INC $SRC | sort -t: -k2 -rn | head -15
```

These count *lines*, not occurrences, which is the right unit here. The citation count includes
internal comments, which may cite; it sizes the work rather than counting violations.

### 2. Group the files

Group by area, not by rule. Reading a file once per rule is the waste `CLAUDE.md` warns about; every
rule gets applied in one read. Aim for roughly 250 comment lines per group, and keep files that talk
about each other together.

### 3. Recon, all groups, before any editing

One read-only `Explore` agent per group, in parallel. **Run every group's recon before editing
anything.** Duplication clusters span groups: one fact can be written out four times across three
files and `docs/design.md`. Merging a cluster before you can see all of it means picking a canonical
home that the next group then touches again.

Use `Explore`, never a general agent — the agents must not be able to edit. Write each list to the
scratchpad.

The prompt template is in [recon-prompt.md](recon-prompt.md). It is long on purpose: the agent
starts cold, with no access to the conversation, `CLAUDE.md`, or the dial.

### 4. Spot-check before trusting a list

On receiving each list, verify three or four of its highest-ranked claims directly. This is a
go/no-go on the list as a whole, not per-entry validation — that happens naturally at edit time,
since the file is open anyway.

A list that survives the spot-check is still only a candidate list. An agent that read the file once
can be confidently wrong about what a comment is for, and the reported line numbers drift if
anything above them was edited first.

### 5. Edit by hand, one group per commit

Serially. One voice. Never delegate the editing, and never run editing agents in parallel — it makes
the diff pane unreviewable and produces as many styles as there are agents.

After each group, before moving on:

```sh
scripts/devfmt.py --diff
```

`--diff` reflows only paragraphs overlapping a changed line, so pre-existing debt elsewhere is left
alone. Run the style pass *before* devfmt, never after, or the same paragraph gets reformatted
twice. If devfmt refuses the project's language, adding it is a chunk of its own; finish the sweep
without it and note the overflow.

Two traps that cost time in the first sweep.

`awk 'length>100'` counts **bytes**, so an em-dash reads as three columns and reports violations
that are not there. Shell `${#var}` does the same under some shells. Measure characters, or just
trust devfmt.

BSD `sed` (macOS) has no `\b`, so a comment-wide rename needs `perl`, not `sed`. `sed` fails
silently here.

### 6. Finish

`scripts/verify.sh` at the end of the sweep. A comment-only sweep cannot break a test, which is
exactly why an unexpected failure is worth reading rather than assuming.

## Where findings go

Candidate lists live in the scratchpad and are consumed by the edit passes.

Anything still unfixed when the sweep ends **graduates to a `docs/issues.md` entry**, tier 4 (*Prose
— a comment or document contradicts the code. No behaviour at stake*), numbered from that document's
counter. Nothing outstanding is left without a destination; a finding with no entry is a finding
that will be dropped.

Two things always graduate rather than being fixed in the sweep: a comment that is *wrong* about the
code rather than merely verbose, and a duplication cluster whose canonical home is a genuine design
question rather than a clerical choice.

## Calibration

Ask a model to find sixty problems and it will find sixty. Some of what comes back is real and some
is a rule nobody would ever violate.

The recon prompt caps its list and asks for omissions rather than padding, which is the guard. If a
returned list is at its cap, treat that as a signal it was padded.
