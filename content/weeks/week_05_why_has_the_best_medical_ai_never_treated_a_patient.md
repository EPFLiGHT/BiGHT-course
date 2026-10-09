---
page_id: "Week_05"
page_title: "Week 5: Models Without Patients"
nav_title: "Week 5 - Models Without Patients"
sidebar_group: "Block II - High-Stakes Decisions"
order: 5
week: 5
lecture_date: "2026-10-07"
theme: "Models Without Patients"
context_lecture: "The Machine That Was Right and Was Never Used"
slides_pdf: "slides/BiGHT-W5.pdf"
engineering_lecture: "From Technological Implementation to Clinical Use"
---

## Overview

**Block II: High-Stakes Decisions** (Weeks 5, 6, 8)

**Central question:** When an algorithm is right, why might a clinician still be right not to use it?

**Big idea:** **Clinical performance is not clinical usefulness.** A model can outperform experts on clean cases and still harm patients in practice if it enters the wrong workflow, sees the wrong population, gives advice at the wrong time, or quietly shifts responsibility without anyone admitting it.

**Block focus:** Understand how clinicians make decisions under uncertainty and how AI can safely support human expertise.

This week starts Block II with an uncomfortable distinction: **being right on paper is not the same as improving care**. Medicine is not a benchmark table. Every recommendation enters a system of incomplete records, interruptions, liability, hierarchy, trust, and tired people. The final benchmark is not only "Was the answer correct?" It is: **Did care become safer, fairer, and better?**

## Learning Objectives

After this lecture, you should be able to:

- Explain why strong case-level performance does not guarantee clinical usefulness.
- Identify evaluation, workflow, liability, and local-validity gaps in clinical AI.
- Compare MYCIN, INTERNIST-1, HELP, UpToDate, and Watson for Oncology as different lessons in clinical decision support.
- Explain automation bias, algorithm aversion, alert fatigue, dataset shift, silent failure, and algorithmic friction.
- Translate clinician trust into engineering requirements: representative data, reliable recommendations, real-world validation, and safe integration.
- Reason about training-data mixture problems when small local or language-specific domains are underrepresented.
- Explain how RAG can reduce hallucination and knowledge cutoffs, and why retrieval design still matters.
- Treat output verification as a separate engineering problem, not a final cosmetic check.

## The Machine That Was Right and Was Never Used

MYCIN is the anchor case because it is not a story of a weak model. In a famous 1979 evaluation, infectious-disease experts judged MYCIN's therapy recommendations acceptable in 90.9% of cases. On carefully assembled case summaries, it performed at least comparably with expert physicians.

And yet: **MYCIN never treated a patient.**

That failure is the point. MYCIN was evaluated on a paper version of clinical work. Real clinical work contains missing and contradictory data, uncertain diagnoses, delayed lab results, changing patient status, competing priorities, interruptions, and patients who cannot follow the ideal plan. A model can be correct **conditional on clean inputs** and still be unsafe in the world that supplies dirty ones.

We use MYCIN to separate several gaps that are often collapsed into "the model works":

- **Evaluation gap:** the test case is cleaner than the clinical situation.
- **Workflow gap:** the recommendation must arrive to the right person, with the right information, in the right format, through the right channel, at the right time.
- **Liability gap:** clinical AI does not eliminate responsibility; it redistributes responsibility, often without making that redistribution explicit.
- **Local-validity gap:** a system trained or validated elsewhere may not remain valid in a new hospital, population, language, documentation style, or clinical practice.

Other systems make the contrast sharper. INTERNIST-1 showed that adding more medical knowledge can create an encyclopedic but unwieldy tool. HELP showed that integration matters: decision support works better when it lives inside care delivery. UpToDate is not usually called AI, but it may be one of the most successful clinical decision-support tools because it **supports professional agency** instead of pretending to replace judgment.

## What Fails Between Accuracy and Use

Clinical AI fails in predictable ways. The important vocabulary this week is not just technical; it is behavioral and organizational.

- **Automation bias:** accepting a computer recommendation too readily, even when it is wrong.
- **Algorithm aversion:** rejecting an algorithm after seeing a small error, often more harshly than a human error.
- **Alert fatigue:** training clinicians to ignore warnings because there are too many of them.
- **Calibration:** whether an 80% risk estimate really means roughly 80% risk in the population where it is used.
- **Dataset shift:** when the deployment world differs from the training world.
- **Algorithmic friction:** the extra work created by a tool: logins, data correction, documentation, overrides, and explanation.
- **Silent failure:** confident outputs continuing after the system's assumptions have become false.
- **Automation complacency:** human vigilance declining because the system is assumed to be watching.

For your projects, these are not abstract risks. They are design requirements. If your system adds friction, fires too many alerts, cannot explain uncertainty, or performs well only in a population unlike your users, it is not clinically useful yet.

## From Technological Implementation to Clinical Use

The engineering lecture uses IBM Watson for Oncology as the failure case. It looked impressive and was marketed at scale, but the core problems were familiar:

1. **Unrepresentative training data** and poor generalization across healthcare settings.
2. **Unreliable clinical recommendations**.
3. **Scaling before sufficient real-world validation**.

The inverse gives us a first design rule for clinical decision-support systems: earn clinician trust through representative data, reliable recommendations, and validation in the real setting before scaling.

We then make this concrete with an AI-powered medical assistant for health workers in Rwanda. Three engineering problems matter immediately:

- Is the underlying model well trained for the target setting?
- How do we reduce hallucination and knowledge cutoffs?
- How do we verify that answers are true and safe?

### Training-time problem: what the model learns depends on what it sees

If a model sees far more data from one domain than another, that domain dominates the parameter updates. In a mixed dataset with English medical QA, French medical QA, Kinyarwanda medical QA, Rwanda clinical guidelines, and general biomedical guidelines, simply concatenating everything will not make the model equally good at every target task.

The average loss can improve while the capabilities we actually care about improve slowly. **Average progress can hide local failure.** If Kinyarwanda clinical QA and code-switched QA are lagging, we should not celebrate only the global average. We should increase exposure to the source domains whose gradients help those target tasks.

The general cycle is:

```text
Train model -> Evaluate target tasks -> Calculate return on improvement -> Update target priorities -> Update training data mixture
```

The project lesson is simple: if your target users are local, multilingual, low-resource, or institution-specific, then "more data" is not enough. You must ask **which data help the target task**.

### Inference-time problem: knowledge is not guaranteed

Even a better-trained model can hallucinate or miss current knowledge. Retrieval-Augmented Generation (RAG) is one way to address this: retrieve relevant documents, then condition the answer on that evidence.

RAG can improve medical QA performance, but it is not magic. The corpus matters. The retrieval approach matters. The number of chunks matters. The position of useful chunks in the retrieved top-k matters. Retrieving more information can help up to a point, then introduce noise and hurt performance.

So the workflow is not "add RAG and trust the output." It is:

- choose the corpus deliberately;
- evaluate retrieval quality;
- test whether the retrieved context actually improves the target task;
- monitor when retrieval adds noise;
- show enough evidence that a clinician can understand where the recommendation came from.

### Output verification problem

Even after better training and retrieval, we still need to ask: **can we verify what the system actually says?** This is a separate layer. The answer may be fluent, retrieved, and still unsafe. Clinical-use engineering therefore includes checking claims against sources, detecting unsupported recommendations, surfacing uncertainty, and making it easy for a human to challenge or override the system.

## Key Terms

- **Clinical decision support system (CDSS):** software that helps clinicians make decisions by providing relevant information, alerts, recommendations, or references.
- **Evaluation gap:** the gap between clean test cases and messy clinical reality.
- **Workflow gap:** the gap between a correct recommendation and a recommendation that reaches the right person at the right time in the right form.
- **Liability gap:** uncertainty about who is responsible when a system's recommendation is followed, ignored, or deployed in the wrong setting.
- **Dataset shift:** a change between training/validation conditions and deployment conditions.
- **Calibration:** whether predicted probabilities match observed frequencies in the deployment population.
- **Automation bias:** over-trusting an automated recommendation.
- **Algorithm aversion:** rejecting an algorithm because it makes visible errors humans would also make.
- **Alert fatigue:** desensitization caused by too many warnings.
- **Algorithmic friction:** extra work imposed by a tool on the people expected to use it.
- **Silent failure:** continued confident output after the system's assumptions have stopped holding.
- **RAG:** retrieval-augmented generation, where a model answers using retrieved documents as context.
- **Output verification:** checking whether a generated answer is supported, safe, and appropriate before use.

## Project Reflection

Use these questions to pressure-test your own project.

- What would make a clinician or frontline worker right not to use your system, even if your model score is good?
- Which gap is most dangerous for your project: evaluation, workflow, liability, or local validity?
- What behavior would your tool ask users to change, and why should they accept that change?
- Is your training data mixture aligned with the users, languages, sites, and tasks you actually care about?
- If you use RAG, what corpus is allowed to ground answers, and how will you evaluate retrieval quality?
- What is your simplest real-world validation before scaling beyond one controlled setting?
- How will a human verify, challenge, or override your system's output?

## Further Reading

**Context**

- Shortliffe et al. [An artificial intelligence program to advise physicians regarding antimicrobial therapy](https://doi.org/10.1016/0002-9343(77)90027-3), *The American Journal of Medicine*, 1977.
- Miller. [A history of the INTERNIST-1 and Quick Medical Reference (QMR) computer-assisted diagnosis projects](https://doi.org/10.1111/j.1553-2712.1994.tb03403.x), *Academic Emergency Medicine*, 1994.
- Kuperman et al. [HELP: a dynamic hospital information system](https://doi.org/10.1016/1532-0464(91)90112-6), *Journal of Medical Systems*, 1991.
- Sutton et al. [An overview of clinical decision support systems: benefits, risks, and strategies for success](https://doi.org/10.1038/s41746-020-0221-y), *npj Digital Medicine*, 2020.

**Engineering**

- Case discussion: [The $4 billion AI failure of IBM Watson for Oncology](https://www.henricodolfing.ch/en/case-study-20-the-4-billion-ai-failure-of-ibm-watson-for-oncology/).
- Xiong et al. [Benchmarking Retrieval-Augmented Generation for Medicine](https://arxiv.org/abs/2402.13178), 2024.
- Lewis et al. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401), 2020.
- Sendak et al. [The human body is a black box: supporting clinical decision-making with deep learning](https://doi.org/10.1145/3173574.3173894), CHI, 2018.
