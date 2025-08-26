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
1) Parse provided text
2) Normalize to JournalGuideline contract
3) Upsert to **core-memory**

## Notes
- Idempotent by `journal` key