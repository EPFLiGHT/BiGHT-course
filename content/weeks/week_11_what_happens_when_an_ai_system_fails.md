---
page_id: "Week_11"
page_title: "Week 11: Designing for Failure"
nav_title: "Week 11 - Designing for Failure"
sidebar_group: "Block III - Trustworthy Evidence"
order: 11
week: 11
lecture_date: "2026-11-25"
theme: "Designing for Failure"
context_lecture: "Proven ≠ Trustworthy or Ethical"
slides_pdf: "slides/BiGHT-W11.pdf"
engineering_lecture: "Uncertainty as Architecture"
---

## Overview

**Block III: Trustworthy Evidence** (Weeks 7, 10-13)

**Central question:** When is it ethical to run a trial, and when can we trust its result?

**Big idea:** **Proven is not the same as trustworthy, or ethical.** Last week, we saw that plausible is not proven. This week, we ask whether a trial was fair to its participants, whether chance or bias could explain its result, and what all the evidence says together. Then we carry the same question into our systems: when should a model act, and when should it know that it does not know?

**Block focus:** Design, evaluate, and deploy AI systems that are safe, effective, and ready for real-world use.

## Learning Objectives

After this lecture, you should be able to:

- Explain informed consent, clinical equipoise, and independent oversight, and the failures that made each one necessary.
- Describe how randomization, allocation concealment, blinding, and prespecified outcomes protect a trial against bias.
- Read a systematic review and a forest plot, and recognize publication bias and heterogeneity.
- Explain why randomizing treatment is not the same as a random train/test split.
- Distinguish aleatoric from epistemic uncertainty and explain why RL-trained LLMs tend to be overconfident.
- Name the main types of distribution shift and explain how to detect them after deployment without labels.

## Proven ≠ Trustworthy, or Ethical

**Protect: is the trial fair to the people in it?**

- **Informed consent:** people understand what taking part involves and freely choose whether to join. The Nuremberg Code (1947) and the Declaration of Helsinki (1964) were written in response to abuse. Yet in Tuskegee, penicillin was withheld from Black men with syphilis for decades, and in Guatemala, at least 1,308 people were exposed to sexually transmitted infections without consent.
- **Clinical equipoise:** informed experts genuinely disagree about which option is better *for these patients*. Equipoise depends on the comparator. The Bangkok zidovudine trial compared a short course against placebo (9.4% vs 18.9% of infants infected) when a proven longer regimen existed elsewhere. FEAST asked whether children in shock should receive a fluid bolus, a practice everyone believed in. The trial stopped early: mortality was 10.6% with an albumin bolus and 10.5% with saline, versus 7.3% without.
- **Independent oversight:** someone must check the protocol before recruitment and review emerging harms. Thalidomide was marketed as safe in pregnancy without trials. More than 10,000 children were affected. In the US, FDA reviewer Frances Kelsey kept asking for better safety evidence, and the drug was never approved there.

**Design: could chance or bias explain the result?**

- **Randomization** lets chance decide who gets which care. Simple, blocked, and stratified schemes trade unpredictability against balance. **Allocation concealment** keeps the next assignment hidden until enrolment is irreversible; otherwise recruiters can choose who enters next.
- **Blinding** hides assignments from anyone whose knowledge could influence care or outcome assessment. Say exactly who was masked: "double-blind" is ambiguous.
- **Outcomes** must be decided in advance and must matter to patients. In CAST, drugs that suppressed abnormal heartbeats after a heart attack *increased* mortality (7.7% vs 3.0% on placebo). Improving a surrogate is not the same as saving lives.

**Weigh: what does all the evidence say, taken together?**

A **systematic review** searches for every study on a question, using rules written down in advance (registered on PROSPERO, reported with PRISMA). A **meta-analysis** pools their estimates. It can find effects too small for any single trial, catch harms early, and show when one more trial is one too many. Two classic traps:

- **Publication bias:** if only "heads" results get published, a perfect search still finds a biased coin.
- **Heterogeneity:** head in the oven, feet in the freezer, and the average temperature is comfortable. Pooling different effects can hide harm in one group.

**For AI, published is not proven in patients.** Tens of thousands of AI-in-health papers appear every year, but only 86 randomized trials of AI in clinical practice were published between 2018 and 2023. The ones that exist show what to measure:

- **EAGLE** randomized 120 clinical teams to see AI-flagged ECGs or not: more new diagnoses of weak heart pumping (2.1% vs 1.6%), but no demonstrated survival benefit.
- **Manz et al.** combined mortality predictions with clinician prompts: documented serious-illness conversations rose from 3.4% to 13.5%, and therapy near death fell from 10.4% to 7.5%; other outcomes did not clearly improve.
- **Downing et al.** found no difference in antibiotic orders between an active and a silent sepsis alert. The trial stopped at 1,123 of 3,000 planned patients, and **a null result is not proof of equivalence.**

Finally: **randomizing treatment is not a train/test split.** Random allocation makes groups comparable before care is assigned. A random split of observational records preserves whatever confounding was already there.

## Uncertainty as Architecture

Failure is an expected state, so we design for it. A clinical decision support system should **estimate** a prediction with an uncertainty signal, **detect** inputs unlike its training data, **decide** whether to act or abstain, **monitor** all outputs, and **recover** by recalibrating or updating the model. Most of these steps are still open research questions.

**Use simple models where possible.** Small models can be very effective on well-defined tasks, and uncertainty estimation and out-of-distribution (OOD) detection are much easier with them. Resist the general push to scale.

**Know where uncertainty comes from.** *Aleatoric* uncertainty is intrinsic randomness. *Epistemic* uncertainty is lack of knowledge, which more data or better models can reduce. A model is **calibrated** when its predicted probabilities match observed frequencies (see Week 7).

**LLMs trained with reinforcement learning tend to be overconfident.** With verifiable rewards (RLVR), a lucky guess earns the same reward as a confident correct answer, and "I don't know" is penalized like a wrong answer. Two recent responses:

- **RLCR** adds a Brier score term to the reward so that the model learns to report calibrated confidence. A Brier term alone can be gamed: the model learns to give wrong answers with 0% confidence.
- **UMPIRE** is a training-free measure for multimodal models: sample several responses, and treat high diversity as a sign of uncertainty.

Neither reports subgroup analyses. In low-resource settings, a model may be more uncertain, or more confidently wrong, for underrepresented populations. Optimizing aggregate calibration alone can hide this.

**Expect the deployment data to differ.** ML research speaks of out-of-distribution or out-of-domain data. Medical research distinguishes:

- **Subgroup shift:** the mix of patients changes (not necessarily OOD).
- **Population shift:** for example, a university hospital versus a rural clinic.
- **Time shift:** for example, new imaging equipment.
- **Drift:** the data-generating process changes continuously during deployment.

Regulators require **post-market surveillance** of medical devices. The difficulty is detecting shift *without labels*, because outcomes often arrive too late. Shift detection can be framed as a hypothesis test, H₀: P = Q, comparing validation data P with deployment data Q. Fixes such as transfer learning or continual learning must avoid **catastrophic forgetting**.

## Key Terms

- **Informed consent:** understanding what taking part involves and freely choosing whether to join.
- **Clinical equipoise:** genuine expert disagreement about which option offers patients the better balance of benefits and harms.
- **Allocation concealment:** keeping the next assignment hidden until enrolment is irreversible.
- **Surrogate outcome:** a measurement used in place of an outcome patients care about.
- **Publication bias:** studies with unfavourable or null results are less likely to be published.
- **Heterogeneity:** variation in true effects across studies or groups.
- **Aleatoric / epistemic uncertainty:** irreducible randomness / reducible lack of knowledge.
- **Distribution shift:** a difference between the data a model was validated on and the data it meets in deployment.

## Project Reflection

- If your system were evaluated in a trial, what would the comparator be, and would informed experts consider it fair?
- Is your main outcome one that patients care about, or a surrogate?
- How does your system know when it should not answer, and what happens then?
- Which shift (subgroup, population, time) is most likely between your data and your deployment setting, and how would you detect it without labels?
- Who would be more uncertain, or more confidently wrong, under your model?

## Further Reading

- Maitland et al., [Mortality after Fluid Bolus in African Children with Severe Infection (FEAST)](https://doi.org/10.1056/NEJMoa1101549), *NEJM*, 2011. A widely accepted practice overturned by a trial run where the question mattered most.
- Sunday Times Insight Team, *Suffer the Children: The Story of Thalidomide*, 1979. Why independent oversight and drug regulation exist.
- Han et al., [Randomised controlled trials evaluating artificial intelligence in clinical practice: a scoping review](https://doi.org/10.1016/S2589-7500(24)00047-5), *The Lancet Digital Health*, 2024. How few AI systems have been tested in trials, and what those trials measured.
- Yao et al., [Artificial intelligence–enabled electrocardiograms for identification of patients with low ejection fraction: a pragmatic, randomized clinical trial (EAGLE)](https://doi.org/10.1038/s41591-021-01335-4), *Nature Medicine*, 2021.
- Manz et al., [Long-term Effect of Machine Learning–Triggered Behavioral Nudges on Serious Illness Conversations and End-of-Life Outcomes Among Patients With Cancer](https://doi.org/10.1001/jamaoncol.2022.6303), *JAMA Oncology*, 2023.
- Pavlovic, [Understanding Model Calibration](https://iclr-blogposts.github.io/2025/blog/calibration/), ICLR Blogposts, 2025. A visual introduction to calibration and the limits of ECE.
- Damani, Puri et al., [Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty](https://arxiv.org/abs/2507.16806), ICLR, 2026.
- Lau, Dao et al., [Uncertainty Quantification for Multimodal Large Language Models with Incoherence-adjusted Semantic Volume](https://arxiv.org/abs/2602.24195), NeurIPS, 2026.
- Subasri et al., [Detecting and Remediating Harmful Data Shifts for the Responsible Deployment of Clinical AI Models](https://doi.org/10.1001/jamanetworkopen.2025.13685), *JAMA Network Open*, 2025.
- Koch, Baumgartner, and Berens, [Distribution shift detection for the postmarket surveillance of medical AI algorithms: a retrospective simulation study](https://doi.org/10.1038/s41746-024-01085-w), *npj Digital Medicine*, 2024.
