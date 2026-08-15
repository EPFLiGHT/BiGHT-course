# Final Submission

Deadline: Final Presentation: Wednesday December 16, 13:15. Code and final report: Friday January 8 2027, 21:59.

Weight: 50% of the project grade (37.5% for the repo state and final report, 12.5% for the final oral presentation).

The final submission includes code, report, documentation, and final oral presentation with a live demo in front of the class.

## Submission Location

Submit everything inside your team GitHub repository.

Required final artifacts:

- final code;
- final report as PDF;
- reproducibility instructions;
- demo instructions;
- final presentation material;
- the contribution statement signed by each team member;
- handover or maintenance documentation.

## Final Report

The final report must be submitted as a PDF inside the repository.

Strict page limit: 10 pages, excluding references and appendices.

The report should include:

- problem statement and intended user(s);
- system architecture;
- data sources and preprocessing;
- models, prompts, algorithms, or external tools used;
- evaluation and error analysis;
- UX and design decisions;
- limitations and failure modes;
- ethical, safety, privacy, and deployment considerations;
- reproducibility summary.

Ensure that your final report addresses the five recurring questions:
- **Constraints**: What constraints shape the setting?
- **Trust**: Why should users trust the system?
- **Evidence**: What evidence shows that it works?
- **Larger Scale**: What changes at larger scale?
- **Uncertain**: What remains uncertain?

References and appendices do not count toward the 10-page limit.

## Individual Contribution Reports

Your repository must include the completed `docs/contribution-statement.md` document provided in the repo at the beginning of the semester, signed by each team member.

It should include for each student:

- main technical, design, evaluation, documentation, and presentation contributions;
- links or references to relevant pull requests, issues, commits, experiments, or report sections;
- decisions the student influenced and tradeoffs they handled;
- parts of the project they reviewed, tested, debugged, or helped integrate;
- any major blockers, handovers, or unfinished work relevant to their contribution.

## Final Presentation And Live Demo

The final oral presentation should feature a live demo in front of the class.

Recommended presentation structure:

- problem statement and intended user(s);
- live demo;
- one slide for the architecture of your system;
- evaluation results;
- main limitations;
- what the team would do next if it had more one more semester.

It is strongly recommended to reuse the slides of your midterm oral presentation.

Have a backup plan for the live demo, such as a short recorded demo, screenshots, or a deterministic local example. The backup does not replace the live demo requirement, but it protects you from network or hardware issues. The midterm presentation allows you to have a recorded demo, for the final presentation you have to produce a demo that can work live.

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
- passing pre-commit hooks with proper linting;
- meaningful tests for representative project logic;
- a clear package structure;
- configuration separated from code;
- no committed secrets;
- no unapproved large files;
- readable documentation;
- clear instructions on how to run the demo or the main pipeline.

## Common Problems

Avoid:

- submitting code that only runs on one machine;
- relying on an API key without documenting it;
- showing a demo that cannot be reproduced;
- having a documentation that cannot be trusted for running the demo or the main pipeline;
- reporting only successful examples;
- hiding limitations;
- making the report longer by moving core content to appendices;
- submitting individual contribution descriptions that are vague or disconnected from repository evidence.
