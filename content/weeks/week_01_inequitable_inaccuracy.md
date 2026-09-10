---
page_id: "Week_01"
page_title: "Week 1: Inequitable Inaccuracy"
nav_title: "Week 1 - Inequitable Inaccuracy"
sidebar_group: "Block I - Volatile Contexts"
order: 1
week: 1
lecture_date: "2026-09-09"
theme: "Inequitable Inaccuracy"
context_lecture: "Tutti Fratelli: The Principles That Created a Movement"
slides_pdf: "slides/BiGHT-W1.pdf"
engineering_lecture: "Building for Broken Environments"
last_edited: "2026-09-10"
change_note: "Added Week 1 course notes and clarified the Switzerland/Nigeria comparison."
---

## Overview

**Block I: Volatile Contexts** (Weeks 1-4)

**Central question:** Why do systems fail the people who need them most?

**Big idea:** Inequity is not background noise. It decides who appears in our data, who reaches care, and who is harmed when we optimize for the people who are already visible.

**Block focus:** Understand the environments in which AI must operate, and why technology often fails in humanitarian and clinical settings.

We start the course with an uncomfortable observation: by being here, we are part of a tiny global elite. Most people do not have this level of education, institutional protection, health spending, connectivity, or choice. That matters because many AI systems are built from the records of people who already reached services, already survived long enough to be counted, and already live close enough to institutions to be visible.

So the first question is not "which model should we train?" It is: who has already disappeared before the dataset begins?

We then use the origin story of the Red Cross and Red Crescent Movement to introduce the humanitarian principles. These principles are not decorative ethics slides. They are practical constraints for any technology that claims to serve people in crisis.

## Learning Objectives

After this lecture, you should be able to:

- Explain how survivorship bias and unequal access to care distort health data.
- Use humanity, impartiality, neutrality, and independence as design constraints, not only as values.
- Recognize humanitarian dilemmas where two legitimate duties conflict.
- Explain why minimum standards, coordination, accountability, and data protection exist in humanitarian response.
- Translate this week's context constraints into concrete risks for your project.

## Core Ideas and Case Anchor

**Key concepts**

- Humanity, neutrality, impartiality, and independence
- Inequity, survivorship bias, unequal access, need-based prioritization, and data absence
- Humanitarian dilemmas, temoignage, humanitarian space, clusters, Sphere Standards, AAP, Do No Harm, and localization
- Data minimization, privacy, persistence of records, reproducibility, auditability, and responsible deployment

**Context themes in this block**

- Humanitarian systems
- Community medicine
- Global health
- Epidemics and outbreaks

**Engineering themes in this block**

- Participatory design
- ML infrastructure
- Federated learning
- Privacy
- Reproducibility
- Edge computing

**Historical anchor:** Battle of Solferino and the creation of the humanitarian movement.

**Great thinker/personality:** Henri Dunant

**Memorable fact:** Switzerland's life expectancy is about 84 years with roughly CHF 9,963 in annual health spending per person; Nigeria's is about 64 years with roughly CHF 62 per person.

## Why Inequity Produces Inaccuracy

Welcome to the elite. That is not meant as a compliment or an accusation; it is a design fact. If you are sitting in this course, you are much more educated, resourced, connected, and institutionally protected than most people affected by preventable illness or humanitarian crisis.

This matters for AI because privilege leaves a data trail. Poverty, displacement, illness, fear, distance, and weak infrastructure often do the opposite.

So when we look at health data, we should ask what had to happen before a person became a row in the dataset:

- A model that assumes connectivity has already chosen its users.
- A dataset that requires a clinic visit has already excluded many of the sickest people.
- An objective function that maximizes throughput has already decided whose time matters.

This is the first version of inequitable inaccuracy. The system may be accurate for the patients who reached care, for the clinics that file digital records, or for the countries that can afford measurement. But if the sickest people die before reaching care, delay because care is unaffordable, or are treated on paper that never becomes analyzable data, they are absent from the benchmark.

That is survivorship bias. The model learns from survivors of the system, then we are tempted to call its validation score "performance." Before optimizing anything, ask who had to survive, travel, pay, be connected, be literate, be documented, or be institutionally legible in order to appear.

## Humanitarian Principles as Design Constraints

We start the context lecture at Solferino, in 1859. Henri Dunant was a Geneva businessman, not a doctor. What he found after the battle was not a shortage of compassion only; it was a failure of organization. Tens of thousands of wounded soldiers needed care. Dunant's contribution was to coordinate, advocate, and insist on a simple principle: wounded people should be cared for regardless of which side they fought for.

That story leads to the ICRC, the Geneva Conventions, and the protective meaning of the red cross emblem. It also gives us four principles that are directly relevant to AI:

| Humanitarian principle | Practical meaning | AI design implication |
| --- | --- | --- |
| Humanity | Relieve suffering and protect dignity wherever suffering is found. | Use AI only when it plausibly protects life, relieves suffering, or preserves dignity. Efficiency is not a sufficient goal. |
| Impartiality | Provide assistance according to need, without discrimination. | Look for unequal errors, missingness, and exclusion. Do not reward the system for serving people who are easiest to measure. |
| Neutrality | Do not take sides in hostilities or political, religious, racial, or ideological controversies. | Do not build tools that enable targeting, partisan surveillance, propaganda, or coercive control. Trust and access are operational requirements. |
| Independence | Keep humanitarian action autonomous from political, economic, or military objectives. | Humanitarian actors must be able to question, override, refuse, or stop the system. |

The hard part is that these principles can conflict. Neutrality may require restraint to preserve access. Humanity may require speaking out when suffering is severe. Impartiality may require giving more assistance to those in greatest need, even if that looks political. A dilemma is not a puzzle with a clever technical answer. It is a situation where two legitimate duties conflict and no choice satisfies everything.

## Crises That Shaped the Humanitarian System

Several crises forced humanitarian organizations to choose what kind of system they were becoming:

- **Solferino and the founding of the ICRC:** care for wounded and sick soldiers regardless of side, protection for medical personnel and facilities, and a shared protective emblem.
- **Biafra:** the tension between preserving access through confidential negotiation and speaking out publicly against intolerable suffering.
- **Vietnamese boat people:** the tension between diplomacy with states and direct action to reach people stranded at sea.
- **Rwanda and the refugee crisis after the genocide:** the question of whether any aid is better than no aid, especially when camps lack basic water, sanitation, and health services and when armed groups can divert assistance.

These cases are not just history. They explain why the modern humanitarian system cares so much about coordination, standards, and accountability. Good intentions do not make aid good. Aid can be ineffective, captured, discriminatory, or harmful.

## Minimum Standards and Disaster Framing

After Rwanda, one response was Sphere: a Humanitarian Charter plus measurable minimum standards. The point is simple: people affected by crisis have a right to competent assistance, not just any assistance. Minimum standards are not bureaucratic decoration; they are a way to define what survival and dignity require in practice.

We will also use a simple disaster-risk frame:

```text
Impact = hazard x exposure x vulnerability / capacity
```

A hazard alone is not a disaster. The same flood, outbreak, attack, or power failure has different consequences depending on who is exposed, how vulnerable they are, and what capacity exists to respond.

For your projects, this means risk assessment cannot stop at model performance. You need to ask about infrastructure, staff attention, governance, trust, fallback procedures, and what happens when the system fails.

Humanitarian response is also coordinated. The cluster system divides response into sectors such as health, shelter, nutrition, WASH, and protection. If you build a dashboard, classifier, or optimization tool that does not fit how decisions are actually coordinated, you may add noise rather than capacity.

## Data Protection Is Protection

The ICRC tracing records make the data lesson concrete. Keeping records can reunite families and preserve evidence. The same persistence also extends the lifetime of risk. A record that is valuable for protection can become dangerous if it is exposed, linked, or reused for another purpose.

The engineering rule is data minimization: collect only what the stated purpose requires, keep it only as long as needed, and use the coarsest resolution that still serves the purpose. In humanitarian AI, data protection is not a compliance afterthought. It is part of protection.

## Engineering Takeaways

- Treat data absence as evidence, not emptiness. Missing records often indicate barriers to care, documentation, infrastructure, or trust.
- Define the population your system can see, then explicitly name who it cannot see.
- Test performance across need-relevant groups and data-availability conditions, not only on the easiest validation split.
- Preserve meaningful human control, especially where outputs could affect access to care, protection, or resources.
- Minimize data collection and retention. More data can mean more protection value, but also more exposure risk.
- Design for crisis coordination: make outputs interpretable, auditable, and usable within existing roles and response structures.
- Avoid the failure mode of optimizing for visible, connected, institutionally legible users while claiming to serve the most vulnerable.

## Project Reflection and Further Reading

**Reflection questions**

- Which stakeholder or constraint is easiest for your project team to overlook?
- Who must already have access, connectivity, documentation, or institutional trust to appear in your data?
- What evidence would show that your system is useful for people with the greatest need, not only for people who are easiest to measure?
- Which humanitarian principle would be easiest for your project to compromise under pressure?
- What is the minimum data your system actually needs, and what data would be dangerous to collect or retain?
- Which part of your current design would be hardest to audit, explain, override, or stop after deployment?

**Further reading**

- Core: International Federation of Red Cross and Red Crescent Societies, [The Fundamental Principles](https://www.ifrc.org/who-we-are/international-red-cross-and-red-crescent-movement/fundamental-principles).
- Core: Sphere Association, [The Sphere Handbook: Humanitarian Charter and Minimum Standards in Humanitarian Response](https://spherestandards.org/handbook/).
- Core: ICRC and Brussels Privacy Hub, [Handbook on Data Protection in Humanitarian Action](https://www.icrc.org/en/data-protection-humanitarian-action-handbook).
- Optional: Our World in Data, [Financing Healthcare](https://ourworldindata.org/financing-healthcare).
- Optional: Our World in Data, [Economic Inequality](https://ourworldindata.org/economic-inequality).
