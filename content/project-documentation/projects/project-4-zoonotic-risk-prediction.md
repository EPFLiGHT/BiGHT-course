# Project 4: AI-Powered Zoonotic Disease Risk Prediction

Proposed team size: 5 students, or 4 if needed.

Project lead: David.

Keywords: machine learning, disease risk prediction, geospatial intelligence, explainable AI.

## Short Description

Build an AI-powered disease risk prediction system that integrates human, animal, and environmental data to identify and visualize areas at high risk of zoonotic disease outbreaks.

## Motivation

Emerging infectious diseases are increasingly driven by interactions between humans, animals, and the environment. Data from these domains are often collected separately, which makes it difficult for public health agencies to detect emerging threats early enough to respond effectively.

Existing surveillance systems may also require significant GIS and statistical expertise. This project should make risk analysis more accessible through a working prototype that integrates heterogeneous data, predicts or scores risk, visualizes hotspots, and explains the factors contributing to risk.

## Intended Users

Potential users include:

- public health agencies;
- epidemic preparedness teams;
- zoonotic disease surveillance teams;
- environmental health analysts;
- decision makers planning interventions.

## Possible Features

Possible features include:

- data ingestion from human, animal, and environmental sources;
- spatial and temporal feature engineering;
- baseline disease risk model;
- risk maps;
- hotspot detection;
- interpretable explanation of risk factors;
- comparison of regions;
- evidence export for decision makers.

## Design Questions

Consider:

- What is the prediction target?
- What time and location unit defines a prediction?
- Which data sources are available and compatible?
- How will the split avoid temporal and spatial leakage?
- What baseline is meaningful?
- How should uncertainty be shown on the map?
- What explanations are useful to a public health user?

## Technical Directions

Possible technical components include:

- geospatial data harmonization;
- temporal feature engineering;
- baseline machine learning model;
- valid train, validation, and test split;
- explainability method;
- interactive or static risk map;
- error analysis by geography or time.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one valid risk-prediction path.

Minimum convincing POC:

- the system loads a small multi-source dataset or a representative sample;
- the team defines a clear prediction target and spatial/temporal unit;
- the system trains or runs a baseline model;
- the system generates risk predictions or scores;
- the predictions are displayed on a map or spatial visualization;
- the system provides at least one explanation signal for the prediction;
- the evaluation uses a split that is appropriate for the target and does not leak future information.

The POC may use a limited region or simplified dataset. It should not be only a map visualization without a prediction target and baseline.

## Evaluation Ideas

Possible evaluation approaches include:

- comparing against a simple baseline;
- using temporal validation where appropriate;
- measuring predictive performance with a justified metric;
- checking calibration or ranking quality;
- evaluating performance across regions;
- analyzing false positives and false negatives;
- testing whether explanations align with known risk factors.

## Final Demo Target

The final demo should show data ingestion, risk prediction, hotspot visualization, explanation of selected high-risk areas, and a discussion of model limitations for public health decision-making.
