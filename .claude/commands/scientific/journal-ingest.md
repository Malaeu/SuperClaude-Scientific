---
name: /journal-ingest
description: Create/Update JournalGuideline nodes in core-memory graph
category: workflow
mcp-servers: [core-memory]
---

# /journal-ingest

## Usage
- `/journal-ingest --journal "NEJM" --paste`
- `/journal-ingest --journal "Lancet" --from-file docs/lancet_guidelines.md`

## Workflow Pattern
1) Parse the provided guideline text.
2) Extract normalized fields (see agent-journal-spec Output Contract).
3) Upsert node `JournalGuideline(journal=<name>)` in **core-memory**.

## Notes
- Idempotent by `journal` key. Supports iterative refinement.