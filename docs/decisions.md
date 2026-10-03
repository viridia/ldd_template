# Decisions

Why the project is shaped the way it is. [design.md](./design.md) says how it works and does not say
why; this is the other half.

**What earns an entry.** A decision belongs here only if reversing it would break something
expensive: a public interface, a stored format, the shape of a core subsystem. The test is that the
reversal cost can be named in a sentence. If it cannot, it is a code comment, not a decision.

Each entry says what was decided, what it rules out, and what reversing it would cost. Where a
decision has an accepted price or an unresolved remainder, that is stated rather than left for a
reader to discover.

**What an entry keeps.** An entry is read by someone weighing whether to reverse it, so it keeps
what would change their mind: what going back would cost, and each fact that makes a rejected
alternative worse, cited so that its expiry can be noticed. A choice between alternatives that were
equally good needs no argument; saying it was arbitrary is enough, and tells the reader nothing is
waiting down the other path. An entry that has been revised states the decision as it now stands,
not how the argument got there.

Numbers are identities, and an entry is never renumbered — a withdrawn one is struck and kept.

[requirements.md](./requirements.md) tags requirements with these numbers, as `(D<n>)`, where a
requirement follows from a settled decision.

**The shape of an entry.**

```markdown
### D<n> — <the decision, as a sentence>

What was decided. What it rules out. **Reversing it** would cost <the sentence the test asks for>.
```

---

| #   | Decision | Mechanism |
| --- | -------- | --------- |
