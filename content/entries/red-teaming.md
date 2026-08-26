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
diagram:
  kind: steps
  title: Find it deliberately, before somebody finds it accidentally
  footer: The attack surface changes with every new capability, so this is a standing process rather than
    a pre-launch gate. A model that gains a tool has gained attacks that did not previously exist.
  steps:
  - title: The cycle
    visual:
      kind: chips
      items:
      - define
      - attack
      - found
      - fix
      loop: and again, because every new capability opens new attacks
  - title: A successful attack has three possible homes
    notes:
    - label: First, always
      text: a regression test — whatever else happens, it must never work again
    visual:
      kind: fan
      source: an attack
      caption: which one depends on whether the flaw is in the model, the permissions, or the product
      targets:
      - text: regression test
        new: true
      - training data
      - a permissions fix
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


Start by writing down what must never happen. Without that the exercise has no
success criterion and becomes an unbounded search for anything embarrassing.

Then attack it, from three directions at once: human experts who understand the
domain and think adversarially, automated attackers that generate and mutate
prompts at volume, and a library of known techniques replayed against the current
system. Volume finds the ordinary failures; expertise finds the ones nobody
thought to automate.

Every successful attack has three possible homes. It becomes a regression test
first, always — whatever else happens, it must never work again. If the flaw is
in the model's behaviour it becomes training data. If it is really a permissions
problem, the fix is architectural and no amount of training will substitute.

And it repeats, because the attack surface changes with every new capability. A
model that gains a tool has gained attacks that did not exist the week before,
which makes this a standing process rather than a pre-launch gate.

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
