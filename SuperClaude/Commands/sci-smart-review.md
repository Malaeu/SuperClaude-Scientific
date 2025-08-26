---
name: sci-smart-review
description: "Iterative smart literature review with progressive question refinement and knowledge gap identification"
category: scientific
complexity: advanced
mcp-servers: [sequential]
personas: [lit-scout, bc-transplant-expert, medical-stats-validator]
---

# /sc:sci-smart-review - Smart Literature Review Engine

## Triggers
- Literature review requirements for scientific manuscripts and grant applications
- Knowledge gap identification in specific medical research domains
- Systematic evidence synthesis for hypothesis generation and validation
- Progressive literature exploration with iterative question refinement
- Comprehensive evidence collection for meta-analyses and systematic reviews

## Usage
```
/sc:sci-smart-review [topic] [--iterations 10] [--years 2020-2025] [--domain liver|cardiac|general] [--depth comprehensive|focused] [--databases pubmed,wos,cochrane]
```

## Behavioral Flow
1. **Knowledge Base Assessment**: Analyze existing research materials and current understanding
2. **Initial Question Generation**: Formulate broad research questions based on current knowledge gaps
3. **Iterative Search Execution**: Conduct progressive literature searches with increasing specificity
4. **Gap Analysis**: Identify unexplored areas and methodological limitations in existing evidence
5. **Evidence Synthesis**: Integrate findings across iterations to build comprehensive understanding

Key behaviors:
- Executes up to 10 iterations of increasingly sophisticated literature searches
- Generates smart questions based on accumulating knowledge and identified gaps
- Uses Sequential MCP for systematic analysis and hypothesis testing
- Maintains evidence sufficiency monitoring to determine completion criteria
- Integrates domain expertise for clinically relevant question formulation

## Smart Review Loop Architecture

### Iteration Framework (10 Cycles Maximum)
```
Iteration 1-2: Foundational Knowledge
├── Broad domain coverage and basic understanding
├── Establish terminology and key concepts
└── Identify major research themes

Iteration 3-4: Methodological Focus
├── Study design patterns and statistical approaches
├── Population characteristics and outcome measures
└── Quality assessment and bias evaluation

Iteration 5-6: Clinical Applications
├── Patient populations and clinical contexts
├── Treatment outcomes and prognostic factors
└── Healthcare implementation and cost-effectiveness

Iteration 7-8: Knowledge Gaps
├── Unexplored research questions and populations
├── Methodological limitations and improvements needed
└── Novel applications and future directions

Iteration 9-10: Validation and Completion
├── Confirmation of identified gaps and opportunities
├── Evidence synthesis and systematic integration
└── Research priority ranking and feasibility assessment
```

### Question Evolution Pattern
- **Base Question**: "Body composition in liver transplant candidates"
- **Iteration 2**: "Sarcopenia prediction of waitlist mortality independent of MELD score"
- **Iteration 3**: "Serial CT measurements vs single assessments for prognosis improvement"
- **Iteration 4**: "Optimal timing and frequency of body composition monitoring"
- **Iteration 5**: "Cost-effectiveness of routine sarcopenia screening protocols"
- **Iteration 6**: "Interventions for sarcopenia reversal in liver disease"
- **Iteration 7**: "Machine learning applications in body composition analysis"
- **Iteration 8**: "Population-specific thresholds and diagnostic criteria"
- **Iteration 9**: "Integration with existing clinical decision tools"
- **Iteration 10**: "Implementation barriers and healthcare system requirements"

## Tool Coordination
- **Sequential MCP**: Multi-step analysis and systematic hypothesis testing
- **WebSearch**: Literature database querying and evidence retrieval
- **Read**: Existing research material analysis and knowledge base assessment
- **Write**: Iteration reports and evidence synthesis documentation
- **TodoWrite**: Progress tracking and milestone management

## Core Processing Capabilities

### Knowledge Base Management
- **Current State Assessment**: Analysis of existing research materials and preliminary findings
- **Gap Identification Matrix**: Systematic mapping of knowledge gaps across methodology, populations, and outcomes
- **Evidence Quality Scoring**: Assessment of study quality and methodological rigor
- **Research Timeline Tracking**: Historical context and temporal trends in evidence
- **Citation Network Analysis**: Identification of key papers and research communities

### Smart Question Generation
- **Context-Aware Formulation**: Questions informed by accumulating knowledge and clinical expertise
- **Specificity Progression**: Evolution from broad to highly targeted research questions
- **Clinical Relevance Assessment**: Prioritization of questions with practice-changing potential
- **Feasibility Evaluation**: Consideration of research practicality and resource requirements
- **Impact Prediction**: Assessment of potential contribution to existing knowledge

### Evidence Sufficiency Monitoring
- **Coverage Assessment**: Evaluation of breadth across key research dimensions
- **Quality Threshold**: Minimum standards for evidence quality and methodological rigor
- **Saturation Detection**: Identification of diminishing returns from additional searches
- **Gap Confirmation**: Validation of identified knowledge gaps through comprehensive coverage
- **Stopping Criteria**: Objective determination of review completion

## Advanced Search Strategies

### Database Integration
- **PubMed/MEDLINE**: Medical literature with MeSH term optimization
- **Web of Science**: Citation analysis and interdisciplinary coverage
- **Cochrane Library**: Systematic reviews and clinical trial registries
- **Embase**: European medical database with drug and device focus
- **Specialized Databases**: Domain-specific resources (UNOS, clinical registries)

### Search Optimization
- **Progressive Term Refinement**: Evolution of search terms based on retrieved literature
- **Citation Tracking**: Forward and backward citation analysis for comprehensive coverage
- **Author Network Analysis**: Identification of key researchers and collaboration patterns
- **Grey Literature Integration**: Conference proceedings, theses, and technical reports
- **Multilingual Considerations**: Non-English literature inclusion when appropriate

### Quality Filtering
- **Study Design Hierarchy**: Systematic reviews > RCTs > Cohort studies > Case series
- **Journal Impact Assessment**: Publication venue quality and credibility evaluation
- **Sample Size Adequacy**: Statistical power and generalizability considerations
- **Bias Risk Assessment**: Systematic evaluation using appropriate tools
- **Clinical Relevance Scoring**: Direct applicability to research questions and patient care

## Domain-Specific Optimization

### Body Composition Research
- **Measurement Techniques**: CT, DEXA, BIA, anthropometric methods
- **Clinical Populations**: Liver disease, cardiac conditions, oncology, aging
- **Outcome Measures**: Mortality, functional status, quality of life, healthcare utilization
- **Intervention Studies**: Exercise, nutrition, pharmacologic approaches
- **Biomarker Integration**: Laboratory values, imaging findings, functional assessments

### Liver Transplantation
- **Clinical Scores**: MELD, Child-Pugh, transplant-specific risk assessments
- **Outcome Categories**: Waitlist mortality, transplant eligibility, post-operative outcomes
- **Population Characteristics**: Etiology of liver disease, geographic variations, temporal trends
- **Healthcare Systems**: Organ allocation, center volume effects, disparities
- **Economic Considerations**: Cost-effectiveness, resource allocation, policy implications

## Output Structure

### Iteration Reports
```markdown
# Smart Review Iteration [N]: [Question]

## Search Strategy
- **Databases**: PubMed, Web of Science, Cochrane
- **Search Terms**: [MeSH terms and keywords]
- **Filters**: [Date range, study types, language]
- **Results**: [N] papers identified, [N] relevant after screening

## Key Findings
- **Novel Evidence**: [New findings not previously identified]
- **Methodological Insights**: [Study design patterns and statistical approaches]
- **Population Coverage**: [Demographics and clinical characteristics]
- **Outcome Patterns**: [Consistent findings and contradictory results]

## Knowledge Gaps Identified
- **Methodological**: [Limitations in study design or analysis]
- **Population**: [Underrepresented groups or clinical contexts]
- **Temporal**: [Outdated evidence requiring updated research]
- **Geographic**: [Limited representation from diverse populations]

## Next Iteration Question
**Rationale**: [Justification for next question based on current gaps]
**Specificity**: [How question builds on previous iterations]
**Clinical Impact**: [Potential contribution to patient care or research]
```

### Evidence Synthesis Dashboard
```json
{
  "review_progress": {
    "total_iterations": 10,
    "current_iteration": 7,
    "papers_reviewed": 347,
    "unique_references": 298,
    "evidence_sufficiency": "approaching_complete"
  },
  "knowledge_gaps": {
    "high_priority": [
      "Serial measurement protocols",
      "Population-specific thresholds",
      "Cost-effectiveness data"
    ],
    "medium_priority": [
      "Intervention effectiveness",
      "Machine learning applications"
    ],
    "low_priority": [
      "Historical perspectives",
      "Alternative measurement techniques"
    ]
  },
  "research_opportunities": {
    "methodology_improvements": 3,
    "population_studies": 5,
    "intervention_trials": 2,
    "implementation_research": 4
  }
}
```

## Quality Assurance Framework

### Iteration Validation
- **Question Appropriateness**: Clinical relevance and scientific merit evaluation
- **Search Completeness**: Comprehensive coverage of relevant databases and terms
- **Evidence Quality**: Systematic assessment of study methodology and reporting
- **Gap Identification**: Objective validation of identified knowledge gaps
- **Progress Assessment**: Measurable advancement in understanding across iterations

### Synthesis Quality
- **Thematic Consistency**: Logical organization and categorization of evidence
- **Bias Recognition**: Acknowledgment of publication bias and systematic limitations
- **Clinical Translation**: Appropriate emphasis on practice implications
- **Future Research**: Actionable recommendations for next research priorities
- **Methodological Rigor**: Adherence to systematic review principles

## Integration Workflows

### Manuscript Development
- **Introduction Background**: Comprehensive literature context for research rationale
- **Methods Benchmarking**: Comparison with established methodological standards
- **Discussion Framework**: Evidence-based interpretation and clinical implications
- **Future Research**: Prioritized research questions based on identified gaps

### Grant Application Support
- **Significance Justification**: Evidence-based rationale for research importance
- **Innovation Assessment**: Documentation of novel contributions to existing knowledge
- **Feasibility Evaluation**: Research practicality based on existing evidence patterns
- **Impact Prediction**: Potential contribution to clinical practice and patient outcomes

## Outputs
- **Iteration Reports**: Detailed documentation of each search iteration with findings and gaps
- **Evidence Synthesis**: Comprehensive integration of findings across all iterations
- **Research Gap Analysis**: Systematic identification of high-priority research opportunities
- **Reference Database**: Complete bibliography in RIS format with quality annotations
- **Research Priority Matrix**: Ranked opportunities based on impact potential and feasibility

## Quality Standards
- **Systematic Methodology**: Reproducible search strategies and evidence evaluation criteria
- **Comprehensive Coverage**: Multiple databases and comprehensive search term strategies
- **Objective Analysis**: Systematic bias assessment and quality evaluation
- **Clinical Relevance**: Focus on practice-relevant questions and patient-centered outcomes
- **Evidence Integration**: Thoughtful synthesis respecting study limitations and quality variations