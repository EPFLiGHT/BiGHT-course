# Project 6: AI-Powered Dengue Early-Warning Platform

Proposed team size: 5 students.

Project lead: To be confirmed.

Keywords: machine learning, time series forecasting, public health, data visualization, full-stack development, explainable AI.

## Short Description

Build an AI-powered dengue early-warning platform that predicts upcoming disease incidence and turns these forecasts into interpretable information that public health decision-makers can explore and use.

## Motivation

Dengue outbreaks can place substantial pressure on health systems. Anticipating increases in cases can help public health agencies prepare resources, plan interventions, and communicate risk earlier.

This project is built around the DrivenData DengAI: Predicting Disease Spread challenge. The competition provides the machine-learning component, but the project goes beyond competition scoring. Students should develop rigorous temporal validation, compare forecasting approaches, and turn the model into a usable decision-support platform.

The final prototype should demonstrate the complete pipeline from reproducible data processing and ML experimentation to an interpretable forecasting service that could support public-health decision-making.

Challenge link: https://www.drivendata.org/competitions/44/dengai-predicting-disease-spread/

## Intended Users

Potential users include:

- public health decision-makers;
- epidemiological surveillance teams;
- outbreak preparedness teams;
- analysts comparing dengue risk across time and locations;
- health agencies planning resources or interventions.

## Possible Features

Possible features include:

- reproducible DengAI data ingestion and preprocessing;
- temporal train, validation, and test splits;
- comparison of baseline and stronger forecasting models;
- backend endpoint serving forecasts;
- interactive dashboard for historical incidence and forecasts;
- visualization of environmental conditions;
- uncertainty visualization;
- explanation of factors influencing predictions;
- forecast export or summary for decision-makers.

The team should avoid treating the project as only a leaderboard exercise. The platform should make forecasts interpretable and usable.

## Design Questions

Consider:

- What forecast horizon is most useful for a public health decision-maker?
- What temporal validation strategy avoids future leakage?
- Which baseline is meaningful for dengue incidence forecasting?
- How should uncertainty be represented to non-technical users?
- What environmental or seasonal factors appear to influence predictions?
- How should the system distinguish historical observations from forecasts?
- What action could a decision-maker take based on the dashboard?

## Technical Directions

Possible technical components include:

- DrivenData DengAI dataset processing;
- time series feature engineering;
- baseline forecasting models;
- machine learning models for incidence prediction;
- temporal cross-validation or backtesting;
- model explainability;
- backend forecast service;
- interactive dashboard;
- visualization of historical cases, predicted cases, uncertainty, and drivers.

## Proof-Of-Concept Expectation

The proof of concept should demonstrate one valid dengue forecasting and decision-support path.

Minimum convincing POC:

- the system loads the DengAI data or a documented representative subset;
- the team defines a clear forecast target, city, time unit, and forecast horizon;
- the system uses a temporal split that avoids future leakage;
- the system trains or runs at least one baseline forecasting model;
- the system generates dengue incidence forecasts for a held-out period;
- the forecasts are displayed in a simple dashboard or visualization alongside historical incidence;
- the system shows at least one uncertainty, error, or explanation signal useful to a public health user.

The POC may use one city, one baseline model, and a simple dashboard. It should not be only a competition notebook or only a static visualization without a reproducible forecasting path.

## Evaluation Ideas

Possible evaluation approaches include:

- comparing against a seasonal or persistence baseline;
- using temporal backtesting;
- reporting the DrivenData metric and at least one interpretable error summary;
- analyzing errors by season, city, or outbreak period;
- evaluating calibration or uncertainty quality if uncertainty is provided;
- checking whether explanations align with known temporal or environmental patterns;
- testing whether the dashboard makes forecast limitations visible.

## Final Demo Target

The final demo should show the full path from data processing to forecast generation and dashboard exploration. A public health decision-maker should be able to inspect historical dengue incidence, predicted cases, uncertainty or error information, and explanations of important factors influencing the forecast.
