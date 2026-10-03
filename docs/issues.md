# Findings awaiting triage

The triage queue: things known to be wrong, missing, or out of proportion, and proposals to widen
the project's scope, that the author has not yet decided what to do about. An entry leaves when that
decision is made — given a chunk, an entry in [deferred.md](./deferred.md), a decision in
[decisions.md](./decisions.md), or dropped — and whatever it knew goes with it to that destination.
Nothing here describes what the project does, which is [design.md](./design.md)'s job. Why this is a
file rather than an issue tracker is in [workflow.md](./workflow.md).

**How to read an entry.** Each says where the problem is, what someone would actually observe, and
whether it was confirmed by running something or only by reading. Some will have been found by a
model asked to scan the source, and some of those are rules nobody would violate, so that
distinction matters; where the reachable case is hypothetical, the entry says so. A sketched fix
carries its effort level, `E[n]` ([G7](./guidelines.md)); an entry without a sketch is not yet
scoped, and one that cannot be sketched yet says what it waits on, under _Before a sketch_.

**A requirement below `MUST` is cited with its level**, as `R<s>.<n> (MAY)`: a gap against a `MAY`
is a smaller thing than it reads out of context (G13).

**Line numbers drift.** Take a `file:NNN` as "roughly here"; the symbol named beside it is the part
that stays good. Re-verify before acting on one.

**Numbering.** Each entry is `I<n>`, a permanent identity from a single counter, independent of its
tier, and never reused. A gap in the sequence is a retired entry. A reference to an entry is
rewritten to its destination when it leaves; `scripts/xref.py` fails on one that points nowhere.

**Next: 1.**

**What the tiers mean.**

|                         | Test                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------ |
| **1. Live**             | An ordinary build, an ordinary call, and the answer is wrong                                     |
| **2. Latent**           | The code is wrong and the path is not taken in tree — a feature exists that nothing has used yet |
| **3. Absent**           | Not wrong, missing, where a requirement or the acceptance test's own job says it should exist    |
| **4. Prose**            | A comment or document contradicts the code. No behaviour at stake                                |
| **5. Cost and surface** | Public items nothing asks for, and machinery out of proportion                                   |
| **6. Proposed**         | No requirement asks for it, and someone argues it should: an expansion of the requirements       |

**The shape of an entry.**

```markdown
### I<n> <what someone would observe, as a sentence>

`file` `symbol`, and wherever else it reaches · confirmed by <what was run>, or reasoned from the
code, **not probed**

What happens, and to whom. A paragraph, not a story.

_Fix, sketched (E[n]):_ the change, in a sentence or two, and the alternative where there is one.
```

---

## 1. Live — an ordinary build gets a wrong answer

## 2. Latent — the code is wrong and nothing in tree takes the path

## 3. Absent — something should exist and nothing does

## 4. Prose — a comment or document contradicts the code

## 5. Cost and surface

## 6. Proposed — something no requirement asks for

---

## Checked and correct

Recorded so nobody re-derives it. Every one of these was read against the code and holds. A scan
that reported one of them as a defect is listed under **Plausible and wrong**, with why.
