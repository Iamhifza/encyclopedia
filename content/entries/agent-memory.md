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
diagram:
  kind: steps
  title: One live window, and three stores behind it
  footer: The hard part is not storing things — it is retrieval and forgetting. A store that returns everything
    is the context window again, and a store nothing prunes becomes slower and less relevant every week.
  steps:
  - title: Working memory is the context window, and it is small
    notes:
    - label: Lifetime
      text: one request — everything here is reassembled from scratch next turn
    visual:
      kind: segments
      width: 720
      label: the live window
      caption: whatever is not in here does not exist as far as the model is concerned
      segments:
      - text: system prompt
        value: 12
      - text: retrieved memory
        value: 26
        tone: accent
      - text: recent turns
        value: 34
      - text: tool results
        value: 28
  - title: Three stores, holding different kinds of thing
    visual:
      kind: columns
      width: 740
      columns:
      - title: Episodic
        lines:
        - what happened, and when
        - '"we tried X on Tuesday"'
        - retrieved by similarity
      - title: Semantic
        accent: true
        lines:
        - durable facts and preferences
        - '"deploys go out on Thursday"'
        - retrieved by relevance
      - title: Procedural
        lines:
        - how this team does things
        - '"our release notes look like this"'
        - retrieved by task match
      caption: read into the window before the model runs; written back after it
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


Working memory is the context window, and it is rebuilt from nothing on every
request. Nothing in it persists. Anything the agent should still know next week
has to be written somewhere durable and deliberately read back in.

What gets stored splits usefully three ways. Episodic memory records events —
what was tried, when, and how it went. Semantic memory holds durable facts and
preferences that are true independent of any occasion. Procedural memory holds
how this particular team does a thing: formats, conventions, the shape of an
acceptable answer.

The storage is the easy half. The hard half is retrieval and forgetting. A store
that returns everything has merely reconstructed the context problem one layer
down, so retrieval has to be selective, and selection needs a relevance signal
that is usually weaker than you would like. And a store nothing ever prunes fills
with stale facts, superseded preferences and events that no longer matter —
getting slower and less useful with every entry.

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
