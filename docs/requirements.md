# Requirements

<!-- Fill in: what the project is for, in one paragraph, and who it serves. -->

**What this document admits.** Normative statements. The test is whether one can be violated; if
nothing could violate it, it is design. A requirement states what must be true and stops. It may
carry whatever structure it takes to say that precisely — enumerated states, a table of cases, a
worked example — but not the argument for it. A withdrawn requirement keeps enough to stop the idea
being re-proposed. How this document is drafted is in [workflow.md](./workflow.md).

**The shape of a requirement.** One list item, defined once and cited bare everywhere else:

```markdown
- **R1.1 (MUST)** _(D2)_ _(from: author)_ The statement, and one clause of reason if it needs one.
  - A sub-bullet is part of the requirement it sits under.
```

Requirements are numbered `R<section>.<n>` so they can be referenced from the design, the roadmap
and the code. A `(D<n>)` tag marks a requirement that follows from a settled decision, numbered as
in [decisions.md](./decisions.md).

**Levels.** `MUST`, `SHOULD` and `MAY` per RFC 2119. `WITHDRAWN` marks a requirement that no longer
should hold, and `BLOCKED` one that should but cannot yet be met, naming the deferred entry that
waits on it.

- **A `MUST` names something without which the project fails its purpose**, for the people this
  document says it serves. Ask what breaks for them if it is missing; if the answer is "it would be
  less complete", it is a `SHOULD`.
- **Prior art is evidence of a use, not of a level.** That an established product does something
  shows someone wanted it, and nothing about how much this project needs it. A requirement drawn
  from a survey enters as a `MAY` unless the author raises it.
- **A level travels with its citation.** Outside this document, in the roadmap, issues and deferred
  entries, a `SHOULD` or `MAY` is cited with its level, as `R<s>.<n> (MAY)`, so a chunk built on it
  does not read as an obligation once the context is gone. `scripts/xref.py` checks this.

**Provenance.** Every requirement carries a `_(from: …)_` tag saying where it came from, so the
question "why is this here?" has an answer other than "it was in the first draft". The tag holds one
or more of these, separated by commas:

| Source | Meaning |
| --- | --- |
| `author` | the author's own goal, stated while drafting or since |
| `sources/<name>` | a survey written up in [sources/](./sources/README.md), which `<name>.md` records |
| `R<s>.<n>` | derived from another requirement, which it would fall with |
| `D<n>` | follows from a decision |
| `unrecorded` | predates this rule, and nobody knows; honest, and greppable |

`scripts/xref.py` fails on a requirement with no tag, and on a source file that does not exist.

## Scope

<!-- Boundaries set before drafting: what is owned, what is not, and what is first-class rather than
deferred. -->

## Who this is for

<!-- Each audience the project serves, what it needs and what it is short of; then where their needs
conflict, and the rule that resolves a conflict. Most tensions later in this document are this one
in another form, so it is stated once here rather than rediscovered per section. -->

## Non-goals

## 1. <the first area>
