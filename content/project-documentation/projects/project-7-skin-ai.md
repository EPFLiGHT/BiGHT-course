# Project 7: WHO Skin AI For Offline Dermatology

Proposed team size: 3 students.

Project lead: David.

Partner: WHO.

Partner logo: https://upload.wikimedia.org/wikipedia/commons/c/c2/WHO_logo.svg

Keywords: machine learning, skin disease, dermatology.

## Short Description

Build an offline mobile application that can be used to reliably detect skin disease in the Global South.

## Motivation

Skin diseases are common in many low-resource settings, but specialist dermatology expertise is often unavailable or difficult to access. Connectivity constraints can also make cloud-based AI tools unsuitable for frontline clinical use.

This project will focus on the development and evaluation of a fully open-source, AI-based skin disease detection tool designed for use in low-resource and connectivity-constrained healthcare settings. Students will identify and curate suitable open-source dermatology image datasets, train and benchmark one or more computer vision models for the recognition of both selected common and neglected tropical rare skin diseases, and integrate the resulting model into a lightweight application that can operate entirely offline, without requiring access to cloud services or external APIs.

Particular attention will be given to model efficiency, robustness across different skin tones and populations, and suitability for deployment on resource-constrained devices such as smartphones or local edge-computing hardware. The resulting system will be independently evaluated using the clinical evaluation data collected during the first validation phase of the existing tool, allowing its performance to be compared with the current solution under realistic clinical conditions.

The overarching goal is to establish a transparent and reproducible foundation for an openly available skin disease detection system whose source code, trained models, and, where licensing and ethical requirements permit, supporting training and evaluation resources can be shared with the wider research and global health community.

## Intended Users

Potential users include:

- frontline health workers in low-resource settings;
- clinicians without immediate access to dermatology specialists;
- mobile health teams working in rural or connectivity-constrained areas;
- global health researchers evaluating open-source clinical AI tools;
- public health programs addressing common and neglected tropical skin diseases.

## Possible Features

Possible features include:

- curated dermatology image dataset pipeline using open-source data;
- model training for selected common and neglected tropical rare skin diseases;
- image capture or upload flow for skin lesion classification;
- fully offline inference without cloud services or external APIs;
- lightweight mobile or mobile-like interface;
- model confidence and uncertainty display;
- explanations or guidance about limitations and appropriate use;
- benchmarking across skin tones, populations, or disease groups;
- exportable evaluation reports or model cards.

The team should avoid building a diagnostic black box. The prototype should make clear what the model can and cannot support, and how it should be interpreted by a clinical or public health user.

## Design Questions

Consider:

- Which skin diseases are in scope for the first version, and why?
- Which open-source dermatology datasets are suitable, licensed, and ethically usable?
- How should the system handle uncertain, low-quality, or out-of-distribution images?
- How can the interface communicate that the tool supports decision-making rather than replacing clinical judgment?
- What device, latency, memory, and offline constraints matter for deployment?
- How will performance be assessed across skin tones, populations, and disease groups?
- What information should be shared openly with the wider research and global health community?

## Technical Directions

Possible technical components include:

- discovery and curation of open-source dermatology image datasets;
- dataset documentation, licensing review, and provenance tracking;
- computer vision model training or fine-tuning;
- model compression, quantization, or lightweight architecture selection;
- offline inference pipeline for smartphones or edge devices;
- mobile application, mobile web prototype, or local-device demo;
- evaluation using clinical validation data from the existing tool's first validation phase;
- fairness and robustness analysis across skin tones and populations;
- model card and reproducibility documentation.

The resulting system should be designed so that source code, trained models, and supporting training or evaluation resources can be shared where licensing and ethical requirements permit.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one valid offline skin-disease detection path from image input to model output and user-facing interpretation.

Minimum convincing POC:

- the team identifies and documents at least one suitable open-source dermatology dataset;
- the system trains, fine-tunes, or runs a computer vision model for a clearly scoped set of skin diseases;
- the model can run inference locally without cloud services or external APIs;
- the prototype accepts a representative image input and returns a classification or triage-style output;
- the interface communicates confidence, uncertainty, or limitations;
- the team reports at least one evaluation result using a held-out dataset or validation subset;
- the repository includes reproducible instructions for dataset preparation, model execution, and demo use.

The POC may focus on a limited disease set, a small dataset, and a simple mobile or local-device interface. It should not be only a training notebook without an offline user-facing inference path.

## Evaluation Ideas

Possible evaluation approaches include:

- comparing model performance against a simple baseline or the current existing solution;
- evaluating on clinical validation data collected during the first validation phase of the existing tool;
- reporting performance by disease class, skin tone, population group, or image quality;
- measuring latency, memory use, and offline readiness on a constrained device or simulated target environment;
- testing robustness to image quality variation, lighting, framing, and camera differences;
- documenting failure modes and unsafe use cases;
- reviewing licensing, ethical constraints, and reproducibility of released resources.

## Final Demo Target

The final demo should show a fully offline skin-disease detection workflow. A user should be able to provide a representative skin image, run local inference, view the model output with confidence or limitations, and see evidence that the system has been evaluated against realistic clinical data or a documented validation subset.
