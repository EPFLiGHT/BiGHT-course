---
page_id: "Week_02"
page_title: "Week 2: Deciding Under Fire"
nav_title: "Week 2 - Deciding Under Fire"
sidebar_group: "Block I - Volatile Contexts"
order: 2
week: 2
lecture_date: "2026-09-16"
theme: "Deciding Under Fire"
context_lecture: "Deciding Under Fire: Triage, Uncertainty & Care"
slides_pdf: "slides/BiGHT-W2.pdf"
engineering_lecture: "Building for Broken Environments"
resource_1_label: "Mock Quiz (PDF)"
resource_1_file: "resources/mock_quiz.pdf"
---

## Overview

**Block I: Volatile Contexts** (Weeks 1-4)

**Central question:** When there is not enough time, information, or capacity to treat everyone, who should we help FIRST?

**Big idea:** Scarcity changes both care and engineering. In triage, the difficult question is not simply who is sickest. It is how to prioritize when urgency, benefit, time, and resources all matter, and what each decision makes unavailable to someone else (opportunity cost). In engineering, the same lesson applies: when a system may affect people in need, small workflow failures, hidden assumptions, and unreproducible outputs become accountability problems.

**Block focus:** Understand the environments in which AI must operate, and why technology often fails in humanitarian and clinical settings.

## Learning Objectives

After this lecture, you should be able to:

- Explain why triage is a decision under scarcity, not simply a rule for treating the sickest person first.
- Use the priority framing from the lecture to reason about urgency, benefit, time, and resources, and what each decision makes unavailable to someone else.
- Describe why referral chains, pre-positioning, pre-planning, and communication protocols matter during surge.
- Use triage categories (SALT, START, P-categories) and handover prompts (SOAP) to structure urgent clinical decisions.
- Explain why deterministic scaffolding—such as checklists—is relevant when complex decisions must be made under limited reasoning budget.
- Explain how everyday engineering choices create or prevent accountability failures.
- Apply the lecture's Git workflow expectations: protected `main`, semantic branches, pull requests, teammate review, meaningful commits, and no secrets or large artifacts in Git.
- Explain why reproducibility requires tracking dependencies, configuration, parameters, code, data assumptions, commands, and produced numbers.
- Recognize when a simple visualization or analysis is more useful than a polished but misleading summary.

## Context Lecture: Deciding Under Fire

The context lecture starts from a practical and ethical problem: a patient is someone who suffers and endures, and suffering is a function of time. Triage is the solution to scarcity: sorting and prioritizing patients according to assessed urgency. When there is not enough capacity, priority depends on several quantities at once:

```text
Priority = Urgency x Benefit / (Time x Resources)
```

This is not a formula to automate blindly. It is a way to make visible the tensions that already shape decisions: who needs help now, who is likely to benefit, how much time the decision takes, and how scarce the required resources are. Prioritizing one patient always has a cost elsewhere: what does this decision make unavailable to someone else (opportunity cost)?

Larrey's flying ambulances (1766-1842) show that triage was never only a bedside decision. The system had to decide what it was optimizing: severity, survival probability, return to duty, arrival order, or preserving resources for patients who appeared more salvageable.

The lecture then introduces standardized triage and clinical communication tools:

- **SALT:** Sort, Assess, Life-saving interventions, Treat/Transport.
- **START:** Simple Triage And Rapid Treatment, a context-agnostic system: it sorts patients the same way regardless of setting.
- **Expectant:** a category for a patient who is unlikely to survive given the available time and resources.
- **ABCDEG:** Airway, Breathing, Circulation, Disability, Exposure/environment, Glucose.
- **SBAR:** Situation, Background, Assessment, Recommendation/Request.
- **P-categories:** operational labels that follow from START: P0 (deceased), P1 (urgent and manageable given available resources), P2 (can wait, next up), P3 (walking wounded), and P4 (expectant, "left to die").
- **SOAP:** a structured handover prompt - Subjective, Objective, Assessment, Plan.

The lecture is explicit about what these tools are: more mnemonics, more checklists for basic things we already know, used as decision-making tools. Assessment and reassessment parameters matter because a patient's category can change as resources change.

The larger point is that care depends on systems. A referral chain links home or community care, clinics, primary care, district hospitals, regional or specialist hospitals, tertiary referral centres, and follow-up back home. Triage decisions must also be based on upstream pre-positioned resources. During surge, the question is not just how fast someone can be transported. It is where they should go, what capacity exists there, and what happens to other patients when the system is overloaded.

Pre-positioning is another system-level answer to scarcity. Supplies, kits, and response capacity often need to be prepared before a disaster. You cannot invent all capacity after the surge has already started. The lecture illustrates this with the UNICEF Supply Division (emergency warehouse in Copenhagen) and its menstrual hygiene kits shipped to emergencies.

Pre-planning also applies to reasoning, not only to supplies. Florence Nightingale, a self-taught statistician, demonstrated that rapid decisions do not rely on rapid statistics: she ran one of the first interventional before-and-after studies on the value of sanitation (deaths by cause before and after sanitation) as pre-positioned statistical reasoning. The larger lesson is that triage is based on assessment and reassessment according to available resources.

Rapid decisions are intricately complex. The lecture asks: how can AI help? The problem is complex decisions under a limited reasoning budget. The proposed solutions:

- **deterministic scaffolding** (fixed rules: same input, same output) such as checklists;
- **externalization of memory**, writing things down so they are not forgotten;
- **shared state**, through training and standardization;
- **adaptive reasoning**, delegating deeper thought to more capable systems or experts on the more difficult tasks.

Checklists appear simple, but the lecture frames them as a serious safety intervention. A good checklist:

1. protects against simple-but-preventable omissions;
2. creates a pause point;
3. turns individuals into a team.

The WHO Surgical Safety Checklist is the example used in the lecture, structured around sign in, time out, and sign out. Its value is not bureaucratic box-ticking. Its value is communication, synchronization, and respect for patients when attention is limited. Polls in the lecture invite reflection: do we really need checklists, and how would you use AI here?

## Engineering Lecture: Building for Broken Environments

The engineering lecture begins with accountability. In this course, engineering is not abstract. You are building systems for people in need, and your decisions may affect them immediately. That is why basic engineering discipline matters.

The Excel gene-name error example shows how small tooling assumptions can corrupt scientific work. Gene names such as `MARCH1` or `SEPT2` can be silently converted by spreadsheet software into dates. The problem was not just one file. Studies found these errors across many published supplementary files, and later work suggested the problem persisted or even worsened: a 2016 follow-up reported roughly 20% of papers with supplementary Excel gene lists affected, and a 2021 study reported the rate had risen to about 30%. The Human Gene Nomenclature Committee has since changed gene names to reduce autocorrect failures. The lesson is not only "do not use Excel." The lesson is that convenient tools can silently transform data, and workflows need checks before their outputs become evidence.

The Git section turns accountability into a workflow. Course projects must live in the BiGHT course GitHub organization, and the checklist is grade relevant:

- protect `main`; development happens on feature branches;
- give branches semantic names;
- put all changes through pull requests;
- have teammates review pull requests;
- never merge your own pull requests; this is a shared responsibility - empower your teammates to collaborate with you;
- write meaningful commit messages;
- keep datasets, model weights, checkpoints, `.env` files, and keys out of Git; write `.gitignore` from day 1.

Code hygiene is part of the same argument. A pull request with dozens of changed files and thousands of lines is not reviewable in a serious way. This is especially important when using AI coding agents, which can introduce formatting churn, vague comments, or meaningless back-and-forth edits. Your commits should be semantic: each change should be self-contained, justified, and documented.

Reproducibility asks a simple but uncomfortable question: if someone sees a number, a plot, or a model result, can they recover how it was produced? If patient-facing decisions depend on your numbers, this is not optional. At minimum, track the parameters, configuration, dependencies, code version, data assumptions, commands, and outputs that went into an experiment.

Different tools address different parts of this problem:

- lockfiles help make dependency versions explicit;
- configuration tools such as Hydra help track logic and settings;
- tracking and logging tools such as W&B can connect runs, parameters, outputs, and produced numbers.

The lecture's golden rule is: every number you produce must be reproducible. If a result cannot be reproduced, the compute was wasted.

The final part returns to simple analysis and visual storytelling. A p-value, slope, or fitted line can hide structure that a scatterplot immediately reveals. Spurious correlations are a reminder that polished numbers can still answer the wrong question. Often, simple tooling is enough: NumPy, pandas, Matplotlib, seaborn, scikit-learn, and `scipy.stats` can already take you far if you ask the right question and present the answer clearly.

## Key Terms

- **Patient:** from Latin `patiens`, one who suffers or endures.
- **Triage:** prioritizing care when need exceeds available time, information, staff, transport, beds, or resources.
- **SALT:** Sort, Assess, Life-saving interventions, Treat/Transport.
- **START:** Simple Triage And Rapid Treatment.
- **Expectant:** categorization for a patient unlikely to survive under the currently available time and resources.
- **ABCDEG:** Airway, Breathing, Circulation, Disability, Exposure/environment, Glucose.
- **SBAR:** Situation, Background, Assessment, Recommendation/Request.
- **P-category:** operational triage labels that follow from START - P0 (deceased), P1 (urgent, manageable given available resources), P2 (can wait, next up), P3 (walking wounded), P4 (expectant, "left to die").
- **SOAP:** Subjective, Objective, Assessment, Plan - a structured handover prompt.
- **Opportunity cost:** the benefit forgone when scarce resources go to one patient rather than another; what does this decision make unavailable to someone else?
- **Deterministic scaffolding:** fixed rules that map the same input to the same output; checklists are a common form in clinical and engineering contexts.
- **WHO Surgical Safety Checklist:** a short team checklist structured around sign in, time out, and sign out.
- **Semantic commit:** a commit whose message and contents clearly describe one meaningful, self-contained change.
- **Lockfile:** a file that records exact dependency versions so an environment can be reconstructed more reliably.
- **Hydra:** a configuration-management tool used to organize and reproduce experimental settings.
- **Tracking/logging:** recording commands, parameters, configurations, code versions, data assumptions, outputs, and metrics so results can be traced and reproduced.
- **W&B:** an example tool for experiment tracking and logging.

## Project Reflection

Use these questions to pressure-test your own project.

- What is the scarcest resource in your project context: data, time, staff attention, compute, trust, transport, or clinical capacity?
- What would your next decision make unavailable to someone else?
- What would break if your repository had to be run from a fresh clone today?
- Which number, chart, or model output in your project would be dangerous if it were not reproducible?
- Which checklist would prevent the most likely mistake your team could make this week?
- Which pull-request rule will matter most for your team: small PRs, semantic commits, teammate review, or keeping `main` protected?

## Further Reading

**Context**

- [WHO Surgical Safety Checklist](https://www.who.int/teams/integrated-health-services/quality-of-care-and-patient-safety/patient-safety-guidance-and-tools/safe-surgery/tool-and-resources).
- [Paediatric emergency triage, assessment and treatment (ETAT)](https://www.who.int/publications/i/item/9789241510219).
- [UNICEF Supply Division Warehouse Tour](https://www.youtube.com/watch?v=cc-h16sEwmU).
- [UNICEF menstrual hygiene products in emergencies](https://www.youtube.com/watch?v=Mv81Ml-KSHk).

**Engineering**

- [Mistaken identifiers: gene name errors can be introduced inadvertently when using Excel in bioinformatics](https://doi.org/10.1186/1471-2105-5-80) (Zeeberg et al., 2004).
- [Gene name errors are widespread in the scientific literature](https://doi.org/10.1186/s13059-016-1044-7) (Ziemann et al., _Genome Biology_ 2016).
- [Gene name errors: Lessons not learned](https://doi.org/10.1371/journal.pcbi.1008984) (Abeysooriya et al., _PLoS Computational Biology_ 2021).
- [Guidelines for human gene nomenclature](https://www.nature.com/articles/s41588-020-0669-3) (Bruford et al., _Nature Genetics_ 2020).
- [1,500 scientists lift the lid on reproducibility](https://doi.org/10.1038/533452a) (Baker, _Nature_ 2016).
- [Hydra documentation](https://hydra.cc/docs/intro/) for configuration management.
- [Weights & Biases documentation](https://docs.wandb.ai/) for experiment tracking.
- [Tyler Vigen's spurious correlations](https://www.tylervigen.com/spurious-correlations).
