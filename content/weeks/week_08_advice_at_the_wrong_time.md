---
page_id: "Week_08"
page_title: "Week 8: Advice at the Wrong Time"
nav_title: "Week 8 - Advice at the Wrong Time"
sidebar_group: "Block II - High-Stakes Decisions"
order: 8
week: 8
lecture_date: "2026-11-04"
theme: "Advice at the Wrong Time"
context_lecture: "Why Doctors Ignore Good Advice"
slides_pdf: "slides/BiGHT-W8.pdf"
engineering_lecture: "Integration Without Interruption"
---

## Overview

**Block II: High-Stakes Decisions** (Weeks 5, 6, 8)

**Central question:** When does the cure become worse than the disease?

**Big idea:** **More medicine is not always better medicine, and more alerts do not always produce better decisions.** We must evaluate advice by its consequences for patients and the work it creates, not just whether its content is correct.

**Block focus:** Understand how clinicians make decisions under uncertainty and how AI can safely support human expertise.

## Learning Objectives

After this lecture, you should be able to:

- Explain why a correct recommendation can still make care worse.
- Distinguish overdiagnosis from false positives and explain downstream care cascades.
- Explain alert fatigue and choose between interruptive and non-interruptive advice.
- Apply threshold thinking to clinical decision support.
- Design for human oversight, safe takeover, and feedback after deployment.

## Why Doctors Ignore Good Advice

Humans are error prone. Medical doctors too, they need advice as they work under multidimensional conditions of uncertainty. 

Uncertainty alone is not a reason to test. **Threshold thinking** separates three situations: too little suspicion to justify testing, enough uncertainty for a test to help, or enough evidence to treat without further testing. The thresholds depend on the harms and benefits of each choice.

Before asking why advice was ignored, we should ask: **was it worth following?** South Korea's thyroid-cancer screening experience is a useful warning. Diagnoses increased dramatically without a corresponding reduction in mortality. Finding more disease does not necessarily mean helping more people.

- **Overdiagnosis is not a false positive:** the condition is real, but would never have caused symptoms or death.
- **Incidental findings can start care cascades:** repeat scans, biopsies, treatment, anxiety, and cost. Some findings matter; others lead to harm without benefit.
- Before ordering a test, ask: **would the result change what we do, and would that help this patient?**


We also need to ask how advice was delivered. Repeated low-value warnings create **alert fatigue**, making important warnings easier to miss. Ignoring advice can reflect patient preferences, local constraints, or reasonable disagreement. **An override is feedback, not automatically a mistake.** Vanderbilt's Clickbusters program (https://www.vumc.org/vclic/clickbusters) shows what clinicians and engineers can achieve by reviewing unnecessary alerts together.

## Integration Without Interruption

**Human attention is a limited resource.** Every alert spends some of it. Give us a practical check: the right information, to the right person, in the right format, through the right channel, at the right time.

Horvitz's mixed-initiative approach asks whether the assistant should **stay quiet, ask, or act**. Confidence matters, but so do the cost of interruption and the consequences of getting it wrong. Routine advice may belong in a quiet suggestion. An interruptive warning needs a stronger justification; a hard stop needs a safe way forward when its assumptions are wrong.

For your projects, make these choices explicit:

- **Start with the workflow:** who needs this advice, and at which decision point? Choose the interface afterwards.
- **Make the next step easy:** give actionable advice, avoid unnecessary data entry, and prefer a useful alternative to simply blocking an action.
- **Make takeover possible:** users need to know what the system did and what remains uncertain. “A human is in the loop” means little if that person cannot spot a failure or intervene.
- **Learn from use:** review overrides and feedback, monitor downstream harm and workload, and maintain the underlying knowledge. Fewer alerts or more clicks alone do not establish safer care.

For implementation, distinguish the tools: **FHIR** supports clinical data exchange, **CDS Hooks** defines calls at workflow points, and **openEHR** specifies clinical records. Connecting to a record system is only part of integrating into clinical work.

The aviation analogy applies to AI-assisted coding too: **could you take over if the assistant failed?** Vigilance takes effort, and skills can fade through disuse. We need to preserve the abilities we rely on when automation stops working.

## Key Terms

- **Low-value care:** care whose expected benefits do not justify its harms and costs.
- **Overdiagnosis:** detecting a real condition that would never have caused symptoms or death.
- **Incidental finding:** a finding discovered while investigating something else; it may or may not require action.
- **Care cascade:** further investigations or treatments triggered by an initial finding.
- **Alert fatigue:** reduced responsiveness after repeated warnings and cognitive overload.
- **Mixed-initiative interaction:** humans and systems sharing initiative; the assistant may stay quiet, ask, or act.
- **De-skilling:** loss of skills through disuse, including those needed when automation fails.

## Project Reflection

- What downstream actions could your recommendation trigger, and who bears their risks and costs?
- When should your system stay silent, ask for clarification, or interrupt?
- Can a user understand, challenge, and safely take over from your system?
- What evidence would show better patient outcomes rather than simply more activity?

## Further Reading

- Ahn et al., [Korea's Thyroid-Cancer “Epidemic” — Screening and Overdiagnosis](https://doi.org/10.1056/NEJMp1409841), *NEJM*, 2014. A concrete example of detection without corresponding population benefit.
- Bates et al., [Ten Commandments for Effective Clinical Decision Support: Making the Practice of Evidence-Based Medicine a Reality](https://doi.org/10.1197/jamia.M1370), *JAMIA*, 2003. Practical workflow-design principles.
- Horvitz, [Principles of Mixed-Initiative User Interfaces](https://doi.org/10.1145/302979.303030), *CHI*, 1999. A framework for deciding when assistance is worth its interruption cost.
- [HL7 FHIR](https://hl7.org/fhir/) and [CDS Hooks](https://cds-hooks.hl7.org/). Technical references for data exchange and workflow-triggered decision support.
- [openEHR specifications](https://specifications.openehr.org/) and [EHRbase](https://ehrbase.org/). Resources for exploring structured clinical records and integration.
