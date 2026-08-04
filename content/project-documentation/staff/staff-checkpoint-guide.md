# Staff Week 10 Checkpoint Guide

The Week 10 checkpoint is a non-graded 30-minute conversation with each team.

The purpose is to help teams finish well, not to grade them. This checkpoint is separate from the graded Week 8 technical checkpoint and midterm oral presentation.

## Before The Checkpoint

Staff should review:

- milestone 3 proof-of-concept document;
- current README;
- recent pull requests;
- CI status;
- issue board or task list;
- any obvious unresolved risks.

## Suggested Structure

| Activity | Time |
|---|---:|
| Team status summary | 5 min |
| Current artifact or demo | 10 min |
| Risks, blockers, and evidence gaps | 7 min |
| Staff feedback and scope decision | 8 min |

Keep the meeting focused. Avoid turning it into a full presentation.

## Core Questions

Ask:

- What currently works?
- What changed since the proof of concept?
- What is still blocked?
- What is the riskiest remaining component?
- What will definitely be in the final demo?
- What has moved to stretch goals?
- What evidence or evaluation will appear in the final report?
- What do you need from staff?

## Scope Decision

End with one of these outcomes.

| Outcome | Meaning |
|---|---|
| Continue | Current plan is feasible |
| Simplify | Final scope must be reduced |
| Replace component | A failing technical component needs an alternative |
| Escalate | Staff intervention is needed for data, model, scope, or team process |

The outcome should be written down in a short note or issue comment.

## Warning Signs

Watch for:

- no working demo path;
- no evaluation plan;
- central data still unavailable;
- central model or API still untested;
- CI failing for a long time;
- team members unclear about responsibilities;
- project scope unchanged despite weak POC;
- too much work planned for the final week;
- no live demo plan.

## Suggested Intervention Patterns

For over-scoped projects, ask the team to name the smallest final demo that would still be meaningful.

For missing data, ask for a fallback dataset or simulated example that preserves the technical structure.

For weak evaluation, ask for one baseline and one error-analysis table.

For UI-only projects, ask for the smallest real backend or model path that can be connected before the final.

For model-only projects, ask for the smallest user-facing output that demonstrates the decision support use case.

For team-process problems, ask students to create explicit issues and ownership for the remaining work.

## After The Checkpoint

Staff should record:

- checkpoint date;
- attending team members;
- outcome decision;
- required scope changes;
- staff commitments;
- any team-process concerns.
