# Project 3: Geospatial Intelligence For Public Health Decisions

Proposed team size: 5 students.

Project lead: David.

Keywords: geospatial intelligence.

## Short Description

The main aim of the project is to provide reliable Geospatial Intelligence for Public Health decisions.

## Motivation

Public health decisions are usually spatial-related decisions. Public health agencies need to know which services are missing in particular areas, where vulnerable populations might exist, and what environmental or infrastructural risks to look out for in particular areas.

Due to the recent popularity of LLMs, many organizations turn to them today to assist with decision-making and planning. The issue is that LLMs are notoriously unreliable for this use case because they do not reason well across maps and other forms of visual spatial data.

The aim of this project is therefore to build a working prototype of a geospatial intelligence system that can assist with public health decision-making. Instead of relying solely on LLMs to generate answers using their internal knowledge, the system should connect them to open-source geospatial analysis tools so that public health questions can be answered with structured and verifiable evidence.

The prototype should include a user interface that allows users to submit public health questions, inspect the resulting geospatial analysis and recommendations on a map, and review the evidence used to support them. Students should also systematically evaluate the reliability of the system on representative public health decision-making tasks, including the correctness of the geospatial analysis and the quality and verifiability of the resulting recommendations.

## Intended Users

Potential users include:

- public health agencies;
- humanitarian coordination teams;
- responders planning service deployment;
- analysts without deep GIS expertise;
- decision-makers who need spatial evidence quickly;
- organizations using LLMs for public health planning but needing more reliable geospatial reasoning.

## Example Query

An example query could be:

```text
Where is the best place to deploy a mobile clinic in Freetown within Sierra Leone to best tackle the current increase in Ebola cases?
```

The system should find, leverage, and organize relevant open-source geospatial data so that it can be analyzed with geospatial tools and, where appropriate, summarized with an LLM to produce a specific and actionable response.

## Possible Features

Possible features include:

- natural-language public health query input;
- user interface for asking questions and inspecting recommendations;
- geospatial data retrieval, loading, and organization;
- connection to open-source geospatial analysis tools;
- map display of data layers, analysis outputs, and recommendations;
- structured evidence table supporting each recommendation;
- explanation of assumptions, data sources, and spatial operations;
- LLM-generated summary grounded in geospatial outputs;
- uncertainty, missing-data, or low-quality-data warnings;
- representative task set for reliability evaluation.

The team should avoid building a generic map chatbot. The central goal is to connect user questions to verifiable geospatial analysis and evidence-backed recommendations.

## Design Questions

Consider:

- What public health decision-making tasks should the system support?
- What spatial operation is needed to answer each task?
- What open-source data is required, and is it available for the target region?
- What should the LLM do, and what should deterministic geospatial tools do?
- How can users inspect the map, evidence, assumptions, and recommendation path?
- How can the system make its evidence verifiable?
- How should missing, stale, low-resolution, or conflicting geospatial data be communicated?
- What makes a recommendation specific and actionable for public health planning?
- How will the team evaluate whether the geospatial analysis is correct?

## Technical Directions

Possible technical components include:

- public health task and query design;
- open-source geospatial data loading and preprocessing;
- spatial joins, buffers, distance calculations, accessibility analysis, or service-area analysis;
- map visualization and layer inspection;
- backend orchestration between query handling, geospatial tools, and LLM summarization;
- structured evidence generation;
- reproducible query examples;
- reliability evaluation against representative public health tasks;
- checks that LLM-generated recommendations match computed geospatial evidence.

The system should clearly separate geospatial computation, structured evidence, and LLM-generated explanation. A reviewer should be able to trace a recommendation back to the data sources and spatial operations that support it.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one evidence-backed geospatial public health query.

Minimum convincing POC:

- the user submits one predefined public health decision-making query through a basic interface;
- the system loads or retrieves at least one relevant open-source geospatial dataset;
- the system runs at least one verifiable spatial operation;
- the result is shown on a map or in a structured spatial output;
- the system produces a recommendation that cites or displays the evidence used;
- the user can inspect the map, analysis output, and supporting evidence;
- the system clearly separates geospatial computation from LLM-generated explanation;
- the team evaluates the correctness of the geospatial operation on at least one representative task.

The POC may use a simplified region, a small dataset, or a predefined query. It should not be only an LLM response to a map-related question, and it should not be only a map visualization without a decision-support recommendation.

## Evaluation Ideas

Possible evaluation approaches include:

- checking whether the spatial operation is appropriate for each representative task;
- validating geospatial outputs against known examples, manual GIS analysis, or expert review;
- inspecting whether LLM-generated summaries and recommendations match the computed evidence;
- testing sensitivity to missing, noisy, stale, or low-resolution data;
- measuring reproducibility of query execution;
- reviewing whether recommendations are specific, actionable, and evidence-backed;
- evaluating whether users can inspect the map and evidence used to support a recommendation;
- comparing the tool-supported answer with a generic LLM answer for the same public health question.

## Final Demo Target

The final demo should show a user submitting a public health question, the system loading or organizing relevant open-source geospatial data, running spatial analysis, displaying the results and recommendation on a map, and exposing the structured evidence used to support the answer. The demo should make clear why the recommendation is more reliable and verifiable than an unsupported LLM response.
