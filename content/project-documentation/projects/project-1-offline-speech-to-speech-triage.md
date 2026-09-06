# Project 1: Offline Speech-To-Speech System For Humanitarian Triage

Proposed team size: 5 students.

Project lead: David.

Partner: ICRC.

Partner logo: https://upload.wikimedia.org/wikipedia/commons/b/b6/Emblem_of_the_ICRC.svg

Keywords: natural language processing, conversational AI.

## Short Description

Offline speech-to-speech system that can help humanitarian workers in Yemen with triage.

## Motivation

This project explores the development of a small, open-source, offline speech-to-speech system for medical triage in low-resource settings. It is motivated by a real-world ICRC use case in Yemen, where Arabic-speaking medical staff may need to communicate with patients who speak Amharic, Oromo, Somali, or Tigrinya, and where reliable internet access or interpreters may not be available.

Students will investigate and compare open-source components for automatic speech recognition, machine translation, and speech synthesis. They will assess how effectively these components can be combined to provide two-way spoken translation between Arabic and the target languages, with Oromo as the highest priority.

The project will also explore interactive and collaborative translation workflows. These may include using an LLM to discuss or refine possible translations, mechanisms for users or conversation partners to verify and correct translations, and forward and backward translation as a possible sanity check. Students may also investigate recording and multi-turn interaction workflows, for example allowing utterances to be revisited, reviewed by another person, or refined across a conversation.

The project will focus particularly on what can run fully offline on low-cost, resource-constrained hardware. The goal is not to produce a deployment-ready clinical application, but to establish what is currently technically possible, identify promising models and architectures, explore effective human-in-the-loop interaction patterns, and determine the key limitations that would need to be addressed before such a system could eventually be deployed on ordinary Android phones in Yemen or similar low-resource settings.

## Intended Users

Potential users include:

- humanitarian workers supporting medical triage in Yemen;
- Arabic-speaking medical staff communicating with patients who speak Amharic, Oromo, Somali, or Tigrinya;
- patients who need to describe symptoms, history, or concerns across a language barrier;
- field teams working without reliable internet access or interpreters;
- technical and humanitarian teams assessing offline translation feasibility for low-resource settings.

## Possible Features

Possible features include:

- offline speech input and recording;
- automatic speech recognition for Arabic and one or more target languages;
- machine translation between Arabic and Amharic, Oromo, Somali, or Tigrinya;
- speech synthesis for translated outputs;
- two-way spoken translation workflow;
- forward and backward translation as a sanity check;
- LLM-assisted discussion or refinement of possible translations when feasible;
- mechanisms for users or conversation partners to verify, reject, or correct translations;
- multi-turn conversation history;
- delayed review of recorded utterances by another person;
- lightweight interface designed for medical triage in constrained settings.

The team should not attempt all features. The technical design should identify a core triage communication workflow, prioritize Oromo where feasible, and define a realistic proof-of-concept path.

## Design Questions

Consider:

- Which language pair should be prioritized for the proof of concept, and why?
- What can realistically run fully offline on low-cost, resource-constrained hardware?
- How accurate are available open-source ASR, translation, and speech synthesis components for Arabic, Oromo, Amharic, Somali, and Tigrinya?
- How should the interface communicate uncertainty, alternative translations, and possible errors?
- How can a patient or conversation partner verify or correct a translation without speaking the staff member's language?
- When is backtranslation useful, and when might it create false confidence?
- How should recordings, conversation history, and reviewed utterances be stored, deleted, or protected?
- What parts of the workflow are safe for triage support, and what must remain out of scope?

## Technical Directions

Possible technical components include:

- comparison of open-source ASR models;
- comparison of open-source machine translation models;
- comparison of open-source speech synthesis options;
- offline inference pipeline design;
- model-size, latency, storage, and hardware-feasibility analysis;
- Arabic-to-target-language and target-language-to-Arabic translation path;
- LLM-assisted translation refinement where feasible, with clear limits if offline LLM use is not realistic;
- user interface for recording, playback, translation display, correction, and conversation history;
- scripted medical triage scenarios for evaluation;
- bilingual or expert review of translation outputs.

The system should be designed so that the core path can run reproducibly in the project repository. The project should make clear which components run offline, which require optional connectivity, and which remain simulated or experimental.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one thin vertical slice through an offline triage translation workflow.

Minimum convincing POC:

- the user records or enters one triage-relevant utterance;
- the system processes the utterance through an ASR, translation, and output path, or clearly documents which speech components are simulated;
- the system supports at least one Arabic-to-target-language or target-language-to-Arabic translation path, with Oromo prioritized where feasible;
- the translated result is displayed and, if feasible, spoken back to the user;
- the interface provides at least one mechanism for verification or refinement, such as backtranslation, alternative translations, partner confirmation, correction, or LLM-assisted discussion;
- the demo uses at least one scripted medical triage scenario;
- the system clearly identifies what runs offline, what is simulated, and what requires optional connectivity.

The POC may use one prioritized language pair, a small model, sample audio, or scripted utterances. It should not be only a static UI mock-up or a generic text translator without speech, triage context, or offline-feasibility analysis.

## Evaluation Ideas

Possible evaluation approaches include:

- comparing ASR outputs against reference transcripts for scripted triage utterances;
- comparing translation outputs against bilingual reference translations or bilingual review;
- measuring whether backtranslation or partner verification catches obvious translation failures;
- assessing latency, model size, storage requirements, and offline runtime feasibility;
- testing the workflow on low-cost or resource-constrained hardware where possible;
- evaluating whether the interface makes uncertainty, alternatives, verification, and corrections understandable;
- analyzing privacy and data-retention risks for recordings and conversation history;
- documenting language coverage gaps and points of failure across Arabic, Oromo, Amharic, Somali, and Tigrinya.

## Final Demo Target

The final demo should show a short medical triage exchange in which the system records or receives speech, translates between Arabic and a target language, presents or speaks the translated output, and supports verification or correction. The demo should also explain what ran offline, what hardware or resource constraints were tested, which models and architectures were most promising, and what limitations must be solved before deployment on ordinary Android phones in Yemen or similar low-resource settings.
