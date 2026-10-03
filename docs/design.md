# How it works

<!-- Fill in: one paragraph saying what the project is, in terms its user would recognize. -->

This document describes what is built. It follows the path the project's main input takes through
it, and does not argue for any of it: why each part is the way it is lives in
[decisions.md](./decisions.md), and what must be true in [requirements.md](./requirements.md).

**What this document admits.** Mechanism, in the present tense. The test is whether a sentence would
still be true after the reason for it is forgotten. What has been built is described here and
nowhere else, so a second description elsewhere is a regression.

**Numbering.** Sections are `## <n>.` and subsections `### <n>.<m>`, cited as `TD<n>` and
`TD<n>.<m>`. A section is renumbered only in a sweep that rewrites every reference to it, which
`scripts/xref.py` confirms.

---

## 1. Architecture

<!-- The layers, or the stages, and the one structural property everything else rests on. -->
