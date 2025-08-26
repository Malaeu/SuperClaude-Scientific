---
name: sci-parse
description: "Parse scientific presentations and papers using page-by-page analysis"
category: scientific
complexity: advanced
mcp-servers: [context7]
personas: [paper-parser, bc-transplant-expert]
---

# /sc:sci-parse - Scientific Document Parser

## Triggers
- PDF research papers and presentations requiring structured analysis
- Medical manuscripts needing comprehensive content extraction
- Scientific documents with figures, tables, and statistical data
- Multi-page presentations from conferences or research meetings
- Clinical research papers requiring systematic information extraction

## Usage
```
/sc:sci-parse [pdf-path] [--output-dir ./analysis] [--focus results|methods|figures] [--depth quick|comprehensive] [--domain liver|cardiac|general]
```

## Behavioral Flow
1. **Document Analysis**: Systematic page-by-page examination using Claude Code's native PDF reader
2. **Content Categorization**: Classification of pages by content type (methods, results, figures, references)
3. **Information Extraction**: Comprehensive extraction of text, figures, tables, and statistical data
4. **Knowledge Graph Construction**: Building interconnected understanding of document content
5. **Structured Output Generation**: Creation of organized analysis files and summaries

Key behaviors:
- Utilizes Claude Code's native PDF reading capabilities for direct document access
- Performs incremental knowledge building with cross-page context maintenance
- Extracts and describes all visual content including figures and tables
- Generates structured markdown output with categorized information
- Integrates domain expertise for medical and scientific content interpretation

## Core Processing Capabilities

### Page-by-Page Analysis
- **Document Structure Recognition**: Title pages, abstracts, methods, results, discussion sections
- **Content Type Classification**: Text content, figures, tables, equations, references
- **Cross-Reference Tracking**: Links between figures, tables, and text references
- **Statistical Information Extraction**: P-values, confidence intervals, sample sizes
- **Citation Collection**: Reference extraction and bibliographic information capture

### Visual Content Processing
- **Figure Description**: Detailed analysis of graphs, charts, and clinical images
- **Table Extraction**: Structured data extraction from tables and clinical datasets
- **Statistical Graphics**: Kaplan-Meier curves, ROC curves, forest plots interpretation
- **Clinical Images**: CT scans, MRI images, histology slides description
- **Data Point Extraction**: Numerical values and trends from visualizations

### Medical Content Specialization
- **Clinical Terminology**: Medical term recognition and context interpretation
- **Statistical Methods**: Recognition of appropriate statistical tests and results
- **Study Design**: Identification of research methodology and study type
- **Outcome Measures**: Primary and secondary endpoints identification
- **Population Characteristics**: Demographics and clinical characteristics extraction

## Tool Coordination
- **Read**: Native PDF processing using Claude Code's built-in capabilities
- **Write**: Structured output generation in markdown and JSON formats
- **Context7**: Medical framework and methodology pattern recognition
- **Grep**: Content pattern matching and information extraction
- **TodoWrite**: Processing milestone tracking and workflow management

## Output Structure

### Comprehensive Analysis Report
```markdown
# Document Analysis: [Title]

## Executive Summary
- **Document Type**: Research paper/presentation/thesis
- **Research Domain**: Clinical/basic science/epidemiological
- **Study Population**: [N] participants with [characteristics]
- **Key Findings**: Primary outcomes and statistical significance

## Page-by-Page Analysis
### Page 1-2: Title and Abstract
- **Title**: [Full title extraction]
- **Authors**: [Author list with affiliations]
- **Abstract**: [Structured abstract with background, methods, results, conclusions]
- **Keywords**: [Key terms and MeSH headings]

### Page 3-5: Methods
- **Study Design**: [Observational/experimental design type]
- **Population**: [Inclusion/exclusion criteria, demographics]
- **Statistical Methods**: [Analysis plan and software used]
- **Ethical Approval**: [IRB approval and consent procedures]

### Page 6-12: Results
- **Primary Outcomes**: [Main findings with statistics]
- **Secondary Outcomes**: [Additional findings and subgroup analyses]
- **Figures**: [Detailed description of each figure]
- **Tables**: [Structured extraction of tabular data]

### Page 13-15: Discussion and References
- **Key Interpretations**: [Clinical significance and limitations]
- **Future Research**: [Identified gaps and recommendations]
- **References**: [Complete bibliography in structured format]
```

### Figure Analysis Database
```json
{
  "figures": [
    {
      "figure_number": "Figure 1",
      "page": 8,
      "type": "Kaplan-Meier survival curve",
      "description": "Waitlist survival stratified by sarcopenia status",
      "key_findings": "Sarcopenic patients: median survival 8.2 months vs 14.7 months (p<0.001)",
      "statistical_details": {
        "p_value": "<0.001",
        "hazard_ratio": "2.34",
        "confidence_interval": "1.67-3.28",
        "sample_size": "n=432"
      }
    }
  ],
  "tables": [
    {
      "table_number": "Table 2",
      "page": 6,
      "title": "Baseline characteristics by body composition status",
      "variables": ["age", "gender", "MELD", "BMI", "SMI"],
      "statistical_tests": "Chi-square and t-tests",
      "key_comparisons": "Sarcopenic vs non-sarcopenic groups"
    }
  ]
}
```

## Advanced Processing Features

### Context-Aware Extraction
- **Cross-Page Relationships**: Connecting methods descriptions with results tables
- **Reference Integration**: Linking in-text citations with bibliography
- **Figure-Text Correlation**: Matching figure references with descriptive text
- **Statistical Consistency**: Verifying statistical reporting across sections
- **Methodology Validation**: Ensuring results align with stated methods

### Domain-Specific Processing
- **Body Composition Research**: Sarcopenia definitions, CT measurements, functional assessments
- **Liver Disease Studies**: MELD scores, Child-Pugh classifications, transplant outcomes
- **Clinical Trials**: CONSORT compliance, randomization details, intention-to-treat analysis
- **Epidemiological Studies**: STROBE adherence, confounding variables, bias assessment

### Quality Assurance
- **Completeness Verification**: Ensuring all pages processed successfully
- **Content Validation**: Cross-checking extracted information for consistency
- **Statistical Accuracy**: Verifying numerical extraction precision
- **Figure Description Quality**: Comprehensive visual content interpretation
- **Reference Completeness**: Complete bibliographic information capture

## Integration Workflows

### Literature Review Preparation
- **Reference Export**: RIS format for reference manager import
- **Gap Identification**: Comparison with existing knowledge for research opportunities
- **Methodology Benchmarking**: Comparison with established methodological standards
- **Statistical Power Assessment**: Sample size and effect size evaluation

### Manuscript Development
- **Methods Template**: Extracted methodology for replication studies
- **Results Framework**: Statistical reporting templates based on extracted examples
- **Figure Standards**: Visual presentation benchmarks from high-quality papers
- **Discussion Points**: Key interpretations and clinical implications identification

## Specialized Processing Modes

### Quick Analysis Mode
- **Key Information Only**: Executive summary, main findings, statistical significance
- **Figure Overview**: Basic figure descriptions without detailed statistical extraction
- **Reference List**: Complete bibliography without detailed annotation
- **Processing Time**: Optimized for rapid document review

### Comprehensive Mode
- **Complete Extraction**: All text, figures, tables, and statistical information
- **Detailed Annotations**: Extensive figure descriptions and methodological analysis
- **Cross-Reference Mapping**: Complete citation and reference relationship mapping
- **Quality Assessment**: Methodological rigor and statistical appropriateness evaluation

### Domain-Focused Mode
- **Liver Research**: Specialized extraction of transplant-specific metrics and outcomes
- **Body Composition**: Focus on sarcopenia definitions, measurement techniques, and outcomes
- **Clinical Trials**: Emphasis on trial design, endpoints, and statistical analysis plans

## Outputs
- **Structured Analysis Report**: Comprehensive markdown document with all extracted information
- **Figure Database**: JSON database of all visual content with detailed descriptions
- **Reference Collection**: RIS-formatted bibliography for literature management
- **Statistical Summary**: Extracted numerical data and statistical test results
- **Knowledge Graph**: Interconnected representation of document content relationships

## Quality Standards
- **Complete Coverage**: All pages and content types systematically processed
- **Accuracy Preservation**: Faithful extraction without interpretation bias
- **Structured Organization**: Consistent formatting and categorization of extracted information
- **Visual Content Quality**: Comprehensive description of all figures and tables
- **Reference Integrity**: Complete and accurate bibliographic information extraction