---
term: Sandboxing
aliases: [Sandbox, Isolated Execution, Container Isolation, Confinement]
category: agent-engineering
subcategory: control
depth: full
status: established
difficulty: intermediate
one_liner: "Running an agent's actions inside a confined environment so that mistakes and attacks cannot reach anything that matters."
historical_period: agentic
tags: [agents, safety]
relations:
  part_of: [guardrails, harness]
  solves: [prompt-injection]
  related_to: [coding-agent, computer-use, human-in-the-loop]
prerequisites: [ai-agent]
encountered_in: [production-systems, github, documentation, job-descriptions]
sources:
  - type: docs
    title: "OWASP Top 10 for LLM Applications"
    url: https://owasp.org/www-project-top-10-for-large-language-model-applications/
  - type: repo
    title: "gVisor — a container sandbox with a user-space kernel"
    url: https://github.com/google/gvisor
updated: 2026-08-21
---

## Simple Explanation

An agent that can run code will eventually run bad code — through its own error,
or because something it read told it to. Sandboxing accepts that as a given and
makes it survivable: the code runs somewhere disposable, with no credentials, no
access to your files, and no route to the network unless you granted one.

## Technical Definition

Execution of untrusted operations within an isolated environment with restricted
capabilities: separate filesystem namespace, no ambient credentials, constrained
or denied network egress, resource limits on CPU, memory and runtime, and a
lifecycle that discards the environment afterwards. Implementations range from
containers through stronger isolation layers such as gVisor and Firecracker to
full virtual machines.

## Why Does It Exist?

Prompt injection has no complete defence. Since you cannot guarantee an agent
will never be manipulated into a harmful action, the remaining lever is bounding
what a manipulated agent can reach.

## What Problem Does It Solve?

Blast radius. It does not stop the agent doing the wrong thing; it stops the
wrong thing from mattering.

## How Does It Work?

```text
      agent decides to run code
                │
┌───────────────▼──────────────────────────────┐
│ SANDBOX                                      │
│  own filesystem  ·  no host mounts           │
│  no credentials in env                       │
│  egress: denied, or allow-listed hosts only  │
│  CPU / memory / wall-clock caps              │
│  destroyed after the task                    │
└───────────────┬──────────────────────────────┘
                │ only declared outputs come back
                ▼
        results returned as untrusted data
```

The last line matters as much as the isolation: whatever comes out is still
attacker-influenced text entering the context window.

## Mental Model

A fume cupboard. You are not trying to prevent reactions — you are containing
them, on the assumption that some will go wrong.

## Example

Egress control is the step most often skipped and the one that matters most.
An agent with private repository access, exposure to untrusted web content, and
an open network connection has all three legs of the lethal trifecta. Denying
outbound network access by default removes the exfiltration path even when the
injection succeeds.

## Real-World Usage

Coding agents executing tests, data-analysis agents running generated code,
computer-use agents operating a disposable virtual machine, and hosted code
interpreters. Practical baseline: ephemeral container, read-only mounts for
anything the agent must see but not change, scoped short-lived tokens rather than
long-lived keys, deny-by-default egress, and full logging of what ran.

## Common Confusions

* **Containers are isolation, not a security boundary** — a plain container
  shares the host kernel. For genuinely untrusted code, VM-level isolation is the
  stronger choice.
* **Sandboxing is not a guardrail against bad output** — it constrains *effects*.
  A sandboxed agent can still return a confidently wrong answer.
* **The sandbox's output is untrusted** — treat returned text as data, never as
  instructions, or you have simply moved the injection one step later.

## Why Should I Care?

It is the control that converts "this agent might do something catastrophic" into
"this agent might waste a container", and it is the first thing a security review
will ask about for anything that executes code.
