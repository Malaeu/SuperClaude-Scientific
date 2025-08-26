---
name: /paper-clone
description: USPG pipeline driver (analyze-template, map-data, generate, refine)
category: workflow
complexity: advanced
mcp-servers: [context7, sequential, serena]
---

# /paper-clone

## Usage
- `/paper-clone init --dataset=examples/scientific/dataset_sample.csv --template=examples/scientific/template_paper.pdf`
- `/paper-clone analyze-template`
- `/paper-clone map-data`
- `/paper-clone generate --sections "methods,results,discussion"`
- `/paper-clone refine --journal "Nature Medicine"`

## Workflow Pattern
1) analyze-template → load agent-paper-parser
2) map-data → propose column↔variable mapping (KM, Cox, baseline table)
3) generate → draft sections respecting template word counts
4) refine → style/citation/tables to target journal

## Notes
- This is a **context pattern** read by Claude Code; no executable code is run.
- Uses Sequential MCP for multi-step workflow orchestration
- Integrates with Serena MCP for project state persistence
- Leverages Context7 MCP for journal-specific formatting patterns

## State Management
- Project state stored via Serena MCP
- Template analysis cached for reuse
- Data mapping preferences remembered
- Journal formatting applied consistently

## Integration Points
- Triggers scientific agents based on workflow step
- Coordinates with other /sc: commands
- Maintains session context across iterations