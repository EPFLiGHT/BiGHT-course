---
page_id: "Week_03"
page_title: "Week 3: The Last Mile"
nav_title: "Week 3 - The Last Mile"
sidebar_group: "Block I - Volatile Contexts"
order: 3
week: 3
lecture_date: "2026-09-23"
theme: "The Last Mile"
context_lecture: "Care at the Fringe: Community Medicine"
slides_pdf: "slides/BiGHT-W3.pdf"
engineering_lecture: "The Last Mile: Getting Intelligence to the Edge"
---

## Overview

**Block I: Volatile Contexts** (Weeks 1-4)

**Central question:** What happens when care leaves the hospital and comes home? Who provides it, what happens to medical advice as it dilutes into community life, and how can intelligent technologies support care across this last mile?

**Big idea:** Community medicine fills the gap when formal healthcare does not reach people. AI faces the same gap at the technical edge: when connectivity, compute, or language support run out, a system must still be accessible, contextualized, and reliable, or it has no business being patient-facing at all.

**Block focus:** Understand the environments in which AI must operate, and why technology often fails in humanitarian and clinical settings.

## Learning Objectives

After this lecture, you should be able to:

- Explain how community and traditional medicine function as a health-system response to gaps in formal care access, not as an irrational fringe.
- Describe the shared values and real points of friction (safety, regulation, standardization, documentation) between traditional and formal medicine.
- Explain why naive patient-facing AI is dangerous, using the ChatGPT Health triage stress test as evidence.
- Translate "accessible, contextualized, reliable" into a last-mile pipeline: speech-to-text, retrieval, language model, text-to-speech.
- Reason about the tradeoffs of running that pipeline at the edge: latency, quality, uptime, privacy, quality control, available resources.
- Recognize how WEIRD (Western, Educated, Industrialized, Rich, Democratic) training data shows up twice in this pipeline: as accent bias in speech recognition, and as shrinking language coverage in newer speech synthesis models.

## Context Lecture: Care at the Fringe: Community Medicine

The lecture opens with Southern African community healers, the **sangoma**, a diviner specializing in medicinal remedies, explicitly *not* a "witchdoctor", and contrasts this with the **voodoo priest** of Western Africa, who fills an overlapping role but is, by local definition, a witchdoctor too. The point is not the terminology itself but what it protects against: flattening distinct healing traditions into one undifferentiated "traditional medicine" erases real differences in what each practitioner actually claims to do.

Community medicines (**muti**, **dawa**, **jamu**, depending on region) carry both medicinal and spiritual significance, span everything from herbal therapy to ritual cuttings, and are not marginal: reported figures put South African traditional healers at roughly 200,000 against 25,000 medical doctors, with 60-80% of the population using muti. For most people, the healer, not the clinic, is the default point of contact with care. Interview footage frames illness as a **disagreement with ancestors**, diagnosed through personalized divination, the healer as an ordained medium negotiating a truce between ancestry and patient.

Traditional and formal medicine are **not necessarily opposed**: both claim to be patient-centered, holistic, and evidence-based. The real friction is safety, regulation, standardization, and documentation. Only 4 of 14 Southern African Development Community countries legislate traditional practice at all, and standardized training remains rare. Yet traditional healers have measurably extended formal healthcare's reach, into HIV response and TB case-finding, even as some practitioners' claimed scope stretches implausibly far (from cancer to gambling luck), and commercial "muti" now ships in branded retail bottles without a matching evidence base.

This tension motivates the lecture's central engineering cautionary tale: the WHO has floated an AI tool that photographs a local plant and suggests a pharmaceutical substitute when medicine is unavailable. It breaks on three fronts: the same plant looks different across specimens, there is no reliable dose or clinical-effect data to retrieve, and a wrong suggestion reaches a patient with no evidence trail. LiGHT's proposed alternative is a **compendium of traditional knowledge**, healers cataloguing plants and practices themselves, building consensus, then subjecting that catalogue to scientific review, community knowledge and scientific review working together rather than a model guessing from a photo. The lecture closes by asking what would happen without traditional medicine at all (a queue outside a rural clinic), pointing to community interventions that already close that gap, the **Friendship Bench** (grandmothers trained to deliver therapy in Zimbabwe) and **Coach Mpilo** (a free WhatsApp AI health coach in South Africa), and by placing muti next to acupuncture, cupping, and other "western" fringe practices, unsettling any easy traditional-vs-rational framing.

## Engineering Lecture: The Last Mile: Getting Intelligence to the Edge

The engineering lecture starts from a concrete problem: a patient in a rural, low-resource context (Ethiopia has roughly one physician per 10,000 patients) has a medical question, and needs an answer that is **accessible, contextualized, and reliable**. AI is a plausible new driver of healthcare that actually reaches people, but the lecture is emphatic that this **should never mean AI directly replacing a clinician as a patient-facing decision-maker**. A structured stress test of ChatGPT Health across 960 clinician-authored vignettes found it **undertriaged 52% of gold-standard emergencies**, sending diabetic ketoacidosis or impending respiratory failure to a 24-48 hour evaluation instead of the emergency department. The rest of the lecture is a working engineer's answer to that problem: a pipeline of **speech-to-text → knowledge retrieval → language model → text-to-speech**, with every stage judged against the same six constraints: latency, quality, uptime, privacy, quality control, and available resources.

**Listening (speech-to-text)** is framed as close to solved for English: Whisper-family models scale from 39M to 1.55B parameters and, together with alternatives, now run entirely offline on a phone, laptop, or even inside a browser tab via WebAssembly or WebGPU. The catch is data, not architecture: benchmarked on African-accented speech (AfriSpeech-200), word-error rates roughly double relative to standard benchmarks, across open models and commercial cloud ASR alike. **Takeaway:** training data matters more than model size, and depending on the deployment context there may be no solution at all.

**Thinking (the language model)** runs into the opposite problem: small, open-weight models (from a few hundred million to tens of billions of parameters) fit on a phone, laptop, or a single clinic GPU, but frontier capability still lives in hyperscale datacenters that assume a network connection. Small models also hit a factual wall quickly, this "isn't even about reasoning yet, it's about memorization." Retrieval-augmented generation (RAG) is presented as the fix: in one cited framework (MOBAYES), a mid-size open model paired with grounded retrieval matched the diagnostic accuracy of much larger frontier models at a fraction of the cost, while an even larger model used *without* grounding scored worse. **Takeaway:** small models are fluent and wrong, bigger models are fluent and less wrong, and grounding, not scale, is what actually closes that gap.

**Speaking (text-to-speech)** is the easiest box to tick: it runs in real time on a CPU, needs no server, and costs almost nothing in resources. But it repeats the STT lecture's data lesson from the other direction: language *coverage* has been shrinking with each newer model generation. A 2023 model (MMS-TTS) speaks over a thousand languages, including Amharic; every commercial model released since speaks fewer, and **none of the newer ones speak Amharic at all**. **Takeaway:** the newer the model, the shorter the language list.

## Key Terms

- **Last mile:** the final, hardest-to-reach stretch between an available resource and the person who needs it, where infrastructure and reach typically break down.
- **Sangoma:** a Southern African diviner specializing in medicinal remedies; explicitly not a "witchdoctor," unlike a West African voodoo priest.
- **Muti / dawa / jamu:** regional terms for community medicines carrying both medicinal and spiritual significance.
- **Compendium of Traditional Knowledge:** LiGHT's proposed alternative to a naive plant-identification AI tool: healer engagement, cataloguing, consensus, then scientific review.
- **WEIRD data:** training or benchmark data skewed toward Western, Educated, Industrialized, Rich, Democratic populations and languages, producing systems that perform worse, or don't exist, for everyone else.
- **Patient-facing:** any system output a patient receives directly without a clinician mediating; the lecture argues unvalidated triage-capable AI should never occupy this role.
- **RAG / grounding:** supplying a model with retrieved, verifiable evidence instead of relying on what it memorized during training; shown to matter more than raw model scale.
- **Open-weight model:** a model whose trained parameters are published for anyone to download and run locally, rather than only through a hosted API.

## Project Reflection

Use these questions to pressure-test your own project.

- Who currently fills the "last mile" in your project's context, and what would your system need to match or complement about that role?
- If your users lost network connectivity tomorrow, which parts of your system would still work?
- Which of the six constraints (latency, quality, uptime, privacy, quality control, available resources) is the binding one for your deployment context, and why?
- Would any part of your system's output ever reach a patient directly, unmediated? What evidence backs its reliability, given the ChatGPT Health triage result?
- Does the language or speech data your system depends on actually cover the languages your users speak?

## Further Reading

**Context**

- WHO. *[Traditional medicine strategy 2014-2023](https://www.who.int/publications/i/item/9789241506096).* Geneva: WHO, 2013.
- *[Legislative landscape for traditional health practitioners in Southern African development community countries: a scoping review](https://pubmed.ncbi.nlm.nih.gov/31915157/)*, BMJ Open.
- *[Traditional healers' role in the detection of active tuberculosis cases in a pastoralist community in Ethiopia: a pilot interventional study](https://pubmed.ncbi.nlm.nih.gov/31182067/)*, BMC Public Health, 2019.
- *The Friendship Bench: How Fourteen Grandmothers Inspired a Mental Health Revolution*, Dixon Chibanda, MD.

**Engineering**

- [AfriSpeech-200: Pan-African Accented Speech Dataset for Clinical and General Domain ASR](https://arxiv.org/pdf/2310.00274).
- [ChatGPT Health performance in a structured test of triage recommendations](https://www.nature.com/articles/s41591-026-04297-7), *Nature*, 2026.
- [World Bank: physicians per 1,000 people, Ethiopia](https://data.worldbank.org/indicator/SH.MED.PHYS.ZS?locations=ET).
- [MOBAYES: A Modular Bayesian Framework for Separating Reasoning from Language in Conversational Clinical Decision Support](https://arxiv.org/pdf/2604.20022v3).
