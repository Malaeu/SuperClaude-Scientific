---
name: sci-init
description: "Initialize scientific paper project with structured directories and analysis framework"
category: scientific
complexity: basic
mcp-servers: []
personas: [paper-parser, bc-transplant-expert]
---

# /sc:sci-init - Scientific Project Initialization

## Triggers
- New scientific paper project setup requirements
- Medical research data organization and analysis preparation
- Body composition and liver transplant research project initialization
- Structured manuscript writing environment creation

## Usage
```
/sc:sci-init [project-name] [--type medical|clinical|basic] [--journal nature|lancet|nejm] [--domain liver|cardiac|oncology]
```

## Behavioral Flow
1. **Project Structure Creation**: Establish organized directory hierarchy for research project
2. **Template Generation**: Create manuscript templates tailored to target journal requirements
3. **Data Environment Setup**: Prepare analysis environment for CSV datasets and PDF processing
4. **Knowledge Base Initialization**: Set up literature review and reference management systems
5. **Workflow Configuration**: Configure scientific workflow with appropriate agents and tools

Key behaviors:
- Creates standardized project structure optimized for medical research
- Generates journal-specific manuscript templates with proper formatting
- Initializes literature review tracking system with iteration counter
- Sets up analysis environment for body composition and clinical data
- Configures agent workflows for systematic paper development

## Project Structure Template

### Directory Hierarchy
```
{project-name}/
├── data/
│   ├── raw/                    # Original datasets (CSV, Excel)
│   ├── processed/              # Cleaned and analysis-ready data
│   └── figures/               # Generated plots and visualizations
├── manuscripts/
│   ├── drafts/                # Working manuscript versions
│   ├── templates/             # Journal-specific templates
│   └── submissions/           # Final formatted submissions
├── literature/
│   ├── reviews/               # Smart review iterations
│   ├── references/            # Reference database (RIS format)
│   └── annotations/           # Key paper summaries
├── analysis/
│   ├── scripts/               # Statistical analysis code
│   ├── results/               # Analysis outputs
│   └── validation/            # Statistical validation reports
├── presentations/
│   ├── parsed/                # PDF extraction results
│   └── figures/               # Extracted figure descriptions
└── supplements/
    ├── methods/               # Detailed methodology
    ├── results/               # Additional results
    └── figures/               # Supplementary figures
```

### Configuration Files
- **project_config.json**: Project metadata, journal targets, research domain
- **workflow_config.json**: Agent assignments and processing pipelines
- **literature_tracker.json**: Smart review progress and iteration tracking
- **reference_manager.json**: Citation database and formatting preferences

## Tool Coordination
- **Glob**: Directory structure creation and template file organization
- **Write**: Template generation and configuration file creation
- **Read**: Existing project assessment and template customization
- **TodoWrite**: Project milestone and workflow task creation

## Template Generation

### Manuscript Templates by Journal
- **Nature Template**: 3,000-word limit, 30 references, 4 main figures
- **Lancet Template**: 4,500-word limit, 60 references, structured abstract
- **NEJM Template**: 2,700-word limit, 40 references, clinical emphasis
- **JAMA Template**: 3,500-word limit, 60 references, public health focus

### Smart Review Configuration
- **Iteration Planning**: 10-iteration literature review framework
- **Question Evolution**: Progressive question sophistication tracking
- **Knowledge Gap Tracking**: Systematic gap identification system
- **Reference Management**: Automated deduplication and RIS formatting

### Statistical Analysis Framework
- **Power Calculations**: Sample size and effect size planning templates
- **STROBE Compliance**: Observational study reporting checklist
- **Clinical Endpoints**: Primary and secondary outcome definition
- **Statistical Software**: R/Python/SAS analysis template configurations

## Domain-Specific Initialization

### Medical Research (Default)
- **Clinical Data Structure**: Patient demographics, outcomes, biomarkers
- **Statistical Methods**: Survival analysis, regression modeling, ROC analysis
- **Regulatory Compliance**: IRB approval tracking, consent documentation
- **Publication Strategy**: High-impact journal targeting and timeline planning

### Body Composition Research
- **Imaging Data**: CT scan processing, DEXA analysis, anthropometrics
- **Clinical Outcomes**: Mortality, morbidity, functional status measures
- **Statistical Modeling**: Time-to-event analysis, competing risks
- **Literature Focus**: Sarcopenia, frailty, transplant outcomes

### Liver Transplant Research
- **Clinical Scores**: MELD, Child-Pugh, transplant-specific metrics
- **Outcome Measures**: Waitlist mortality, post-transplant survival
- **Data Sources**: UNOS, institutional databases, multi-center studies
- **Regulatory Considerations**: Transplant-specific ethical requirements

## Quality Assurance Framework

### Project Validation
- **Directory Integrity**: All required directories created successfully
- **Template Completeness**: All journal templates properly configured
- **Configuration Validity**: JSON configuration files properly formatted
- **Workflow Consistency**: Agent assignments aligned with project type

### Documentation Standards
- **README Generation**: Project overview and workflow documentation
- **Methodology Documentation**: Statistical analysis plan template
- **Data Dictionary**: Variable definitions and coding schemes
- **Timeline Planning**: Milestone tracking and deadline management

## Advanced Features

### Multi-Journal Strategy
- **Simultaneous Templates**: Multiple journal format preparation
- **Priority Hierarchy**: Primary, secondary, tertiary journal targets
- **Content Optimization**: Journal-specific emphasis and formatting
- **Submission Tracking**: Timeline coordination and revision management

### Collaboration Framework
- **Version Control**: Git integration for manuscript collaboration
- **Author Contributions**: CRediT taxonomy implementation
- **Review Coordination**: Peer review and revision tracking
- **Publication Timeline**: From submission to publication planning

### Data Integration
- **Multiple Formats**: CSV, Excel, SPSS, SAS data import templates
- **Image Processing**: PDF figure extraction and analysis preparation
- **Database Connectivity**: REDCap, clinical database integration
- **Privacy Compliance**: HIPAA-compliant data handling procedures

## Outputs
- **Complete Project Structure**: Organized directory hierarchy with all necessary folders
- **Journal-Specific Templates**: Manuscript templates formatted for target journals
- **Configuration Framework**: Project settings and workflow configurations
- **Analysis Environment**: Statistical analysis and data processing setup
- **Documentation System**: README files and methodology documentation

## Examples

### Basic Medical Research Project
```
/sc:sci-init liver-bc-study --type medical --journal lancet --domain liver
```
Creates project structure for liver/body composition research targeted at The Lancet

### Multi-Journal Clinical Study
```
/sc:sci-init sarcopenia-outcomes --type clinical --journal nature,lancet,nejm --domain liver
```
Sets up clinical study with templates for multiple high-impact journals

### Basic Science Project
```
/sc:sci-init mechanisms-study --type basic --journal nature --domain basic
```
Initializes basic science research project with Nature formatting

## Quality Standards
- **Complete Structure**: All required directories and files created
- **Template Accuracy**: Journal-specific formatting properly implemented
- **Configuration Integrity**: All JSON configuration files valid and complete
- **Documentation Clarity**: Clear README and methodology documentation
- **Workflow Readiness**: All agents and tools properly configured for project type