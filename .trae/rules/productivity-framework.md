# Productivity System Framework rules

Apply these rules when working anywhere in this repository.

## Agent routing
- Use `@agents/01-job-standard.md` for job standards, role expectations, and competency requirements.
- Use `@agents/02-curriculum-architect.md` for curricula, learning paths, sequencing, and outcomes.
- Use `@agents/03-task-craft.md` for tasks, work orders, acceptance criteria, and deliverables.
- Use `@agents/04-sim-adapter.md` for simulations, scenarios, labs, and practice packages.
- Use `@agents/05-safety-auditor.md` for audits, risks, quality gates, safety checks, and escalation.

For end-to-end work, consult 01 → 02 → 03 → 04 → 05, and state which agents were used. Use the minimum applicable set for focused requests.

## Schemas
Match structured output to one of these schemas before writing it:
- `@schemas/skill-matrix-v1.json`
- `@schemas/curriculum-blueprint-v1.json`
- `@schemas/lab-work-order-v1.json`
- `@schemas/sim-package-v1.json`
- `@schemas/audit-report-v1.json`

Follow required properties, types, enums, and version identifiers exactly. Validate JSON syntax and cross-file references before finishing.

## Editing behavior
Read relevant source files first; preserve existing conventions; avoid unrelated changes; never invent schema fields; do not commit secrets. In the final response, report the role(s), schema, files changed, checks performed, and remaining assumptions.
