# Deferred

Work that has been decided against for now, each entry held until a stated gate.
[issues.md](./issues.md) holds what has not been decided yet; an entry here has been, and the
decision was "not yet". [roadmap.md](./roadmap.md) holds the work that is scheduled.

**What this document admits.** Work that will be done when a named event happens, and not before.
The gate is the entry: one with no gate is an item that will be dropped, which is ground rule 5.

**When a gate fires**, the entry becomes a chunk in `roadmap.md` and is deleted here, and whatever
it knew goes into the chunk's section.

A requirement below `MUST` is cited with its level, as `R<s>.<n> (MAY)` (G13).

**Numbering.** Each entry's number is a permanent identity from a single counter, independent of its
group, and never reused. A gap in the sequence is an entry that left.

**Next: 1.**

**How it is grouped.** By the kind of gate, so the question "has anything fired?" is asked of one
group at a time. A dependency's version moving is the usual first group, checked on every upgrade.

**The shape of an entry.**

```markdown
### X<n> — <the work, as a title>

**Gate:** <the event that reopens it, specific enough that someone can tell it has happened>.

What the work is, what is known about it, and what it would touch.
```

---

## 1. A dependency moving past the pin

## 2. A decision still open elsewhere

## 3. Something in tree that needs it
