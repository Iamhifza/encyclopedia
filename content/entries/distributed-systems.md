---
term: Distributed Systems
aliases: [Distributed Computing, Cluster Computing, Consensus, Fault Tolerance]
category: computing-foundations
subcategory: networking
depth: full
status: foundational
difficulty: advanced
one_liner: "Many machines cooperating on one job, and the failure, coordination and consistency problems that come free with that."
tags: [hardware]
relations:
  used_by: [pipeline-parallelism, tensor-parallelism]
  related_to: [throughput, parallel-computing, operating-system, inference-provider]
prerequisites: [parallel-computing]
encountered_in: [interviews, job-descriptions, production-systems]
sources:
  - type: paper
    title: "Time, Clocks, and the Ordering of Events in a Distributed System (Lamport)"
    url: https://lamport.azurewebsites.net/pubs/time-clocks.pdf
    year: 1978
  - type: paper
    title: "Fallacies of Distributed Computing Explained"
    url: https://www.rgoarchitects.com/Files/fallacies.pdf
  - type: report
    title: "The Llama 3 Herd of Models — training infrastructure and failures"
    url: https://arxiv.org/abs/2407.21783
    year: 2024
updated: 2026-08-21
---

## Simple Explanation

One machine either works or it does not. A thousand machines are always in some
partial state: several are slow, one has just died, two disagree about what
happened, and the network dropped a message somebody is still waiting for.

Distributed systems is the discipline of getting useful work out of that
situation. Every large training run and every serving fleet is one, which is why
AI infrastructure is largely a distributed systems job wearing different
vocabulary.

## Technical Definition

Systems whose components run on networked machines and coordinate by message
passing. The defining difficulties are partial failure (some components fail
while others continue), absence of a global clock, unbounded message delay, and
the consequent trade-offs formalised by results such as CAP and FLP.

## Why Does It Exist?

Some workloads exceed any single machine — in compute, memory, storage or
required availability. Once you cross that line, you inherit the whole problem
set whether you wanted it or not.

## What Problem Does It Solve?

Scale and availability, at the cost of coordination complexity that does not
exist on one machine.

## How Does It Work?

```text
the fallacies — assumptions that are always wrong at scale:
   the network is reliable          latency is zero
   bandwidth is infinite            the network is secure
   topology never changes           there is one administrator
   transport cost is zero           the network is homogeneous

what you get instead:
   partial failure · stragglers · retries and duplicates ·
   consistency choices · coordination overhead
```

## Mental Model

An orchestra where the musicians cannot see each other, the conductor's beat
arrives late and by different amounts, and occasionally a player leaves without
saying so. Coordination is the entire problem.

## Example

Large-scale training makes this concrete. The Llama 3 training run reported
frequent hardware failures across its cluster — at that scale, something breaking
is the steady state rather than an incident. Synchronous training means every
step waits for the slowest worker (the straggler problem), and a single failure
requires restarting from a checkpoint. Checkpoint frequency becomes a direct
trade between storage cost and how much work a failure destroys.

Serving has the mirror problem: replicas, load balancing, health checks, and
graceful degradation when a node dies mid-generation.

## Real-World Usage

Every multi-node training run, every serving fleet, every inference provider.
The specific vocabulary of AI infrastructure — all-reduce, NCCL, sharding,
checkpointing, straggler mitigation — is distributed systems vocabulary applied
to a particular workload.

## Common Confusions

* **Distributed vs parallel** — parallelism is about doing work simultaneously;
  distribution adds the network, and with it partial failure and the absence of
  shared memory. All distributed systems are parallel; the reverse is not true.
* **More machines is not proportionally more speed** — communication and
  synchronisation grow, and beyond some point they dominate.
* **Failure is normal at scale** — designing for "the happy path plus error
  handling" fails; failure is the operating condition.

## Why Should I Care?

Beyond a single GPU, every AI system is a distributed system, and its hardest
problems — stragglers, failures mid-run, consistency between replicas — were
studied and named decades before anyone trained a Transformer.
