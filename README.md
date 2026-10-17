# Project template: ledger-driven development

A starting point for a project developed with an LLM coding agent under a structured process, in
which the project's knowledge lives in a set of numbered, single-purpose documents that the agent
reads and maintains alongside the code.

It is a different way of working from code completion. The agent writes the code; the author directs
it, reviews each change as a diff, and keeps the documents true. It needs an agent that works in the
repository, reading and editing files and running commands, such as Claude Code. A chat window
without access to the repository cannot run it, and most of these agents need a paid plan.

The process is explained in [docs/workflow.md](docs/workflow.md). The agent's own instructions are
in [AGENTS.md](AGENTS.md).

This file is a placeholder. Replace it with the project's own README once the project has one; the
process does not depend on it.
