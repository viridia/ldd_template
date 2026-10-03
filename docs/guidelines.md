# Guidelines

How this project makes the judgements it makes repeatedly: how much to build, and what shape code
takes. Read the first group before scoping a chunk and the second before writing code.

**What this document admits.** Advice a maintainer would otherwise have to learn by being corrected.
The test is whether someone new, following it, would choose differently than without it. A guideline
may be departed from, with the reason stated where the departure is made ("departs from G5 because
…"); a requirement in [requirements.md](./requirements.md) may not. What the project is built to do
belongs there, and why a particular choice was made belongs in [decisions.md](./decisions.md).

**Where a guideline comes from.** A correction the author has had to make more than once. Each is
written with the case that produced it, because the case is what lets a reader recognize the next
one. The ones here at the start are general; a project's own accumulate in the second group.

**Numbering.** Each guideline's number is a permanent identity from a single counter, independent of
its group, and never reused. A gap in the sequence is a retired guideline.

**Next: 14.**

---

## 1. Scoping

### G1 — Build for a use that exists

Anchor every interface and every chunk to a concrete use, never to a hypothetical one: an imagined
problem is unbounded, and a real one is not. Where a type could accept arbitrary combinations or
only the ones something asks for, take the narrow type, even at the cost of a slightly larger
surface. A closed enumeration of the four cases a caller needs beats an open pair of arbitrary
values: the pair admits combinations nothing wants, and each needs a fallback, an error or a caveat.

### G2 — The cheaper defensible design wins

Between designs that are both correct enough, choose the one with less code and less retained state.
Runtime cost counts as investment alongside code. How uncertain the use case is sizes the
investment: the less sure the benefit, the less it is worth spending. Before engineering against a
defect a chunk names, ask what a user observes and whether prior art treats it as a problem; a
mechanism planned against a hypothetical complaint often evaporates once it turns out the
established tools in the field do the simple thing and nobody minds.

That nothing in tree exercises a use sizes its priority. It is not evidence that nobody wants it:
imagine the strongest case before dismissing one.

### G3 — Trace a constraint to its source

When a chunk justifies scope with "X must hold", find the requirement that says so before building
for it. A claim can be an assumption a later document inherited: a component that "must stay
generic" may trace back to a debugging aid that reused it for convenience, and was never required.
Check too whether data already in hand answers the need, before declaring something new to hold it.

### G4 — A requirement can bend

A requirement is written down, not immovable. When a design contorts around one, say which
requirement is forcing it and what relaxing it would buy, and offer withdrawal when its reason has
gone. Test a requirement against how its output is consumed, not only against its own text. Read a
parenthesized list as illustration unless it says otherwise, and write illustrative lists with
"e.g.": a list of names read as exhaustive is how examples become scope. Requirements drafted early,
from a survey of prior art, may carry a motivating case that is stale.

### G13 — Read a requirement's level before building for it

A chunk or issue that cites a requirement inherits its level, and out of context every citation
reads like law. Before scoping work around one, check whether it is a `MUST`, and where it came from
(its `from:` tag): a `MAY` drawn from a survey of other products is evidence that someone once
wanted it, and a chunk built on it is optional work that should say so. Priority inflates silently,
one confident citation at a time, which is why the level travels with the citation.

### G5 — An exclusion has a cost too

A scope-limiting "not doing X" is not free until its enforcement is priced. Excluding one case from
a general mechanism can take a special case in every module that touches it, and each special case
is a place for a bug; folding the case into the general path is sometimes less code than the
exclusion.

### G6 — Do not codify what is not understood

An observation nobody can explain does not become guidance in the README, a requirement or the
design. Record what was seen, and any proposed cause as a hypothesis a measurement could falsify, on
the chunk that will run it; it becomes a documented fact once measured. A rule written around a
symptom hardens a guess into documentation.

### G7 — Estimate effort on an exponential scale

An estimate is for sorting and prioritizing, not scheduling, so a wrong one costs a misplaced item
and nothing more. Each level is several times the one below, judged by what the change touches
rather than by how long it seems:

| Level | Touches                                                                             |
| ----- | ----------------------------------------------------------------------------------- |
| E[0]  | One line, or prose only                                                             |
| E[1]  | One function or one document section, with its test                                 |
| E[2]  | Several functions, or a new piece of the acceptance test; the design stays as it is |
| E[3]  | A new mechanism or a changed public interface, and a `TD` section rewritten: one chunk |
| E[4]  | More than a chunk, or a changed requirement or decision; split before it is written |
| E[5]  | A core subsystem redesigned                                                         |

A chunk carries its level at the end of its heading, and a sweep's is one unit's. An issue carries
one on its sketched fix, and only there: an issue without a sketch has nothing to measure yet, so a
missing level marks it unscoped. A level is written once and overwritten when scoping proves it
wrong, not kept up to date. It measures effort, not risk: a one-line change to a one-way door is
still E[0].

## 2. Code

### G8 — A test reads as a narrative

Read top to bottom, a test tells what happens in order. A helper is welcome when it compresses a
step the reader would otherwise write inline and its call site says what it does, as `press(key)`
does wherever `press` is defined. A table-driven loop, a parametrized helper or an assertion helper
with its own branching makes the reader reconstruct the story.

### G9 — A name carries its adjective

Name things explicitly, even at the cost of a word: `FoldKind` over `Fold`, `BindingReading` over
`Reading`, a local `held_button` over a bare `held`. A one-word name assumes the reader shares the
writer's context, and a name that narrows what it could mean makes the code easier to follow.
Closure parameters are exempt. The same holds for prose: a term coined mid-analysis is introduced
before it is used.

### G10 — A pair of same-typed values is a struct

A tuple whose slots share a type, such as `(string, string)` mapping one name to another, becomes a
small struct with named fields. Two slots of one type can be swapped without the compiler noticing.
Define the struct up front rather than waiting for review to ask for it.

### G11 — Similar items sit side by side

Parallel functions, a family of predicates, the variants of one pattern: each sits beside its
siblings, so a reader compares them without other code in between. Where a caller walks through them
in order, consider placing them just below it, in that order.

### G12 — In dense code, orient at the point of use

Most comments follow the rule that a thing is explained once. Code where understanding a line takes
several jumps, a call site to a table to the type it holds, is the exception: there, a comment
orients the reader where a concept is used, with a sentence beside the pointer, and accepts some
restatement to do it. A bare cross-reference makes the reader jump again before the line makes
sense. Which modules qualify is named here as they are found; the rule for `docs/` is unchanged.
