# Milestone 1: Technical Design

Deadline: Friday of Week 3, September 25, 21:59.

Weight: 5% of the course grade.

## Purpose

This milestone checks whether your project is well-scoped, technically feasible, and evaluable before you invest heavily in implementation.

The main goal is to make your assumptions explicit. Staff feedback will focus on scope, feasibility, evaluation validity, and whether the work can genuinely be divided across the team.

Your technical design should also address the five recurring project questions from the course overview: constraints, trust, evidence, scale, and uncertainty.

## Assigned Project

Your team is assigned one of the proposed course projects. Read the brief for your project in `project-documentation/projects/` before writing the design.

Your technical design must be consistent with your assigned project brief.

It should:

- commit to a small core use case from the brief rather than attempting all possible features;
- answer the brief's design questions in the relevant sections;
- target the brief's minimum convincing proof of concept;
- use the brief's evaluation ideas when defining your evaluation strategy.

## Submission

Submit inside your team repository.

Required file:

```text
docs/milestone-1-technical-design.md
```

Your repository should also contain an initial task breakdown, for example through GitHub issues or a project board.

## Required Content

Your technical design should include:

- exact problem statement;
- intended users and usage context;
- core use cases;
- connection to the assigned project brief's proof-of-concept expectation;
- non-goals;
- proposed system architecture;
- datasets, models, APIs, and external dependencies;
- evaluation strategy and success criteria;
- major risks and fallback plans;
- division of responsibilities;
- semester-level work plan (identify the strengths and weaknesses of each team member to split the work).

## Additional Requirements For ML Projects

All five course projects involve prediction, classification, ranking, generation, retrieval, or risk scoring. Include:

- prediction target or model objective;
- available data and data assumptions;
- train, validation, and test split strategy;
- baseline method;
- evaluation metric;
- expected failure modes;
- validity risks.

## Recommended Structure

```markdown
# Milestone 1: Technical Design

## Team

## Problem Statement

## Intended Users And Context

## Core Use Cases

## Non-Goals

## System Architecture

## Data, Models, APIs, And Dependencies

## Evaluation Strategy

## Risks And Fallback Plans

## Team Responsibilities

## Work Plan

```

## Rubric

| Criterion | Weight |
|---|---:|
| Problem framing and user/context understanding | 20% |
| System architecture and technical feasibility | 20% |
| Data, model, and dependency plan | 15% |
| Evaluation strategy and success criteria | 20% |
| Risks, fallback plans, and non-goals | 15% |
| Team organization and semester plan | 10% |

## Common Problems

Avoid:

- defining the project only as a list of features;
- attempting every feature in the project brief instead of committing to the core use case;
- proposing an architecture without an evaluation plan;
- assuming unavailable data will appear later;
- planning to build everything before testing anything;
- assigning all technical risk to the final weeks;
- describing users too vaguely;
- ignoring privacy, safety, or deployment constraints.
