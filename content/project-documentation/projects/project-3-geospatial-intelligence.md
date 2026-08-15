# Project 3: Geospatial Intelligence For Public Health Decisions

Proposed team size: 4 students, or 3 if needed.

Project lead: TBD.

Keywords: geospatial intelligence, public health decision support, LLMs, structured evidence.

## Short Description

Build a working prototype of a geospatial intelligence system that supports public health decision-making using structured and verifiable spatial evidence.

## Motivation

Public health decisions are often spatial decisions. Agencies need to know which services are missing, where vulnerable populations may live, and which environmental or infrastructural risks matter in particular locations.

LLMs are often unreliable for this use case because they do not reason well over maps and visual spatial data. This project should connect language-based interaction to open-source geospatial analysis tools, so answers are supported by structured evidence rather than only by an LLM's internal knowledge.

## Intended Users

Potential users include:

- public health agencies;
- humanitarian coordination teams;
- responders planning service deployment;
- analysts without deep GIS expertise;
- decision makers who need spatial evidence quickly.

## Example Query

An example query could be:

```text
Where is the best place to deploy a mobile clinic in Freetown within Sierra Leone to best tackle the current increase in Ebola cases?
```

The system should identify relevant data, run spatial analysis, and produce a specific and evidence-backed response.

## Possible Features

Possible features include:

- natural-language query input;
- geospatial data retrieval or loading;
- connection to open-source geospatial analysis tools;
- map display;
- structured evidence table;
- explanation of assumptions;
- LLM-generated summary grounded in spatial outputs;
- uncertainty or missing-data warnings.

## Design Questions

Consider:

- What spatial operation is needed to answer the query?
- What data is required, and is it available?
- What should the LLM do, and what should deterministic geospatial tools do?
- How can the system make its evidence verifiable?
- How should missing, stale, or low-resolution data be communicated?
- What makes a recommendation actionable for public health planning?

## Technical Directions

Possible technical components include:

- geospatial data loading with public datasets;
- spatial joins, buffers, distance calculations, or accessibility analysis;
- map visualization;
- LLM orchestration around tool outputs;
- structured report generation;
- reproducible query examples.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one evidence-backed geospatial query.

Minimum convincing POC:

- the user submits one predefined public health query;
- the system loads or retrieves at least one relevant geospatial dataset;
- the system runs at least one verifiable spatial operation;
- the result is shown on a map or in a structured spatial output;
- the system produces an answer that cites or displays the evidence used;
- the system clearly separates geospatial computation from LLM-generated explanation.

The POC may use a simplified region, a small dataset, or a predefined query. It should not be only an LLM response to a map-related question.

## Evaluation Ideas

Possible evaluation approaches include:

- checking whether the spatial operation is appropriate for the query;
- validating outputs against known examples or manual GIS analysis;
- inspecting whether the LLM summary matches the computed evidence;
- testing sensitivity to missing or noisy data;
- measuring reproducibility of query execution;
- reviewing whether recommendations are specific and actionable.

## Final Demo Target

The final demo should show a public health query, spatial data processing, map or evidence output, and a grounded recommendation that can be traced back to the underlying geospatial analysis.
