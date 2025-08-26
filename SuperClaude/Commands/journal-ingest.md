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
- `/journal-ingest --journal "Nature Medicine" --from-file docs/natmed_guidelines.md`

## Workflow Pattern
1) Parse pasted/loaded guideline text
2) Extract normalized fields (see agent-journal-spec Output Contract)
3) Upsert node `JournalGuideline(journal=<name>, payload=<normalized_json>)` in **core-memory**

## Notes
- Idempotent by `journal` key (merge updates).
- Keep original text in `payload.raw_text` (optional) for traceability.

