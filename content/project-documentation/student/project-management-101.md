# Project Management 101

Working in teams can be challenging. Here is a guide we provide you to help you manage your teams and (hopefully) go through less drama over the course of the semester.

A lot of things are covered, we encourage you to regularly check this guide throughout the semester to check tips that may get useful as you progress on the project.

Good project management in this course means keeping the project scoped, runnable, evaluated, and honestly documented while several people work on it at the same time.

## Start With The Brief

Find a time to meet, get to know each other and the project together before starting actual work. Read the project brief individually, make sure you understand it before meeting with your peers. This will make the following easier, better know what you will be talking about ;)

Agree on:

- the intended user;
- one core use case;
- the minimum convincing end-to-end proof of concept;
- what evidence will show that the system works;
- what is out of scope.

Do not turn the brief into a list of every possible feature. Choose the smallest useful system that addresses the central technical risk.

## Have The Team Conversation Early

During the first project meeting, explicitly discuss each team member's strengths, weaknesses, constraints (think of things that may compromise the time you spend on this project throughout the semester), why not learning goals too.

Useful questions:

- What have you already done: courses, data work, ML, backend, frontend, evaluation, writing in English (prompting an LLM to ask it to write your report is not what we are talking about for this one), presentations?
- What do you want to learn in this project?
- What made you choose this project?
- What kinds of tasks are you slow at or uncomfortable with?
- When are you usually available to meet / work together?
- What deadlines or external constraints should the team know about?

Use this conversation to split roles. Do not assign roles only based on who speaks first or who seems most confident.

## Cover The Core Responsibilities

Every team must cover these responsibilities. One person may cover several (there are more responsibilities than team members…), and roles can change during the semester.

| Responsibility | Main Job |
|---|---|
| Project coordination | Keep the scope / big picture in mind, meetings, GitHub issues, and deadlines under control. |
| Data | Find, clean, document, and track datasets, licenses, and provenance. |
| Model or algorithm | Build baselines, models, prompts, retrieval, inference, or reasoning modules. |
| Evaluation | Define metrics, splits, baselines, test cases, error analysis, and evidence. |
| Interface and demo | Build the user-facing path and keep the demo runnable. |
| Integration and reproducibility | Keep setup, CI, tests, configuration, and run instructions working. |

Do ensure to split evaluation and reproducibility: That's the best way to ensure the documentation is solid and the environment is actually reproducible, if reproducing results requires coordination with the person who did the evaluation, that's a signal the documentation lacks something.

## Build A Vertical Slice First

Your proof of concept should be a thin vertical slice: one meaningful path through the system that works end to end.

Examples:

- data sample -> baseline forecast -> simple dashboard;
- a few guideline documents -> retrieval -> grounded answer with sources;
- image input -> local model inference -> result screen;
- patient dialogue -> structured observations -> Bayesian update;
- speech input -> translation -> verification or correction workflow.

Avoid isolated work packages that only meet at the end. A weak integrated demo is more useful than five polished components that cannot run together.

## Work In Small Tasks

Use GitHub issues or a project board from Week 3 onward.

A good task has:

- one owner (you may work with several members on a specific task, but one person has to be held accountable for the completion of the task to avoid [diffusion of responsibility](https://en.wikipedia.org/wiki/Diffusion_of_responsibility));
- a clear output;
- a deadline;
- a link to a milestone or risk;
- a definition of successfully completed.

Bad task: `Work on model`.

Better task: `Add persistence baseline for DengAI weekly cases and report MAE on temporal split`.

## Use Pull Requests Early

Use pull requests throughout the semester, not only before deadlines.

A good pull request:

- solves one clear problem;
- explains what changed and why;
- includes tests or a reason why tests do not apply;
- passes formatting, linting, type checks, and tests;
- is small enough for a teammate to review seriously (absolute max 1,000 lines, aim for (way) less).

Assign PRs to a different team member for review, do not approve you own PRs.

Approving a PR means you read it and believe it is safe to merge. Do not approve because the deadline is close.

## Keep The Project Runnable

At least once per week, someone should check that the project runs from a fresh clone or a clean environment. This takes max 10 minutes of human effort and avoids stress close to the deadline. Do not always make the same teammate do this.

Run the Fresh Clone Health Check from the [Project Setup Guide](?step=3) to confirm the repository is healthy from a clean environment.

## Make Evaluation A Week 1 Topic

Define evaluation early, this will change (in a good way) your implementation decisions and avoid last minute changes.

Decide early:

- the baseline(s), what should your project be compared to;
- the metric or review criterion;
- the data split or test cases;
- what counts as a failure;
- how you will show uncertainty, limitations, or unsafe cases.

Each project needs evidence. A demo without evaluation is not enough.

## Plan Around Milestones

Use the course milestones as management checkpoints.

| Moment | Management Goal |
|---|---|
| Week 1-2 | Understand the brief, form the team, discuss strengths and weaknesses, choose roles. |
| Week 3 | Submit a scoped design, runnable repository skeleton, and initial task breakdown. |
| Week 8 | Demonstrate one vertical slice with current evaluation evidence. |
| Week 11 | Decide what will definitely be in the final demo and what should be cut. |
| Week 14 | Be able to present a live demo with a backup plan and show a flawless presentation. |
| Final submission | Submit reproducible code, report, contribution statement, and handover documentation. |

## Control Scope Deliberately

Use three categories:

- **Must have**: needed for the minimum convincing proof of concept.
- **Should have**: useful if the core system works early.
- **Stretch**: only attempted after the demo, evaluation, and reproducibility are stable.

Cut scope early when needed, better do a smaller but neatly made project than having weak parts.

## Keep A Decision Log

You may create a small file such as `docs/decision-log.md`.

Record decisions like:

- chosen core use case;
- datasets included or rejected;
- baseline model;
- evaluation split;
- API or UI contract;
- features cut from scope;
- known risks and fallbacks.

This will make the final report easier to write and help staff understand your tradeoffs.

## Define Interfaces Between People

Before working in parallel, agree on simple contracts.

Examples:

- data file schema;
- model input and output format;
- API endpoint request and response;
- UI fields expected from the backend;
- evaluation dataset format;
- configuration keys.

Write these contracts down. Most team delays come from hidden assumptions, not from hard algorithms.

Be open about your availability for communication, this can avoid unnecessary frustrations…

## Use AI Tools Carefully

AI coding assistants can help with boilerplate, tests, documentation, debugging, and first drafts.

They can also produce incorrect, verbose, overcomplicated, or untested code (ok, LLMs tend to do this one less often than humans).

Rules for AI-generated work:

- understand the code before merging it;
- run the checks;
- require teammate review;
- remove hallucinated APIs, fake assumptions, and unnecessary abstractions;
- do not weaken tests just to make them pass (current LLMs love to do this).

You are responsible for the code in your repository.

## Weekly Meeting Template

Keep weekly meetings short and concrete. The project coordinator should write an agenda and submit it to the rest of the team beforehand.

Suggested agenda:

```text
1. What changed since last week?
2. What works now in the repository?
3. What is blocked?
4. Which tasks can/must be merged this week?
5. What evidence or evaluation did we add?
6. What should we cut, defer, or ask staff about?
7. New external constraints?
```

End every meeting with tasks for the upcoming week, with owners and deadlines.

## Definition Of Done

A task is done when:

- the code or document is committed;
- the relevant checks pass;
- the README or docs are updated if needed;
- data, configuration, or assumptions are documented;
- a teammate has reviewed the change;
- the work can be reproduced by someone else.

If it only works on your laptop, it is not done.

## Common Failure Modes

Avoid:

- building only a notebook;
- building only a UI mock-up;
- postponing integration to the final weeks;
- reporting model scores without a baseline or valid split;
- having no owner for evaluation;
- committing undocumented data or outputs;
- using direct pushes instead of PRs;
- letting one person silently do all integration;
- writing a final report that claims more than the repository shows;
- preparing no backup for the live demo.

## Before Each Deadline

Ask:

- Can staff run the project from the repository?
- Is the current scope clear?
- Is the central technical risk addressed?
- Do we have evidence, even if imperfect?
- Are limitations and simulated parts explicit?
- Is every teammate's contribution visible through issues, PRs, reviews, commits, or documents?

If the answer is no, fix that before adding new features. The earlier this happens, the better.
