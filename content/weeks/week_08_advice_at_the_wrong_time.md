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
- Identify workflow, timing, alert fatigue, and accountability risks in decision support.
- Compare interruptive and non-interruptive integration patterns.
- Translate workflow analysis into safer AI system behavior.
- Distinguish overdiagnosis from false positives and explain downstream care cascades.
- Apply threshold thinking and the Five Rights of clinical decision support.
- Design for human oversight, safe takeover, and feedback after deployment.

## Why Doctors Ignore Good Advice

Before asking why advice was ignored, ask **whether it was worth following**. A test can correctly detect an abnormality without improving a patient's life. South Korea's thyroid-cancer screening experience illustrates the distinction: diagnoses increased dramatically without a corresponding reduction in mortality. **More sensitive does not necessarily mean more useful.**

Overdiagnosis means detecting a real condition that would never have caused symptoms or death. It is different from a false positive. An incidental finding is something discovered while looking for something else; some are important, while others start a cascade of repeat imaging, biopsies, treatment, anxiety, and cost with little benefit. Before recommending another test, we should ask: **would its result change management in a way that benefits this patient?**

Threshold thinking helps us avoid treating every uncertainty as a reason to investigate. Below a testing threshold, testing may do more harm than good; between testing and treatment thresholds, information can change the decision; above the treatment threshold, treatment may be justified without further testing. These thresholds depend on **the consequences of missing disease, testing, and treatment**, not one universal probability cutoff.

Even useful advice can arrive in the wrong form. Repeated low-value warnings create **alert fatigue**: cognitive overload and desensitization make important warnings easier to miss. Overrides can also reflect disagreement, patient preferences, local constraints, or lack of training. **An override is information about the system, not automatically a clinician's mistake.** Vanderbilt's Clickbusters program illustrates the value of clinicians and engineers reviewing unnecessary alerts together.

## Integration Without Interruption

**Human attention is a limited resource.** Each interruption competes with patient care and other decisions. We use the **Five Rights of clinical decision support (CDS)** to make integration concrete: the right information, to the right person, in the right intervention format, through the right channel, at the right time in the workflow.

Horvitz's mixed-initiative approach gives us three choices: **stay quiet, ask, or act**. Which is appropriate depends on uncertainty, expected benefit, the cost of interruption, and the consequences of acting incorrectly. A non-interruptive suggestion may be enough for routine advice; an interruptive warning needs a stronger justification. A hard stop also needs a safe path forward when its assumptions are wrong.

For your projects, make these choices explicit:

- **Fit the existing workflow:** identify the decision point and responsible user before choosing an interface. FHIR supports clinical data exchange; CDS Hooks defines calls at workflow points; openEHR provides clinical record specifications. These solve different integration problems.
- **Make the next step easy:** give actionable advice, avoid unnecessary data entry, and prefer a useful alternative to simply blocking an action.
- **Preserve the ability to take over:** a human needs to understand what happened, what the system did, and what remains uncertain. Vigilance takes effort; automation bias and skills lost through disuse make “a human is in the loop” an insufficient safety argument.
- **Learn from use:** review overrides and feedback, monitor downstream harm and workload, and maintain the underlying knowledge. Fewer alerts or more clicks alone do not establish safer care.

The aviation analogy also applies to AI-assisted coding: **could you take over if the assistant failed?** Oversight is only meaningful when we retain enough understanding and skill to intervene.

## Key Terms

- **Low-value care:** care offering little or no benefit, or harm, relative to its costs.
- **Overdiagnosis:** correct detection of a condition that would not have caused symptoms or death.
- **Care cascade:** downstream investigations or treatments triggered by an initial finding.
- **Alert fatigue:** reduced responsiveness caused by repeated warnings and overload.
- **Mixed-initiative interaction:** humans and systems sharing initiative, with the system deciding when to offer help, ask, or defer.
- **De-skilling:** loss of skills through disuse, including skills needed when automation fails.

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
