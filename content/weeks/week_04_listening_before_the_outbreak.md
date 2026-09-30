---
page_id: "Week_04"
page_title: "Week 4: Building at the Speed of Infection"
nav_title: "Week 4 - Building at the Speed of Infection"
sidebar_group: "Block I - Volatile Contexts"
order: 4
week: 4
lecture_date: "2026-09-30"
theme: "Building at the Speed of Infection"
context_lecture: "Ebola: Engineering Trust"
slides_pdf: "slides/BiGHT-W4.pdf"
engineering_lecture: "Listening to the World: Epidemic Intelligence at Scale"
---

## Overview

**Block I: Volatile Contexts** (Weeks 1-4)

**Central question:** How do we detect a catastrophe before it becomes one, convince others to act on it, and do so equitably?

**Big idea:** The fastest signal is not always the truest one. Epidemic intelligence is not just pattern detection. It is a series of choices about what counts as a signal, whose data count, whose absence is ignored, and what level of evidence is enough to act.

**Block focus:** Understand the environments in which AI must operate, and why technology often fails in humanitarian and clinical settings.

This week closes Block I by putting outbreak response and data engineering in the same frame. We use Ebola because it makes the stakes concrete: **the outbreak is not visible directly**. It appears through symptoms, rumors, contact histories, delayed reports, triage decisions, lab tests, maps, curves, genomes, and dashboards. The job of an intelligent system is **not to pretend those traces are reality**. It is to make their uncertainty visible enough that people can act responsibly.

## Learning Objectives

After this lecture, you should be able to:

- Explain why outbreak surveillance sees biased signals, not the epidemic directly.
- Describe why syndromic surveillance often prioritizes sensitivity over specificity.
- Reason about the trust consequences of delayed referral, triage, and care-seeking during an Ebola outbreak.
- Define epidemic intelligence as a pipeline: gather data, make it usable, analyze deviations, and support action.
- Distinguish event time from report time, and explain why the present is always incomplete.
- Use simple baselines, z-scores, EWMA, and CUSUM as first outbreak-detection tools before reaching for complex models.
- Explain why text signals require source-quality metadata and corroboration before alarm.
- Use Google Flu Trends as a cautionary example of proxy signals and overconfident big-data claims.

## Ebola: Engineering Trust

Ebola is a useful case because it exposes the gap between **biological reality** and **operational visibility**. A pathogen may be spreading before anyone knows what it is. Before confirmation, responders do not see a clean dataset. They see unexplained fevers, bleeding, sudden deaths, contact histories, rumors, fear, and uneven care-seeking.

That is why the language of reservoirs, zoonosis, spillover, fomites, intermediate hosts, vectors, and carriers matters. It is not just terminology. It reminds us that outbreaks are ecological, clinical, social, and institutional processes at the same time.

Syndromic surveillance makes the central tradeoff explicit. If we alert on broad signs such as fever unresponsive to usual treatment, bleeding, or sudden death, we **increase sensitivity**. We are less likely to miss a true case. But we also **reduce specificity**. We will send some non-cases into an already strained response system.

That tradeoff is **not a technical footnote**. Missing an Ebola case can be catastrophic. Over-referring can also create harm: fear, stigma, overload, distrust, and avoidance of care. A triage score, such as the malaria-sensitive Ebola score used in Sierra Leone, is therefore not "the answer." It is a disciplined way to **make uncertainty explicit** while decisions still have to be made.

The **trust problem** is just as important as the **classification problem**. If people see that patients who go to an Ebola treatment facility often die, they may infer that the facility is dangerous and stay home. Statistically, that association may be confounded by late referral and severe disease. Socially, the reaction is understandable. For AI systems, the lesson is direct: **a correct alert can still fail** if it arrives too late, is not trusted, or cannot be connected to action people understand.

## Listening to the World

We frame epidemic intelligence as a pipeline:

```text
Gather data and make it usable -> Analyze data -> Take action
```

Each arrow hides hard work. Local reports may be **sparse, delayed, political, or produced from areas affected by conflict**. Observations must be grouped by time and place. Analysis has to estimate what would normally happen, adjust for delay and noise, and detect deviations. Action requires **communicating uncertainty** to people who must decide whether to investigate, warn, or intervene.

The most important engineering principle is this: **we do not see the epidemic, only biased signals**. Infection may not produce symptoms. Symptoms may not lead to care-seeking. Care-seeking may not lead to testing. Testing may not be reported quickly. Every step introduces selection bias, measurement bias, or reporting delay.

For that reason, **every signal needs metadata** for reminding relevant context elements:

- **event time:** when the underlying event happened;
- **report time:** when it became visible to the system;
- **location:** where the signal applies;
- **specificity:** how strongly it points to the event of interest;
- **source quality:** how much trust the source deserves.

Early warning starts with a **baseline**: what did we expect if nothing unusual was happening? A first detector can be as simple as a rolling mean and standard deviation followed by a z-score. **EWMA** and **CUSUM** are useful next steps because they react to gradual or persistent deviations. These methods are not glamorous, but they are the right standard to beat. **If a complex model cannot outperform a transparent detector, it has not earned its complexity.**

Text can also be a signal: school absenteeism, pharmacy reports, emergency-department waits, news articles, or social media posts. NLP can help filter relevant text, classify documents, and extract locations, dates, symptoms, and diseases. But the workflow is **not** "send everything to an LLM and trust the answer." **Source quality and corroboration come first.** A signal should become stronger when independent sources agree across places, modalities, or institutions.

**Google Flu Trends** is the failure case to keep in mind. Search queries were fast and geographically detailed, but **searching for symptoms is not the same as being sick**. Media attention, fear, platform behavior, and changing search habits all changed the proxy. The lesson is not that proxies are useless. The lesson is that proxies need **humility, recalibration, source awareness, and corroboration**.

## Key Terms

- **Syndromic surveillance:** surveillance based on symptoms or broad clinical patterns before laboratory confirmation.
- **Sensitivity:** ability to detect true cases; prioritizing sensitivity reduces missed cases but can increase false alarms.
- **Specificity:** ability to exclude non-cases; prioritizing specificity reduces false alarms but can miss true cases.
- **Epidemic intelligence:** gathering, filtering, analyzing, corroborating, and communicating signals that may indicate an outbreak.
- **Event time:** when the underlying event occurred.
- **Report time:** when the event became visible in a data stream.
- **Baseline:** expected behavior if nothing unusual is happening.
- **Z-score:** standardized deviation from expected behavior.
- **EWMA:** exponentially weighted moving average, useful for gradual increases.
- **CUSUM:** cumulative sum, useful for persistent small deviations.
- **NER:** named entity recognition; extraction of locations, dates, symptoms, diseases, and other structured information from text.
- **Corroboration:** confirming the evidence we have is strong. In our case, better do it before escalating it into an alert.
- **Proxy signal:** an indirect measurement that may correlate with disease activity but is not the disease itself.

## Project Reflection

Use these questions to pressure-test your own project.

- What signal does your system observe directly, and what real-world event are you hoping it represents?
- Where can selection bias, measurement bias, or reporting delay enter your pipeline?
- What is the simplest baseline your model must beat before it deserves to be more complex?
- Which source in your project is fastest, and which source is most trustworthy? Are they the same?
- What would you require as corroboration before recommending action?
- What would your dashboard hide if the most affected people were absent from the data?

## Further Reading

**Context**

- Peter Piot, *No Time to Lose: A Life in Pursuit of Deadly Viruses*.
- Bermejo et al. [Ebola outbreak killed 5000 gorillas](https://doi.org/10.1126/science.1133105), *Science*, 2006.
- Hartley et al. [Predicting Ebola infection: A malaria-sensitive triage score for Ebola virus disease](https://doi.org/10.1371/journal.pntd.0005356), *PLOS Neglected Tropical Diseases*, 2017.
- WHO, [Ebola disease fact sheet](https://www.who.int/news-room/fact-sheets/detail/ebola-virus-disease).

**Engineering**

- Swiss Federal Office of Public Health, [Influenza statistics](https://www.idd.bag.admin.ch/en/diseases/influenza/statistic).
- Lazer et al. [The Parable of Google Flu: Traps in Big Data Analysis](https://doi.org/10.1126/science.1248506), *Science*, 2014.
- Wikipedia, [Google Flu Trends](https://en.wikipedia.org/wiki/Google_Flu_Trends).
- ProMED, [International Society for Infectious Diseases](https://promedmail.org/).
