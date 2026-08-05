# Project 5: AI-Powered Medical Assistant For Health Workers In Rwanda

Proposed team size: 5 students.

Project lead: Fabrice.

Keywords: machine learning, UX, multilingual AI, medical assistant.

## Short Description

Build an AI-powered medical assistant for health workers in Rwanda that supports questions in Kinyarwanda, English, and French through text or voice interaction.

## Motivation

Health workers may need access to medical guidance through interfaces that match their language, workflow, and connectivity constraints. This project aims to build a multilingual assistant that can receive a typed or spoken question, route it through a medical language-model pipeline, display an answer, generate audio output, and support multi-turn conversation.

The project should pay careful attention to language support, medical safety, UX, and the limitations of AI-generated medical answers.

## Intended Users

Potential users include:

- health workers in Rwanda;
- clinicians or community health workers who use Kinyarwanda, English, or French;
- supervisors evaluating multilingual medical support tools;
- teams exploring language adaptation for medical LLMs.

## Possible Features

Possible features include:

- text question input in Kinyarwanda, English, or French;
- voice recording;
- speech-to-text;
- medical LLM response generation;
- translation or language adaptation for Kinyarwanda with English medical terms;
- French support;
- audio generation of the answer;
- multi-turn conversation;
- safety warnings and uncertainty display;
- source or rationale display where possible.

The team should define which language and modality path is core for the final system and which are stretch goals.

## Design Questions

Consider:

- Which language paths must work for the proof of concept?
- How will the system handle mixed Kinyarwanda and English medical terms?
- What medical questions are in scope and out of scope?
- How should the assistant refuse unsafe requests?
- What should be displayed when confidence is low?
- How should audio input and output fit into the health worker workflow?
- What safety disclaimers or escalation guidance are needed?

## Technical Directions

Possible technical components include:

- multilingual text interface;
- speech-to-text;
- text-to-speech;
- medical LLM integration;
- translation model adaptation;
- fine-tuning or adaptation of a medical LLM such as MeditronFO;
- prompt and safety layer;
- conversation state management;
- evaluation examples in Kinyarwanda, English, and French.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one complete multilingual medical-assistant path.

Minimum convincing POC:

- the user submits one medical question through text or voice;
- the question passes through the language/model/interface pipeline;
- the system displays a medical assistant response;
- the system supports at least minimal multi-turn context;
- the system generates audio output or provides a clearly simulated audio-output path;
- the team clearly identifies which languages are fully working and which are simulated or partial;
- the system includes at least one safety or limitation behavior.

The POC may start with one primary language path. It should not be only a generic LLM chat interface without the multilingual and medical workflow being attempted.

## Evaluation Ideas

Possible evaluation approaches include:

- testing a small set of medical questions across supported languages;
- comparing translations or answers against reference examples;
- checking whether medical terminology is preserved;
- evaluating refusal or safety behavior on out-of-scope questions;
- measuring latency for text and voice paths;
- qualitative review of UI clarity for health workers;
- error analysis on mixed-language inputs.

## Final Demo Target

The final demo should show a health worker asking a question, receiving a multilingual medical response, continuing the conversation, hearing or generating audio output, and seeing clear safety or limitation cues.
