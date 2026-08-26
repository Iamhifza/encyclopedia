---
term: Harness
aliases: [Agent Harness, Harness Engineering, Agent Runtime]
category: agent-engineering
subcategory: structure
status: contested
disputed: true
difficulty: intermediate
one_liner: The code around a model that decides what it sees, what it may do, and what happens to its output — with the caveat that people use the word for at least three different things.
origin:
  year: 2023
  circa: true
  attribution: Borrowed from software testing ("test harness"); adopted for agent runtimes and for evaluation rigs, in parallel and independently
historical_period: agentic
diagram:
  kind: figure
  title: Everything around the model that is not the model
  footer: Swap the model and behaviour shifts. Swap the harness and the same model becomes a different
    product. Almost every reliability problem attributed to a model is one of these seven rows.
  visual:
    kind: stack
    width: 780
    caption: the model sits underneath all of it, and is called afresh each iteration
    layers:
    - label: context
      text: what goes into the window, and in what order
      note: decides cost and cache hits
      accent: true
    - label: tools
      text: schemas, descriptions, how results are shaped
      note: the model only sees this
    - label: execution
      text: sandbox, timeouts, retries, error surfaces
      note: where reality intrudes
    - label: permissions
      text: what runs freely, what needs approval, what is refused
      note: the blast radius
    - label: loop
      text: step budget, cost cap, stop conditions
      note: when to give up
    - label: state
      text: memory, checkpoints, resumption
      note: surviving a restart
    - label: observability
      text: traces, evaluations, replay
      note: how you learn it broke
tags: [agents, culture]
relations:
  similar_to: [scaffold]
  different_from: [scaffold, evaluation-harness]
  part_of: [ai-agent]
  depends_on: [agent-loop, context-engineering, tool-calling]
  used_by: [coding-agent]
prerequisites: [ai-agent, agent-loop]
encountered_in: [technical-blogs, github, job-descriptions, social-media, conferences]
sources:
  - type: post
    title: "Building Effective Agents"
    url: https://www.anthropic.com/engineering/building-effective-agents
    year: 2024
  - type: paper
    title: "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering"
    url: https://arxiv.org/abs/2405.15793
    year: 2024
    note: The agent-computer interface argument is the strongest technical case for the concept.
  - type: repo
    title: "OpenAI Evals — harness in the evaluation sense"
    url: https://github.com/openai/evals
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

A model on its own is a text function. To make it an agent, something has to run
it in a loop, assemble what it sees, execute the tools it asks for, catch errors,
enforce limits and stop it when it goes wrong. That surrounding machinery is the
harness. Two teams using the same model and different harnesses will get very
different results.

## Technical Definition

The runtime layer between a model and its environment. Responsibilities: context
assembly and compaction, the tool interface and its schemas, execution and error
handling, permission checks and sandboxing, loop control and budgets, state
persistence, and tracing. In evaluation contexts, the same word denotes the rig
that runs benchmark tasks against a model and scores them.

## Why Does It Exist?

Because when agent quality was measured carefully, a large share of the variance
turned out to live outside the model. SWE-agent's central finding was that
redesigning the *interface* the model acts through — how files are shown, how
errors are reported, how commands are constrained — changed task success
substantially with the model held fixed. That result gave the surrounding code a
name and a claim to be engineering rather than glue.

## What Problem Does It Solve?

Everything that determines whether a capable model produces a reliable system:
what it can see, what it can do, what it costs, and what happens when it fails.

## How Does It Work?


The model contributes one thing: given a context, produce the next tokens. It is
stateless, it cannot run anything, and it has no memory between calls. Every
other property an agent appears to have is supplied by the code around it.

That code has seven jobs. It assembles the context and decides what goes in and
in what order. It presents the tools and shapes their results. It executes what
the model asks for, inside whatever isolation it chose. It decides which actions
proceed freely and which need a person. It controls the loop — how many steps,
what budget, when to stop. It carries state between calls. And it records enough
to tell you afterwards what happened.

Which is why two products built on the same model behave completely differently,
and why "the model got it wrong" is usually a misdiagnosis. Context that was
assembled badly, a tool whose errors are unreadable, a loop with no stop
condition — these look like model failures and are not.

## Mental Model

The cockpit around a pilot. The pilot's skill matters; so does whether the
instruments are readable, the controls are guarded, and the warnings arrive in
time.

## Terminology Note

This term is genuinely contested. At least three usages are current:

1. **Agent runtime** (most common since 2024) — the loop, tools, context
   management and permissions around a model in production.
2. **Evaluation rig** (older, from software testing via ML benchmarking) — the
   code that runs a benchmark against a model and scores it, as in "the eval
   harness". `lm-evaluation-harness` uses the word this way.
3. **Thin API wrapper** (loose, marketing) — any code that calls a model.

Usage 1 and usage 2 collide constantly: "our harness improved results" means
opposite things depending on which is meant. *Harness engineering* is a newer
coinage for usage 1 as a discipline; it is not standardised, and some
practitioners regard it as a rebranding of "building the application properly".
Both readings have merit — see the terminology-evolution discussion in the
[Prompt Engineering](prompt-engineering.md) entry.

## Example

Two teams, same model, same task. Team A returns raw 4,000-line stack traces into
context, offers thirty tools, has no step budget. Team B truncates errors to the
relevant frames, exposes six tools, caps at twenty steps, and requires approval
before writes. Team B's agent succeeds far more often. Nothing about the model
differed.

## Real-World Usage

Coding agents, computer-use agents and research agents all ship substantial
harness code. In job descriptions the term now appears as a named skill; in
practice it covers context engineering, tool design, sandboxing and evaluation.

## Differences

* **Harness vs scaffold** — heavily overlapping. In common usage, *scaffold*
  leans toward the prompt-and-structure arrangement that shapes reasoning, and
  *harness* leans toward the executing runtime with tools, permissions and
  budgets. Many practitioners use them interchangeably; neither has a
  standards-body definition.
* **Harness vs framework** — a framework is a reusable library; a harness is your
  specific runtime, whether or not it uses one.
* **Harness vs orchestrator** — an orchestrator routes work between models and
  agents; that is one component of a harness.

## Common Confusions

* **"The harness is just glue"** — it is where most reliability, cost and safety
  behaviour is decided.
* **Assuming which meaning is intended** — in evaluation contexts, "harness"
  almost always means the scoring rig.

## Why Should I Care?

When an agent underperforms, the instinct is to change model or rewrite the
prompt. The harness — what the model sees, how tools report, where the loop stops
— is usually where the actual defect is.
