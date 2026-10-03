# Working on this project

<!-- Fill in: one paragraph saying what the project is, its language and toolchain, and any hard
constraints on the code (target platforms, forbidden features, dependency policy). -->

## Starting a session

One chunk per session, ending at the commit. To orient, in this order — it is cheap and it is the
whole bootstrap:

1. `git log --oneline -5` — what landed, and therefore where in the sequence we are.
2. `docs/issues.md` for what is known to be wrong.
3. The current chunk's `###` section in `docs/roadmap.md`.

Everything below is on demand. Name the session after its chunk, so the author can find it again; if
a session is going to take on a second chunk, say so rather than continuing silently.

## The documents, and when to open one

Every section is numbered, so a known target is one command away: `scripts/show.py <anchor>...`
prints it, given a chunk number or an `I`, `TD`, `D`, `X`, `G` or `R` anchor, and takes several at
once. `--outline` prints only the headings and requirements inside, with line numbers, for a section
too long to read whole; `--toc TD` (or `R`, `D`, `X`, `G`, `I`, `chunks`) lists every heading of one
document, to find a section before its anchor is known. Use that for lookups; see "Context" below
for when not to.

| File | Holds | Reach for it when |
| --- | --- | --- |
| `docs/roadmap.md` | what is left, what is broken, the chunk sequence | **start here for any chunk** |
| `docs/requirements.md` | numbered requirements, `R<section>.<n>`, each with its level and provenance | you need to know what must be true, or a chunk cites an R-number |
| `docs/sources/` | the surveys the requirements were drawn from, a record rather than a ledger | a requirement's `from:` tag names one, or you are asked why a requirement exists |
| `docs/design.md` | how the project works, in sections `TD<n>` | you need the shape of a thing before changing it |
| `docs/decisions.md` | why it is that way, in entries `D<n>` | a decision looks arbitrary, or you are about to reverse one |
| `docs/issues.md` | findings awaiting routing, in entries `I<n>`, tiered by severity | a finding needs routing, or you are about to re-find one |
| `docs/deferred.md` | work decided against for now, in entries `X<n>`, each with its gate | a gate may have fired, or you are about to defer something |
| `docs/guidelines.md` | how this project judges scope and shapes code, in entries `G<n>` | you are about to scope a chunk or write code |
| `docs/architecture.md` | a diagram-led tour for a new maintainer, unnumbered | you are new to the project, or a diagram would settle a question faster than prose |
| `docs/workflow.md` | this process, explained for a human | a person asks how the project is run |

Each numbered document has its own prefix, so a reference never needs to know which document it is
standing in. `docs/requirements.md`'s sections are `R<n>`, told from the requirements inside them by
the dot: `R<s>` is the section, `R<s>.<n>` a requirement in it. `docs/design.md`'s are `TD<n>`, with
subsections `TD<n>.<m>`. Chunks alone are bare numbers, because commit messages and code comments
cite them.

A requirement is defined once, as a list item reading `- **R<section>.<n> (MUST)**` followed by its
`_(from: …)_` provenance tag, and is cited bare everywhere else, so `**` followed by the number
appears nowhere but the definition. The exception is a requirement below `MUST` cited in the
roadmap, issues or deferred entries, which carries its level, as `R<s>.<n> (MAY)` (G13). A new
requirement gets its provenance when it is written, and a `MUST` only when the project fails its
purpose without it: that a competing product does something is not a reason. Indented sub-bullets
are part of the requirement; `scripts/show.py` includes them, where a fixed `grep -A` cuts them off.

## Workflow

Work proceeds in numbered **chunks** defined in `docs/roadmap.md`. Chunk numbers are stable
identities, not positions.

- **The author commits.** Never run `git commit` or `git push`. Produce the commit message as text
  in your reply and stop there.
- **A landed chunk** gets a row in `docs/roadmap.md`'s "What has landed" index, and its `###`
  section deleted from the sequence. What it taught, if durable, becomes an entry in
  `docs/decisions.md`.
- **Ground rule 5 is the one that bites:** nothing outstanding may be left without a destination. An
  item with no chunk number is an item that will be dropped. "Later" and "its own decision" are not
  destinations — an entry in `docs/deferred.md` with a stated gate is.
- **A new chunk gets a `###` section**, with its effort level (G7), and nothing else. A chunk split
  into lettered parts gives each part its own `###` section; a sweep's units are the exception,
  lettered as they land under the sweep's section. The "Next" list is the author's shortlist: do not
  add to it or reorder it. When suggesting what to take on, sort candidates by effort level.
- **A structural idiom is proposed before it is built.** A new kind of function, module dependency
  or wrapper arrives as options with a recommendation, not in a diff.
- **A plan opens with what changes**, in sentences that assume nothing, and answers a question about
  scope or complexity with counts rather than assurance.
- **Never post publicly.** No issue, PR or comment on a public forum, through `gh` or anything else,
  even when asked to "file an issue": write a short brief for the author to edit and post. Anything
  public speaks in the author's name.
- **The agent's own memory, where it keeps one, is for facts about the author**, such as how they
  work and where their expertise lies: things that would not hold for a different developer. A fact
  about the project belongs in one of the documents, where it is versioned and reviewed.
- **The tools grow with the project.** When the same lookup, check or tally keeps being done by
  hand, propose a script for it, as a chunk under "Tooling" in `docs/roadmap.md`. The scripts in
  `scripts/` and `tools/` began that way and are expected to change.

## Ground rules

1. **One chunk, one reviewable change.** Each chunk is a single branch: code, its tests, and any doc
   changes it forces. If a chunk turns out to be more than roughly a day's reading, it gets split
   before it gets written. Two items that could share a chunk default to two, with an ordering note.
2. **Every chunk is verifiable on its own.** It lands with a test, or with something runnable that
   shows it working. No chunk lands whose only justification is "the next one needs it".
3. **There is always something to run.** The project keeps a runnable acceptance test — an example,
   a demo, a sample input — and it is the arbiter. When a chunk is an internal change, the criterion
   is that *the acceptance test does not change*: a diff there during a refactor chunk is a signal
   the abstraction leaked.
4. **Deliberate omissions are stated.** Each chunk lists what it does *not* do, so review can tell
   "not yet" from "overlooked".
5. **Nothing outstanding is left without a destination.** A chunk that lands short of its own
   description says so, and the obligation is written onto the chunk that finishes the job.

## Where a piece of prose belongs

Each document admits one kind of thing, and the test is what distinguishes them.

| Document | Admits | The test |
| --- | --- | --- |
| `docs/design.md` | mechanism, present tense | Would this still be true after the reason for it is forgotten? |
| `docs/architecture.md` | the shape of the mechanism, taught | Does it help a newcomer build a mental model? A signature, a variant list or an edge case belongs in `design.md`, linked by `TD` section. |
| `docs/decisions.md` | decisions expensive to reverse | Name what breaks if it is reversed. If you cannot, it is a code comment. |
| `docs/requirements.md` | normative statements | Can it be violated? If nothing could violate it, it is design. |
| `docs/sources/` | research, as it was believed when the requirements were drafted | Did a requirement rest on it? Findings are corrected with a dated note, never rewritten. |
| `docs/roadmap.md` | work not done, and gaps | Does it name something that will change? If it describes the present, it is design. |
| `docs/issues.md` | findings not yet routed | Is something wrong, and has no chunk taken it? A finding with a chunk belongs to the chunk. |
| `docs/guidelines.md` | judgement a maintainer would otherwise learn by correction | Would someone new choose differently with it? If it cannot be departed from with a reason, it is a requirement. |
| `docs/deferred.md` | work decided against for now | Has the decision been made, and is it "not yet"? Name the event that reopens it; with no event, it is dropped. |
| `AGENTS.md` | process | Is it about the work rather than about the project? |

**What has been built is described in exactly one place, `docs/design.md`.** A second description
anywhere is the regression to watch for. `docs/architecture.md` is the one sanctioned companion: it
teaches the shape in diagrams, defers every detail to a `TD` section, and does not argue. It is a
frozen snapshot, refreshed in batches: a chunk does not update it, even when it changes a flow it
draws.

## House style

Readers are sensitive to text that reads as machine-authored. The standard is: **the code should
read as though a maintainer of the surrounding codebase wrote it.**

**Internal comments are terse.** Don't explain what a maintainer already knows — the language's
semantics, the framework's standard behaviour. Comment the non-obvious decision: the thing that
would break if someone changed it. They may go into detail on an algorithm or a theory of operation
where that is genuinely needed, and they keep their `R`-number and `docs/` references.

**Public API documentation is the exception, and addresses a different reader**: someone who wants
to use the code, so **pedagogy is the ruling principle**. Explain the concept, show the usage, say
why it matters. Length is whatever teaching that costs and not a word more — being public licenses
clarity, not loquacity. Don't explain how it is implemented, and never cite a requirement number, a
section, a decision or a chunk: users do not care, and wherever the documentation is published the
documents being cited do not exist. The reasoning usually survives the edit — drop the parenthesis,
keep the sentence.

**Analysis belongs in the review conversation.** The reasoning that produced a design — why an
alternative was rejected, what the trade-off was — goes in the chunk's discussion, and where it
needs to persist it goes in `docs/decisions.md`. What it must not do is accumulate as prose in the
code, or in the requirements.

**Comments get a second pass, on their own.** Before a chunk is handed over, read every comment and
doc line it added or changed (`git diff`, the comment lines alone, with the code around them), with
attention on the text and nothing else, and hold each to this section. Comments written in the same
breath as the code follow the letter of these rules and miss their spirit, because attention is
split; and the reasoning that produced the code, which belongs in chat, leaks into them as
chain-of-reasoning prose: "first … then … so …", what was considered, why the obvious approach would
not work. Cut that to the conclusion and the warning it carries. Then run devfmt.

**`docs/requirements.md` is the constitution, not the Federalist Papers.** A requirement states what
must be true and stops. It may carry whatever *structure* it takes to say that precisely —
enumerated states, a table of cases, a worked example — because that structure is the requirement.
What it may not carry is the argument. One clause of reason where a requirement needs one to be
intelligible; not a paragraph defending the choice. A **withdrawn** requirement is the exception: it
keeps enough to stop the idea being re-proposed, which is the only argument in the document with a
job to do.

**Avoid the tells:** restating what the code says, hedging, enumerating the obvious, unusual
punctuation or phrasing. "Nothing" as an agent ("nothing reports it") is the commonest; prefer a
first-class antonym ("unranked", "dead") or name what is absent.

**More room is not more words.** Turning prose into bullets, a table or a new section keeps one line
per item; a longer explanation points at the document that owns it.

**Every term is introduced for this document's reader.** A word familiar where it was written is
used only once this reader has met it, and a sentence beside two lists says which one it means.

**Name a rejected alternative only where a reader would reach for it**, in one clause. Once the code
exists the argument is won, and a paragraph against a ruled-out option is the dead horse.

**An introduction defines a category by kind**, not by listing or counting its members, which go
stale every chunk. Keep a number only where its change is itself a signal.

**Prefer sketches over applied refactors.** Small, staged, individually reviewable edits — ground
rule 1 applied within a chunk.

**User-facing prose tone.** Public documentation and the README are the user manual, and the
internal documents' voice does not transfer. Watch for retired metaphors ("load-bearing", "seam",
"fold", "reach for" instead of "use") that ask a reader to learn what a word means here before the
sentence parses; for defending anything; for manufactured significance ("Crucially,", "It's worth
noting that"); for project history; for hedges that gate no real exception; and for a constant diet
of em-dash asides, which reads as a fingerprint once noticed. Concise is not thin — cut the padding
around every parameter, error and edge case, not the content.

Prose in the markdown documents wraps at 100 columns; tables are exempt. The same limit applies to
source comments.

After editing a comment or a doc paragraph — a rename, added prose, anything that could have pushed
a line over the limit — fix the overflow with devfmt rather than by hand:

```sh
scripts/devfmt.py --diff
```

`--diff` (default `HEAD`) only touches paragraphs overlapping a line the working tree actually
changed, so pre-existing debt elsewhere in the file is left alone — add `--preview` first to read
exactly what it would rewrite, or `--check` for just the list of files. A paragraph it reaches is
refilled whether or not its lines already fit, since an edit shortens a line as often as it
lengthens one; a scope flag is therefore required, and `--sweep <path>` is the deliberate one.
devfmt knows Markdown and a fixed set of source languages, and refuses a source file in any other;
adding one is a chunk. It classifies lines rather than parsing them, so a run over an unusual
construct (an indented code block, an HTML block, a fence inside a list item) needs its output read.

Do the style pass on edited comments before the code formatter, so formatting runs once. devfmt is
the only authority on width: `awk` and `wc` count bytes, and an em-dash is three of them. A "file
changed on disk" notice after a devfmt run is devfmt's own rewrap, not the author editing; re-read
the file before an edit that depends on the text around it.

## Commit messages

<!-- Fill in: the project's commit-message convention, including how LLM involvement is disclosed.
One form, for a project whose code is effectively all LLM-authored to a human's direction:

```
LLM Usage Disclosure: implementation, tests and documentation written by
{model}; design decisions, review and acceptance by the author.
```

Name the model that actually did the session's work, not whichever one wrote the last commit. -->

A commit for a chunk names it, as "(chunk 12)" in the subject, so `git log --grep 'chunk 12)'` finds
it once its section is gone from the roadmap. When a chunk lands as more than one commit, give the
exact `git add` and `git restore --staged` commands beside each message; a partly staged index does
not reliably survive until the author commits.

## Tool use, and what the author reviews

The author reviews every change as a diff, and should not have to approve the steps that only gather
information.

- **Every change to a tracked file goes through the agent's file-editing tool**, so the author sees
  and approves each change as a diff. Not `sed -i`, `perl -pi`, a copy over a file or a script that
  rewrites documents: those hide the change from review even when they are pre-approved. This
  includes roadmap bookkeeping, and a temporary probe such as disabling a line to prove a test
  fails, made and reverted the same way. The formatters are the exception. Where the agent has no
  reviewed edits, the author reviews `git diff` before committing instead.
- **A mechanical refactor across many files is the other exception.** Show the list of hits first,
  run the rewrite once, and the author reviews it through `git diff`. Confirm it by grepping for the
  result, never by the exit status: a pattern the tool does not support (BSD `sed` has no `\b`) can
  exit 0 having changed nothing.
- **Read-only calls should match an allow rule** in the agent's permission settings (for Claude
  Code, `.claude/settings.json`), so they run without a prompt. A leading `cd <dir> &&`, a shell
  variable or an unlisted filter breaks the match. When a session still collects prompts, list which
  calls prompted, grouped by shape, as data for new rules; do not change the settings without
  asking. Propose a narrowly scoped script to allowlist by its path rather than a rule that allows a
  powerful tool outright (`python3 *`, `perl *`); `docs/workflow.md` says why. In Claude Code, a
  rule in `.claude/settings.local.json` takes effect where one in `.claude/settings.json` may not,
  since the local file has been found to take precedence.
- **Do not run several file-editing agents in parallel** without asking first. Each opens its own
  diff to approve, the review becomes unmanageable, and the result reads in as many voices as there
  were agents.
- **After a rejected or interrupted edit, check the disk before redoing anything**: an edit that
  reported as rejected has been found applied. After a correction to wording, make a narrow edit to
  the sentence named, not a rewrite, so the rest of the approved diff stays as it was.

## Verification

`scripts/verify.sh` runs the whole recipe in one call and is the routine way to do this — prefer it
to running each step by hand. It filters routine output, widens it for a step that fails, and counts
a warning as a failure.

<!-- Fill in: the recipe verify.sh runs, one command per line, as it grows. -->

```sh
python3 scripts/xref.py                                 # the documents' cross-references
```

The tree is warning-free, so a warning is a regression — treat one as such rather than assuming it
was already there. A known exception is listed here, with the chunk that owns it.

## Context, and what not to economize on

Sessions run out before the work does. But the value of working this way is noticing that two widely
separated things disagree, and that is not free — so cut waste, not reading. Distinguish:

- **A lookup**: you know what you need and where it lives. Go straight there. Reading the whole file
  is waste.
- **A sweep**: you are looking for something you do not yet know to look for — a decision that moved
  and left a stale copy behind, a requirement the change quietly contradicts, a configuration nobody
  has built. This costs context and is worth it, and it finds things no diff would have shown.
  `scripts/mentions.sh <pattern>` is the grep for one: it skips ignored files, and cuts each line to
  a fixed width.
- **A scan**: a script finds a signature, and only its hits are read. Validate it against a known
  positive first; a clean result from an unvalidated scan is worth nothing. Prefer a scan to a sweep
  wherever the thing sought has a signature.

Before a tree-wide mechanical change, run it on one file of each kind and read the output. Tests
prove it correct, not legible.

**Price tree-wide work before offering it**, in calls, and say whether it is a sweep or a scan. Cost
follows the shape of the work, not its label: a whole-tree comment sweep through parallel subagents
once cost a week's token budget in two days, where an inline sweep of one document cost about one
percent per handful of entries. Say too when a chunk's review is the expensive part, such as a large
mechanical diff, so the author can schedule it.

What to scope down is **tool output**: `| head`, `| wc -l`, `git diff` rather than a sweep over four
files dumped into the transcript to find five long lines. `scripts/verify.sh` already does this for
the verification recipe. Apply the same filtering by hand only when running one of its steps
directly, and drop the filter only when something actually fails and you need to see which part.
This costs nothing in accuracy; it is pure waste to keep paying for it.

**Say when the problem has outgrown the window.** A large change held half in view produces
confident work with holes in it, which is worse than the same change split in two. If something
needs more of the tree in mind at once than is left, say so and propose the split rather than
starting it and hoping.
