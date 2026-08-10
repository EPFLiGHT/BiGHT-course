# Milestone 2: Proof Of Concept

Deadline: Friday of Week 8, November 6, 21:59.

Weight: 20% of the course grade.

The midterm oral presentation is a separate 10% assessment.

## Purpose

This is the most important intermediate milestone. Your proof of concept should show a thin vertical slice through the system.

A vertical slice means that one meaningful path through the system works end to end, even if the dataset, scale, model quality, or interface is simplified.

The proof of concept should not be only a collection of isolated components. It should not be only a polished UI mock-up. It should demonstrate that the central technical idea has been attempted.

## Submission

Submit inside your team repository.

Required file:

```text
docs/milestone-2-proof-of-concept.md
```

Also include:

- demo instructions;
- midterm presentation slides or notes for the separate oral assessment;
- current evaluation results;
- updated scope and risk assessment.

## Required Content

Your milestone document should include:

- what works now;
- how to run the proof of concept;
- what is simulated, mocked, or simplified;
- current evaluation results, even if weak;
- unresolved technical risks;
- updated project scope;
- concrete plan for the remaining six weeks;
- list of features moved to stretch goals.

## Project-Specific Expectations

Each project has its own proof-of-concept expectations. See the project brief for your assigned project in `project-documentation/projects/`.

General examples:

| Project Type | Minimum Convincing POC |
|---|---|
| Translation | One utterance enters the system, is translated, and is shown in a way that supports verification or refinement |
| Public health messenger | One question is answered from a trusted source and one comprehension signal is captured |
| Geospatial intelligence | One public health query triggers one verifiable spatial operation and displays evidence |
| Risk prediction | One valid dataset path trains or runs a baseline, generates predictions, and displays risk information |
| Medical assistant | One multilingual question goes through the interface, language/model pipeline, answer display, and speech-related path |

Dummy or small data is acceptable only if clearly identified. A convincing proof of concept makes clear what is real and what is simulated.

## Midterm Presentation

Your midterm presentation should be concise and demo-centered.

Suggested structure:

- problem and intended user;
- one-slide architecture;
- live or recorded demonstration;
- current evidence or sanity checks;
- main risks;
- scope decision for the rest of the semester.

The presentation should make it possible for staff to decide whether the project should continue as planned, be simplified, or replace a failing component.

## Rubric

| Criterion | Weight |
|---|---:|
| End-to-end vertical slice | 25% |
| Technical integration of core components | 20% |
| Evidence, evaluation, or sanity checks | 15% |
| UX and user-facing clarity | 10% |
| Handling of constraints, risks, and uncertainty | 10% |
| Updated scope and remaining work plan | 10% |
| Checkpoint communication and demo clarity | 10% |

## Common Problems

Avoid:

- showing only slides when a system should run;
- showing only a UI mock-up without the core pipeline;
- hiding that data is fake or simulated;
- presenting a model score without explaining the split or metric;
- postponing the central technical risk to the final weeks;
- keeping all originally planned features despite clear time constraints.
