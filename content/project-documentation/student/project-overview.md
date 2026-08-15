# Course Project Overview

The course project is a semester-long team project in which you will design, build, evaluate, and document an AI system for global health or humanitarian response.

The goal is not only to train a model or build an interface. We want to make you build a credible prototype of an AI system that could support decision making, communication, translation, risk analysis, or clinical work in a constrained and high-stakes setting.

See the [Project Briefs page](../projects/) for the available project descriptions.

## Project Philosophy

Your project will be evaluated through five recurring questions.

| Question | What It Means For Your Project |
|---|---|
| What **constraints** shape the setting? | Identify the technical, social, clinical, or operational limits that make the problem difficult. |
| Why should users **trust** the system? | Explain what makes the system reliable, transparent, useful, and safe enough for its intended users. |
| What **evidence** shows that it works? | Define how you will evaluate the system, what baseline or comparison matters, and what success means. |
| What changes at **larger scale**? | Consider what happens if the system reaches many people, responders, health workers, regions, or workflows. |
| What remains **uncertain**? | State what the system does not know, where it may fail, and how it communicates limitations or uncertainty. |

These questions should appear in your technical design, your proof of concept, and your final report.

### Note on AI use

This course is happening in late 2026. LLMs are a thing. Nowadays they are _rather_ good at coding.

You are allowed to use AI _responsibly_ to help you in the project. It can be a powerful tool for brainstorming, debugging, coding boring parts of the code faster (including tests and documentation, there is no longer an excuse not to write them!).

**Beware!** As of August 2026, LLMs still hallucinate and can still bring a lot of mess, excessively verbose code, when tests do not pass they may prefer making tests easier to pass than fix the actual code logic.

If you do choose to generate code with LLMs, carefully check it all manually. You should understand everything, be critical, replace slop with proper content, [be rude to your coding agent](https://arxiv.org/pdf/2510.04950).

__We will look for traces of detrimental AI slop in your submissions and penalize them. We think it's part of your engineering journey to learn how to make a smart use of AI in your work.__

## Project Timeline

Deadlines are set at 21:59. Students will choose on the first lecture whether to have deadlines on Fridays or Sundays.

| Date | Moment | Deliverable |
|---:|---|---|
| September 7 | Week 1 | Project descriptions and scopes released |
| September 20, 21:59 | Sunday of Week 2 | Group assignment finalized |
| September 25, 21:59 | Friday of Week 3 | Technical design and reproducible repository skeleton |
| November 4, 13:15 | Wednesday of Week 8 | Proof of concept: Oral presentations |
| November 6, 21:59 | Friday of Week 8 | Proof of concept: Submission |
| November 23-27 | Week 11 | 30-minute team checkpoint |
| December 16, 13:15 | Wednesday of Week 14 | Final presentations |
| January 8, 21:59 | 3 weeks after Final presentations | Final submission |

## Assessment

The project counts for 80% of the course grade.

| Component | % of the Project Grade |
|---|---:|
| Milestone 1: Technical Design and Reproducible Repository | 12.5% |
| Milestone 2: Proof Of Concept | 25% |
| Midterm oral presentation with live demo | 12.5% |
| Final presentation with a live demo | 12.5% |
| Final project report and code | 37.5% |

## Repository-Based Submission

All project submissions happen inside your team GitHub repository.

Staff will grant you the access for the one repository for your project in the [course GitHub organization](https://github.com/BiGHT-Course-Projects). The `main` branch will be protected. You will have to work through branches, pull requests, and peer review.

Your repository is both your software artifact and your submission record. Reports, milestone documents, presentation material, and final documentation should be committed to the repository.

## Required Technical Stack

All teams use the same baseline engineering stack.

| Area | Requirement |
|---|---|
| Language | Python |
| Environment | `uv` virtual environments |
| Package configuration | `pyproject.toml` |
| Formatting and linting | `ruff` |
| Type checking | `pyright` |
| Tests | `pytest` or an equivalent Python test runner approved by staff |
| Pre-commit hooks | Required |
| Continuous integration | Required for tests, linting, and type checks |
| Repository workflow | Pull requests into `main` (direct pushes discouraged) |

## Expected Final Output

By the end of the course, each team should submit:

- a working prototype;
- a reproducible code repository;
- tests, linting, type checks, pre-commit hooks, and CI;
- a final report submitted as a PDF inside the repository;
- one individual contribution report per team member;
- handover or maintenance documentation.

## What Counts As Success

A successful project does not need to solve the full real-world problem. It should instead make a well-scoped, technically credible, and well-evaluated contribution.

Strong projects usually have:

- a clear user and use case;
- a working vertical slice through the system;
- a realistic evaluation strategy;
- honest limitations and failure analysis;
- readable and reproducible code;
- evidence of collaboration through issues, pull requests, and reviews;
- a final demo that shows the system working, not just slides describing it.
