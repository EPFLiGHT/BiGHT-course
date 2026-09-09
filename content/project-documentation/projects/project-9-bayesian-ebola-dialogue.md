# Project 9: Bayesian Conversational System For Ebola Virus

Proposed team size: 3 students.

Project lead: Yusuf.

Keywords: Bayesian inference, Clinical Decision Support, Conversational AI, Data Curation, Explainable AI, LLMs, Natural Language Processing.

## Short Description

Curate and document the lab's Ebola dataset, then use it as the empirical knowledge base for a MoBayes style modular Bayesian dialogue system for Ebola triage.

## Motivation

Clinical conversational AI is risky when language generation and clinical reasoning are mixed together in an opaque way. In high-stakes Ebola triage, a system should be able to explain what evidence it has, what it still does not know, and why it asks the next question.

This project has two objectives. The first is data work: students will investigate the Ebola dataset available in the lab, reconstruct what each variable and label actually means, and produce a cleaned, well-documented dataset with a proper data card.

The second objective is to implement the MoBayes framework (Kesmen et al., arXiv:2604.20022) on top of this dataset, and make a user interface for it. MoBayes separates language from reasoning: the LLM acts only as a sensor and verbalizer, parsing patient conversation into structured observations, while a Bayesian module maintains an explicit posterior over conditions, selects the next question by expected information gain, and decides when to stop or defer using calibrated thresholds.

Students will evaluate the resulting system in terms of predictive performance, calibration, dialogue efficiency, and the accuracy with which the LLM extracts structured observations from patient conversations.

Reference: https://arxiv.org/abs/2604.20022

## Intended Users

Potential users include:

- clinicians or triage workers evaluating possible Ebola cases;
- outbreak response teams using structured symptom and exposure information;
- researchers studying interpretable clinical dialogue systems;
- data stewards documenting clinical or outbreak datasets;
- public health teams comparing transparent reasoning systems with generic LLM chatbots.

## Possible Features

Possible features include:

- data audit and cleaning workflow for the lab Ebola dataset;
- data dictionary and data card documenting variables, labels, provenance, and limitations;
- structured observation schema for symptoms, exposures, timing, and risk factors;
- LLM-based parsing of patient dialogue into structured observations;
- Bayesian inference module maintaining posterior probabilities over conditions or triage states;
- expected-information-gain question selection;
- calibrated stopping or deferral thresholds;
- user interface for patient conversation and reasoning inspection;
- natural-language verbalization of the current reasoning state;
- explanation view showing observations, posterior updates, and next-question rationale.

The team should avoid building a generic Ebola chatbot. The core of the project is the explicit separation between language processing and Bayesian clinical reasoning.

## Design Questions

Consider:

- What does each variable and label in the lab Ebola dataset actually mean?
- Which variables can be used as observations in a patient dialogue?
- What target conditions, triage states should the Bayesian module represent?
- How should the system handle missing, uncertain, contradictory, or ambiguous patient answers?
- What question should be asked next, and how is expected information gain computed?
- When should the system stop, provide a recommendation, ask for more information, or defer to a clinician?
- What interface makes the separation between conversation, extracted observations, and Bayesian reasoning visible?

## Technical Directions

Possible technical components include:

- dataset audit, cleaning, and documentation;
- data dictionary construction and data-card writing;
- structured observation extraction from dialogue using an LLM;
- modular Bayesian inference engine;
- expected-information-gain calculation for question selection;
- threshold-based stopping, deferral, or escalation policy;
- conversational interface that separates user dialogue from reasoning state;
- evaluation against scripted patient cases or held-out dataset records.

The system should make the Bayesian state inspectable. A reviewer should be able to see which observations changed the posterior and why the next question was selected.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one valid path from curated Ebola data to modular Bayesian dialogue.

Minimum convincing POC:

- the team produces a cleaned subset of the Ebola dataset with a clear data dictionary;
- the repository includes a data card describing provenance, variables, labels, missingness, and limitations;
- the Bayesian module maintains an explicit posterior over a clearly defined set of conditions or triage states;
- the system accepts at least one patient-style conversational input and converts it into structured observations;
- the system updates the posterior after each observation;
- the system selects at least one next question using an information-gain or uncertainty-reduction criterion;
- the system can decide to continue, stop, or defer using documented thresholds;
- the demo includes a user interface that explains the reasoning state in a way a technical reviewer can inspect.

## Evaluation Ideas

Possible evaluation approaches include:

- checking data documentation quality with a data-card rubric;
- validating variable meanings and labels with staff or domain experts where possible;
- measuring predictive performance and calibration;
- measuring dialogue efficiency, such as number of questions before stopping or deferral;
- measuring whether the selected next questions reduce uncertainty;
- testing robustness to missing, ambiguous, or contradictory patient answers;
- evaluating LLM observation extraction accuracy against manually labeled dialogue snippets;
- comparing explanations from the modular system with those from a generic clinical chatbot;
- analyzing calibration of stopping or deferral thresholds.

## Final Demo Target

The final demo should show a short Ebola triage conversation in which the system parses patient answers into structured observations, updates an explicit Bayesian posterior, chooses the next question using information gain, and explains why it continues, stops, or defers. The demo should also show the cleaned dataset documentation, data card, predictive performance, calibration, dialogue efficiency, and LLM extraction accuracy evidence that support the reasoning module.
