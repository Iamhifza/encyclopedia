---
term: Agent Skills
aliases: [Skills, Skill Files, Agent Capabilities]
category: agent-engineering
subcategory: capability
status: emerging
difficulty: intermediate
one_liner: Packaged instructions and resources an agent loads only when a task needs them, so its context is not filled with procedures it is not using.
origin:
  year: 2025
  attribution: Formalised as loadable skill folders in agent products during 2025; the word "skill" has older, unrelated uses in RL and voice assistants
historical_period: agentic
tags: [agents]
relations:
  part_of: [ai-agent]
  depends_on: [context-engineering, tool-calling]
  different_from: [tool-calling]
  related_to: [harness, mcp]
prerequisites: [ai-agent, context-engineering]
encountered_in: [documentation, github, technical-blogs]
sources:
  - type: docs
    title: "Anthropic — Agent Skills"
    url: https://docs.claude.com/en/docs/agents-and-tools/agent-skills
    year: 2025
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

Some knowledge is only needed sometimes: how your team formats a release note,
how to fill a particular PDF form, the steps for a quarterly report. Putting all
of it in the system prompt wastes context on every request. A skill is that
knowledge kept in a folder with a short description; the agent reads the full
contents only when the description matches what it is doing.

## Technical Definition

A named bundle of instructions, and optionally scripts and reference files, with
metadata used for discovery. The agent sees only the name and description by
default and loads the body on demand — progressive disclosure applied to
procedural knowledge, so cost scales with relevance rather than with the size of
the library.

## Why Does It Exist?

Organisational procedure does not fit in a system prompt, and does not belong in
model weights either. It changes too often to fine-tune and is too specific to
retrieve as prose. Skills give it a unit of packaging.

## What Problem Does It Solve?

Context bloat from rarely-used instructions, and the difficulty of sharing and
versioning agent know-how across a team.

## How Does It Work?

```text
skills/
  release-notes/    SKILL.md  ← name + description always visible
  pdf-forms/        SKILL.md  + scripts, templates
  incident-report/  SKILL.md

agent sees:  "release-notes — how this team writes release notes"
task matches ──▶ read the full SKILL.md ──▶ follow it, run its scripts
```

## Mental Model

A shelf of standard operating procedures. You do not memorise them all; you know
what is on the shelf and fetch the one the job needs.

## Example

A team's document formatting conventions, checklists and helper scripts live in a
skill. Every agent in the team behaves consistently without a 5,000-token system
prompt that most requests never use.

## Terminology Note

"Skill" is heavily overloaded. In reinforcement learning it means a learned
sub-policy; in voice assistants it meant a third-party app; in agent products
since 2025 it means a loadable instruction bundle. The senses are unrelated.
Distinguish it from tools: a **tool** is a function the model can invoke; a
**skill** is instructions the model reads. Skills often tell the model how to use
tools.

## Real-World Usage

Agent products supporting skill folders, and team repositories where conventions
travel with the codebase rather than living in someone's saved prompt.

## Common Confusions

* **Skills vs tools** — instructions versus executable functions.
* **Skills vs MCP servers** — MCP connects an agent to external systems and their
  tools; skills supply procedural knowledge. They compose.
* **Skills vs fine-tuning** — a skill is editable in a text editor, versioned in
  git, and takes effect immediately.

## Why Should I Care?

It is the current answer to a real problem: how organisational knowledge gets
into an agent without being pasted into every prompt or baked into weights.
