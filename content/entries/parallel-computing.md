---
term: Parallel Computing
aliases: [Concurrency, SIMD, Multiprocessing, Amdahl's Law]
category: computing-foundations
subcategory: os
depth: full
status: foundational
difficulty: intermediate
one_liner: "Splitting work so that many processors make progress at the same time rather than one doing it all."
historical_period: early-computing
tags: [hardware]
relations:
  used_by: [tensor-parallelism, pipeline-parallelism]
  related_to: [gpu, cpu, distributed-systems, throughput]
prerequisites: [cpu]
encountered_in: [interviews, research-papers, production-systems]
sources:
  - type: paper
    title: "Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities (Amdahl)"
    url: https://dl.acm.org/doi/10.1145/1465482.1465560
    year: 1967
  - type: book
    title: "Computer Architecture: A Quantitative Approach"
    url: https://www.elsevier.com/books/computer-architecture/hennessy/978-0-12-811905-1
updated: 2026-08-21
---

## Simple Explanation

Processors stopped getting much faster around 2005. They started getting more
numerous instead. Since then, going faster has meant splitting the work — and the
central, unavoidable fact is that the parts you *cannot* split determine your
ceiling.

Every parallelism strategy in AI training and serving is an answer to the
question of how to split a specific piece of work, and what synchronisation the
split forces you to pay for.

## Technical Definition

Simultaneous execution of computation across multiple processing elements.
Classified by what is replicated: **data parallelism** (same operation, different
data — SIMD within a core, or replicated model copies across GPUs), **task
parallelism** (different operations concurrently), and **pipeline parallelism**
(stages of a sequence overlapping across units).

## Why Does It Exist?

Dennard scaling ended: transistors kept shrinking but power density stopped
falling, so clock speeds plateaued. Additional transistors went into more cores
rather than faster ones, and the burden of using them moved to software.

## What Problem Does It Solve?

Throughput on work that decomposes. It does nothing for work that does not.

## How Does It Work?

```text
        serial fraction limits everything
   ┌────────┬──────────────────────────────┐
   │ serial │      parallelisable          │
   └────────┴──────────────────────────────┘
        ▲
   with infinite processors, total time
   still cannot fall below this part

plus the costs parallelism adds:
   synchronisation · communication · load imbalance · contention
```

## Mental Model

Nine women cannot deliver a baby in one month. Some work decomposes; some
categorically does not, and the difference is a property of the problem rather
than of your effort.

## Formula

Amdahl's law, the discipline's central constraint:

$$S = \frac{1}{(1-p) + \frac{p}{N}}$$

* $p$ — fraction of the work that can be parallelised.
* $N$ — number of processors.
* $S$ — resulting speedup.

At $p = 0.95$ and infinite processors, the maximum speedup is 20×. A 5% serial
fraction caps you at twenty times, no matter how much hardware you buy — which is
why identifying and shrinking the serial portion matters more than adding
devices.

## Example

Autoregressive decoding is the AI example that Amdahl explains perfectly. Token
$t+1$ cannot begin until token $t$ exists — that dependency is strictly serial and
no amount of hardware removes it. This is precisely why decode is latency-bound,
why batching helps throughput but not per-request speed, and why speculative
decoding is interesting: it is an attempt to break the serial chain by guessing
ahead.

## Real-World Usage

Inside a GPU (thousands of threads in lockstep), across GPUs (tensor, pipeline,
data and expert parallelism), and across machines. Each level adds communication
cost, which is why the parallelism strategy for a large training run is chosen
against the interconnect topology rather than in the abstract.

## Common Confusions

* **Concurrency vs parallelism** — concurrency is structuring work as independent
  tasks; parallelism is executing them simultaneously. You can have either
  without the other.
* **More processors is not more speed** — communication and synchronisation grow
  with $N$, and past some point adding devices makes things slower.
* **Amdahl vs Gustafson** — Amdahl fixes the problem size; Gustafson observes
  that with more compute people solve *bigger* problems, which is a fairer
  description of what actually happens in AI.

## Why Should I Care?

Every distributed training and serving decision is a parallelism decision, and
Amdahl's law explains the one thing about LLM inference that no amount of hardware
fixes: generation is sequential by construction.
