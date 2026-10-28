---
page_id: "Week_07"
page_title: "Week 7: The Fragility of Accuracy"
nav_title: "Week 7 - Fragility of Accuracy"
sidebar_group: "Block III - Trustworthy Evidence"
order: 7
week: 7
lecture_date: "2026-10-28"
theme: "The Fragility of Accuracy"
context_lecture: "How We Learned to Count What We Were Losing"
slides_pdf: "slides/BiGHT-W7.pdf"
engineering_lecture: "When 99% Accuracy Is Dangerous"
---

## Overview

**Block III: Trustworthy Evidence** (Weeks 7, 10-13)

**Central question:** What does it mean to trust a number?

**Big idea:** Why published performance can be misleading and what valid evaluation requires.

**Block focus:** Design, evaluate, and deploy AI systems that are safe, effective, and ready for real-world use.

## Learning Objectives

After this lecture, you should be able to:

- Explain why a single performance number can hide clinically important failure modes.
- Identify data leakage, missing uncertainty estimates, and subgroup failure in AI evaluation.
- Apply minimal best practice for reporting results: fixed seeds, repeated runs, and mean with standard deviation.
- Describe why evaluating LLM outputs is hard and how the evaluation protocol can change results and model rankings.
- Know the main medical AI reporting guidelines (TRIPOD+AI, TRIPOD-LLM, STARD-AI, DECIDE-AI, SPIRIT/CONSORT-AI).
- Interpret sensitivity, specificity, precision, AUROC, and AUPRC, and explain why accuracy fails for low-prevalence conditions.
- Distinguish discrimination from calibration and compute and interpret the Expected Calibration Error (ECE).
- Translate trustworthy evaluation into concrete reporting and engineering practices.

## Core Ideas and Case Anchor

**Key concepts**

- Data leakage and test-set contamination
- Statistical significance and uncertainty of results
- Evaluation of LLM outputs
- Subgroup disparities and intersectionality
- Reporting guidelines
- Measurement: construct, operationalization, measurement error
- Discrimination vs. calibration

**Context themes in this lecture**

- Reproducibility and overoptimism in ML research
- Reporting standards in medicine vs. machine learning
- Measurement theory from the social sciences

**Engineering themes in this lecture**

- Classification metrics beyond accuracy
- Threshold-independent comparison (AUROC, AUPRC)
- Calibration and its metrics (ECE, adaptive ECE, Brier score)

**Case anchor**

The anchor is a model that scores **99% accuracy but doesn't help anybody.** Take a disease that affects 1% of a population and a dummy model that always predicts "healthy." On 10,000 patients, it is right 9,900 times, so the accuracy is 99%. But its sensitivity is 0%. Every sick patient is sent home.

The same pattern appears in less obvious forms. A chest X-ray model with strong aggregate performance systematically labels some groups healthy when they are not: its false-positive rate for "no finding" (that is, underdiagnosis) is higher for female than male patients, and higher again for Hispanic female patients than white female patients. And a care-management algorithm can predict exactly what it was trained to predict, future care costs, and still fail patients, because cost was never the same thing as need.

## Engineering Takeaways

- **Report more than accuracy:** sensitivity, specificity, and precision at your chosen threshold; AUROC and AUPRC for threshold-free comparison; and a calibration measure (ECE or Brier score, ideally with a calibration plot) whenever users see probabilities. Report each as mean ± standard deviation over at least five runs.
- **Add a subgroup analysis:** break your error rates (especially the clinically dangerous one, such as missed cases) down by the subgroups relevant to your users, including intersections, and plan to repeat it after deployment.
- **Communicate so limitations are visible:** state the dataset, protocol, and population each claim holds for; show uncertainty; and follow the reporting guideline that matches your project's evaluation stage.

## Project Reflection and Further Reading

**Reflection questions**

- Which performance number in your project could be misleading, and what would a trivial baseline score on it?
- Could any form of leakage (shared pre-processing, duplicates, a reused test set, contaminated LLM training data) be inflating your results?
- Are the differences you report larger than the variation across runs and seeds?
- What subgroup, or intersection of subgroups, might expose a hidden failure?
- If you evaluate LLM outputs, does your protocol match how your users actually interact with the system?
- Will users act on your model's probabilities, and if so, how well calibrated is it?

**Further reading**

Optional:

- Kapoor and Narayanan. [Leakage and the reproducibility crisis in machine-learning-based science](https://doi.org/10.1016/j.patter.2023.100804), *Patterns*, 2023.
- Biderman et al. [Lessons from the Trenches on Reproducible Evaluation of Language Models](https://arxiv.org/abs/2405.14782), 2024.
- Röttger et al. [Political Compass or Spinning Arrow? Towards More Meaningful Evaluations for Values and Opinions in Large Language Models](https://arxiv.org/abs/2402.16786), ACL, 2024.
- Seyyed-Kalantari et al. [Underdiagnosis bias of artificial intelligence algorithms applied to chest radiographs in under-served patient populations](https://doi.org/10.1038/s41591-021-01595-0), *Nature Medicine*, 2021.
- Vasey et al. [Reporting guideline for the early-stage clinical evaluation of decision support systems driven by artificial intelligence: DECIDE-AI](https://doi.org/10.1038/s41591-022-01772-9), *Nature Medicine*, 2022.
- Collins et al. [TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods](https://doi.org/10.1136/bmj-2023-078378), *BMJ*, 2024.
- Jacobs and Wallach. [Measurement and Fairness](https://doi.org/10.1145/3442188.3445901), FAccT, 2021.
- Van Calster et al. [Evaluation of performance measures in predictive artificial intelligence models to support medical decisions: overview and guidance](https://doi.org/10.1016/j.landig.2025.100916), *The Lancet Digital Health*, 2025.