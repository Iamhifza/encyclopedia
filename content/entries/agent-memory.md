---
term: Agent Memory
aliases: [Long-Term Memory, Working Memory, Episodic Memory, Semantic Memory, Agent State]
category: agents
subcategory: memory
status: emerging
difficulty: intermediate
one_liner: Anything an agent keeps outside the context window so it can remember across steps and sessions.
origin:
  year: 2023
  circa: true
  attribution: Emerged from autonomous-agent projects; terminology borrowed loosely from cognitive psychology
historical_period: agentic
tags: [agents]
relations:
  part_of: [ai-agent]
  different_from: [context-window]
  depends_on: [vector-database]
  related_to: [context-engineering, rag]
prerequisites: [ai-agent, context-window]
encountered_in: [production-systems, github, technical-blogs]
sources:
  - type: paper
    title: "Generative Agents: Interactive Simulacra of Human Behavior"
    url: https://arxiv.org/abs/2304.03442
    year: 2023
  - type: paper
    title: "MemGPT: Towards LLMs as Operating Systems"
    url: https://arxiv.org/abs/2310.08560
    year: 2023
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

The model remembers nothing between calls. Everything it appears to remember was
put back into the prompt by your code. "Agent memory" is the machinery that
decides what to store, what to retrieve, and what to re-insert.

## Technical Definition

External state maintained across model invocations, together with the policies
for writing to and reading from it. Implementations span an append-only message
log, rolling summaries, key-value profile stores, vector-indexed episode
archives, and structured scratchpads or files the agent reads and writes.

## Why Does It Exist?

The context window is finite and expensive, and each API call is independent.
Long-running work therefore needs storage outside the window, plus a policy for
what comes back in.

## What Problem Does It Solve?

Continuity across sessions, retention of durable facts (preferences,
constraints, project conventions), and survival of tasks longer than one context
window.

## How Does It Work?

```text
                    ┌──── working memory: the live context window ────┐
                    │  system prompt · recent turns · tool results     │
                    └──────────────▲───────────────────┬───────────────┘
                        retrieve   │                   │ write
                    ┌──────────────┴───────────────────▼───────────────┐
                    │ episodic: what happened, when                    │
                    │ semantic: durable facts and preferences          │
                    │ procedural: how this team does things            │
                    └──────────────────────────────────────────────────┘
```

## Mental Model

A colleague with total amnesia at the end of each meeting, plus an assistant who
writes the notes and hands them a briefing before the next one. All the
intelligence about *what goes in the briefing* is the assistant's.

## Terminology Note

The cognitive-science vocabulary — episodic, semantic, procedural, working — is
borrowed by analogy and used inconsistently across frameworks. Two products
labelled "long-term memory" may mean a vector store of past messages and a
hand-curated user profile respectively. Ask what is stored, what triggers a
write, and what triggers a read.

## Example

A coding agent that records "this repository uses pnpm, not npm" after being
corrected once, and re-injects it at the start of every future session, has
semantic memory. One that can summarise last Tuesday's debugging session has
episodic memory. These are different mechanisms with different failure modes.

## Real-World Usage

Memory features in agent frameworks and assistant products; project files that
agents read on startup; summarisation and compaction when context fills.

## Common Confusions

* **Memory vs context window** — the window is what the model sees now; memory is
  what could be brought back into it.
* **Memory vs RAG** — the same retrieval machinery, different content: RAG
  retrieves documents, memory retrieves the agent's own history.
* **Stored is not remembered** — if retrieval does not surface it, storage is
  irrelevant.
* **Memory accumulates errors** — a wrong fact written once is re-injected
  forever. Memory needs editing and expiry.

## Why Should I Care?

It is the difference between a tool that starts from zero every session and one
that accumulates useful context about your work — and the leading cause of agents
that confidently repeat an outdated assumption.
