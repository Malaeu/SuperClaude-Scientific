---
name: /paper-clone
description: USPG pipeline driver (analyze-template, map-data, generate, refine)
category: workflow
complexity: advanced
mcp-servers: [sequential, core-memory, context7]
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

### refine
- Если указан `--journal`:
  1) активировать `agent-journal-spec`
  2) получить из core-memory нормализованные правила `JournalGuideline`
  3) сформировать compliance-report (word_counts, refs_style, figures/tables/image_specs)
  4) выдать список правок по секциям и ссылкам, ограничениям на фигуры/таблицы

## Notes
- This is a **context pattern** read by Claude Code; no executable code is run.
- **Sequential** → многошаговый пайплайн.
- **core-memory** → проектный **graph**: хранит Template structure, Style metrics, JournalGuideline, ReviewIteration.
- **Context7** → использовать для **технической документации** по софту/библиотекам, не для правил журналов.

## State Management
- Project state stored in **core-memory graph** (nodes: Section, Subsection, Transition, FigureSpec, TableSpec, StyleMetrics, JournalGuideline, ReviewIteration).
- Template analysis cached for reuse
- Data mapping preferences remembered
- Journal formatting applied consistently

## Integration Points
- Triggers scientific agents based on workflow step
- Coordinates with other /sc: commands
- Maintains session context across iterations