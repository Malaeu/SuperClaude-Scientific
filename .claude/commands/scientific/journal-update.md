---
name: /journal-update
description: Orchestrate monthly refresh of JournalGuideline nodes using agent-journal-harvester
category: workflow
mcp-servers: [core-memory]
---

# /journal-update

## Usage
- `/journal-update --dry-run`
- `/journal-update --journals "NEJM,Lancet,Nature Medicine"`

## Workflow Pattern
1) Load curated list `docs/scientific/journals_sources.yaml`
2) For each journal in scope: activate `agent-journal-harvester`
3) Upsert normalized guideline nodes into **core-memory**
4) Produce report: updated, unchanged, missing-fields

## Notes
- This is a **context pattern** read by Claude Code; scheduling is external (e.g., GitHub Actions monthly).