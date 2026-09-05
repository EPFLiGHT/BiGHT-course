# Project 5: AI-Powered Medical Assistant For Health Workers In Rwanda

Proposed team size: 5 students.

Project lead: Fabrice.

Keywords: machine learning, UX, multilingual AI.

## Short Description

The aim of this project is to build an AI-powered medical assistant for health workers in Rwanda, with a focus on adapting medical AI to Kinyarwanda and French.

## Motivation

Build an AI-powered medical assistant for health workers in Rwanda. The interface should allow the user to ask a question in Kinyarwanda, English, or French, either by typing the question or with a voice recording. The question should then be submitted to a medical LLM. The interface should show the response, allow generating an audio version of the response, and support multi-turn conversation.

Students are also asked to prepare the medical LLM to support Kinyarwanda, including English medical terms, and French. This may be done by using and fine-tuning a translation model, or by fine-tuning MeditronFO directly, with datasets in Kinyarwanda and French.

The main technical focus of the project is multilingual model adaptation and speech interaction rather than retrieval from country-specific clinical guidelines. Students should evaluate both the medical accuracy and the language accuracy of the resulting pipeline.

The project should pay careful attention to language support, medical safety, UX, and the limitations of AI-generated medical answers.

## Intended Users

Potential users include:

- health workers in Rwanda;
- clinicians or community health workers who use Kinyarwanda, English, or French;
- health workers who use mixed Kinyarwanda and English medical terminology;
- supervisors evaluating multilingual medical support tools;
- teams exploring language adaptation for medical LLMs;
- researchers evaluating speech interaction for low-resource medical AI.

## Possible Features

Possible features include:

- text question input in Kinyarwanda, English, or French;
- voice recording for medical questions;
- speech-to-text for one or more supported languages;
- medical LLM response generation;
- translation model adaptation for Kinyarwanda and French;
- fine-tuning or adaptation of MeditronFO directly;
- support for Kinyarwanda with English medical terms;
- datasets and evaluation examples in Kinyarwanda and French;
- audio generation of the answer;
- multi-turn conversation;
- safety warnings, refusal behavior, and uncertainty display;
- UX designed for health workers.

The team should define which language and modality paths are core for the final system and which are stretch goals. The project should not be framed primarily as retrieval from country-specific clinical guidelines.

## Design Questions

Consider:

- Which Kinyarwanda, English, and French paths must work for the proof of concept?
- How will the system handle mixed Kinyarwanda and English medical terms?
- Will the team adapt a translation model, fine-tune MeditronFO directly, or compare both approaches?
- What datasets are available for Kinyarwanda and French medical adaptation?
- What medical questions are in scope and out of scope?
- How should the assistant refuse unsafe requests or communicate uncertainty?
- How should audio input and output fit into the health worker workflow?
- How will medical accuracy and language accuracy be evaluated separately?
- What safety disclaimers or escalation guidance are needed?

## Technical Directions

Possible technical components include:

- multilingual text interface;
- speech-to-text for typed or recorded questions;
- text-to-speech for generated answers;
- medical LLM integration;
- translation model adaptation for Kinyarwanda and French;
- fine-tuning or adaptation of MeditronFO;
- dataset curation for Kinyarwanda and French medical examples;
- prompt, safety, and refusal layer;
- conversation state management for multi-turn interaction;
- evaluation of medical correctness and language quality;
- error analysis on mixed-language inputs and medical terminology.

The system should make clear which language paths are fully implemented, which are partial, and which are simulated. It should also distinguish model adaptation and speech interaction work from any optional retrieval or guideline-grounding component.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one complete multilingual medical-assistant path.

Minimum convincing POC:

- the user submits one medical question in Kinyarwanda, English, or French through text or voice;
- the question passes through the language, model, and interface pipeline;
- the system displays a medical assistant response;
- the system supports at least minimal multi-turn context;
- the system generates audio output or provides a clearly simulated audio-output path;
- the team demonstrates at least one concrete approach to Kinyarwanda or French model adaptation, such as translation-model adaptation, direct MeditronFO adaptation, or an evaluated comparison of candidate components;
- the team clearly identifies which languages and speech components are fully working, partial, or simulated;
- the system includes at least one safety, refusal, uncertainty, or limitation behavior.

The POC may start with one primary language path, but it should show that the multilingual adaptation problem has been attempted. It should not be only a generic LLM chat interface, and it should not be mainly a retrieval system over country-specific guidelines.

## Evaluation Ideas

Possible evaluation approaches include:

- testing a small set of medical questions across Kinyarwanda, English, and French;
- comparing translations or adapted-model outputs against reference examples;
- checking whether English medical terminology is preserved in Kinyarwanda contexts;
- evaluating medical correctness of answers using clinician or expert review where possible;
- evaluating language accuracy, fluency, and meaning preservation;
- evaluating refusal or safety behavior on out-of-scope or unsafe questions;
- measuring latency for text and voice paths;
- qualitative review of UI clarity for health workers;
- error analysis on mixed-language inputs, speech transcripts, and medical terminology.

## Final Demo Target

The final demo should show a health worker asking a medical question in Kinyarwanda, English, or French, optionally through voice, receiving a medical response, continuing the conversation, and hearing or generating audio output. The demo should also show evidence of multilingual model adaptation, evaluation of medical and language accuracy, and clear safety or limitation cues.
