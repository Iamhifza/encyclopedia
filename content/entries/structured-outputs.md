---
term: Structured Outputs
aliases: [Constrained Decoding, JSON Mode, Grammar-Constrained Generation, Schema Enforcement]
category: protocols
subcategory: calling
depth: full
status: modern
difficulty: intermediate
one_liner: "Forcing a model's output to match a schema or grammar by masking out any token that would break it."
tags: [protocol, inference]
relations:
  depends_on: [sampling]
  used_by: [tool-calling, ai-workflow]
  different_from: [tool-calling]
  related_to: [hallucination, evaluation-harness]
prerequisites: [sampling]
encountered_in: [documentation, production-systems, github]
sources:
  - type: repo
    title: "Outlines — structured generation for language models"
    url: https://github.com/dottxt-ai/outlines
  - type: paper
    title: "Efficient Guided Generation for Large Language Models"
    url: https://arxiv.org/abs/2307.09702
    year: 2023
  - type: docs
    title: "Anthropic — tool use and structured output"
    url: https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview
updated: 2026-08-21
---

## Simple Explanation

Asking politely for JSON gets you JSON most of the time — and the rest of the
time you get a preamble, a code fence, a trailing comma, or a field that should
have been a number and is a string. At scale, "most of the time" is a parsing
error queue.

Structured outputs remove the problem rather than mitigating it. At each step,
any token that would make the output invalid is simply removed from
consideration before sampling. Malformed output becomes impossible, not unlikely.

## Technical Definition

Constrained decoding: a schema (JSON Schema, regular expression, or context-free
grammar) is compiled into a state machine, and at each generation step the set of
tokens that keep the output on a valid path is computed. Logits for all other
tokens are set to $-\infty$ before sampling, so the model can only choose
continuations that conform.

## Why Does It Exist?

Any program consuming model output needs to parse it. Prompt instructions are
advisory — the model can ignore them, and does, especially under distribution
shift or at high temperature. Retry-until-it-parses works and costs a request
each time it fails.

## What Problem Does It Solve?

The interface between a probabilistic component and deterministic code.

## How Does It Work?

```text
schema: {"age": integer}

partial output:  {"age":
                        │ state machine says: only digits are valid here
logits:  "  0.8   ← masked to −∞
         2  0.1   ← allowed
         t  0.05  ← masked to −∞
                        │
                  sample only from what remains
```

The constraint is applied to the *sampler*, not the prompt. The model's
preferences still decide which valid token is chosen; the grammar decides which
tokens are valid at all.

## Mental Model

Rails, not instructions. You are not asking the train to stay on the track.

## Example

Extracting fields from an invoice with a schema requiring `total` to be a number
means you cannot receive `"total": "£4,320 (incl. VAT)"`. The model must emit
digits. Note carefully what this does and does not guarantee: the output will
parse, and the number may still be wrong. Structure is not accuracy.

## Real-World Usage

Supported by major model APIs and by open-source serving stacks through libraries
such as Outlines, and the same machinery underpins reliable tool calling, since
a tool invocation is a schema-constrained object. Standard for extraction
pipelines, classification with a fixed label set, and any step whose output feeds
code rather than a person.

## Common Confusions

* **Structured outputs vs tool calling** — one constrains the *format* of a
  response; the other is a protocol for requesting an *action*. Tool calling
  usually relies on this machinery, which is why they are so often conflated.
* **Valid is not correct** — the single most important caveat. Schema conformance
  says nothing about whether the values are right.
* **Constraints can hurt quality** — over-restrictive grammars, or demanding
  structured output on a task requiring reasoning, can degrade the answer.
  Letting the model reason in free text first and then emit structure usually
  works better.
* **Not the same as JSON mode** — some providers' "JSON mode" only guarantees
  syntactic validity, not adherence to your schema. Check which you are getting.

## Why Should I Care?

It converts a whole category of production flakiness — parse failures, missing
fields, inconsistent types — from a probabilistic problem into an impossibility,
and it is usually one parameter away in an API you already call.
