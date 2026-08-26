---
term: Computer Vision
aliases: [CV, Image Understanding, Visual Recognition, Object Detection]
category: multimodal
subcategory: vision-language
depth: full
status: foundational
difficulty: intermediate
one_liner: "Getting a machine to extract meaning from images — the field that deep learning conquered first, and where much of it was invented."
origin:
  year: 1966
  circa: true
  attribution: MIT's Summer Vision Project famously assigned it to an undergraduate for one summer; it took fifty years
historical_period: classical-ai
diagram:
  kind: figure
  title: 2012 split the field in half
  footer: The learned column did not win by being cleverer about vision. It won by replacing the hand-designed
    half of the pipeline with more data.
  visual:
    kind: columns
    width: 700
    caption: the same task, before and after the features stopped being designed
    columns:
    - title: Classical · before 2012
      lines:
      - hand-designed features
      - SIFT · HOG · edge detectors
      - feed them to a classifier
      - brittle, domain-specific
      - a new domain means new features
    - title: Learned · after
      accent: true
      lines:
      - features learned from data
      - 'early layers: edges'
      - 'middle: textures and parts'
      - 'late: whole objects'
      - one pipeline, trained end to end
tags: [architecture]
relations:
  used_by: [vision-language-model, computer-use, embodied-ai]
  depends_on: [cnn, transformer]
  related_to: [image-generation, video-understanding, benchmark]
prerequisites: [cnn]
encountered_in: [research-papers, production-systems, conferences, job-descriptions]
sources:
  - type: paper
    title: "ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)"
    url: https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks
    year: 2012
  - type: paper
    title: "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (ViT)"
    url: https://arxiv.org/abs/2010.11929
    year: 2020
  - type: paper
    title: "Segment Anything"
    url: https://arxiv.org/abs/2304.02643
    year: 2023
videos:
  - title: "How Computer Vision Works"
    channel: "Computerphile"
    url: https://www.youtube.com/results?search_query=computerphile+how+computer+vision+works
updated: 2026-08-21
---

## Simple Explanation

An image is a grid of numbers. Computer vision is the problem of getting from
those numbers to statements about the world — there is a cat, it is here, this
tumour is malignant, that pedestrian is about to step out.

It is worth knowing because it went first. Nearly every technique now applied to
language was tested on images a decade earlier, and the field's history is the
best available account of how deep learning actually won.

## Technical Definition

The extraction of structured information from visual input. Canonical tasks:
classification (what is this), detection (what and where, as bounding boxes),
segmentation (which pixels belong to what), depth estimation, pose estimation,
and tracking across frames.

## Why Does It Exist?

Because most information about the physical world arrives visually, and none of
it is text. Any system that must act in the world — a robot, a vehicle, a quality
inspection line — needs this before it needs anything else.

## What Problem Does It Solve?

Perception. It is the input layer for everything from medical diagnosis to
autonomous driving to an agent reading a screen.

## How Does It Work?

The shift from designing features to learning them is the whole story, and
AlexNet in 2012 is where it happened.

## Mental Model

Not "seeing" but "measuring, repeatedly, at increasing levels of abstraction".
The model has no visual experience; it has a hierarchy of learned filters.

## Example

The field's benchmarks tell its history. ImageNet classification error fell from
around 26% in 2011 to under 4% within five years — past typical human performance
on that particular task, which prompted an important correction: the benchmark
was saturated, not vision solved. Models remained fragile to adversarial
perturbations, distribution shift and unusual viewpoints, and much of the
subsequent decade went into that gap rather than into the leaderboard.

## Real-World Usage

Medical imaging, manufacturing inspection, autonomous vehicles, retail
checkout, agriculture, satellite analysis, and the perception layer inside
multimodal models. Foundation models have arrived here too: Segment Anything
made "segment whatever I point at" a general capability rather than a
task-specific training project.

## Common Confusions

* **Computer vision vs a vision-language model** — the field versus one current
  approach to it. A VLM answers questions in text; a detector returns boxes, and
  for counting, measuring or localising, the detector is usually better.
* **Benchmark performance is not robustness** — models exceeding human accuracy
  on ImageNet still fail on lighting, occlusion and viewpoints outside their
  training distribution.
* **Vision is not solved** — recognition largely is, in-domain. Reliable
  understanding of novel scenes under real conditions is not.

## Why Should I Care?

It is the field that proved deep learning works, its architectures and its
benchmark culture were inherited wholesale by language modelling, and it remains
where AI most often touches physical processes.
