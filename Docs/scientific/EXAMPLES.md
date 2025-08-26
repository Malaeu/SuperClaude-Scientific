# 📚 USPG Examples and Use Cases

**Real-world examples of the Universal Scientific Paper Generator in action**

## Example 1: Clinical Trial Analysis

### Scenario
You have a dataset from a hepatology clinical trial comparing treatment outcomes.

### Dataset Structure
```csv
patient_id,treatment_group,time_to_event,event_occurred,age,sex,bmi,baseline_meld,phase_angle,sarcopenia
HEP001,treatment,365,0,65,M,24.5,18,5.2,0
HEP002,control,180,1,58,F,26.1,22,4.8,1
HEP003,treatment,450,0,72,M,23.8,20,5.5,0
```

### Workflow
```bash
# 1. Initialize with your data and a Lancet template
/paper-clone init --dataset=hep_trial.csv --template=lancet_template.pdf

# 2. Analyze the template structure
/paper-clone analyze-template
# → Extracts: 4500 words, structured abstract, 60 refs max

# 3. Map your data to analyses
/paper-clone map-data
# → Suggests: Kaplan-Meier (time_to_event), baseline table (demographics), Cox regression

# 4. Generate manuscript sections
/paper-clone generate --sections "methods,results,discussion"
# → Creates draft sections with proper statistical analysis

# 5. Refine for Lancet submission
/paper-clone refine --journal "Lancet"
# → Applies Lancet formatting, structured abstract, citation style
```

### Expected Output
- **Methods**: Study design, statistical analysis plan
- **Results**: Baseline characteristics table, Kaplan-Meier curves, Cox regression results  
- **Discussion**: Clinical implications, limitations, conclusions
- **Figures**: Survival curves with 95% CI, forest plots for subgroups
- **Tables**: Patient characteristics, primary/secondary outcomes

---

## Example 2: Observational Cohort Study

### Scenario
Retrospective analysis of body composition in liver transplant candidates.

### Dataset Structure
```csv
patient_id,enrollment_date,outcome_date,died,transplanted,age,sex,etiology,meld,smi,sarcopenia
BC001,2023-01-15,2023-12-15,0,1,56,F,NASH,15,42.3,1
BC002,2023-02-20,2023-11-10,1,0,68,M,ALD,28,38.1,1
BC003,2023-03-10,2024-01-15,0,0,45,F,HCV,12,48.7,0
```

### Advanced Workflow
```bash
# Detailed data analysis
/map-data analyze --dataset=bc_cohort.csv
# → Identifies: competing risks (death vs transplant), time-varying covariates

# Literature integration
/lit-scout progressive --topic "body composition liver transplant sarcopenia"
# → 10 iterations of literature review, identifies research gaps

# Methods validation
/methods-validator check --study-type "retrospective-cohort" --statistical-plan cox-competing-risks.json
# → Validates statistical approach, suggests STROBE compliance

# Multi-journal comparison
/journal-match compare --journals "Hepatology,Journal of Hepatology,Liver Transplantation"
# → Compares fit, impact factor, formatting requirements
```

---

## Example 3: Systematic Review and Meta-Analysis

### Scenario
Meta-analysis of sarcopenia prevalence in chronic liver disease.

### Template Analysis
```bash
# Analyze PRISMA-compliant template
/paper-clone analyze-template --template=prisma_template.pdf
# → Extracts: PRISMA flow diagram, forest plot specifications, risk of bias tables

# Literature extraction
/lit-scout systematic --search-strategy cochrane --databases "pubmed,embase,central"
# → Systematic search with iterative refinement, study selection criteria

# Data synthesis
/map-data meta-analysis --outcome-type "prevalence" --heterogeneity-assessment i2
# → Random-effects models, subgroup analysis planning, sensitivity analysis
```

---

## Example 4: Figure and Table Generation

### Advanced Figure Analysis
```bash
# Analyze template figures
/figure-analyzer template --source=template_paper.pdf --page=3
# → Extracts: Kaplan-Meier curve specifications, color scheme, confidence intervals

# Map data to figure requirements
/map-data visualize --figure-type "kaplan-meier" --groups "treatment,control"
# → Generates: figure specifications, statistical annotations, layout requirements

# Generate figure code
/paper-clone generate --sections "figures" --format "R-ggplot2"
# → Creates: R code for manuscript-ready figures
```

### Table Generation
```bash
# Baseline characteristics table
/map-data table --type "baseline" --variables "age,sex,bmi,meld" --groups "treatment,control"
# → Generates: Table 1 with appropriate statistics (mean±SD, n(%), p-values)

# Results table for survival analysis
/map-data table --type "cox-regression" --outcome "time_to_death" --covariates "age,sex,treatment"
# → Generates: Hazard ratios with 95% CI, p-values, model statistics
```

---

## Example 5: Multi-Journal Adaptation

### Single Dataset, Multiple Journals
```bash
# Generate Nature Medicine version
/refine-style --journal "Nature Medicine" --word-limit 3000 --focus "clinical-significance"
# → Emphasizes clinical impact, moves methods to supplement

# Generate Lancet version  
/refine-style --journal "Lancet" --structured-abstract --word-limit 4500
# → Structured abstract, detailed methods in main text

# Generate NEJM version
/refine-style --journal "NEJM" --clinical-focus --trial-registration check
# → Clinical perspective, trial registration verification, key points summary
```

---

## Example 6: Quality Assurance Workflow

### Statistical Validation
```bash
# Comprehensive methods review
/methods-validator comprehensive --checklist "STROBE,CONSORT,STARD"
# → Validates: study design, statistical methods, reporting completeness

# Power analysis check
/methods-validator power --effect-size 0.3 --alpha 0.05 --power 0.80
# → Assesses: sample size adequacy, detectable effect sizes

# Assumption testing
/methods-validator assumptions --test "cox-proportional-hazards" --dataset bc_cohort.csv
# → Tests: proportional hazards assumption, linearity, outliers
```

### Literature Validation
```bash
# Citation accuracy check
/lit-scout validate --references manuscript_refs.bib --databases "pubmed,crossref"
# → Validates: DOIs, citation accuracy, journal abbreviations

# Gap analysis
/lit-scout gaps --topic "current-research" --existing-literature refs.json
# → Identifies: research gaps, novelty claims, positioning statements
```

---

## Common Use Case Patterns

### Pattern 1: RCT Analysis
1. `/paper-clone init` → Set up project
2. `/paper-clone analyze-template` → Extract CONSORT structure  
3. `/map-data` → Primary/secondary endpoints, ITT analysis
4. `/methods-validator` → CONSORT compliance check
5. `/refine-style` → Journal-specific formatting

### Pattern 2: Observational Study
1. Template analysis → Extract cohort study structure
2. Data mapping → Survival analysis, confounders
3. Literature review → Background, comparisons  
4. Methods validation → STROBE compliance
5. Multi-journal adaptation → Target journal selection

### Pattern 3: Meta-Analysis
1. PRISMA template → Systematic review structure
2. Literature extraction → Study selection, data extraction
3. Statistical synthesis → Random-effects models
4. Quality assessment → Risk of bias, GRADE
5. Publication → High-impact journal formatting

---

## Tips for Success

### Data Preparation
- **Clean column names**: Use descriptive, standardized names
- **Missing data**: Code consistently (NA, blank, or specific codes)  
- **Date formats**: Use ISO format (YYYY-MM-DD) for consistency
- **Categorical variables**: Use clear factor levels

### Template Selection
- **Choose similar studies**: Same design, similar analysis approach
- **High-quality journals**: Better structure and reporting standards
- **Recent publications**: Current formatting and style requirements
- **Domain-specific**: Templates from your research field

### Workflow Optimization  
- **Start simple**: Use basic workflow first, then add complexity
- **Iterate frequently**: Generate drafts early, refine progressively
- **Validate methods**: Always run statistical validation checks
- **Multi-journal**: Consider multiple target journals from the start

### Quality Control
- **Statistical review**: Always validate analysis approaches
- **Literature validation**: Check citation accuracy and completeness
- **Format checking**: Verify journal requirement compliance
- **Expert review**: USPG assists but doesn't replace expert judgment

---

## Troubleshooting

### Common Issues

**Dataset not recognized**:
- Check CSV format and column headers
- Ensure proper encoding (UTF-8)
- Verify data types (numeric, categorical, dates)

**Template analysis fails**:
- Use PDF format for templates (not Word or HTML)
- Ensure readable text (not scanned images)
- Try templates from recent publications (last 2-3 years)

**Statistical mapping unclear**:
- Review variable types and distributions
- Clarify research questions and hypotheses  
- Consult domain expert for analysis approach

**Journal formatting issues**:
- Update Context7 MCP for latest requirements
- Check journal website for current guidelines
- Consider journal-specific templates

---

**Next Steps**: Try these examples with your own data and templates to see USPG in action! 🚀