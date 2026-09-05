# Project 4: AI-Powered Disease Risk Prediction System For Zoonotic Disease Outbreaks

Proposed team size: 5 students.

Project lead: David.

Partner: WHO.

Partner logo: https://upload.wikimedia.org/wikipedia/commons/c/c2/WHO_logo.svg

Keywords: machine learning, disease risk prediction, geospatial intelligence, explainable AI.

## Short Description

The aim of this project is to build an AI-powered disease risk prediction system that integrates human, animal, and environmental data to identify and visualize areas at high risk of zoonotic disease outbreaks.

## Motivation

Emerging infectious diseases are increasingly driven by interactions between humans, animals, and the environment. However, data from these three domains are often collected in isolation, making it difficult for public health agencies to detect emerging threats early enough to respond effectively.

Existing surveillance systems also require significant technical expertise in GIS and statistical modelling, limiting their accessibility and widespread use.

This WHO project for AI4Risk aims to develop a working prototype of an AI-powered risk analysis platform that integrates heterogeneous datasets from human health, animal health, and environmental sources to predict and visualize zoonotic disease risks. Students will design a pipeline that collects and harmonizes multi-source data, engineers relevant spatial and temporal features, trains machine learning models for disease risk prediction, and generates interactive geospatial risk maps.

The system should also provide interpretable explanations of its predictions and enable users to explore the factors contributing to disease risk in different locations. Students will systematically evaluate the predictive performance, robustness, and calibration of the models using appropriate spatial and temporal validation strategies and compare them against suitable baselines.

By the end of the project, the prototype should demonstrate how AI can support early warning, hotspot detection, and evidence-based decision-making for epidemic preparedness and public health planning.

## Intended Users

Potential users include:

- public health agencies;
- epidemic preparedness teams;
- zoonotic disease surveillance teams;
- environmental health analysts;
- WHO and AI4Risk stakeholders;
- decision-makers planning interventions or resource allocation.

## Possible Features

Possible features include:

- data ingestion from human health, animal health, and environmental sources;
- harmonization of heterogeneous spatial and temporal datasets;
- spatial and temporal feature engineering;
- baseline disease risk prediction model;
- comparison of multiple forecasting or risk-scoring approaches;
- interactive geospatial risk maps;
- hotspot detection;
- interpretable explanation of risk factors;
- exploration of factors contributing to disease risk in different locations;
- uncertainty, robustness, or calibration views;
- evidence export or summary for decision-makers.

The team should avoid building only a static map or only a model notebook. The central goal is an integrated risk analysis platform that connects data, prediction, explanation, and decision-support visualization.

## Design Questions

Consider:

- What is the prediction target, and what does a high-risk area mean?
- What spatial unit, temporal unit, and forecast horizon define a prediction?
- Which human, animal, and environmental data sources are available and compatible?
- How will the split avoid temporal and spatial leakage?
- What baselines are suitable for disease risk prediction?
- How should uncertainty, robustness, and calibration be communicated to public health users?
- What explanations are useful for understanding disease risk in different locations?
- How should the system support early warning, hotspot detection, and evidence-based planning?
- What limitations arise from missing, biased, sparse, or misaligned data?

## Technical Directions

Possible technical components include:

- multi-source data collection and documentation;
- geospatial and temporal data harmonization;
- spatial and temporal feature engineering;
- baseline machine learning model for disease risk prediction;
- model comparison against suitable baselines;
- spatial and temporal validation strategy;
- robustness and calibration evaluation;
- explainability method for risk factors;
- interactive geospatial risk map;
- dashboard or interface for exploring risk, predictions, explanations, and uncertainty;
- error analysis by geography, time, and outbreak context.

The system should make clear how data sources, features, model predictions, explanations, and map outputs are connected. A reviewer should be able to trace a displayed high-risk area back to the data and model evidence supporting it.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one valid zoonotic disease risk-prediction path.

Minimum convincing POC:

- the system loads a small multi-source dataset or a documented representative sample from human, animal, and environmental sources;
- the team defines a clear prediction target, spatial unit, temporal unit, and forecast horizon;
- the system engineers at least a small set of spatial and temporal features;
- the system trains or runs at least one suitable baseline model;
- the system generates disease risk predictions or scores;
- the predictions are displayed on a map or spatial visualization;
- the system provides at least one explanation signal for the prediction;
- the evaluation uses a spatial and temporal validation strategy that is appropriate for the target and avoids leakage;
- the demo includes at least one current result on predictive performance, robustness, or calibration.

The POC may use a limited region, simplified dataset, or reduced feature set. It should not be only a map visualization without a prediction target and baseline, and it should not report model performance without a valid spatial or temporal validation strategy.

## Evaluation Ideas

Possible evaluation approaches include:

- comparing against a simple spatial, temporal, seasonal, or persistence baseline;
- using temporal validation, spatial validation, or combined spatial-temporal backtesting;
- measuring predictive performance with justified metrics;
- evaluating calibration of predicted risks;
- testing robustness to missing, noisy, sparse, or misaligned data;
- evaluating performance across regions, time periods, and outbreak contexts;
- analyzing false positives and false negatives;
- testing whether explanations align with known risk factors or plausible domain assumptions;
- reviewing whether the map and dashboard support evidence-based decision-making.

## Final Demo Target

The final demo should show multi-source data ingestion, harmonization, feature engineering, disease risk prediction, hotspot visualization, explanation of selected high-risk areas, and evaluation results. It should demonstrate how the prototype could support early warning, hotspot detection, and evidence-based decision-making for epidemic preparedness and public health planning, while clearly communicating limitations around data quality, robustness, calibration, and deployment.
