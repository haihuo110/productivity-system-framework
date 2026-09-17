# Trae CN setup

This repository includes Trae rules in `.traerules` and `.trae/rules/productivity-system-framework.md`. They route requests to the five repository agents and their JSON schemas.

## Quick start

1. Open or clone `haihuo110/productivity-system-framework` in Trae CN.
2. Make sure the repository root is the active workspace so Trae can load `.traerules` and `.trae/rules/`.
3. In Trae Chat, reference the relevant agent with `@`, for example:
   - `@agents/01-job-standard.md` for job standards.
   - `@agents/02-curriculum-architect.md` for curriculum design.
   - `@agents/03-task-craft.md` for executable tasks and work orders.
   - `@agents/04-sim-adapter.md` for simulations and lab packages.
   - `@agents/05-safety-auditor.md` for risk and quality audits.
4. Also reference the matching schema when requesting a structured artifact, such as `@schemas/lab-work-order-v1.json` or `@schemas/audit-report-v1.json`.
5. Ask Trae to state the selected agent(s), schema, files it will change, and validation it will perform before making an edit.
6. Review the diff and run the repository's normal checks before committing.

## Suggested prompts

- `@agents/03-task-craft.md @schemas/lab-work-order-v1.json Create a work order for ...`
- `@agents/02-curriculum-architect.md @schemas/curriculum-blueprint-v1.json Design a learning path for ...`
- `@agents/05-safety-auditor.md @schemas/audit-report-v1.json Audit this proposed change for risks and missing controls.`

For a request spanning the full workflow, ask Trae to use the sequence 01 → 02 → 03 → 04 → 05, skipping roles that are not relevant. Keep secrets out of chat and commits, and treat the repository files and schemas as the source of truth.
