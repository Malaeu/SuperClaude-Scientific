---
name: /paper-clone
description: USPG pipeline driver (analyze-template, map-data, generate, refine)
category: workflow
mcp-servers: [context7, sequential, core-memory]
---

# /paper-clone

## Usage
- `/paper-clone analyze-template --template examples/scientific/template_paper.txt`
- `/paper-clone map-data --dataset examples/scientific/dataset_sample.csv`
- `/paper-clone generate --sections "methods,results"`
- `/paper-clone refine --journal "Nature Medicine"`

## Workflow Steps

### analyze-template
Parse template paper structure and extract:
- Section hierarchy (Introduction, Methods, Results, Discussion)
- Writing style patterns (sentence length, technical density)  
- Figure/table placeholders and formats
- Reference style and citation patterns

### map-data
Analyze dataset and propose statistical analysis plan:
- Detect survival analysis schema (time, event, group)
- Identify baseline characteristics for Table 1
- Suggest appropriate statistical tests
- Plan figure generation (KM curves, forest plots)

### generate
Generate manuscript sections based on template + data mapping:
- Methods: Study design, statistical analysis plan
- Results: Baseline characteristics, primary outcomes
- Figures: Kaplan-Meier curves, baseline table
- References: Formatted according to template style

### refine
If `--journal` is provided:
  1) activate `agent-journal-spec`
  2) fetch normalized `JournalGuideline` from **core-memory**
  3) compute compliance report:
     - word_counts (abstract/main/methods)
     - refs_style (Vancouver/Harvard; superscripts/brackets)
     - limits: figures/tables/panels; image_specs (dpi, width_mm)
  4) propose actionable edits and a diff plan per section/asset

## Integration
- Uses **core-memory** for persistent state across workflow steps
- Leverages `agent-journal-spec` for journal compliance
- Stores progress and intermediate results for incremental processing