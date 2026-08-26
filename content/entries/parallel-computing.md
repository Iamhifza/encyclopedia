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
diagram:
  kind: steps
  title: The serial fraction sets the ceiling
  footer: Amdahl's law is the reason a hundred-fold increase in hardware rarely buys a hundred-fold speed-up,
    and the reason the first question about any parallel plan is what fraction cannot be parallelised
    at all.
  steps:
  - title: Some part of the work simply cannot be split
    visual:
      kind: segments
      width: 700
      label: one job
      caption: setup, coordination, the final reduction — whatever must happen in order
      segments:
      - text: serial
        value: 10
        value_label: 10%
        tone: warn
      - text: parallelisable
        value: 90
        value_label: 90%
  - title: So speed-up saturates however many processors you add
    notes:
    - label: And worse
      text: parallelism adds costs of its own — synchronisation, communication, load imbalance, contention
    visual:
      kind: plot
      width: 700
      height: 210
      x_range: [1, 64]
      y_range: [0, 11]
      x_label: processors
      y_label: speed-up
      caption: with a 10% serial fraction the ceiling is ten times, and sixteen processors already reach
        most of it
      curves:
      - label: actual
        tone: accent
        points: [[1.0, 1.0], [2.58, 2.225], [4.15, 3.156], [5.72, 3.888], [7.3, 4.479], [8.88, 4.965],
          [10.45, 5.373], [12.03, 5.719], [13.6, 6.018], [15.17, 6.277], [16.75, 6.505], [18.32, 6.706],
          [19.9, 6.886], [21.47, 7.047], [23.05, 7.192], [24.62, 7.323], [26.2, 7.443], [27.77, 7.553],
          [29.35, 7.653], [30.93, 7.746], [32.5, 7.831], [34.07, 7.911], [35.65, 7.984], [37.23, 8.053],
          [38.8, 8.117], [40.38, 8.177], [41.95, 8.234], [43.52, 8.287], [45.1, 8.336], [46.67, 8.383],
          [48.25, 8.428], [49.82, 8.47], [51.4, 8.51], [52.98, 8.548], [54.55, 8.584], [56.12, 8.618],
          [57.7, 8.651], [59.27, 8.682], [60.85, 8.712], [62.42, 8.74], [64.0, 8.767]]
      - label: ideal
        tone: muted
        points: [[1, 1], [11, 11]]
      marks:
      - at: [64, 10.0]
        text: 'ceiling: 1 ÷ serial fraction'
        dx: -10
        dy: -20
        anchor: end
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


Split work across processors and the runtime falls — but only for the part that
can actually be split. Whatever must happen in order, setup, coordination, the
final reduction, takes the same time however much hardware you add.

Amdahl's law makes this exact. If a fraction *s* of the work is serial, the best
achievable speed-up is 1/*s*, no matter how many processors are used. Ten per
cent serial means a ceiling of ten times, and about sixteen processors already
reach most of it. Adding more buys almost nothing.

Parallelism also adds costs the serial version did not have: synchronisation at
every barrier, communication between workers, load imbalance when one worker
finishes late, and contention for shared resources. Past some point these grow
faster than the parallel gains, and the curve turns downward — which is why the
first question about any parallel plan is what fraction cannot be parallelised
at all, and the second is what coordination the plan introduces.

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
