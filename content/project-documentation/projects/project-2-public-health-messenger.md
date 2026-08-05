# Project 2: Interactive Public Health Messenger

Proposed team size: 4 or 5 students.

Project lead: Lars.

## Short Description

Build an interactive communication system that helps people understand public health or crisis instructions, asks lightweight understanding checks, and aggregates patterns of misunderstanding for responders.

## Motivation

During a disaster, outbreak, or crisis, authorities may broadcast critical instructions about water safety, evacuation, disease prevention, or treatment-seeking behavior. The problem is not only whether information was sent. The problem is whether people actually understood it.

Small misunderstandings can have serious consequences. A useful system should help users clarify instructions and help responders detect which messages are being misunderstood.

## Intended Users

Potential users include:

- affected community members;
- public health responders;
- emergency communication teams;
- local authorities;
- humanitarian organizations.

## Possible Features

Possible features include:

- text or voice-based question answering;
- retrieval from trusted guidance documents;
- answers grounded in vetted sources;
- lightweight understanding checks;
- explain-back or scenario-based questions;
- detection of partial or dangerous misunderstandings;
- aggregation of misunderstanding patterns;
- dashboard for responders showing confusing guidance;
- suggestions for clearer alternative phrasing.

The team should choose a focused scenario and avoid building a generic chatbot without a clear communication loop.

## Design Questions

Consider:

- How do you ask someone to demonstrate understanding without sounding like a test?
- How do you avoid encouraging users to repeat the exact wording they just saw?
- What makes an answer safely grounded in trusted sources?
- What counts as a dangerous misunderstanding?
- How should misunderstandings be aggregated without exposing individual users?
- What should happen when guidance is ambiguous or missing?

## Technical Directions

Possible technical components include:

- retrieval-augmented generation over trusted documents;
- prompt design for clear public health explanations;
- comprehension checks;
- classification or clustering of misunderstanding patterns;
- low-connectivity-friendly interface design;
- responder dashboard;
- logging and privacy-aware aggregation.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one complete communication loop.

Minimum convincing POC:

- the user submits one public health question;
- the system retrieves at least one relevant trusted passage;
- the system generates or displays an answer grounded in that source;
- the system asks one understanding check;
- the user response is captured as a comprehension or misunderstanding signal;
- at least one aggregate signal is displayed, logged, or shown in a simple responder view.

The POC may use a small trusted document set and a simple dashboard. It should not be only a chatbot that answers questions without checking understanding.

## Evaluation Ideas

Possible evaluation approaches include:

- checking whether generated answers are supported by retrieved sources;
- testing understanding-check prompts on example user responses;
- measuring whether known misconceptions are detected;
- evaluating whether the dashboard highlights recurring issues;
- reviewing privacy risks in interaction logs;
- comparing alternative phrasings for clarity.

## Final Demo Target

The final demo should show a user asking for guidance, receiving a grounded explanation, responding to an understanding check, and the responder view updating with a meaningful misunderstanding or comprehension signal.
