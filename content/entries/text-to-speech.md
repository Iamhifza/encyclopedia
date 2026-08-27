---
term: Text-to-Speech
aliases: [TTS, Speech Synthesis, Voice Cloning, Neural Vocoder]
category: multimodal
subcategory: audio
depth: full
status: established
difficulty: intermediate
one_liner: "Generating natural-sounding speech from text, increasingly with the speaker's voice and tone under control."
historical_period: foundation-model
diagram:
  kind: figure
  title: Speech as tokens, and a voice from three seconds of reference
  footer: Prosody, emphasis and emotion come from the token model rather than from markup or rules, which
    is why current systems sound natural and why they cannot be precisely directed. Cloning a voice from
    seconds of audio is the same capability, and the same problem.
  visual:
    kind: pipeline
    width: 740
    caption: 'the codec is what made this tractable: audio becomes a discrete sequence, so the same machinery
      that models text can model speech'
    stages:
    - text: text, plus ~3 seconds of reference audio
      note: what and who
    - text: audio tokens
      tone: accent
      via: an autoregressive or diffusion model over a learned codec
    - text: a waveform
      via: codec decoder
tags: [architecture]
relations:
  related_to: [speech-recognition, diffusion-model, autoregressive-generation, tokenization]
prerequisites: [transformer]
encountered_in: [production-systems, research-papers, documentation]
sources:
  - type: paper
    title: "WaveNet: A Generative Model for Raw Audio"
    url: https://arxiv.org/abs/1609.03499
    year: 2016
  - type: paper
    title: "Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers (VALL-E)"
    url: https://arxiv.org/abs/2301.02111
    year: 2023
updated: 2026-08-21
review_by: 2027-02-01
---

## Simple Explanation

Older speech synthesis stitched together recorded fragments, which is why it
sounded like a ransom note read aloud. Modern systems generate the audio itself —
and the current generation does it by tokenising audio and treating speech
synthesis as, essentially, another language modelling problem.

That framing is why voice cloning from a few seconds of reference audio became
possible.

## Technical Definition

Generation of a speech waveform from text. The modern pipeline encodes audio into
discrete tokens with a neural codec, models those tokens autoregressively (or with
diffusion) conditioned on text and on a reference speaker embedding, and decodes
back to a waveform. This replaced the earlier two-stage design of predicting a
mel-spectrogram then converting it with a separate vocoder.

## Why Does It Exist?

Interfaces where reading is impractical — driving, accessibility, telephony — and,
more recently, conversational agents where latency and prosody determine whether
an interaction feels usable.

## What Problem Does It Solve?

Making generated speech sound like a person rather than a machine, and doing it
fast enough for real-time conversation.

## How Does It Work?

The neural audio codec is the enabling piece: it compresses a waveform into a
short sequence of discrete tokens, which is what allows language-model machinery
to be applied to sound.

## Mental Model

Reading aloud rather than assembling recordings. The system decides how the
sentence should sound, then produces it — which is why it can convey emphasis it
was never explicitly told to use.

## Example

Zero-shot voice cloning is the capability that changed the field's ethics
overnight. A few seconds of reference audio is sufficient to produce arbitrary
speech in that voice. The technique has legitimate uses — accessibility for
people losing their voice, localisation, audiobook production — and obvious ones
for fraud and impersonation. Consent verification, watermarking and provenance
standards exist because the capability arrived faster than any norms around it.

## Real-World Usage

Voice assistants, screen readers, audiobooks, dubbing and localisation, and the
output stage of voice agents. In conversational systems the binding constraint is
latency: streaming synthesis must begin before the sentence is complete, which
constrains how much context the model can use for prosody.

## Common Confusions

* **TTS vs voice cloning** — synthesis in general versus synthesis conditioned on
  a specific speaker. The second is a capability of most current systems, not a
  separate technology.
* **Naturalness is not intelligibility** — a system can sound human and stumble
  on names, acronyms, code and numbers, which is where practical failures live.
* **Speech is not text reversed** — speech recognition and synthesis share
  machinery but are not symmetric problems; prosody has no equivalent in the
  text direction.

## Why Should I Care?

It is half of every voice agent, its latency behaviour determines whether such an
agent feels conversational, and it is the clearest current example of a
capability whose ethical infrastructure is still being built after the fact.
