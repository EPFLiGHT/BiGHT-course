---
page_id: "Week_06"
page_title: "Week 6: Reasoning Against Ourselves"
nav_title: "Week 6 - Reasoning Against Ourselves"
sidebar_group: "Block II - High-Stakes Decisions"
order: 6
week: 6
lecture_date: "2026-10-14"
theme: "Reasoning Against Ourselves"
context_lecture: "The Confident Fool: How Expertise Breeds Error"
slides_pdf: "slides/BiGHT-W6.pdf"
engineering_lecture: "Debiasing the Machine"
---

## Overview

**Block II: High-Stakes Decisions** (Weeks 5, 6, 8)

**Central question:** How do experts reliably deceive themselves, and can machines do better?

**Big idea:** Expertise improves clinical reasoning. It does not eliminate cognitive bias. Doctors can make mistakes despite strong medical knowledge. Language models can exhibit similar failures. Reliable systems need explicit uncertainty and structured reasoning.

**Block focus:** We examine how clinicians reason under uncertainty. We explore why diagnostic errors occur. We investigate whether AI can reduce these errors. We then develop principles for reliable clinical decision support.

## Learning Objectives

After this lecture you should be able to

- Explain how clinicians represent patient problems.
- Describe semantic qualifiers and illness scripts.
- Distinguish between System 1 and System 2 reasoning.
- Identify common cognitive biases in clinical diagnosis.
- Explain why expertise does not guarantee diagnostic accuracy.
- Understand the limitations of common debiasing strategies.
- Recognize similar reasoning failures in language models.
- Explain abductive reasoning and Bayesian inference.
- Describe belief updating and information seeking.
- Understand the importance of uncertainty and abstention.

## Core Ideas and Case Anchor

**Key concepts**

- Clinical reasoning and illness scripts
- System 1 and System 2 reasoning
- Cognitive biases in expert judgment
- Bayesian inference and belief updating
- Information gain and question selection
- Selective prediction and abstention

### Context Themes

- The development of clinical expertise.
- Semantic qualifiers and illness scripts.
- Kahneman and Tversky's research on cognitive biases.
- System 1 and System 2 reasoning.
- Anchoring and availability in clinical diagnosis.
- Framing and confirmation bias.
- Premature closure and search satisfaction.
- Diagnostic momentum and attribution errors.
- Overconfidence and diagnostic calibration.
- Structured reflection and cognitive debiasing.
- The role of medical knowledge in diagnostic accuracy.

### Engineering Themes

- The history of clinical decision support systems.
- Medical language models and diagnostic reasoning.
- Static benchmarks versus interactive clinical consultations.
- Cognitive biases in language models.
- Multimorbidity and multiple diagnostic hypotheses.
- Posterior updating using clinical evidence.
- Expected information gain for question selection.
- Selective prediction and abstention.

### Case Anchor 1. Anne Dodge

Anne Dodge experienced severe illness for fifteen years.
She continued losing weight despite substantial food intake.

Several physicians attributed her symptoms to eating disorders.
Previous diagnoses influenced subsequent clinical assessments.
Her condition remained unexplained for years.

Dr. Myron Falchuk eventually reconsidered these assumptions.
He listened to her history from the beginning.
He identified celiac disease.

The case illustrates several cognitive failure mechanisms.

- **Anchoring**
  Earlier diagnoses influenced later assessments.

- **Confirmation bias**
  New evidence was interpreted through existing assumptions.

- **Diagnostic momentum**
  Repeated diagnostic labels gained increasing authority.

- **Premature closure**
  Alternative explanations received insufficient consideration.

## Engineering Takeaways

- Maintain explicit probabilities over multiple diagnostic hypotheses.
- Select questions that reduce diagnostic uncertainty.
- Represent uncertain patient responses through soft evidence.
- Use calibrated abstention when evidence remains insufficient.
- Separate language understanding from probabilistic reasoning.
- Prevent AI from reinforcing cognitive biases.

## Project Reflection and Further Reading

### Reflection Questions

- How does your system represent patient information?
- What information might disappear during this transformation?
- Does your system maintain multiple diagnostic hypotheses?
- How does it select the next question?
- Can it detect insufficient evidence?
- When should it abstain from predicting?
- How does it communicate uncertainty?
- Could its recommendations reinforce existing clinical biases?
- How would you evaluate accuracy and coverage?
- Can clinicians inspect its reasoning process?

### Core Readings

**1. Jerome Groopman (2007)**

[How Doctors Think](https://books.google.com/books?vid=ISBN9780618610037)


**2. Amos Tversky and Daniel Kahneman (1974)**

[Judgment under Uncertainty: Heuristics and Biases](https://doi.org/10.1126/science.185.4157.1124)

Science 185(4157), 1124–1131.

**3. Pat Croskerry (2002)**

[Achieving Quality in Clinical Decision Making: Cognitive Strategies and Detection of Bias](https://doi.org/10.1111/j.1553-2712.2002.tb01574.x)

Academic Emergency Medicine 9(11), 1184–1204.

**4. Mark L. Graber, Nancy Franklin and Ruthanna Gordon (2005)**

[Diagnostic Error in Internal Medicine](https://doi.org/10.1001/archinte.165.13.1493)

Archives of Internal Medicine 165(13), 1493–1499.

### Additional Context Readings

**5. Henk G. Schmidt, Geoffrey R. Norman and Henny P. Boshuizen (1990)**

[A Cognitive Perspective on Medical Expertise: Theory and Implication](https://doi.org/10.1097/00001888-199010000-00001)

Academic Medicine 65(10), 611–621.

**6. Georges Bordage (1994)**

[Elaborated Knowledge: A Key to Successful Diagnostic Thinking](https://doi.org/10.1097/00001888-199411000-00004)

Academic Medicine 69(11), 883–885.

Discusses knowledge organization in clinical diagnostic reasoning.

**7. Hardeep Singh, Ashley N. D. Meyer and Eric J. Thomas (2014)**

[The Frequency of Diagnostic Errors in Outpatient Care: Estimations from Three Large Observational Studies Involving US Adult Populations](https://doi.org/10.1136/bmjqs-2013-002627)

BMJ Quality & Safety 23(9), 727–731.

**8. Kaveh G. Shojania and colleagues (2003)**

[Changes in Rates of Autopsy-Detected Diagnostic Errors Over Time: A Systematic Review](https://doi.org/10.1001/jama.289.21.2849)

JAMA 289(21), 2849–2856.

**9. Sílvia Mamede et. al (2010)**

[Effect of Availability Bias and Reflective Reasoning on Diagnostic Accuracy Among Internal Medicine Residents](https://doi.org/10.1001/jama.2010.1276)

JAMA 304(11), 1198–1203.

**10. Ashley N. D. Meyer et. al (2013)**

[Physicians' Diagnostic Accuracy, Confidence, and Resource Requests: A Vignette Study](https://doi.org/10.1001/jamainternmed.2013.10081)

JAMA Internal Medicine 173(21), 1952–1958.

**11. Geoffrey Norman et. al (2014)**

[The Etiology of Diagnostic Errors: A Controlled Trial of System 1 Versus System 2 Reasoning](https://doi.org/10.1097/ACM.0000000000000105)

Academic Medicine 89(2), 277–284.

**13. Jonathan Sherbino et. al (2014)**

[Ineffectiveness of Cognitive Forcing Strategies to Reduce Biases in Diagnostic Reasoning: A Controlled Trial](https://doi.org/10.2310/8000.2013.130860)

Canadian Journal of Emergency Medicine 16(1), 34–40.

**14. Sílvia Mamede et. al (2020)**

['Immunising' Physicians Against Availability Bias in Diagnostic Reasoning: A Randomised Controlled Experiment](https://doi.org/10.1136/bmjqs-2019-010079)

BMJ Quality & Safety 29(7), 550–559.


### Engineering Readings

**15. Robert S. Ledley and Lee B. Lusted (1959)**

[Reasoning Foundations of Medical Diagnosis; Symbolic Logic, Probability, and Value Theory Aid Our Understanding of How Physicians Reason](https://doi.org/10.1126/science.130.3366.9)

Science 130(3366), 9–21.


**16. Randolph A. Miller, Harry E. Pople and Jack D. Myers (1982)**

[Internist-I, an Experimental Computer-Based Diagnostic Consultant for General Internal Medicine](https://doi.org/10.1056/NEJM198208193070803)

New England Journal of Medicine 307(8), 468–476.


**17. Deepro Choudhury et. al (2026)**

[BED-LLM: Intelligent Information Gathering with LLMs and Bayesian Experimental Design](https://arxiv.org/abs/2508.21184)

International Conference on Learning Representations 2026.

**18. Yusuf Kesmen et. al (2026)**

[MoBayes: A Modular Bayesian Framework for Separating Reasoning from Language in Conversational Clinical Decision Support](https://arxiv.org/abs/2604.20022)

NeurIPS 2026.

**19. Yusuf Kesmen et. al (2026)**

[CLIMB: A Clinical Multimorbidity Benchmark for Diagnosing Co-occurring Conditions through Multiturn Conversations](https://arxiv.org/abs/2609.35462)

arXiv preprint.
