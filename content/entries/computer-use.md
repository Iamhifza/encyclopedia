---
term: Computer Use
aliases: [Computer-Use Agent, GUI Agent, Browser Agent, Screen Agent]
category: multimodal
subcategory: agents
status: emerging
difficulty: advanced
one_liner: An agent that operates a computer the way a person does — looking at the screen, moving the cursor and typing — instead of calling APIs.
origin:
  year: 2024
  attribution: Shipped as a model capability by Anthropic in October 2024; research prototypes and browser agents preceded it
historical_period: agentic
tags: [agents]
relations:
  is_a: [ai-agent]
  depends_on: [vision-language-model, agent-loop]
  related_to: [prompt-injection, guardrails]
prerequisites: [ai-agent, vision-language-model]
encountered_in: [production-systems, documentation, social-media]
sources:
  - type: docs
    title: "Anthropic — computer use documentation"
    url: https://docs.claude.com/en/docs/agents-and-tools/computer-use
    year: 2024
  - type: paper
    title: "OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments"
    url: https://arxiv.org/abs/2404.07972
    year: 2024
updated: 2026-08-21
review_by: 2026-12-01
---

## Simple Explanation

Most software has no API, or has one you cannot get access to. A computer-use
agent sidesteps that entirely: it takes a screenshot, decides where to click,
issues the click, takes another screenshot, and continues. The interface is the
one built for humans.

## Technical Definition

An agent loop whose observation is a screenshot and whose action space is
low-level input events — cursor coordinates, clicks, keystrokes, scrolls —
requiring the model to ground its intent in pixel coordinates and to verify
outcomes visually.

## Why Does It Exist?

The universe of software with a usable API is much smaller than the universe of
software. Legacy internal tools, desktop applications and most enterprise systems
have only a GUI.

## What Problem Does It Solve?

Automation of systems that cannot be integrated with, without waiting for anyone
to build an API.

## How Does It Work?

```text
screenshot ──▶ model ──▶ {"action":"click","x":842,"y":317}
     ▲                          │
     └──── new screenshot ◀── executed in a VM or container
```

Every step costs a full image in context, so sessions are token-heavy and slow
compared with tool calling.

## Mental Model

A remote worker on a screen-share who can see the desktop and use the mouse, but
has no special access to anything underneath.

## Example

Benchmarks on real desktop environments show steady but incomplete progress:
multi-step tasks across applications remain unreliable relative to human
performance, though the trajectory since 2024 has been rapid.

## Real-World Usage

Browser automation, legacy enterprise software without APIs, QA and regression
testing of user interfaces, and form-filling workflows. Deployments run the agent
inside a virtual machine with restricted network access rather than on a user's
own desktop.

## Common Confusions

* **Computer use vs tool calling** — pixels and clicks versus structured function
  calls. Prefer an API whenever one exists: it is faster, cheaper and far more
  reliable.
* **It is not screen scraping** — there is no DOM parsing or selector; the model
  interprets the rendered image.
* **Security exposure is severe** — anything rendered on screen is untrusted
  input capable of carrying instructions, and the agent holds whatever
  credentials the session does. Sandboxed VMs, restricted egress and approval
  gates are baseline requirements.

## Why Should I Care?

It is the most general and least constrained agent capability, which makes it
both the most broadly applicable and the one whose deployment demands the most
containment.
