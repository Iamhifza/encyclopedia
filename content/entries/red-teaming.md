---
term: Red Teaming
aliases: [Adversarial Testing, Safety Testing, AI Red Teaming]
category: evaluation-safety
subcategory: adversarial
depth: full
status: established
difficulty: intermediate
one_liner: "Deliberately attacking your own system to find the failures before someone else does."
historical_period: foundation-model
tags: [safety]
relations:
  part_of: [evaluation-harness]
  related_to: [jailbreaking, prompt-injection, alignment, guardrails, benchmark]
prerequisites: [benchmark]
encountered_in: [research-papers, job-descriptions, conferences, production-systems]
sources:
  - type: paper
    title: "Red Teaming Language Models with Language Models"
    url: https://arxiv.org/abs/2202.03286
    year: 2022
  - type: paper
    title: "Red Teaming Language Models to Reduce Harms"
    url: https://arxiv.org/abs/2209.07858
    year: 2022
  - type: docs
    title: "NIST AI Risk Management Framework"
    url: https://www.nist.gov/itl/ai-risk-management-framework
updated: 2026-08-21
---

## Simple Explanation

Your evaluation set contains the cases you thought of. Attackers will use the
ones you did not. Red teaming is the deliberate attempt to make your own system
misbehave — by people trying to succeed at it, not by people confirming it works.

## Technical Definition

Structured adversarial evaluation: generating inputs intended to elicit
prohibited, harmful or out-of-policy behaviour, documenting successful attacks,
and feeding them back as regression tests and training data. Performed manually
by domain experts, automatically by attacker models, or both.

## Why Does It Exist?

Benchmarks measure average behaviour on anticipated inputs. Safety is determined
by worst-case behaviour on unanticipated ones, and those two numbers are almost
unrelated. Nothing in a standard evaluation suite tells you what a determined
person can extract.

## What Problem Does It Solve?

The blind spot in your own test set — and, for agent systems, the far larger
question of what an attacker can make the system *do* rather than say.

## How Does It Work?

```text
define what must never happen
        │
   attack: manual experts · automated attacker models · known technique library
        │
   successful attack found
        │
        ├─▶ regression test (it must never work again)
        ├─▶ training data (if fixable in the model)
        └─▶ architectural fix (if it is a permissions problem)
        │
   repeat — the attack surface changes with every new capability
```

## Mental Model

Penetration testing, with one crucial difference: the vulnerability is a
*behaviour* rather than a code path, so it cannot be patched, only made less
likely and better contained.

## Example

For a chat model, red teaming means jailbreak attempts, role-play framings,
encoded requests and multi-turn escalation. For an agent, it means something
harder: planting instructions in a web page the agent will read, and seeing
whether it can be induced to use its real permissions. The second is a much more
serious class of finding, because a successful attack causes an action rather
than a sentence.

## Real-World Usage

Standard practice before frontier model releases, increasingly required by
regulatory and procurement frameworks, and a named job function at major labs.
Automated red teaming — one model generating attacks against another — scales
coverage, while human experts remain far better at finding the genuinely novel
framings.

## Common Confusions

* **Red teaming is not evaluation** — evaluation samples typical inputs; red
  teaming searches for worst cases. Both are necessary and they measure
  different things.
* **Red teaming is not a certificate** — failing to find an attack is weak
  evidence of safety. Absence of proof, as ever.
* **Findings expire** — every new tool, integration or capability reopens the
  surface. It is a recurring activity, not a launch gate.

## Why Should I Care?

If your system takes actions in the world, someone will eventually probe it.
Whether that person is on your side the first time is the only variable you
control.
