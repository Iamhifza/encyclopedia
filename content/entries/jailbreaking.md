---
term: Jailbreaking
aliases: [Jailbreak, Safety Bypass, Adversarial Prompting, DAN]
category: evaluation-safety
subcategory: adversarial
depth: full
status: established
difficulty: intermediate
one_liner: "A user manipulating a model into behaviour its training was meant to prevent."
origin:
  year: 2022
  circa: true
  attribution: The term migrated from iOS device jailbreaking to LLMs during the first wave of public chat assistants
historical_period: agentic
diagram:
  kind: figure
  title: Every technique reframes the request so compliance looks like helpfulness
  footer: Refusal is learned behaviour over a distribution of phrasings, not a rule applied to meanings
    — so anything that moves a request off that distribution has a chance. Which is why this is mitigated
    rather than solved.
  visual:
    kind: stack
    width: 780
    caption: roughly in order of how much effort each takes to mount
    layers:
    - label: direct
      text: ask plainly for the prohibited thing
      note: refused
      tone: ok
    - label: role-play
      text: '"you are a character who would explain…"'
      note: fiction as cover
    - label: hypothetical
      text: '"in a story, how would someone…"'
      note: distance as cover
    - label: translation
      text: the same request in a low-resource language
      note: thinner safety data
    - label: encoding
      text: base64, leetspeak, a substitution cipher
      note: obscures the trigger
    - label: optimised
      text: an adversarial token suffix found by search
      note: transfers between models
      tone: warn
    - label: multi-turn
      text: benign, then slightly less, then the target
      note: no single turn looks bad
      tone: warn
tags: [safety]
relations:
  different_from: [prompt-injection]
  related_to: [alignment, red-teaming, guardrails, rlhf]
prerequisites: [large-language-model, alignment]
encountered_in: [social-media, research-papers, conferences, production-systems]
sources:
  - type: paper
    title: "Universal and Transferable Adversarial Attacks on Aligned Language Models"
    url: https://arxiv.org/abs/2307.15043
    year: 2023
  - type: paper
    title: "Jailbroken: How Does LLM Safety Training Fail?"
    url: https://arxiv.org/abs/2307.02483
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

A model is trained to decline certain requests. Jailbreaking is finding the
framing under which it declines to decline — a role-play, a hypothetical, a
translation, a story, an encoding, or a long conversation that walks it there
one step at a time.

The user here is the attacker. That is what separates it from prompt injection,
where the user is the victim.

## Technical Definition

Adversarial input designed to elicit behaviour a model's alignment training was
intended to suppress. Techniques include persona and role-play framing,
hypothetical or fictional distancing, low-resource languages and encodings,
token-level adversarial suffixes found by optimisation, and multi-turn escalation
from benign starting points.

## Why Does It Exist?

Two structural reasons. Safety training teaches the model to refuse *patterns* it
saw during training, and the space of possible framings is unbounded — coverage
is impossible. And there is a genuine tension in the objective: the model is
trained both to be helpful and to refuse, and any framing that makes compliance
look like helpfulness pulls against the refusal.

## What Problem Does It Solve?

For researchers, it measures the robustness of alignment. For everyone else it is
a problem, not a solution.

## How Does It Work?

The optimisation-based attacks are the most theoretically interesting: gradient
search over token sequences finds suffixes that are meaningless to humans and
reliably defeat refusal — and, notably, transfer across models they were not
optimised against.

## Mental Model

Not picking a lock. Talking your way past a doorkeeper whose instructions were
written in natural language and therefore have edges nobody enumerated.

## Example

The transferability result is the uncomfortable one. Adversarial suffixes
computed against open-weight models worked on closed models the attacker could
not inspect — implying the vulnerability is a property of how these models are
trained, not of any one implementation.

## Real-World Usage

A permanent activity: published jailbreaks get patched, new framings appear, and
the cycle continues. Labs run red teams against their own models pre-release, and
robustness to jailbreaking is now a reported safety metric.

## Common Confusions

* **Jailbreaking vs prompt injection** — the crucial distinction. Jailbreaking is
  the *user* attacking the model's policies. Injection is a *third party*
  hijacking a system on behalf of an unwitting user. Different attacker,
  different victim, different defences.
* **It is not hacking** — no system is compromised. The model produces text it
  was trained not to produce.
* **Refusals are not a security boundary** — for anything that must never happen,
  use guardrails in code. A refusal is a behaviour, and behaviours have edges.
* **Not all bypasses are harmful** — a great deal of what is called jailbreaking
  is working around over-refusal on benign requests, which is a real usability
  problem in the other direction.

## Why Should I Care?

It sets the honest expectation for what alignment training can deliver: a strong
default, not a guarantee. Anything you actually need to be impossible belongs in
your architecture, not in the model's disposition.
