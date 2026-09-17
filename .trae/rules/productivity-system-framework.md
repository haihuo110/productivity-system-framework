# Productivity System Framework — Trae rule

When a task concerns this repository, use the following role routing:

- Job definitions, responsibilities, standards, or competency expectations: read and apply `@agents/01-job-standard.md`.
- Learning paths, course/module design, sequencing, or outcomes: read and apply `@agents/02-curriculum-architect.md`.
- Executable tasks, work orders, exercises, acceptance criteria, or deliverables: read and apply `@agents/03-task-craft.md`.
- Simulations, scenarios, lab environments, or practice packages: read and apply `@agents/04-sim-adapter.md`.
- Risk, quality, safety, compliance, or final review: read and apply `@agents/05-safety-auditor.md`.

Use the matching schema before producing structured output:
- `@schemas/skill-matrix-v1.json`
- `@schemas/curriculum-blueprint-v1.json`
- `@schemas/lab-work-order-v1.json`
- `@schemas/sim-package-v1.json`
- `@schemas/audit-report-v1.json`

For a cross-cutting request, use the pipeline 01 → 02 → 03 → 04 → 05 as applicable. State the selected agent(s) and schema in the response, preserve required fields and enums, and do not invent schema fields. Inspect related examples and documentation before editing. Keep changes scoped, avoid secrets, and report validation performed plus any assumptions.
