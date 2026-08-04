# Staff Grading Guide

This guide supports consistent grading across project milestones.

The rubrics are provisional. Staff should calibrate them before grading begins.

## Course Assessment

The table below mirrors the assessment structure in the course overview.

| Component | Weight | Project Documentation Mapping |
|---|---:|---|
| Project report and code, with final presentation with a live demo | 40% | Final submission |
| Initial submission: conception and reproducible base code | 10% | Technical design (5%) and reproducible project skeleton (5%) |
| Midterm checkpoint: technical project design | 20% | Proof of concept technical checkpoint |
| Midterm oral presentation with live demo | 10% | Week 8 oral presentation and live demo |
| In-class tests and quizzes, including ethics certification | 20% | Assessed outside the team repository |

## General Calibration Principles

Reward projects that:

- define a clear user and context;
- make technical risk visible early;
- use valid evaluation methods;
- are reproducible from a fresh clone;
- show working vertical integration;
- are honest about uncertainty and limitations;
- demonstrate real collaboration.

Penalize projects that:

- hide central technical risk behind UI polish;
- rely on unavailable data without a fallback plan;
- report metrics without a valid split or baseline;
- commit secrets or large files;
- cannot be run by staff;
- show little evidence of PR-based collaboration;
- treat ethical, safety, or privacy issues as generic boilerplate.

## Deadline State

For each graded milestone, assess the repository as it existed at the deadline time. Do not grade later commits, edited documents, rerun notebooks, regenerated outputs, or CI fixes unless the course team applies the late-submission policy.

Recommended process:

- identify the latest relevant commit before the deadline using GitHub commit and pull-request history;
- check CI runs associated with that commit, not only the latest CI run on the repository;
- if work was submitted through a pull request, use the PR state at the deadline;
- record the commit SHA, PR number, or release tag used for grading;
- mention in feedback when later changes were visible but not considered for the milestone grade.

## Milestone 1: Technical Design

Assessment weight: 5% of the course grade. This is the conception half of the 10% initial submission component.

| Criterion | Weight |
|---|---:|
| Problem framing and user/context understanding | 20% |
| System architecture and technical feasibility | 20% |
| Data, model, and dependency plan | 15% |
| Evaluation strategy and success criteria | 20% |
| Risks, fallback plans, and non-goals | 15% |
| Team organization and semester plan | 10% |

High-scoring submissions should identify the central technical risk and propose an evaluation strategy that could actually distinguish success from failure.

Warning signs:

- the design is mostly a feature list;
- the user is described only as "doctors" or "responders" without context;
- the evaluation plan says only "we will test accuracy";
- data availability is assumed but not checked;
- the scope is too broad for the team size;
- responsibilities are vague.

## Milestone 2: Reproducible Project Skeleton

Assessment weight: 5% of the course grade. This is the reproducible-base-code half of the 10% initial submission component.

Milestone 2 is a repository-state checkpoint. Students do not submit a separate milestone document for this checkpoint.

| Criterion | Weight |
|---|---:|
| Reproducible installation and execution | 20% |
| Repository structure and Python project organization | 15% |
| CI, pre-commit, linting, formatting, and type checks | 20% |
| Minimal executable pipeline | 15% |
| Tests and basic quality checks | 10% |
| Data/configuration handling and secret hygiene | 10% |
| PR workflow and team contribution evidence | 10% |

High-scoring submissions should be runnable by staff without private local knowledge.

Suggested staff checks:

- evaluate the repository state at the deadline commit or pull-request state;
- clone repository fresh;
- run `uv sync`;
- run pre-commit;
- run `ruff`, `pyright`, and tests;
- run the minimal pipeline;
- inspect CI history;
- inspect PRs and reviews;
- inspect whether one student is doing nearly all work.

Warning signs:

- checks only pass locally for one student;
- CI exists but is disabled or irrelevant;
- the minimal pipeline is described but not executable;
- `data/` contains large or suspicious files;
- secrets appear in code, notebooks, or configs;
- there are no meaningful PR reviews.

## Milestone 3: Proof Of Concept

Assessment weight: 20% of the course grade. This is the technical midterm checkpoint and is separate from the 10% midterm oral presentation with live demo.

| Criterion | Weight |
|---|---:|
| End-to-end vertical slice | 25% |
| Technical integration of core components | 20% |
| Evidence, evaluation, or sanity checks | 15% |
| UX and user-facing clarity | 10% |
| Handling of constraints, risks, and uncertainty | 10% |
| Updated scope and remaining work plan | 10% |
| Checkpoint communication and demo clarity | 10% |

High-scoring submissions should show one meaningful path through the system, even if simplified.

Warning signs:

- only independent components are shown;
- the central risk is still postponed;
- the demo hides which data or outputs are fake;
- model performance is reported without a credible evaluation setup;
- the remaining plan still includes all original features despite slow progress.

## Midterm Oral Presentation With Live Demo

This is a separate 10% assessment from the technical checkpoint repository grade.

<!-- TBD
| Criterion | Weight |
|---|---:|
| Demo-centered explanation of the technical design and proof of concept | 35% |
| Clarity about evidence, assumptions, risks, and scope decisions | 25% |
| Team participation and role clarity | 20% |
| Live responses and discussion with staff | 20% |
-->

High-scoring presentations should make it easy to understand what works, what remains uncertain, and what the team will change before the final submission.

## Final Submission

Assessment weight: 40% of the course grade.

| Criterion | Weight |
|---|---:|
| Working prototype and live demo | 20% |
| Technical implementation and integration | 20% |
| Evaluation, error analysis, and evidence quality | 20% |
| Reproducibility, CI, tests, and code quality | 15% |
| User/context fit, safety, ethics, and limitations | 10% |
| Final report and documentation | 10% |
| Presentation quality and contribution clarity | 5% |

High-scoring final submissions should be credible handover artifacts, not only class demos.

Suggested staff checks:

- verify final report is a PDF;
- verify report body respects the 5-page limit excluding references and appendices;
- verify one individual contribution report is present for each student;
- clone and run the documented setup;
- inspect demo path;
- inspect evaluation claims;
- inspect limitations and safety discussion;
- verify CI status near final submission.

## Contribution Concerns

If contribution patterns look uneven, staff can inspect:

- PR authorship;
- review participation;
- issue ownership;
- commit history;
- final individual contribution reports;
- presentation roles;
- checkpoint discussion.

The grading policy for unequal contribution should be decided by the course team before final grading.

## Feedback Style

Useful feedback should be specific and actionable.

Examples:

- "Your evaluation metric is not aligned with the public health decision. Define what a useful recommendation means."
- "The current POC is UI-only. For the next milestone, connect it to a real or simplified retrieval path."
- "Your CI runs tests but not type checks. Add `uv run pyright` to the workflow."
- "The report needs a clearer distinction between evidence, assumptions, and generated explanations."
