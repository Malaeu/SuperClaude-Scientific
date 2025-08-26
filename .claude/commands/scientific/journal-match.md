---
name: /journal-match
description: Intelligent journal selection and target analysis
category: workflow
complexity: intermediate
mcp-servers: [context7, sequential]
---

# /journal-match

## Usage
- `/journal-match analyze --research-type "clinical-trial" --domain "hepatology"`
- `/journal-match suggest --impact-factor ">10" --open-access true`
- `/journal-match compare --journals "Nature Medicine,Lancet,NEJM"`
- `/journal-match requirements --target "Lancet" --export checklist.md`

## Workflow Pattern
1) analyze → assess research scope, methodology, and clinical relevance
2) suggest → recommend journals based on fit, impact, and requirements
3) compare → detailed comparison of journal specifications
4) requirements → extract detailed submission requirements and checklists

## Notes
- This is a **context pattern** read by Claude Code; no executable code is run.
- Uses Context7 MCP for current journal databases and requirements
- Supports both high-impact and specialized journal selection

## Matching Criteria
- Research domain and specialty focus
- Study design appropriateness
- Clinical vs. methodological emphasis
- Impact factor and journal prestige
- Open access and publication costs

## Output Formats
- Journal recommendation reports
- Comparative requirement tables
- Submission checklists
- Timeline and process guidance