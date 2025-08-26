#!/usr/bin/env python3
"""
Body Composition in Liver Transplantation - Scientific Pipeline Demo

This script demonstrates the complete SuperClaude-Scientific pipeline for
creating a research paper on body composition in liver transplantation
waiting list patients.

Usage:
    python bc_liver_transplant_demo.py
"""

import sys
import os
from pathlib import Path

# Add SuperClaude Scientific module to path
sys.path.append(str(Path(__file__).parent.parent / "SuperClaude"))

from Scientific import SmartReviewEngine, ReferenceManager, JournalFormatter
import json
import datetime

def main():
    """Main demo function showing complete scientific workflow."""
    
    print("🧬 SuperClaude-Scientific Demo: Body Composition in Liver Transplantation")
    print("=" * 80)
    
    # Step 1: Initialize project with Smart Review Engine
    print("\n📚 Step 1: Initializing Smart Literature Review")
    print("-" * 50)
    
    review_engine = SmartReviewEngine(
        project_name="BC_Liver_Transplant_Study",
        domain="liver", 
        max_iterations=10
    )
    
    # Start review with initial broad question
    initial_question = "Body composition assessment and outcomes in liver transplant waiting list patients"
    
    print(f"Initial Research Question: {initial_question}")
    
    review_status = review_engine.start_review(
        initial_question=initial_question,
        research_context={
            "study_population": "432 liver transplant candidates",
            "primary_outcome": "waitlist mortality",
            "measurement_methods": ["CT-based SMI", "DEXA", "anthropometrics"],
            "follow_up": "median 12 months"
        }
    )
    
    print(f"✅ Review initialized successfully")
    print(f"Search terms: {', '.join(review_status['search_terms'])}")
    
    # Step 2: Simulate iterative literature review
    print("\n🔍 Step 2: Simulating Smart Review Iterations")
    print("-" * 50)
    
    # Simulate search results for first iteration
    mock_search_results_1 = [
        {
            "title": "Sarcopenia in patients with end-stage liver disease: A systematic review",
            "authors": ["Smith J", "Johnson M", "Williams R"],
            "year": 2023,
            "journal": "Hepatology",
            "impact_factor": 11.4,
            "study_type": "systematic review",
            "sample_size": 2456,
            "abstract": "Systematic review of sarcopenia in liver disease patients...",
            "doi": "10.1002/hep.32456",
            "relevance_score": 0.92
        },
        {
            "title": "CT-based body composition analysis predicts mortality in cirrhotic patients",
            "authors": ["Brown A", "Davis K", "Miller L"],
            "year": 2024,
            "journal": "Journal of Hepatology",
            "impact_factor": 20.5,
            "study_type": "cohort study",
            "sample_size": 345,
            "abstract": "Prospective cohort study examining CT-based measurements...",
            "doi": "10.1016/j.jhep.2024.01.012",
            "relevance_score": 0.89
        },
        {
            "title": "MELD score and sarcopenia interaction in liver transplant outcomes",
            "authors": ["Taylor P", "Anderson C", "Wilson D"],
            "year": 2023,
            "journal": "American Journal of Transplantation",
            "impact_factor": 8.9,
            "study_type": "retrospective analysis",
            "sample_size": 1234,
            "abstract": "Analysis of UNOS database examining interaction effects...",
            "doi": "10.1111/ajt.17234",
            "relevance_score": 0.85
        }
    ]
    
    # Execute first iteration
    iteration_1_results = review_engine.execute_iteration(1, mock_search_results_1)
    
    print(f"Iteration 1 Complete:")
    print(f"  Papers found: {iteration_1_results['papers_found']}")
    print(f"  Relevant papers: {iteration_1_results['papers_relevant']}")
    print(f"  Next question: {iteration_1_results['next_question']}")
    print(f"  Evidence sufficiency: {iteration_1_results['evidence_sufficiency']}")
    
    # Step 3: Reference Management
    print("\n📖 Step 3: Reference Management")
    print("-" * 50)
    
    ref_manager = ReferenceManager(project_name="BC_Liver_Transplant_Study")
    
    # Add references from literature review
    for paper in mock_search_results_1:
        ref_id = ref_manager.add_reference(paper)
        print(f"Added reference: {ref_id} - {paper['title'][:50]}...")
    
    # Generate statistics
    stats = ref_manager.generate_statistics()
    print(f"\n📊 Reference Statistics:")
    print(f"  Total references: {stats['total_references']}")
    print(f"  High quality papers: {stats['quality_distribution']['high_quality']}")
    print(f"  Recent papers (5 years): {stats['year_distribution']['recent_5_years']}")
    
    # Export references in different formats
    print(f"\n💾 Exporting references:")
    
    # RIS format for EndNote/Mendeley
    ref_manager.export_ris("examples/bc_study_references.ris")
    print(f"  ✅ RIS format exported")
    
    # BibTeX format for LaTeX
    ref_manager.export_bibtex("examples/bc_study_references.bib")
    print(f"  ✅ BibTeX format exported")
    
    # CSV for analysis
    ref_manager.export_csv("examples/bc_study_references.csv")
    print(f"  ✅ CSV format exported")
    
    # Step 4: Journal Formatting
    print("\n📄 Step 4: Journal Formatting")
    print("-" * 50)
    
    # Create sample manuscript content
    sample_manuscript = """# Body Composition Assessment Predicts Mortality in Liver Transplant Candidates: A Prospective Cohort Study

## Abstract

Background: Sarcopenia is associated with poor outcomes in patients with end-stage liver disease, but optimal assessment methods remain unclear. We evaluated the prognostic value of different body composition measures in liver transplant candidates.

Methods: Prospective cohort study of 432 adult liver transplant candidates. CT-based skeletal muscle index (SMI), DEXA-derived appendicular lean mass, and anthropometric measures were assessed. Primary outcome was waitlist mortality.

Results: During median follow-up of 12 months, 89 patients died (20.6%). Sarcopenic patients (SMI <50 cm²/m² men, <39 cm²/m² women) had significantly higher mortality (HR 2.34, 95% CI 1.67-3.28, p<0.001). CT-based SMI provided superior prognostic value compared to other measures (C-statistic 0.72 vs 0.65, p=0.003).

Conclusions: CT-based skeletal muscle index is a strong independent predictor of waitlist mortality in liver transplant candidates and should be incorporated into routine clinical assessment.

## Introduction

End-stage liver disease is associated with profound alterations in body composition, including loss of skeletal muscle mass (sarcopenia) and changes in fat distribution. These changes have important prognostic implications for patients awaiting liver transplantation...

## Methods

### Study Design and Participants
We conducted a prospective observational cohort study at a large academic medical center from January 2020 to December 2022. Adult patients (≥18 years) newly listed for liver transplantation were eligible...

### Body Composition Assessment
CT-based measurements were performed using axial images at the L3 vertebral level. Skeletal muscle area was calculated using Hounsfield unit thresholds of -29 to +150...

### Statistical Analysis
Survival analysis was performed using Kaplan-Meier curves and Cox proportional hazards regression. Statistical significance was set at p<0.05...

## Results

### Patient Characteristics
A total of 432 patients were included (mean age 56.2 years, 62% male). Primary liver diseases included NASH (34%), alcohol-related liver disease (28%), and viral hepatitis (22%)...

### Body Composition Measurements
Mean SMI was 48.7 ± 12.3 cm²/m² in men and 37.2 ± 9.8 cm²/m² in women. Sarcopenia was present in 198 patients (45.8%)...

### Clinical Outcomes
During median follow-up of 12.3 months, 89 patients died (20.6%) and 187 underwent transplantation (43.3%)...

## Discussion

This large prospective study demonstrates that CT-based skeletal muscle index is a powerful predictor of waitlist mortality in liver transplant candidates, independent of MELD score and other clinical factors...

### Limitations
Several limitations should be acknowledged. First, this was a single-center study which may limit generalizability...

## Conclusion

CT-based assessment of skeletal muscle mass provides valuable prognostic information in liver transplant candidates and should be considered for integration into routine clinical assessment protocols.
"""
    
    # Initialize journal formatter
    formatter = JournalFormatter("examples")
    
    # Save manuscript to file
    manuscript_file = Path("examples/bc_manuscript.md")
    with open(manuscript_file, 'w') as f:
        f.write(sample_manuscript)
    
    # Load manuscript
    load_result = formatter.load_manuscript("bc_manuscript.md")
    print(f"📄 Manuscript loaded:")
    print(f"  Sections: {len(load_result['sections'])}")
    print(f"  Total words: {load_result['total_word_count']}")
    
    # Format for different journals
    target_journals = ["nature", "lancet", "nejm"]
    
    for journal in target_journals:
        print(f"\n🎯 Formatting for {journal.upper()}:")
        
        try:
            format_result = formatter.format_for_journal(journal, f"examples/{journal}_submission")
            
            print(f"  Word count status: {format_result['word_count_status']['current_words']} words")
            print(f"  Reference status: {format_result['reference_status']['compliant']}")
            print(f"  Files created: {len(format_result['files_created'])}")
            
            # Generate submission package
            package = formatter.generate_submission_package(journal, f"examples/{journal}_submission")
            print(f"  Package compliance: {package['compliance_status']}")
            
        except Exception as e:
            print(f"  ❌ Error formatting for {journal}: {e}")
    
    # Step 5: Complete Workflow Demonstration
    print("\n🎉 Step 5: Complete Workflow Summary")
    print("-" * 50)
    
    workflow_summary = {
        "project_name": "BC_Liver_Transplant_Study",
        "workflow_completed": datetime.datetime.now().isoformat(),
        "literature_review": {
            "iterations_planned": 10,
            "iterations_completed": 1,
            "papers_reviewed": iteration_1_results['papers_found'],
            "evidence_sufficiency": iteration_1_results['evidence_sufficiency']
        },
        "reference_management": {
            "total_references": stats['total_references'],
            "export_formats": ["RIS", "BibTeX", "CSV"],
            "quality_distribution": stats['quality_distribution']
        },
        "manuscript_preparation": {
            "sections_identified": len(load_result['sections']),
            "total_words": load_result['total_word_count'],
            "journals_targeted": target_journals,
            "submission_packages": len(target_journals)
        }
    }
    
    # Save workflow summary
    with open("examples/workflow_summary.json", 'w') as f:
        json.dump(workflow_summary, f, indent=2)
    
    print("✅ Complete SuperClaude-Scientific workflow demonstrated!")
    print(f"📊 Workflow summary saved to examples/workflow_summary.json")
    
    # Next steps guidance
    print("\n🚀 Next Steps for Real Implementation:")
    print("-" * 50)
    print("1. Load your actual research data (CSV files, PDF presentations)")
    print("2. Run /sc:sci-init to create project structure")
    print("3. Use /sc:sci-parse to extract information from your PDFs")
    print("4. Execute /sc:sci-smart-review for comprehensive literature analysis")
    print("5. Format manuscript for target journal using JournalFormatter")
    print("6. Export references and prepare submission package")
    
    print(f"\n🎯 Target: Nature/Lancet/NEJM publication ready!")
    print("=" * 80)

if __name__ == "__main__":
    main()