---
term: Speech Recognition
aliases: [ASR, Automatic Speech Recognition, Speech-to-Text, Transcription]
category: multimodal
subcategory: audio
depth: full
status: established
difficulty: intermediate
one_liner: "Turning spoken audio into text, now usually with the same Transformer machinery used for language."
historical_period: foundation-model
tags: [architecture]
relations:
  depends_on: [transformer, encoder-decoder]
  related_to: [text-to-speech, vision-language-model, tokenization]
prerequisites: [transformer]
encountered_in: [production-systems, research-papers, documentation]
sources:
  - type: paper
    title: "Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)"
    url: https://arxiv.org/abs/2212.04356
    year: 2022
  - type: paper
    title: "wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations"
    url: https://arxiv.org/abs/2006.11477
    year: 2020
updated: 2026-08-21
---

## Simple Explanation

Sound arrives as a waveform — tens of thousands of amplitude values per second.
Speech recognition converts that into a spectrogram (a picture of which
frequencies are present when), treats it as a sequence, and runs it through an
encoder-decoder Transformer that emits text.

Once audio is a sequence of vectors, it is the same problem as translation.

## Technical Definition

Mapping an acoustic signal to a text transcript. Modern systems encode audio
frames — typically log-mel spectrogram features — and decode text
autoregressively, trained end to end. This replaced the classical pipeline of
acoustic model, pronunciation lexicon and separate language model with a single
learned mapping.

## Why Does It Exist?

Speech is how people communicate most naturally, and everything downstream —
search, translation, analysis, summarisation — operates on text.

## What Problem Does It Solve?

Access to spoken content at scale: meetings, calls, broadcasts, voice interfaces,
and accessibility for people who cannot use a keyboard or read a screen.

## How Does It Work?

```text
waveform ──▶ spectrogram ──▶ audio encoder ──▶ representations
                                                     │
                                        text decoder ▼ (cross-attention)
                                    "the meeting starts at ten"
```

Two design points differ from text. Audio is continuous, so it is windowed into
frames — typically 25 ms with a 10 ms hop. And the decoder is usually conditioned
on task tokens specifying language, and whether to transcribe or translate, which
is how one model handles many languages.

## Mental Model

Reading a spectrogram the way you read a page. The picture of the sound has
structure; the model learns to read it.

## Example

Whisper's contribution was less architectural than methodological: 680,000 hours
of weakly supervised multilingual audio scraped from the web, rather than clean
curated corpora. The result was robustness — accents, background noise, domain
shift — that carefully trained models on clean data had never achieved. Another
instance of scale and diversity beating curation, and it was released
open-weight, which reset the whole field's baseline.

## Real-World Usage

Meeting transcription, captioning, voice assistants, call-centre analytics,
medical dictation. Hosted APIs and open-weight models both perform well. The
remaining hard problems are less about accuracy than structure: **diarisation**
(who spoke), **streaming** (transcribing before the sentence ends, without the
benefit of future context), code-switching between languages, and domain
vocabulary — names, drugs, part numbers — where a general model reliably guesses
a common word instead.

## Common Confusions

* **Word error rate is not the whole story** — a system with excellent WER can be
  useless if it fails on exactly the proper nouns your application cares about.
* **Streaming versus batch** — offline transcription can look at the whole
  utterance; streaming cannot, and pays for it in accuracy.
* **Transcription is not understanding** — accurate text with no diarisation, no
  punctuation and no structure is often not what the downstream task needed.

## Why Should I Care?

It is the most mature multimodal capability in production, it is the input layer
for voice agents, and it is a clean demonstration that the Transformer stopped
being a text architecture some time ago.
