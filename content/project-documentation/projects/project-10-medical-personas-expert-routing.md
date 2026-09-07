# Project 10: Medical Personas And Expert Routing For Clinical QA

Proposed team size: 4 students.

Project lead: Jeremy.

Keywords: LLM, Clinical Q&A, Medical Personas, Prompt Engineering, Medical AI.

## Short Description

Investigate whether specialist medical personas can improve the accuracy and consistency of large language models on clinical question-answering tasks.

## Motivation

Large language models are increasingly being used for medical question answering, but their performance can vary significantly depending on the type and complexity of the clinical question. One possible way to improve their performance is to prompt them to adopt the perspective of a relevant medical specialist, such as an infectious-disease physician, radiologist, epidemiologist, or another clinical expert.

However, it is not yet clear which specialist personas are most effective for different categories of medical questions, or whether specialization consistently improves model reasoning and accuracy. A persona that helps with one specialty may not help another. Some personas may even make the model more confident while reducing correctness.

The aim of this project is to systematically evaluate how different medical personas affect performance across clinical QA benchmarks and to identify which personas improve or degrade particular types of questions. Students will identify and gather suitable clinical QA datasets, then curate and transform them into a benchmark organized by question type, medical specialty, and complexity where possible.

Based on these findings, students will develop an expert-routing system that predicts the most appropriate persona, or combination of personas, for each question. The system should be compared against a generic physician prompt and multi-persona ensemble approaches to determine whether dynamic specialist routing can improve and standardize clinical QA performance without requiring additional model training.

Students will also develop an interactive interface where users can submit clinical questions, inspect the selected specialist persona or personas, compare alternative routing strategies, and explore the resulting answers and evaluation results.

## Intended Users

Potential users include:

- clinicians and clinical educators studying how LLM prompts affect medical answers;
- medical AI researchers evaluating specialist prompting strategies;
- benchmark designers organizing clinical QA tasks by specialty and complexity;
- developers building safer clinical decision-support interfaces;
- reviewers who need to inspect why a system selected a particular expert persona.

## Possible Features

Possible features include:

- curated benchmark of clinical QA questions with specialty, question type, and complexity labels;
- prompt library for generic physician and specialist medical personas;
- evaluation pipeline comparing persona prompts across clinical QA datasets;
- expert router that selects one or more personas for a given question;
- multi-persona ensemble baseline for comparison;
- answer generation interface showing the selected persona and final answer;
- evaluation dashboard showing accuracy, consistency, calibration, and failure patterns;
- side-by-side comparison of generic, routed, and ensemble strategies;
- analysis tools for identifying which personas improve or degrade specific question categories.

The team should avoid building only a generic medical chatbot. The core of the project is the systematic evaluation and routing of medical personas for clinical question answering.

## Design Questions

Consider:

- Which clinical QA datasets are suitable for evaluating persona-based prompting?
- How should questions be labeled by specialty, type, difficulty, or complexity?
- Which specialist personas should be tested, and how should their prompts be written?
- Does a specialist persona improve factual accuracy, reasoning consistency, calibration, or only style?
- When does specialization degrade performance or introduce overconfidence?
- Should the router select one persona, multiple personas, or an ensemble strategy?
- What features of a question should influence expert routing?
- How should the interface make the selected persona and routing rationale inspectable?
- How should the system communicate uncertainty and avoid presenting generated answers as medical advice?

## Technical Directions

Possible technical components include:

- dataset collection and curation for clinical QA benchmarks;
- specialty, question-type, and complexity annotation workflow;
- prompt engineering for generic physician and specialist personas;
- automated benchmark runner for evaluating multiple prompts and models;
- metric calculation for accuracy, consistency, calibration, and answer stability;
- expert-routing model based on rules, embeddings, classifiers, or LLM-based routing;
- multi-persona ensemble baseline and aggregation strategy;
- interactive web interface for question submission, routing inspection, and result comparison;
- dashboard for per-specialty and per-question-type performance analysis.

The system should clearly separate the question, selected persona, generated answer, evaluation evidence, and routing rationale.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one complete persona-evaluation and routing workflow.

Minimum convincing POC:

- the team curates a small clinical QA benchmark with documented question labels;
- at least one generic physician prompt and several specialist persona prompts are implemented;
- the system evaluates persona prompts on a subset of the benchmark;
- the team reports where specific personas improve or degrade performance;
- an expert router selects a persona or persona set for a new clinical question;
- the selected routing strategy is compared with a generic physician prompt and at least one ensemble baseline;
- the demo interface shows the submitted question, selected persona, generated answer, and comparison results;
- the repository includes clear documentation of datasets, prompts, metrics, and limitations.

The POC may use a small benchmark subset and a limited set of medical specialties. It should not be only a prompt collection, and it should not hide the routing logic from reviewers.

## Evaluation Ideas

Possible evaluation approaches include:

- comparing routed personas against generic physician prompts on accuracy;
- measuring consistency across repeated runs or prompt variants;
- analyzing performance by specialty, question type, and complexity;
- testing whether routing improves difficult or specialty-specific questions;
- checking for overconfidence, unsupported claims, or unsafe medical advice;
- comparing single-persona routing with multi-persona ensemble approaches;
- evaluating the router's specialty selection against labeled questions;
- reviewing whether the interface makes routing decisions and limitations understandable;
- documenting failure cases where persona prompting worsens performance.

## Final Demo Target

The final demo should show a user submitting a clinical question, the router selecting an appropriate specialist persona or persona set, and the system comparing the routed answer with a generic physician prompt and an ensemble baseline. The demo should also show benchmark-level evidence about which personas helped or hurt different categories of clinical questions, along with clear limitations and safeguards around medical use.
