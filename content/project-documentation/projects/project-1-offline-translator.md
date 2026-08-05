# Project 1: Offline Translator For Low-Resource Languages

Proposed team size: 4 students.

Project lead: Lars.

## Short Description

Build an offline or low-connectivity translation assistant for settings where people need to communicate across languages despite unreliable internet access.

## Motivation

A person is traveling, working, or responding in a setting where they do not speak the local language and internet access is unreliable. Existing tools such as downloadable translation models already exist, but the project asks whether the interaction can be made more useful, trustworthy, and participatory.

The challenge is not only translation quality. The challenge is communication under uncertainty.

## Intended Users

Potential users include:

- humanitarian workers;
- health workers;
- travelers in low-connectivity settings;
- field teams working across languages;
- people who need translation support but cannot rely on live internet access.

## Possible Features

Possible features include:

- text input and translation;
- audio recording;
- speech-to-text before translation;
- forward and backward translation;
- a way for the conversation partner to check whether the translation seems faithful;
- interaction with an LLM to discuss possible translations;
- delayed review of recorded utterances in a quieter or safer context;
- collaborative translation across a multi-turn conversation.

The team should not attempt all features. The technical design should identify a small core use case and a realistic proof-of-concept path.

## Design Questions

Consider:

- How does the interface communicate uncertainty in the translation?
- How can a conversation partner provide feedback without needing to speak English fluently?
- When is backtranslation helpful, and when can it be misleading?
- What happens when the system cannot confidently translate?
- What should work offline, and what can require optional connectivity?
- How should recordings be stored, deleted, or protected?

## Technical Directions

Possible technical components include:

- local or downloadable translation models;
- speech-to-text;
- text-to-speech;
- LLM-assisted translation refinement;
- language identification;
- confidence or uncertainty display;
- lightweight user interface for field use.

The system should be designed so that the core path can run reproducibly in the project repository.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one thin vertical slice through the translation workflow.

Minimum convincing POC:

- the user records or enters one utterance;
- the system processes the utterance through the translation path;
- the translated result is displayed to the user;
- the interface provides at least one mechanism for verification or refinement, such as backtranslation, alternative translations, partner confirmation, or LLM-assisted discussion;
- the system clearly indicates what part is real and what part is simulated.

The POC may use a simplified language pair, a small model, or sample audio. It should not be only a static UI mock-up.

## Evaluation Ideas

Possible evaluation approaches include:

- comparing translation outputs against reference translations for a small test set;
- measuring whether backtranslation catches obvious translation failures;
- qualitative review of interaction flows;
- testing whether the user can recover from an uncertain or wrong translation;
- latency and offline-readiness checks;
- privacy and data retention analysis for recordings.

## Final Demo Target

The final demo should show a short conversation or exchange in which the system helps a user translate, verify, and refine meaning under constrained conditions.
