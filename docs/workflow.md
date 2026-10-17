# How this project is run

This document explains, for a person, the process the project is developed under. The agent's
instructions for the same process are in [AGENTS.md](../AGENTS.md); this is the companion that says
what those instructions are for, and what the human half of the arrangement looks like.

The process grew over several months of building a Rust library with an LLM coding agent writing
effectively all of the code to one experienced engineer's direction. Its examples come from there.

---

## The idea

An agent starts every session knowing nothing about the project. Whatever it needs to know has to be
written down, and it has to be findable in a few cheap steps, because every word the agent reads
takes space in its context window, which also has to hold the work.

So the project's knowledge lives in **ledgers**: Markdown files in the repository, each admitting
exactly one kind of thing, with every entry numbered so it can be cited and looked up. What the
project does is in one ledger, why it is that way in another, what must be true in a third, what is
broken in a fourth, and so on. The agent reads two or three of them to orient, fetches anything else
by its number, and updates them in the same commit as the code. The rest of the process exists to
keep those ledgers true.

This is meta-prompting with structure. `AGENTS.md` is the standing prompt; the ledgers are the
context it points into; and the corrections the author makes along the way are written back into
both, so the next session starts from a better prompt than this one did.

The unit of work is the **chunk**: one reviewable change, small enough to read in a day, with its
code, its tests and the documentation it forces, landing as a single commit or branch. A chunk is
planned as a numbered section of the roadmap before it is built, and that number stays with it in
commit messages and code comments after it lands. One session builds one chunk. A chunk too large
for that is split into lettered parts (`12a`, `12b`) before it is written.

Saving tokens is a side benefit. The ledgers exist to carry what one session learned to the next,
and to keep each change small enough to review, which pays off over a project that lasts whatever
its token allowance. A game jam, or a prototype that will be thrown away, gains much less.

## What it needs

An agent that works in the repository: one that reads and edits files and runs commands, showing
each edit as a diff to approve. A chat window without access to the repository cannot run the
process, since the person would have to carry every file in and every edit out by hand. "Which
agent" below covers what is specific to Claude Code.

No session holds the ledgers whole. It reads a fixed bootstrap and fetches the rest by number. In
this template the bootstrap is about 4,400 words, roughly 6,000 tokens, most of it `AGENTS.md`, and
it grows with `issues.md`; `scripts/growth.py` reports the current figure. The agent's own system
prompt and the chunk's work come on top, so a context window of 32k tokens is tight and 8k is too
small.

The harder demand is judgement: deciding which ledger a sentence belongs in, declining to pad, and
pushing back on a bad request. Smaller models are weakest at these, and the process depends on them.

## The ledgers

| Ledger | Holds | Numbered |
| --- | --- | --- |
| [roadmap.md](./roadmap.md) | work not done, as a sequence of chunks, and an index of what has landed | chunks, `<n>` |
| [requirements.md](./requirements.md) | what must be true, and nothing about why | `R<s>.<n>` |
| [design.md](./design.md) | how it works now, in the present tense, and nothing about why | `TD<n>.<m>` |
| [decisions.md](./decisions.md) | why, for choices expensive to reverse, with the cost of reversing | `D<n>` |
| [issues.md](./issues.md) | findings nobody has decided about yet, tiered by severity | `I<n>` |
| [deferred.md](./deferred.md) | work decided against for now, each with the event that reopens it | `X<n>` |
| [guidelines.md](./guidelines.md) | judgement a maintainer would otherwise learn by being corrected | `G<n>` |
| [architecture.md](./architecture.md) | a diagram-led tour for a newcomer, refreshed in batches | unnumbered |
| [sources/](./sources/README.md) | the surveys the requirements were drawn from, a record rather than a ledger | by file name |

Two rules make them work.

**Each fact has one home.** What has been built is described in `design.md` and nowhere else; the
roadmap names chunks but does not describe the project; a decision says why but not how. Each ledger
states the test that decides what it admits, and `AGENTS.md` collects the tests in one table. A
second description is the regression to watch for, because two descriptions drift and then the agent
is confidently wrong about whichever one it read.

**Nothing outstanding is left without a destination.** Work flows between ledgers, and every item
always has a place:

```
  a finding ──▶ issues.md ──┬──▶ a chunk in roadmap.md ──▶ lands ──▶ a row in the landed index,
                            │                                         and a decision if it taught one
                            ├──▶ deferred.md, with a gate ──▶ the gate fires ──▶ a chunk
                            ├──▶ decisions.md
                            └──▶ dropped
```

An item with no chunk number and no gate is an item that will be forgotten. "Later" is not a
destination.

Numbers are permanent identities, issued from a counter at the top of each ledger and never reused.
A gap means an entry left. `scripts/xref.py` checks every reference in every document resolves, and
that no counter has fallen behind a number already spent.

## Writing the requirements

The requirements are the document everything else cites, and the one written first. In the project
this process came from, the first draft took two full days of conversation with the agent before any
code: the author's own goals, then surveys of prior art, industry practice and the relevant
literature, then the requirements drawn from all of it. Expect something similar. It is the cheapest
point at which to discover that two goals conflict.

Gathering requirements is a craft of its own, with its own practices (user stories, personas, use
cases), and this section does not try to teach it. It covers what changes when the drafting is done
with an agent and the result has to serve as a ledger.

**Start with what the author wants.** Who the project serves, what it must do for them, what it
deliberately does not do, and where the author's own expertise lies. These become the document's
scope, its non-goals and its first requirements, tagged `from: author`.

**Name the audiences, and settle how their needs conflict.** Most projects serve more than one kind
of user, and the tension between them is the source of most later arguments about scope. In the
original project, the users were large studios, who need the ceiling (every capability an
established product has), and solo developers, who need no floor (nothing to configure before
anything works). Recognizing that early, and writing down how a conflict between the two is
resolved, let later decisions be checked against a stated rule instead of argued afresh. The
document's "Who this is for" section holds it.

**Then survey, and write each survey down.** Ask the agent to study how established products, the
industry's common practice and the literature handle the problem, one survey at a time, and to write
each up as a file in [sources/](./sources/README.md) before any requirement is drawn from it. Ask it
to mark which findings it checked against a primary source and which come from its own knowledge,
which can be stale or simply wrong. The conversation will not survive; the file will.

**Draw the requirements, each with its provenance.** Every requirement carries a tag saying where it
came from: the author, a survey, another requirement it derives from, or a decision. Whether the
author wanted something or a survey suggested it decides how freely it can be argued with, and
without the tag that has to be guessed. `scripts/xref.py` refuses a requirement with no tag.

**Set each level deliberately, and low.** The common failure is priority inflation. That a
well-known product does something makes it look obligatory, and surveys produce many such
requirements at once; a `MUST` should mean the project fails its purpose without it. A requirement
drawn from a survey enters as a `MAY` unless the author raises it. The inflation continues after
drafting, too: a chunk or issue built on a `MAY` reads, once separated from the requirement, like an
iron law. So in the roadmap, issues and deferred entries, a requirement below `MUST` is cited with
its level, as `R<s>.<n> (MAY)`, and `xref.py` checks that as well.

**Requirements change after drafting, by the same process as anything else.** A requirement that
forces a contorted design is questioned (G4), withdrawn rather than deleted when its reason has
gone, and a new one arrives with its provenance and a level someone has argued for.

## A session

One session works one chunk, and ends at a commit.

1. **Orient.** The agent reads the last few commits, `issues.md`, and the chunk's section of the
   roadmap. That is the whole bootstrap; everything else is on demand, by number, through
   `scripts/show.py`.
2. **Plan.** The agent says what will change, in plain sentences, and answers questions about scope
   with counts. A new structural idiom (a new kind of module, wrapper or dependency) arrives as
   options with a recommendation, not as a diff.
3. **Build**, with tests, and verify with `scripts/verify.sh`.
4. **Review the comments**, in a separate pass over every comment the chunk added or changed (see
   "Working with the agent").
5. **Update the ledgers.** The chunk's roadmap section is deleted and a row added to the landed
   index. Design changes go into `design.md`; anything durable it taught goes into `decisions.md`;
   anything it found and did not fix goes into `issues.md`; anything it leaves undone is written
   onto the chunk that will finish it.
6. **Commit.** The agent writes the commit message; the author reviews and commits. The agent never
   commits or pushes, and never posts anything publicly.

A chunk states what it deliberately does *not* do, so a reviewer can tell "not yet" from
"overlooked", and how it will be verified. Its effort is estimated on a coarse exponential scale
(G7), for sorting rather than scheduling.

## Working with the agent

The process is also a set of habits on the human side. None of these is enforced by a script.

**Ask; don't instruct.** A model asked to do something will do it, and is poorly placed to say it is
a bad idea. Phrased as a question ("I've been thinking about changing this int to a float; what do
you think?") the same request gets an assessment, and the model will still offer to make the change
at the end if it agrees. Getting an LLM to push back is one of the harder parts of working with one,
and this is the cheapest lever.

**Ask for options before code**, wherever the shape of the thing is in question. A diff is expensive
to review and anchors the discussion on what it happens to do.

**Ask for counts, not reassurance.** "How many call sites?" gets a number; "is this a big change?"
gets a tone.

**Conserve the context window.** Everything the agent reads in a session stays in its context, and a
model reasons worse as the context fills: it loses track of what it read early, and work done near
the limit is confident and full of holes. That is much of why a session is one chunk, why the
bootstrap is three short reads, and why everything else is fetched by number rather than by reading
whole documents. Start a new session for a new chunk rather than continuing a long one, filter tool
output down to what answers the question, and spend context deliberately on the sweeps that need it.
Tokens are also money, or a weekly allowance: ask for a tree-wide job to be priced, in calls, before
agreeing to it. A whole-tree comment sweep through parallel subagents once used a week's allowance
in two days, where an inline pass over one document cost about one percent.

**Have the comments reviewed in a pass of their own.** An agent conforms to the spirit of the house
style much better when its attention is on the comment text alone than when it is writing code and
documenting it at once. It also tends to think in chain-of-reasoning prose, which is part of how it
works and belongs in the conversation, but leaks into comments despite the rules against it: what
was considered, what was tried, why the obvious approach would not work. `AGENTS.md` asks for a
second pass over a chunk's new and changed comments before it is handed over. If one is skipped, ask
for it; it costs little, because it reads only the diff. This per-chunk pass is what keeps the tree
compliant; the whole-tree `comment-grooming` sweep is for the rare occasion when the rules
themselves change.

**Review every edit, and correct wording after it lands.** Approve each change as a diff. For a
problem of wording, let the edit apply and then give the correction, which gets a narrow edit to one
sentence; reject only for substance, since a regenerated edit can introduce new errors in text you
had already checked.

**When your review notes start repeating, turn them into rules.** If the same few corrections recur
file after file, name them back to the agent, have it make a first pass over the rest applying them,
and spend your attention on the judgement calls that remain. The rules that hold up belong in the
guidelines.

**Tell the agent where your expertise lies**, and where you defer. It should recommend in the areas
you defer on and bring the others to you. This, and how you like to work, is what the agent's memory
is for: facts about you that would not hold for another developer. Anything about the project goes
in the documents.

**Discount a model's findings.** Ask a model to find sixty problems and it will find sixty, some
real and some rules nobody would ever violate. `issues.md` asks every entry to say whether it was
confirmed by running something or only by reading, and what a user would actually observe.

**Trust the sense that something is wrong before you can say what.** Much of this process is
accumulated judgement written down: each guideline, each house-style rule and each "the test is"
line began as an author noticing that something read wrong or was built wrong, and working out why.
That kind of noticing comes from long experience with code and with prose, and a less experienced
engineer will often feel the problem before being able to articulate it. That feeling is a finding.
Say so to the agent ("this reads wrong to me, and I can't say why"), ask it to argue the other side,
or record the unease in `issues.md` with what prompted it. The guidelines are a head start on the
articulation, not a substitute for the noticing.

**Write every correction down.** A correction made twice belongs in `guidelines.md`, with the case
that produced it. A correction about prose belongs in `AGENTS.md`'s house style. Otherwise the next
session makes the same mistake, because the next session is a stranger.

**Say when the problem is too big.** An agent working on a change larger than it can hold in view at
once produces confident work with holes in it. `AGENTS.md` asks it to say so and propose a split;
the author should welcome that rather than push through.

## Sharpening the saw

A meaningful share of the time on the project goes to the process itself rather than to features:
editing the ledgers for clarity, merging duplicated explanations, retiring stale entries, improving
the tools, and tightening `AGENTS.md`. This is deliberate. The ledgers decay as the code moves, and
an agent reasoning from a stale document does worse work than one with no document at all.

The roadmap has two standing groups for it. **Sweeps** pass over a whole document or module a unit
at a time: an editorial pass on `design.md`, a review of public items nothing uses. **Tooling**
chunks build or improve the scripts. Both are chunks like any other, with effort estimates, and are
scheduled alongside feature work rather than left for a quiet week that never comes.

Comments are kept to the house style chunk by chunk, by the second pass described above, not by
periodic sweeps. The `comment-grooming` skill in `.claude/skills/` is for the exception: after the
house style itself changes, it brings the whole tree into line once. It is expensive, since it reads
every comment, and in the project this came from it ran once.

`scripts/growth.py` measures what a change cost in reading: words per document, the size of each
ledger's entries, how much a session reads before it starts, and a measure of the project's own
complexity. It is a check on slop, the steady accretion of words and surface that no single change
looks responsible for. A sweep starts and ends with it, so its effect is measured rather than
asserted.

**Approval prompts are part of the process to maintain.** An agent asks before running anything not
on its allowlist, and a session that stops for approval every few calls wears the author down until
approving becomes reflex, which is worse than having no prompts. The tempting fix is to allow a
powerful tool outright, `python3 *` or `perl *`, and that approves everything those tools can do.
The practice here is a **trusted script** instead: a script with a deliberately narrow scope, whose
whole behaviour can be read in a minute, allowlisted by its own path. `scripts/show.py` is one; it
can only print sections of documents. When a session collects prompts, the agent lists which calls
prompted, grouped by shape, and the recurring shapes become a trusted script or a narrow allow rule
as a tooling chunk. Two things keep a script trusted. It changes nothing (reading and reporting
only), or it changes files only as the formatters do, in a way the author has already agreed to; and
widening its scope is a reviewed change like any other, not a quiet edit, since the allowlist entry
vouches for whatever the file comes to contain.

In Claude Code, rules go in `.claude/settings.json`, which is shared through the repository, or
`.claude/settings.local.json`, which is personal and ignored by git. Where both exist, the local
file has been found to take precedence: a rule added to the shared file can have no effect on a
machine with a local one. Add a rule to the local file to have it take effect now, and to the shared
file when every developer should have it.

## The tools are a seed

The scripts and tools here are a starting point, and are expected to change. Each one in the project
this came from began as a lookup, a check or a tally that kept being done by hand, until it was
worth a chunk to automate. `AGENTS.md` asks the agent to notice that and propose one.

| Tool | Does | How it is expected to grow |
| --- | --- | --- |
| `scripts/show.py` | prints any numbered section, requirement or entry by its anchor | rarely; a new ledger is a row in `xref.py` |
| `scripts/xref.py` | checks every cross-reference resolves and every counter is current | a new ledger or source tree is a row in its tables |
| `scripts/mentions.sh` | a grep for sweeps, with the exclusions and line width a sweep wants | rarely |
| `scripts/growth.py` | the slop metric, against a base commit | `complexity()` is empty until the project defines it: a library might count public types, a compiler grammar productions, a game its systems |
| `scripts/verify.sh` | the whole verification recipe in one call, with routine output filtered | a step per check the project adds |
| `scripts/devfmt.py` | reflows prose in Markdown and source comments to 100 columns | it knows Rust; a source file in another language is refused with an error saying how to add it |

Some tools the original project grew, as examples of the kind: a script that greps a dependency's
source at the exact locked version; a smoke test that launches each example for ten seconds and
fails it on an unexpected warning; a test driver that plays a running game over its remote protocol;
and a ledger of measured facts about an external system the project depended on, kept because
guesses about its behaviour kept turning out wrong. None is here, because each answered that
project's problem. This project's problems will suggest its own.

## Why plain files

The ledgers could have been an issue tracker or a database. They are Markdown in the repository
because:

- **They version with the code.** Retiring an issue lands in the same commit as its fix, a branch
  carries its own state of the ledgers, and a review sees the documentation change beside the code
  that forced it.
- **The agent reads them for almost nothing.** A file read or a grep, with no API, credentials or
  network, returns prose, which is what the model reasons in.
- **References are checked.** `xref.py` can tell whether an issue's number exists. A link into a
  tracker cannot be checked by anything in the repository.
- **Moving an item between ledgers is an edit**, carrying what it knew in its text. A finding that
  becomes a chunk, a deferral or a decision is one item changing shape, which a tracker would record
  as one closed and another opened.
- **Nothing is public by default.** A tracker on a public host publishes every half-formed finding.
- **A database is opaque to review.** Its changes do not show in a diff, and reading it costs a tool
  call per question.

## Which agent

The process was developed with Claude Code, but nearly all of it is Markdown and plain scripts, and
works with any agent that can read files and run commands. The agent's instructions are in
`AGENTS.md`, the name most coding agents read by convention; `CLAUDE.md` is a one-line file that
imports it for Claude Code.

What is specific to Claude Code is under `.claude/`: the permission allowlist in `settings.json`,
and the `comment-grooming` skill, whose procedure is plain Markdown that another agent can be
pointed at, with its read-only subagents run in whatever form that agent offers, or one after
another. `scripts/growth.py` counts Claude Code's memory index in a session's starting reading, and
skips it where there is none.

The house style's list of tells was compiled by correcting Claude, and another model will have
habits of its own. The process's answer is the same: when a correction recurs, write it down.

## Adopting it

1. Fill in the placeholders in `AGENTS.md`, marked as HTML comments: what the project is, its commit
   convention, and its verification recipe.
2. Write `requirements.md` before much code, as "Writing the requirements" above describes, with the
   surveys in `sources/`. It is the document the rest cite most.
3. Put the first few chunks in `roadmap.md`, aimed at the earliest thing that can be run and judged.
   Ground rule 3 wants something runnable at every step.
4. Add the project's build and tests to `scripts/verify.sh`, and its source directories to `CODE` in
   `scripts/xref.py` once comments start citing requirements.
5. Add the project's language to `scripts/devfmt.py`, as its first tooling chunk, when the first
   source comments need reflowing.
6. Decide what `complexity()` in `scripts/growth.py` should count, once there is enough code to
   know.
