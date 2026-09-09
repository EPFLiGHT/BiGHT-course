# Project 11: Flowchart Meditron: Clinical Answers As Decision Flowcharts

Proposed team size: 3 students.

Project lead: Xavier.

Keywords: LLM, structured generation, clinical decision support, fine-tuning, LLM-as-a-judge, UI/UX.

## Short Description

Build a clinical assistant that answers a question with prose and a decision flowchart generated at the same time, showing the possible next actions and how they branch on the clinician's next finding.

## Motivation

Clinicians reason in branches. A febrile child with a given history leads to one differential if the temperature is above a threshold and another if it is below, and to different next actions depending on what a test returns. Clinical practice guidelines encode this as algorithms and flowcharts, but a language model answers in paragraphs, leaving the clinician to rebuild the branching structure in their head while under time pressure.

This project asks what happens when the answer itself is structured. For a clinical query and a patient vignette, the assistant returns a text answer together with a flowchart describing possible next actions, or the paths that open up depending on the next finding, including differential diagnoses. A chart might branch on a temperature threshold, a test result, or a response to first-line treatment, and end in candidate diagnoses or concrete actions.

There is no existing model that does this and no dataset that teaches it. The team therefore has to define how the model should express a flowchart, build the training data that teaches it, adapt the model, and design an interface that can extract and render what the model produced. Each of those steps is a design decision the team must justify rather than a component to be looked up.

The evaluation problem is as interesting as the generation problem. A flowchart can be well formed and still contradict the text it accompanies, and it can be faithful to the text and still fail to render. Both failure modes have to be measured.

Candidate corpus: https://huggingface.co/datasets/EPFLiGHT/fully-open-meditron

Reference: https://arxiv.org/abs/2605.16215

## Intended Users

Potential users include:

- clinicians working through a differential diagnosis under time pressure;
- frontline health workers deciding what to check or do next;
- medical students and trainees learning how a clinical decision branches;
- clinical educators who want a reasoning path made explicit rather than implied;
- researchers investigating structured or constrained generation for medical AI.

## Possible Features

Possible features include:

- a chat interface where a clinician submits a query together with a patient vignette;
- a text answer and a decision flowchart generated in the same response;
- flowcharts that branch on a threshold, a test result, or a treatment response;
- differential diagnoses as terminal nodes of a branch;
- deterministic extraction of the flowchart from the model output;
- client-side rendering of the flowchart, with a readable fallback when it is malformed;
- validation that flags charts that do not parse, contain dangling nodes, or contradict the text;
- uncertainty and safety cues attached to branches that carry clinical risk;
- an inspection view showing the raw generated chart alongside the rendered one.

The team should decide early which parts of clinical reasoning the flowchart is meant to carry, and which belong in the prose answer.

## Design Questions

Consider:

- What representation should the model generate: a diagram language such as Mermaid or Graphviz that the model has already seen during pretraining, or a constrained schema that is easier to validate but entirely unfamiliar to it?
- How should the flowchart be delimited in the answer so that extraction is deterministic rather than a parsing heuristic?
- Where does training data for this come from, given that no such corpus exists?
- What makes a flowchart clinically correct rather than merely well formed, and who can say so?
- How should the system behave when the model generates a chart that does not parse or render?
- A rendered decision tree looks more authoritative than hedged prose, so how should uncertainty and risk be shown inside the chart itself?
- When is a flowchart the wrong format for an answer, and should the model be able to decline to draw one?
- How large or deep should a chart be before it stops helping the clinician?

## Technical Directions

Possible technical components include:

- a specification of the flowchart representation, its allowed node and edge types, and its validation rules;
- training-data construction by extracting decision algorithms from clinical practice guidelines;
- training-data construction by distillation from a stronger model, keeping only candidates that parse, render, and survive a consistency check;
- reverse construction, where a published clinical algorithm is paired with a vignette and question that would lead to it;
- parameter-efficient fine-tuning of an open medical foundation model such as `EPFLiGHT/Apertus-8B-MeditronFO` using LoRA;
- constrained or grammar-guided decoding to raise the share of outputs that parse;
- an extraction and validation layer that separates prose from chart and checks the chart before it reaches the interface;
- a web interface that renders the chart and degrades gracefully to text when rendering fails;
- an LLM-as-a-judge protocol scoring whether the chart and the text agree;
- a prompted baseline that asks a general model for the same output without any fine-tuning.

The prompted baseline is what the fine-tuned model has to beat, so it should exist from the start rather than be reconstructed at the end.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one complete path from a clinical query to a rendered flowchart.

Minimum convincing POC:

- the flowchart representation is specified and documented, with the reasons for choosing it;
- the team has built a first set of training examples and documented how they were produced and checked;
- a model produces a text answer with an accompanying flowchart, from either fine-tuning or the prompted baseline;
- the interface extracts the chart from the answer and renders it;
- the team reports the share of generated charts that parse and render on held-out queries;
- at least one failure case is shown, with the interface behaving sensibly when the chart is malformed;
- an early version of the consistency judge exists, even if it is only run on a handful of examples;
- the team states which parts are fine-tuned, which are prompted, and which are hand-written.

The parse and render rate is cheap to measure and should be tracked from the first week, since it is the clearest early signal that the generation format works.

## Evaluation Ideas

Possible evaluation approaches include:

- measuring the share of generated charts that parse and render without manual repair;
- checking structural validity, including dangling nodes, unreachable branches, cycles where none should exist, and branch conditions that overlap or leave gaps;
- scoring answer-and-chart consistency with an LLM-as-a-judge, checking that the chart introduces no step absent from the text and omits none of its key steps;
- validating that judge against clinician or expert ratings on a small subset, and reporting how well the two agree;
- comparing the fine-tuned model against the prompted baseline on parse rate, consistency, and clinical quality;
- pairwise comparison of text with a flowchart against text alone for the same vignette, to test whether the chart adds anything;
- measuring how chart size and depth relate to judged usefulness;
- error analysis on the charts that fail, separating format failures from clinical failures.

## Final Demo Target

The final demo should show a clinician submitting a query with a patient vignette and receiving a text answer alongside a flowchart that branches on a plausible next finding and ends in candidate diagnoses or actions. The demo should also show the parse and render rate on a held-out set, the comparison against the prompted baseline, the consistency judge running on real outputs, and how the interface behaves when the model produces a chart it cannot render.
