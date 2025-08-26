---
name: /refine-style
description: Journal-specific style and formatting refinement
category: workflow
complexity: intermediate
mcp-servers: [context7, serena]
---

# /refine-style

## Usage
- `/refine-style --journal "Nature Medicine" --sections "all"`
- `/refine-style --journal "Lancet" --focus "word-count,references"`
- `/refine-style --journal "NEJM" --check "figures,tables,citations"`
- `/refine-style --custom --word-limit 3000 --ref-limit 30`

## Workflow Pattern
1) journal-specs → load target journal requirements via Context7
2) content-analysis → assess current manuscript against requirements  
3) optimization → suggest edits for compliance
4) validation → final check against journal specifications

## Notes
- This is a **context pattern** read by Claude Code; no executable code is run.
- Uses Context7 MCP for up-to-date journal formatting requirements
- Maintains consistency across multiple manuscript versions

## Journal Support
- Nature family: word counts, figure limits, reference styles
- Lancet: structured abstracts, word limits, citation format
- NEJM: clinical focus, figure requirements, trial registration
- JAMA: key points, statistical reporting, conflict disclosure

## Refinement Areas
- Word count optimization
- Reference formatting and limits
- Figure/table specifications  
- Citation style compliance
- Abstract structure requirements