---
name: /map-data
description: Propose dataset↔template mapping for clinical manuscripts (KM/Cox/Baseline)
category: workflow
mcp-servers: [core-memory]
---

# /map-data

## Usage
- `/map-data --dataset examples/scientific/dataset_sample.csv --template examples/scientific/template_paper.txt`

## Heuristics
- Detect survival schema:
  - `time` (numeric), `event` (0/1 or boolean), `group` (categorical)
- Detect covariates: `age`, `sex`, `bmi`, `phase_angle`, `sarcopenia`
- Baseline Table: summarize by `group` (mean±sd, median[IQR], n(%))
- KM Curves: stratify by `group`
- Cox Model: `Surv(time, event) ~ group + age + sex + bmi (+ optional)`

## Output Contract (JSON)
```json
{
  "columns": {
    "time": "time",
    "event": "event",
    "group": "group",
    "covariates": ["age","sex","bmi","phase_angle","sarcopenia"]
  },
  "tasks": ["baseline_table","km_curve","cox_model"],
  "notes": ["binary event assumed 0/1", "group has 2+ levels"]
}
```

## Actions

1. Inspect CSV headers & types
2. Infer mapping → write `DataMapping` node in **core-memory**
3. If ambiguous → return ranked candidates with confidence