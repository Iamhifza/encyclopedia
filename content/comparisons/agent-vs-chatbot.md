---
title: Agent vs Chatbot
question: Is the output the product, or is the change in the world the product?
sides: [ai-agent, large-language-model]
---

## The short version

A chatbot's output *is* the deliverable — you read it and decide what to do. An
agent's output is a change in the world: a file edited, a ticket created, an
email sent. That difference changes everything downstream, from evaluation to
security review.

## Side by side

| | Chatbot | Agent |
|---|---|---|
| **Deliverable** | Text you read | Actions taken |
| **Turns** | One request, one response | Many steps, chosen at run time |
| **Can it be wrong safely?** | Usually — you evaluate before acting | No — it already acted |
| **Cost per request** | Predictable | Variable; needs step and spend caps |
| **Evaluation** | Was the answer good? | Did the task complete, and what did it touch? |
| **Failure** | A bad answer | A bad state, possibly irreversible |
| **Security surface** | The prompt | Every tool, credential and document it reads |
| **Needs** | A good prompt | A harness, permissions, sandbox, traces |

## The line

```text
CHATBOT
  user ──▶ model ──▶ text ──▶ HUMAN decides what to do
                                  ▲
                         the safety mechanism is here

AGENT
  user ──▶ model ──▶ tool ──▶ world changes ──▶ model ──▶ ...
                                  ▲
                    the human may never be in this loop
```

Removing the human from between the model and the consequence is the entire
distinction, and it is why an agent needs an architecture rather than a prompt.

## What people actually mean by "chatbot"

Usually a thin product surface over a model — perhaps with retrieval attached,
which makes it grounded and still not an agent. Adding retrieval improves what it
knows; adding tools changes what it can do. Only the second crosses the line.

## The middle ground most products occupy

Read-only tools. A model that can search a knowledge base, query a database or
fetch a page takes actions with no side effects. That is meaningfully more than a
chatbot and meaningfully less than an agent with write access — and it is the
sensible place to start, because the failure mode is a wrong answer rather than a
wrong action.

## Why the label matters commercially

"Agent" sells, so it is applied to products with no loop, no tool choice and no
autonomy. The test is unchanged from the [Agent vs Workflow](agent-vs-workflow.md)
comparison: ask what happens at step three, and who decides.

## Verdict

If a human reads the output before anything happens, you have a chatbot, and you
should be glad — it is far easier to make reliable. Cross the line only when the
task genuinely requires acting, and when you have the harness, permissions and
traces to justify it.
