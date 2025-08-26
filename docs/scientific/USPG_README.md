# 🧬 USPG: Universal Scientific Paper Generator

**Automated pipeline for transforming datasets into journal-ready manuscripts**

## Overview

USPG (Universal Scientific Paper Generator) is a SuperClaude extension that automates the process of creating scientific papers from datasets and templates. The system uses intelligent agents and commands to:

1. **Analyze** existing paper templates for structure and style
2. **Map** your dataset variables to appropriate statistical analyses  
3. **Generate** manuscript sections respecting journal requirements
4. **Refine** formatting and style for target journals

## How USPG Works in SuperClaude

**Important**: SuperClaude uses **context files** (.md), not executable code:
- Commands `/sc:*` are **context triggers** that Claude Code reads, not terminal commands
- Context files live in `~/.claude/...` (in our repo for installation)  
- Agents are specialized AI assistants activated by specific triggers
- MCP integration: **Sequential** (multi-step workflows), **core-memory** (graph-memory for project state), **Context7** (software docs, not journal rules)

## Quick Start Workflow

### 1. Initialize Project
```bash
/paper-clone init --dataset=examples/scientific/dataset_sample.csv --template=examples/scientific/template_paper.pdf
```

### 2. Analyze Template Structure
```bash
/paper-clone analyze-template
```
- Activates `agent-paper-parser`
- Extracts sections, word counts, figure patterns
- Builds structural template for your paper

### 3. Map Your Data
```bash
/paper-clone map-data
```
- Analyzes your dataset columns
- Suggests statistical analyses (Kaplan-Meier, Cox regression, baseline tables)
- Maps variables to appropriate manuscript sections

### 4. Generate Content
```bash
/paper-clone generate --sections "methods,results,discussion"
```
- Drafts manuscript sections based on template structure
- Respects word count limits from template analysis
- Integrates statistical analysis suggestions

### 5. Refine for Journal
```bash
/paper-clone refine --journal "Nature Medicine"
```
- Applies journal-specific formatting requirements
- Optimizes word counts, references, figure specifications
- Generates submission checklist

## Available Commands

| Command | Purpose | Key Features |
|---------|---------|--------------|
| `/paper-clone` | Main workflow driver | init, analyze-template, map-data, generate, refine |
| `/map-data` | Data analysis mapping | Variable type detection, statistical method suggestions |
| `/refine-style` | Journal formatting | Word counts, reference limits, citation styles |
| `/journal-match` | Journal selection | Impact factor, domain matching, requirements analysis |

## Scientific Agents

| Agent | Specialization | Triggers |
|-------|---------------|----------|
| `agent-paper-parser` | PDF structure analysis | "template", "analyze template", PDF files |
| `agent-figure-analyzer` | Figure/table analysis | "figure", "table", "chart analysis" |
| `agent-lit-scout` | Literature review | "literature", "citations", "smart review" |
| `agent-methods-validator` | Statistical validation | "methods", "statistics", "STROBE", "CONSORT" |
| `agent-journal-matcher` | Journal selection | "journal", "target journal", "impact factor" |

## MCP Server Integration

**Context7**: Journal pattern databases and formatting requirements
- Up-to-date journal specifications
- Citation style databases
- Formatting requirement templates

**Sequential**: Multi-step workflow orchestration
- Smart literature review iterations
- Progressive question refinement
- Workflow state management

**core-memory**: Project state graph persistence
- Template analysis caching as graph nodes
- Data mapping preferences stored as relationships
- Cross-session continuity via graph memory

## Example Dataset Structure

Your dataset should include columns like:
```csv
id, time, event, group, age, sex, bmi, phase_angle, sarcopenia
1, 365, 1, treatment, 65, M, 24.5, 5.2, 0
2, 180, 0, control, 58, F, 26.1, 4.8, 1
```

USPG automatically detects:
- **Survival analysis**: `time` + `event` columns → Kaplan-Meier curves
- **Baseline characteristics**: Categorical/continuous variables → Table 1
- **Group comparisons**: `group` variable → Statistical tests
- **Clinical outcomes**: Binary outcomes → Logistic regression

## Supported Journals

| Journal | Word Limit | References | Figures | Special Requirements |
|---------|------------|------------|---------|---------------------|
| Nature Medicine | 3,000 | 30 | 4 | Methods in supplement |
| Lancet | 4,500 | 60 | 5 | Structured abstract |
| NEJM | 2,700 | 40 | 6 | Trial registration |
| JAMA | 3,500 | 60 | 5 | Key points box |

## Installation in SuperClaude

1. **Clone Repository**:
   ```bash
   git clone https://github.com/Malaeu/SuperClaude-Scientific
   ```

2. **Copy Context Files**:
   ```bash
   # Agents
   cp -r .claude/agents/scientific ~/.claude/agents/
   
   # Commands  
   cp -r .claude/commands/scientific ~/.claude/commands/
   ```

3. **Verify MCP Servers**:
   Ensure Context7, Sequential, and core-memory MCP servers are configured in Claude Code.

## Workflow Example

**Input**: `dataset_patient_outcomes.csv` + `template_lancet_paper.pdf`

**Process**:
1. Template analysis extracts Lancet structure (4,500 words, 60 refs)
2. Data mapping suggests survival analysis + baseline characteristics
3. Content generation creates Methods, Results, Discussion sections
4. Style refinement applies Lancet formatting requirements

**Output**: Complete manuscript draft ready for expert review and submission

## Technical Notes

- **No executable code**: Everything works through Claude Code's context system
- **Agent coordination**: Agents work together through trigger patterns
- **MCP integration**: External tools enhance core functionality
- **Session persistence**: core-memory MCP maintains graph state across sessions
- **Journal adaptation**: Context7 MCP provides current formatting requirements

## Next Steps

1. Try the example workflow with `examples/scientific/dataset_sample.csv`
2. Analyze your own template papers using `agent-paper-parser`
3. Map your research datasets with `/map-data` suggestions
4. Generate manuscript sections for your target journal

**Result**: From dataset to journal submission in days, not months! 🚀