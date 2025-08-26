---
name: /map-data
description: Smart data-to-template mapping for scientific variables
category: workflow
complexity: intermediate
mcp-servers: [sequential, core-memory]
---

# /map-data

## Usage
- `/map-data analyze --dataset=path/to/data.csv`
- `/map-data suggest --template-sections "methods,results"`
- `/map-data validate --mapping-config mapping.json`
- `/map-data export --format "baseline-table,km-analysis,cox-model"`

## Workflow Pattern
1) analyze → examine dataset structure and variable types
2) suggest → propose variable-to-analysis mapping based on template
3) validate → check statistical appropriateness and completeness
4) export → generate analysis code and table structures

## Notes
- This is a **context pattern** read by Claude Code; no executable code is run.
- Focuses on medical/clinical dataset patterns
- Supports survival analysis, baseline tables, statistical modeling

## Mapping Heuristics

### Auto-mapping heuristics
- Survival: `time` + `event` → KM + Cox (primary endpoint).
- Binary exposures (0/1): logistic/Cox covariates.
- Grouping vars (e.g., `group`) → stratified analysis + between-group tests.
- Continuous biomarkers (e.g., `phase_angle`) → descriptive stats, cut-offs, spline sensitivity.
- Baseline table: demographics (age, sex, bmi) → Table 1 with standardized differences.

## Output Patterns
- Statistical analysis recommendations
- Table structure suggestions
- Figure type recommendations
- Missing data handling strategies