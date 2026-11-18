---
page_id: "Week_10"
page_title: "Week 10: Causal Evidence in Practice"
nav_title: "Week 10 - Causal Evidence in Practice"
sidebar_group: "Block III - Trustworthy Evidence"
order: 10
week: 10
lecture_date: "2026-11-18"
theme: "Causal Evidence in Practice"
context_lecture: "Plausible ≠ Proven"
slides_pdf: "slides/BiGHT-W10.pdf"
engineering_lecture: "Causal Inference"
---

## Overview

**Block III: Trustworthy Evidence** (Weeks 7, 10-13)

**Central question:** If it makes sense and everyone believes it, why test it?

**Big idea:** **Plausible is not proven.** A treatment can make biological sense, be recommended in guidelines, and still harm patients. To claim that an intervention works, we need to compare what happened with what would have happened without it.

**Block focus:** Design, evaluate, and deploy AI systems that are safe, effective, and ready for real-world use.

## Learning Objectives

After this lecture, you should be able to:

- Distinguish association from causation, and prediction from intervention effect.
- Recognize confounding and Simpson's paradox in health data.
- Name the main observational and interventional study designs and the typical failure of each.
- Report effects in both relative and absolute terms (risk ratio, risk difference, NNT).
- Draw a causal graph and use the backdoor criterion to choose an adjustment set, avoiding mediators and colliders.
- Estimate an average treatment effect with g-computation or inverse probability weighting.

## Plausible ≠ Proven

Some treatments became standard care because they were obviously beneficial, until someone tested them:

- **Oxygen for premature babies:** generous oxygen was routine in the 1940s. A 1953 randomized trial showed that restricting it cut retinal disease from 23% to 7%. Routine care had been blinding thousands of babies.
- **Radical mastectomy:** the NSABP B-04 trial found no survival advantage over less extensive surgery after 25 years.
- **Steroids for head injury:** the CRASH trial (10,008 patients, 49 countries) was stopped early: 21% of patients died on steroids versus 18% on placebo.

So, before saying "obviously beneficial", ask: **says who, for whom, based on what?**

**Seeing is not doing.** Two things happening together (association) does not mean that changing one changes the other (causation). A **confounder** is a common cause of exposure and outcome: a night of drinking explains both sleeping with shoes on and waking with a headache. Confounding can even reverse a conclusion. In the kidney-stone example, open surgery did better for small stones *and* for large stones, but worse overall, because it received most of the hard, large stones (**Simpson's paradox**).

Every study design has a typical way of failing:

| Design | Useful for | Typical failure |
|---|---|---|
| Case series | Spotting something new (Los Angeles, 1981) | No control group (the retracted MMR–autism paper) |
| Cross-sectional | Prevalence at one point in time (Geneva seroprevalence, 2020) | Unclear temporal order |
| Ecological | Group-level patterns | Ecological fallacy (chocolate and Nobel prizes) |
| Case-control | Rare outcomes (Doll & Hill, 1950) | Recall bias |
| Cohort | Following exposure to outcome (British Doctors Study) | Confounding (hormone therapy looked protective, RR 0.61; the trial found harm, HR 1.29) |
| Before-and-after | Large, fast effects (Semmelweis, 1847) | No concurrent control (the umbrella that "stops the rain") |
| Non-randomized controlled trial | Comparing treatments (Lind's scurvy trial, 1747) | Selection bias (new boots for the best players) |
| Randomized trial | Fair comparison (Salk polio vaccine, 1954) | Ethics, feasibility, and relevance (the parachute trial jumped from 0.6 m) |

When randomization is impossible, the **Bradford Hill considerations** (strength, consistency, temporality, dose–response, plausibility, and others) help weigh observational evidence. None of them is proof on its own.

Report effect sizes in **both relative and absolute terms**, and always state the follow-up period. The Salk trial can be summarized as "71% fewer cases" or as "4 fewer cases per 10,000 children in one season" (about 2,500 children vaccinated per case prevented). Both are correct; they lead readers to different conclusions.

For AI, the unit to evaluate is the **whole clinical intervention**: risk model → clinician response → patient outcome. Predictive accuracy measures something else.

## Causal Inference

Suppose we built an SMS support programme for people on HIV treatment. Does it work? The [WelTel Kenya1 trial](https://doi.org/10.1016/S0140-6736(10)61997-6) answered this for weekly SMS check-ins by randomizing patients to SMS support plus usual care or usual care alone. Randomization was ethical because of **equipoise**: genuine uncertainty about which option is better, with both groups receiving HIV treatment.

Often you simply cannot randomize. Sometimes you find a **natural experiment**: in Japan, retailer lotteries decided who could buy a game console, letting [Egami et al.](https://doi.org/10.1038/s41562-024-01948-y) estimate the effect of console ownership on well-being. Most of the time, though, you only have observational data, and patients chose whether to enrol.

The target is the **average treatment effect**, ATE = E[Y¹] − E[Y⁰]: the difference between outcomes under enrolment and without it. We only ever observe one of those outcomes per patient. Comparing enrolled with non-enrolled patients mixes the effect of the programme with the effect of whatever made people enrol, such as motivation.

**Draw the causal graph first**, then decide what to adjust for:

- **Confounder** (A ← M → Y): adjust for it. Compare patients with the same motivation, then average over the population.
- **Mediator** (A → D → Y): do not adjust. Conditioning on adherence blocks the mechanism you want to measure.
- **Collider** (A → F ← S → Y): do not adjust. Conditioning on a common effect, such as attending a follow-up visit, *opens* a spurious path.

The **backdoor criterion** gives a sufficient rule: choose an adjustment set Z that contains no descendant of the treatment and blocks every path into the treatment. Then

P(Y=1 | do(A=a)) = Σ<sub>z</sub> P(Y=1 | A=a, Z=z) P(Z=z).

Two standard ways to estimate it:

- **G-computation:** fit an outcome model μ̂(a, z), predict each patient's outcome with and without enrolment, then average the difference.
- **Inverse probability weighting:** model the probability of enrolment (the **propensity score**) and weight each patient by the inverse probability of the treatment they actually received. In the lecture example, this shrinks the naive 17.6-point difference to 10 points once motivation is balanced.

Both are only as good as the adjustment set. **Good predictions do not establish a causal effect.**

## Key Terms

- **Confounder:** a common cause of exposure and outcome.
- **Simpson's paradox:** a pattern within every subgroup that reverses when the groups are combined.
- **Counterfactual:** the outcome that would have occurred under the alternative strategy.
- **Number needed to treat (NNT):** 1 ÷ risk difference, for a stated follow-up period.
- **Equipoise:** genuine uncertainty about which option is better; the ethical basis for randomizing.
- **Mediator:** a variable on the causal path from treatment to outcome.
- **Collider:** a variable caused by two others on a path; conditioning on it opens the path.
- **Propensity score:** the probability of receiving the treatment given baseline variables, e(z) = P(A=1 | Z=z).

## Project Reflection

- What does your system actually change: a prediction, a clinician's action, or a patient outcome?
- What would have happened without your system, and how could you estimate that?
- Draw the causal graph for your main claim. Which variables are confounders, mediators, or colliders?
- Is there a natural experiment, staggered rollout, or randomization opportunity you could use?
- Would you report your effect as a relative change, an absolute change, or both?

## Further Reading

- Pearl and Mackenzie, *The Book of Why: The New Science of Cause and Effect*, 2018. **Must read.** Why predicting an outcome is not the same as predicting the consequences of an action.
- Hernán and Robins, [*Causal Inference: What If*](https://miguelhernan.org/whatifbook), 2020. Free textbook covering g-computation, weighting, and target trial emulation.
- Hill, [The Environment and Disease: Association or Causation?](https://doi.org/10.1177/003591576505800503), *Proceedings of the Royal Society of Medicine*, 1965. The original nine considerations.
- CRASH trial collaborators, [Effect of intravenous corticosteroids on death within 14 days in 10,008 adults with clinically significant head injury](https://doi.org/10.1016/S0140-6736(04)17188-2), *The Lancet*, 2004. A plausible standard of care overturned by a large trial.
- Lester et al., [Effects of a mobile phone short message service on antiretroviral treatment adherence in Kenya (WelTel Kenya1)](https://doi.org/10.1016/S0140-6736(10)61997-6), *The Lancet*, 2010. A randomized trial of a digital health intervention.
- Yeh et al., [Parachute use to prevent death and major trauma when jumping from aircraft: randomized controlled trial](https://doi.org/10.1136/bmj.k5094), *BMJ*, 2018. A reminder to ask whether a trial population matches the question.
- Liu et al., [Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension](https://doi.org/10.1038/s41591-020-1034-x), *Nature Medicine*, 2020.
- [DAGitty](https://www.dagitty.net/). Draw causal graphs in the browser and find valid adjustment sets.
