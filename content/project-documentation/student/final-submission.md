# Final Submission

Deadline: Friday of Week 14, December 18, 21:59.

Weight: 40% of the course grade.

The final submission includes code, report, documentation, final presentation, and a live demo in front of the class.

## Submission Location

Submit everything inside your team GitHub repository.

Required final artifacts:

- final code;
- final report as PDF;
- reproducibility instructions;
- demo instructions;
- final presentation material;
- one individual contribution report per team member;
- handover or maintenance documentation.

## Final Report

The final report must be submitted as a PDF inside the repository.

Strict page limit: 5 pages, excluding references and appendices.

The report should include:

- problem and intended users;
- system architecture;
- data sources and preprocessing;
- models, prompts, algorithms, or external tools used;
- evaluation and error analysis;
- UX and design decisions;
- limitations and failure modes;
- ethical, safety, privacy, and deployment considerations;
- reproducibility summary.

References and appendices do not count toward the 5-page limit. Appendices should support the report, not replace it.

## Individual Contribution Reports

Your repository must include one short individual contribution report per team member.

Each report should be written by the student whose contribution it describes. It should include:

- main technical, design, evaluation, documentation, and presentation contributions;
- links or references to relevant pull requests, issues, commits, experiments, or report sections;
- decisions the student influenced and tradeoffs they handled;
- parts of the project they reviewed, tested, debugged, or helped integrate;
- any major blockers, handovers, or unfinished work relevant to their contribution.

Recommended location:

```text
docs/individual-reports/<student-name>.md
```

## Final Presentation And Live Demo

The final presentation should feature a live demo in front of the class.

Recommended presentation structure:

- problem and motivation;
- intended users and context;
- live demo;
- architecture summary;
- evaluation results;
- main limitations;
- what the team would do next.

Have a backup plan for the live demo, such as a short recorded demo, screenshots, or a deterministic local example. The backup does not replace the live demo requirement, but it protects you from network or hardware issues.

## Reproducibility Requirements

The final repository should be reproducible from a fresh clone.

At minimum, the README should explain:

- how to install the environment with `uv`;
- how to run tests;
- how to run linting, formatting checks, and type checks;
- how to obtain or generate sample data;
- how to run the demo or main pipeline;
- which features require credentials, network access, or external APIs;
- known limitations.

## Code Quality Requirements

The final repository should include:

- passing CI;
- passing pre-commit hooks;
- meaningful tests for representative project logic;
- clear package structure;
- configuration separated from code;
- no committed secrets;
- no unapproved large files;
- readable documentation.

<!--
## Rubric

| Criterion | Weight |
|---|---:|
| Working prototype and live demo | 20% |
| Technical implementation and integration | 20% |
| Evaluation, error analysis, and evidence quality | 20% |
| Reproducibility, CI, tests, and code quality | 15% |
| User/context fit, safety, ethics, and limitations | 10% |
| Final report and documentation | 10% |
| Presentation quality and contribution clarity | 5% |

-->

## Common Problems

Avoid:

- beginning the central technical work after the proof of concept;
- submitting code that only runs on one machine;
- relying on an API key without documenting it;
- showing a demo that cannot be reproduced;
- reporting only successful examples;
- hiding limitations;
- making the report longer by moving core content to appendices;
- submitting individual contribution reports that are vague or disconnected from repository evidence.
