# Project 2: Interactive Public Health Messenger

Proposed team size: 3 students.

Project lead: Lars.

Keywords: conversational AI, retrieval-augmented generation, public health communication, understanding-aware communication, UI/UX.

## Short Description

Build an interactive public health messenger that helps people understand crisis instructions, checks whether guidance was understood, and aggregates misunderstanding patterns for responders.

## Motivation

During a disaster or public health crisis, authorities broadcast critical instructions about water safety, evacuation, disease prevention, or other protective actions. But people may misunderstand, reinterpret, or partially remember what they hear. Small misunderstandings can have serious consequences. The core challenge is not just sending information, but ensuring it is actually understood.

This project turns dissemination into an interactive loop. Instead of one-way communication, users can voluntarily engage with a low-connectivity-friendly chatbot through voice or text to ask questions, clarify doubts, or hear the latest guidance. The system should answer using vetted information, for example through retrieval-augmented generation over trusted sources, while also assessing whether the user truly understood the answer.

For example, after explaining something, the system might ask: "Just to check: What would you do in this situation?" The goal is not to test or shame the user. The goal is to reveal whether the message was understood well enough to support safe action.

The most interesting part is what happens across many interactions. Rather than only monitoring passively, the system should aggregate patterns of misunderstanding. If many users misinterpret the same message in the same way, that signals a problem with how the guidance is phrased. The system can then suggest alternative formulations or highlight risky misconceptions to responders.

## Intended Users

Potential users include:

- people affected by a disaster, outbreak, or crisis;
- public health responders communicating urgent guidance;
- emergency communication teams;
- local authorities responsible for public messaging;
- humanitarian organizations monitoring whether guidance is understood;
- community engagement teams improving message clarity.

## Possible Features

Possible features include:

- interactive question answering grounded in trusted public health or crisis guidance;
- text or voice interface designed for low-connectivity settings;
- retrieval-augmented generation over vetted documents;
- lightweight understanding checks, such as explain-back or scenario-based questions;
- detection of partial, repeated, or dangerous misunderstandings;
- aggregation of misunderstanding patterns across conversations;
- responder dashboard highlighting confusing guidance and risky misconceptions;
- suggestions for clearer alternative formulations;
- participatory feedback where users compare phrasings or mark responses as clear or confusing;
- privacy-aware logging and aggregation.

The team should choose a focused crisis or public health scenario and avoid building a generic chatbot without a clear understanding loop.

## Design Questions

Consider:

- How do you ask someone to demonstrate understanding without sounding like a test?
- How do you design prompts that reveal real comprehension instead of encouraging users to repeat what they just heard?
- What makes an answer safely grounded in trusted sources?
- What counts as a partial or dangerous misunderstanding?
- How should misunderstanding patterns be aggregated without exposing individual users?
- How should a responder dashboard flag guidance that is often misunderstood?
- How can users help refine explanations, compare phrasings, or signal which responses felt clear or confusing?
- What should happen when trusted guidance is ambiguous, missing, or internally inconsistent?
- What should work in low-connectivity settings?

## Technical Directions

Possible technical components include:

- retrieval-augmented generation over a small trusted document collection;
- prompt design for public health explanations and understanding checks;
- voice or text-based conversational interface;
- comprehension-check response capture;
- classification, clustering, or rule-based detection of misunderstanding patterns;
- responder dashboard showing frequently misunderstood guidance;
- alternative phrasing generation or ranking;
- low-connectivity-friendly UI/UX design;
- privacy-aware logging and aggregation of interaction signals.

The system should make the source of guidance visible and should distinguish between trusted content, generated explanation, user understanding signal, and aggregate responder insight.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one complete understanding-aware communication loop.

Minimum convincing POC:

- the user submits one public health or crisis-related question through text or voice;
- the system retrieves at least one relevant passage from a trusted source;
- the system generates or displays an answer grounded in that source;
- the system asks one lightweight understanding check, such as an explain-back or scenario-based question;
- the user response is captured as a comprehension or misunderstanding signal;
- the system identifies at least one partial or dangerous misunderstanding pattern from one or more example interactions;
- at least one aggregate signal is displayed, logged, or shown in a simple responder dashboard;
- the system clearly identifies what is retrieved, what is generated, and what is inferred from the user's response.

The POC may use a small trusted document set, scripted example conversations, and a simple dashboard. It should not be only a chatbot that answers questions without checking understanding, and it should not be only a dashboard without an interactive communication loop.

## Evaluation Ideas

Possible evaluation approaches include:

- checking whether generated answers are supported by retrieved trusted passages;
- testing understanding-check prompts on scripted or example user responses;
- measuring whether known misconceptions are detected;
- evaluating whether the dashboard highlights recurring misunderstandings;
- comparing alternative phrasings for clarity;
- assessing whether explain-back prompts reveal comprehension rather than memorization;
- reviewing privacy risks in interaction logs and aggregate reporting;
- qualitative review of UI/UX for users and responders.

## Final Demo Target

The final demo should show a user asking for crisis or public health guidance, receiving an answer grounded in trusted information, responding to an understanding check, and the responder view updating with a meaningful comprehension or misunderstanding signal. The demo should also show how repeated misunderstanding patterns could lead responders to revise guidance or flag risky misconceptions.
