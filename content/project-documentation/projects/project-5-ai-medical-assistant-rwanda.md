# Project 5: AI-Powered Medical Assistant For Health Workers In Rwanda

Proposed team size: 3 students.

Project lead: Xavier.

Keywords: machine learning, multilingual AI, foundation models, LLM, global health, NLP.

## Short Description

Build an AI-powered medical assistant for health workers in Rwanda, with a focus on adapting medical AI to support Kinyarwanda, English, and French.

## Motivation

Health workers, triage nurses, and clinicians in Rwanda regularly navigate clinical protocols across Kinyarwanda, English, French, and mixed-language medical terminology. Code-switching between a local language and English clinical terms is standard, yet general-purpose clinical models are rarely evaluated in this low-resource setting.

The core deliverable is a text-based, multi-turn conversational interface where health workers submit clinical queries in Kinyarwanda, English, or French to a specialized medical LLM. The MVP focuses on a text-based medical chatbot supporting Kinyarwanda, with speech interaction (ASR/TTS) and retrieval-augmented generation (RAG) over Rwandan clinical guidelines serving as optional stretch goals.

Candidate corpus: https://huggingface.co/datasets/EPFLiGHT/fully-open-meditron

Reference: https://arxiv.org/abs/2605.16215

## Intended Users

Potential users include:

- Health workers, clinicians, and community triage nurses in Rwanda consulting protocols or seeking rapid guidance in local and mixed languages.
- Supervisors and researchers evaluating multilingual adaptation, cross-lingual transfer, and clinical safety tools for low-resource languages.

## Possible Features

Possible features include:

- multi-turn conversational interface for clinical question answering in Kinyarwanda, English, and French;
- handling of medical code-switching within Kinyarwanda text;
- preservation of standardized English clinical terminology in generated answers;
- clinical safety guardrails and refusal behavior for emergency triage or unsupported diagnoses;
- uncertainty cues and explicit disclaimers in the interface;
- datasets and evaluation examples in Kinyarwanda and French;
- lightweight interface suitable for low-bandwidth clinic settings;
- speech-to-text and text-to-speech interaction for spoken clinical queries (stretch goal);
- retrieval-augmented generation over Rwandan clinical guidelines and national health protocols (stretch goal).

The team should define which language paths are core for the final system and which are stretch goals.

## Design Questions

Consider:

- How does direct fine-tuning of a clinical LLM compare against a translation-mediated pipeline built on NLLB-200 or Gemma-4 in terms of medical accuracy, translation fidelity, latency, and operational cost?
- How can the system preserve critical clinical terminology such as drug names, dosages, and physiological terms when generating or translating Kinyarwanda?
- What datasets are available for Kinyarwanda and French medical adaptation, and what has to be created or translated?
- What mechanisms best detect out-of-scope, emergency, or high-risk clinical queries to trigger refusal and escalation?
- How should uncertainty and confidence be surfaced to health workers to avoid over-reliance on generated answers?
- How will medical accuracy and language accuracy be evaluated separately?
- If speech is attempted, what are the latency and accuracy trade-offs of streaming versus batch ASR and TTS for low-resource languages in low-bandwidth clinics?

## Technical Directions

Possible technical components include:

- parameter-efficient fine-tuning of an open medical foundation model such as `EPFLiGHT/Apertus-8B-MeditronFO` using LoRA or QLoRA;
- instruction tuning on curated or translated parallel Kinyarwanda clinical question-answering data;
- a translation-mediated pipeline that translates input into English, prompts the medical LLM, and translates the answer back into Kinyarwanda, using a translation model such as NLLB-200 or Gemma-4;
- explicit constraints to keep technical medical vocabulary intact across translation steps;
- dataset curation for Kinyarwanda and French medical examples;
- confidence scoring, uncertainty estimation, and structured refusal logic;
- conversation state management for multi-turn interaction;
- evaluation of medical correctness and language quality;
- error analysis on mixed-language inputs and medical terminology;
- lightweight ASR such as a fine-tuned Whisper model and TTS for Kinyarwanda speech (stretch goal).

The system should make clear which language paths are fully implemented, which are partial, and which are simulated. It should also distinguish model adaptation work from any optional retrieval or speech component.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one complete multilingual medical-assistant path in text.

Minimum convincing POC:

- the user submits a medical question in Kinyarwanda through a command-line or minimal web interface;
- the question passes through the language, model, and interface pipeline;
- the system displays a medical assistant response and supports at least minimal multi-turn context;
- the team demonstrates both baseline approaches, a translation-mediated pipeline and an initial fine-tuned medical model checkpoint;
- the team reports an initial qualitative and quantitative comparison of the two approaches on a representative subset of clinical questions;
- the system refuses at least one high-risk emergency query and shows clinical disclaimers;
- the team documents a data collection, curation, and validation plan for Kinyarwanda clinical evaluation data;
- the team clearly identifies which languages and components are fully working, partial, or simulated.

The POC may start with one primary language path. The adaptation work itself should be visible in the repository, so that the answers can be traced back to a documented translation or fine-tuning step.

## Evaluation Ideas

Possible evaluation approaches include:

- testing a small set of clinician-reviewed medical questions across Kinyarwanda, English, and French for factual correctness and hallucination rate;
- evaluating medical correctness of answers using clinician or expert review where possible;
- measuring language quality, fluency, and meaning preservation in Kinyarwanda with human ratings or reference-based metrics such as BLEU, chrF, or COMET;
- benchmarking correct retention versus mistranslation of essential clinical terms such as medication names, units, and diagnostic terms;
- comparing direct fine-tuning against the translation-mediated pipeline built on NLLB-200 or Gemma-4 on accuracy, inference latency, memory footprint, and compute requirements;
- testing refusal behavior and graceful degradation on out-of-scope, emergency, or adversarial medical prompts;
- measuring latency for the text path, and for the voice path if attempted;
- error analysis on mixed-language inputs, medical terminology, and speech transcripts.

## Final Demo Target

The final demo should show a health worker holding a multi-turn conversation with the medical assistant in Kinyarwanda through the chatbot interface. The demo should also show evidence of model adaptation, separate evaluation of language and clinical quality, visible safety and limitation cues, and, if attempted as a stretch goal, working speech-to-text and text-to-speech interaction.
