---
term: Operating System
aliases: [OS, Kernel, System Software]
category: computing-foundations
subcategory: os
depth: full
status: foundational
difficulty: beginner
one_liner: "The software that shares one machine's processors, memory and devices between many programs."
historical_period: early-computing
tags: [hardware]
relations:
  related_to: [paged-attention, memory-hierarchy, virtual-memory, cpu, inference-scheduler]
prerequisites: [cpu]
encountered_in: [interviews, production-systems, technical-blogs]
sources:
  - type: book
    title: "Operating Systems: Three Easy Pieces"
    url: https://pages.cs.wisc.edu/~remzi/OSTEP/
  - type: paper
    title: "MemGPT: Towards LLMs as Operating Systems"
    url: https://arxiv.org/abs/2310.08560
    year: 2023
    note: An explicit borrowing of OS concepts for context management.
updated: 2026-08-21
---

## Simple Explanation

One machine, many programs, all wanting the processor and the memory at once. The
operating system is the referee: it decides who runs when, gives each program the
illusion of having the machine to itself, and stops any of them reaching into
another's memory.

Worth understanding here for a specific reason — the LLM serving stack has
rebuilt most of it, under different names.

## Technical Definition

The software layer managing hardware resources and providing abstractions to
applications: process and thread scheduling, virtual memory, filesystems, device
drivers, network stacks, and isolation between processes. The kernel runs
privileged; applications request its services through system calls.

## Why Does It Exist?

Without one, every program would need to know the hardware directly, and any
program could corrupt any other. The OS exists to multiplex scarce resources
safely and to give applications a stable interface across different machines.

## What Problem Does It Solve?

Sharing, isolation and abstraction — three problems that recur wherever a scarce
resource serves many demands.

## How Does It Work?

```text
applications
     │ system calls
┌────▼───────────────────────────────────┐
│ scheduler   who runs on which core now │
│ memory      virtual → physical mapping │
│ filesystem  names → blocks             │
│ drivers     hardware specifics         │
│ isolation   processes cannot reach     │
│             into one another           │
└────────────────────────────────────────┘
     hardware
```

## Mental Model

An air traffic controller with a memory allocator attached. Nobody lands
unscheduled, and nobody parks on someone else's stand.

## Example

The reason this appears in an AI encyclopedia: an LLM serving engine is
structurally an operating system for a model. Its **scheduler** decides which
requests run each iteration. Its **block manager** maps logical KV cache
positions to physical blocks through a page table. It **preempts** sequences under
memory pressure and **swaps** them to host memory. It enforces **fairness** across
tenants.

The vLLM paper makes this lineage explicit. The problems are the same because the
situation is the same: one scarce resource, many concurrent demands, unpredictable
lifetimes.

## Real-World Usage

Linux underneath essentially every AI deployment. The parts that matter directly:
cgroups and namespaces for container isolation and sandboxing, huge pages for
reducing translation overhead on large memory footprints, NUMA awareness on
multi-socket machines, and the page cache, which determines how fast model
weights load from disk the second time.

## Common Confusions

* **Kernel (OS) vs kernel (GPU)** — the privileged core of an operating system
  versus a function run by GPU threads. Unrelated meanings.
* **Containers are not virtual machines** — containers share the host kernel and
  are isolated by namespaces; VMs run their own kernel. The distinction matters
  for sandboxing untrusted code.
* **The OS is not free** — system calls, context switches and page faults cost
  time, and on latency-sensitive serving paths they show up in profiles.

## Why Should I Care?

Half the vocabulary in LLM serving — scheduling, paging, preemption, swapping,
fairness — is borrowed from here, and knowing the originals makes the AI versions
read as familiar engineering rather than novel invention.
