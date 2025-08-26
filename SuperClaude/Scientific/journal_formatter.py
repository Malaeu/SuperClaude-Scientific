"""
Journal Formatter for Scientific Manuscripts

This module provides comprehensive manuscript formatting capabilities for
high-impact medical journals including Nature, Lancet, NEJM, and JAMA.
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import tempfile
import shutil


@dataclass
class JournalSpecs:
    """Journal-specific formatting specifications."""
    name: str
    word_limit: int
    reference_limit: int
    figure_limit: int
    citation_style: str  # nature, vancouver, ama, etc.
    abstract_type: str  # structured, unstructured
    abstract_word_limit: int
    title_word_limit: int
    running_head_limit: int
    special_requirements: Dict = None


@dataclass 
class ManuscriptSection:
    """Represents a section of the manuscript."""
    title: str
    content: str
    word_count: int
    order: int
    required: bool = True
    in_supplement: bool = False


class JournalFormatter:
    """
    Comprehensive manuscript formatting system for high-impact journals.
    
    Features:
    - Journal-specific formatting (Nature, Lancet, NEJM, JAMA)
    - Word count optimization and content prioritization
    - Reference formatting and citation style conversion
    - Figure and table preparation guidelines
    - Supplement organization and preparation
    - Cover letter generation
    """
    
    # Journal specifications database
    JOURNAL_SPECS = {
        "nature": JournalSpecs(
            name="Nature",
            word_limit=3000,
            reference_limit=30,
            figure_limit=4,
            citation_style="nature",
            abstract_type="unstructured",
            abstract_word_limit=200,
            title_word_limit=20,
            running_head_limit=40,
            special_requirements={
                "methods_in_supplement": True,
                "requires_significance_statement": True,
                "figure_quality": "300dpi",
                "file_formats": ["tiff", "eps", "pdf"]
            }
        ),
        "lancet": JournalSpecs(
            name="The Lancet",
            word_limit=4500,
            reference_limit=60,
            figure_limit=5,
            citation_style="vancouver",
            abstract_type="structured",
            abstract_word_limit=300,
            title_word_limit=150,  # characters
            running_head_limit=45,
            special_requirements={
                "structured_abstract_sections": ["Background", "Methods", "Findings", "Interpretation"],
                "requires_funding_statement": True,
                "requires_data_sharing": True,
                "figure_quality": "300dpi"
            }
        ),
        "nejm": JournalSpecs(
            name="New England Journal of Medicine",
            word_limit=2700,
            reference_limit=40,
            figure_limit=6,
            citation_style="nejm",
            abstract_type="structured",
            abstract_word_limit=250,
            title_word_limit=100,  # characters
            running_head_limit=50,
            special_requirements={
                "structured_abstract_sections": ["Background", "Methods", "Results", "Conclusions"],
                "requires_clinical_trial_number": True,
                "requires_disclosures": True,
                "figure_quality": "600dpi"
            }
        ),
        "jama": JournalSpecs(
            name="Journal of the American Medical Association",
            word_limit=3500,
            reference_limit=60,
            figure_limit=5,
            citation_style="ama",
            abstract_type="structured",
            abstract_word_limit=350,
            title_word_limit=150,  # characters
            running_head_limit=50,
            special_requirements={
                "structured_abstract_sections": ["Importance", "Objective", "Design", "Setting", 
                                               "Participants", "Main Outcomes", "Results", "Conclusions"],
                "requires_key_points": True,
                "requires_trial_registration": True,
                "figure_quality": "300dpi"
            }
        )
    }
    
    def __init__(self, project_dir: str = "."):
        """
        Initialize journal formatter.
        
        Args:
            project_dir: Directory containing manuscript files
        """
        self.project_dir = Path(project_dir)
        self.manuscript: Dict[str, ManuscriptSection] = {}
        self.references: List[Dict] = []
        self.figures: List[Dict] = []
        self.tables: List[Dict] = []
        self.target_journal: Optional[str] = None
        
        # Word counting settings
        self.exclude_from_count = ["references", "figure_legends", "acknowledgments"]
        
    def load_manuscript(self, manuscript_file: str) -> Dict:
        """
        Load manuscript from markdown or text file.
        
        Args:
            manuscript_file: Path to manuscript file
            
        Returns:
            Dictionary with manuscript sections and metadata
        """
        filepath = self.project_dir / manuscript_file
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse manuscript sections
        sections = self._parse_manuscript_sections(content)
        
        # Create ManuscriptSection objects
        for i, (title, section_content) in enumerate(sections.items()):
            word_count = self._count_words(section_content)
            self.manuscript[title.lower().replace(' ', '_')] = ManuscriptSection(
                title=title,
                content=section_content,
                word_count=word_count,
                order=i,
                required=title.lower() in ["abstract", "introduction", "methods", "results", "discussion"]
            )
        
        return {
            "sections": list(sections.keys()),
            "total_word_count": sum(section.word_count for section in self.manuscript.values()),
            "sections_detail": {name: {"words": section.word_count, "required": section.required} 
                              for name, section in self.manuscript.items()}
        }
    
    def format_for_journal(self, journal: str, output_dir: str = None) -> Dict:
        """
        Format manuscript for specific journal.
        
        Args:
            journal: Target journal name (nature, lancet, nejm, jama)
            output_dir: Output directory for formatted files
            
        Returns:
            Dictionary with formatting results and compliance status
        """
        if journal.lower() not in self.JOURNAL_SPECS:
            raise ValueError(f"Unsupported journal: {journal}")
        
        self.target_journal = journal.lower()
        specs = self.JOURNAL_SPECS[self.target_journal]
        
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
        else:
            output_path = self.project_dir / f"formatted_{journal.lower()}"
            output_path.mkdir(exist_ok=True)
        
        # Format each section according to journal requirements
        formatting_results = {
            "journal": specs.name,
            "compliance_status": {},
            "recommendations": [],
            "files_created": []
        }
        
        # 1. Format title and abstract
        title_result = self._format_title(specs)
        abstract_result = self._format_abstract(specs)
        
        # 2. Optimize word count
        word_count_result = self._optimize_word_count(specs)
        
        # 3. Format references
        reference_result = self._format_references(specs)
        
        # 4. Create main manuscript file
        manuscript_file = output_path / f"manuscript_{journal.lower()}.docx"
        self._create_formatted_manuscript(specs, manuscript_file)
        
        # 5. Create supplement files
        supplement_files = self._create_supplements(specs, output_path)
        
        # 6. Generate cover letter
        cover_letter_file = output_path / f"cover_letter_{journal.lower()}.txt"
        self._generate_cover_letter(specs, cover_letter_file)
        
        # 7. Create submission checklist
        checklist_file = output_path / f"submission_checklist_{journal.lower()}.md"
        self._create_submission_checklist(specs, checklist_file)
        
        # Compile results
        formatting_results.update({
            "title_compliance": title_result,
            "abstract_compliance": abstract_result,
            "word_count_status": word_count_result,
            "reference_status": reference_result,
            "files_created": [
                str(manuscript_file),
                str(cover_letter_file),
                str(checklist_file)
            ] + supplement_files
        })
        
        return formatting_results
    
    def optimize_word_count(self, target_words: int, preserve_sections: List[str] = None) -> Dict:
        """
        Optimize manuscript word count to meet journal limits.
        
        Args:
            target_words: Target word count
            preserve_sections: Sections to preserve from editing
            
        Returns:
            Dictionary with optimization results and recommendations
        """
        current_words = sum(section.word_count for section in self.manuscript.values()
                           if section.title.lower() not in self.exclude_from_count)
        
        if current_words <= target_words:
            return {
                "status": "within_limit",
                "current_words": current_words,
                "target_words": target_words,
                "excess_words": 0,
                "recommendations": ["Manuscript is within word limit"]
            }
        
        excess_words = current_words - target_words
        preserve_sections = preserve_sections or []
        
        # Identify sections that can be trimmed or moved to supplement
        optimization_plan = []
        potential_savings = 0
        
        # Prioritize sections for trimming
        section_priorities = {
            "introduction": 0.7,  # Can trim 30%
            "discussion": 0.6,    # Can trim 40%
            "methods": 0.5,       # Can move to supplement
            "results": 0.2,       # Minimal trimming
            "conclusion": 0.3     # Can trim moderately
        }
        
        for section_name, section in self.manuscript.items():
            if (section_name not in preserve_sections and 
                section_name in section_priorities):
                
                max_reduction = int(section.word_count * section_priorities[section_name])
                optimization_plan.append({
                    "section": section.title,
                    "current_words": section.word_count,
                    "suggested_reduction": max_reduction,
                    "action": "trim" if max_reduction < section.word_count * 0.5 else "move_to_supplement"
                })
                potential_savings += max_reduction
        
        # Sort by potential impact
        optimization_plan.sort(key=lambda x: x["suggested_reduction"], reverse=True)
        
        return {
            "status": "over_limit",
            "current_words": current_words,
            "target_words": target_words,
            "excess_words": excess_words,
            "potential_savings": potential_savings,
            "optimization_plan": optimization_plan,
            "recommendations": self._generate_word_count_recommendations(optimization_plan, excess_words)
        }
    
    def validate_figures_tables(self, figure_dir: str = None, table_dir: str = None) -> Dict:
        """
        Validate figures and tables against journal requirements.
        
        Args:
            figure_dir: Directory containing figure files
            table_dir: Directory containing table files
            
        Returns:
            Dictionary with validation results and requirements
        """
        if not self.target_journal:
            return {"error": "No target journal specified"}
        
        specs = self.JOURNAL_SPECS[self.target_journal]
        validation_results = {
            "journal": specs.name,
            "figure_limit": specs.figure_limit,
            "figures": [],
            "tables": [],
            "compliance": True,
            "issues": []
        }
        
        # Validate figures
        if figure_dir:
            figure_path = Path(figure_dir)
            if figure_path.exists():
                figure_files = list(figure_path.glob("*"))
                
                for fig_file in figure_files:
                    fig_validation = self._validate_figure_file(fig_file, specs)
                    validation_results["figures"].append(fig_validation)
                    
                    if not fig_validation["compliant"]:
                        validation_results["compliance"] = False
                        validation_results["issues"].extend(fig_validation["issues"])
                
                # Check figure count limit
                if len(figure_files) > specs.figure_limit:
                    validation_results["compliance"] = False
                    validation_results["issues"].append(
                        f"Too many figures: {len(figure_files)} > {specs.figure_limit} (journal limit)"
                    )
        
        # Validate tables
        if table_dir:
            table_path = Path(table_dir)
            if table_path.exists():
                table_files = list(table_path.glob("*.csv")) + list(table_path.glob("*.xlsx"))
                
                for table_file in table_files:
                    table_validation = self._validate_table_file(table_file, specs)
                    validation_results["tables"].append(table_validation)
                    
                    if not table_validation["compliant"]:
                        validation_results["compliance"] = False
                        validation_results["issues"].extend(table_validation["issues"])
        
        return validation_results
    
    def generate_submission_package(self, journal: str, output_dir: str) -> Dict:
        """
        Generate complete submission package for journal.
        
        Args:
            journal: Target journal
            output_dir: Output directory
            
        Returns:
            Dictionary with package contents and submission instructions
        """
        # Format manuscript for journal
        formatting_result = self.format_for_journal(journal, output_dir)
        
        # Validate all components
        validation_result = self.validate_figures_tables(
            f"{output_dir}/figures", 
            f"{output_dir}/tables"
        )
        
        # Create submission summary
        package_summary = {
            "journal": self.JOURNAL_SPECS[journal.lower()].name,
            "package_date": datetime.now().isoformat(),
            "manuscript_file": formatting_result["files_created"][0],
            "cover_letter": formatting_result["files_created"][1],
            "submission_checklist": formatting_result["files_created"][2],
            "compliance_status": validation_result["compliance"],
            "word_count": formatting_result["word_count_status"]["current_words"],
            "reference_count": formatting_result["reference_status"]["count"],
            "figure_count": len(validation_result["figures"]),
            "issues_to_resolve": validation_result["issues"],
            "next_steps": self._generate_submission_next_steps(journal, validation_result["compliance"])
        }
        
        # Save package summary
        summary_file = Path(output_dir) / "submission_package_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(package_summary, f, indent=2)
        
        return package_summary
    
    # Private helper methods
    
    def _parse_manuscript_sections(self, content: str) -> Dict[str, str]:
        """Parse manuscript content into sections."""
        sections = {}
        
        # Split by markdown headers
        section_pattern = r'^#+\s+(.+)$'
        parts = re.split(section_pattern, content, flags=re.MULTILINE)
        
        if len(parts) == 1:
            # No headers found, treat as single section
            sections["Manuscript"] = content.strip()
        else:
            # Parse sections
            for i in range(1, len(parts), 2):
                if i + 1 < len(parts):
                    section_title = parts[i].strip()
                    section_content = parts[i + 1].strip()
                    sections[section_title] = section_content
        
        return sections
    
    def _count_words(self, text: str) -> int:
        """Count words in text, excluding references and figure legends."""
        # Remove citations [1], [1-3], etc.
        text_clean = re.sub(r'\[\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*\]', '', text)
        
        # Remove figure/table references
        text_clean = re.sub(r'(?i)(?:figure|fig|table|tbl)\.?\s*\d+', '', text_clean)
        
        # Count words
        words = text_clean.split()
        return len(words)
    
    def _format_title(self, specs: JournalSpecs) -> Dict:
        """Format title according to journal specifications."""
        if "title" not in self.manuscript:
            return {"status": "missing", "issues": ["Title section not found"]}
        
        title_section = self.manuscript["title"]
        title_text = title_section.content.strip()
        
        if specs.title_word_limit > 100:  # Character limit
            char_count = len(title_text)
            compliant = char_count <= specs.title_word_limit
            return {
                "status": "compliant" if compliant else "over_limit",
                "current_characters": char_count,
                "limit_characters": specs.title_word_limit,
                "issues": [] if compliant else [f"Title too long: {char_count} > {specs.title_word_limit} characters"]
            }
        else:  # Word limit
            word_count = self._count_words(title_text)
            compliant = word_count <= specs.title_word_limit
            return {
                "status": "compliant" if compliant else "over_limit",
                "current_words": word_count,
                "limit_words": specs.title_word_limit,
                "issues": [] if compliant else [f"Title too long: {word_count} > {specs.title_word_limit} words"]
            }
    
    def _format_abstract(self, specs: JournalSpecs) -> Dict:
        """Format abstract according to journal specifications."""
        if "abstract" not in self.manuscript:
            return {"status": "missing", "issues": ["Abstract section not found"]}
        
        abstract_section = self.manuscript["abstract"]
        abstract_text = abstract_section.content.strip()
        word_count = self._count_words(abstract_text)
        
        result = {
            "status": "compliant" if word_count <= specs.abstract_word_limit else "over_limit",
            "current_words": word_count,
            "limit_words": specs.abstract_word_limit,
            "type_required": specs.abstract_type,
            "issues": []
        }
        
        if word_count > specs.abstract_word_limit:
            result["issues"].append(f"Abstract too long: {word_count} > {specs.abstract_word_limit} words")
        
        # Check if structured abstract is required
        if specs.abstract_type == "structured":
            required_sections = specs.special_requirements.get("structured_abstract_sections", [])
            if required_sections:
                # Check if abstract contains required sections
                found_sections = []
                for section in required_sections:
                    if section.lower() in abstract_text.lower():
                        found_sections.append(section)
                
                if len(found_sections) < len(required_sections):
                    missing_sections = set(required_sections) - set(found_sections)
                    result["issues"].append(f"Missing structured abstract sections: {', '.join(missing_sections)}")
                    result["status"] = "needs_restructuring"
        
        return result
    
    def _optimize_word_count(self, specs: JournalSpecs) -> Dict:
        """Optimize manuscript word count for journal limits."""
        return self.optimize_word_count(specs.word_limit)
    
    def _format_references(self, specs: JournalSpecs) -> Dict:
        """Format references according to journal citation style."""
        # Extract references from manuscript (simplified)
        reference_pattern = r'\[\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*\]'
        reference_mentions = []
        
        for section in self.manuscript.values():
            matches = re.findall(reference_pattern, section.content)
            reference_mentions.extend(matches)
        
        # Extract unique reference numbers
        unique_refs = set()
        for mention in reference_mentions:
            # Extract numbers from [1], [1-3], [1,2,5] etc.
            numbers = re.findall(r'\d+', mention)
            unique_refs.update(int(n) for n in numbers)
        
        ref_count = len(unique_refs)
        
        return {
            "count": ref_count,
            "limit": specs.reference_limit,
            "citation_style": specs.citation_style,
            "compliant": ref_count <= specs.reference_limit,
            "issues": [] if ref_count <= specs.reference_limit else 
                     [f"Too many references: {ref_count} > {specs.reference_limit}"]
        }
    
    def _create_formatted_manuscript(self, specs: JournalSpecs, output_file: Path) -> None:
        """Create formatted manuscript file."""
        # Create formatted content
        formatted_content = []
        
        # Title page
        if "title" in self.manuscript:
            formatted_content.append(f"# {self.manuscript['title'].content}\n")
        
        # Abstract
        if "abstract" in self.manuscript:
            formatted_content.append("## Abstract\n")
            formatted_content.append(f"{self.manuscript['abstract'].content}\n")
        
        # Main sections
        section_order = ["introduction", "methods", "results", "discussion", "conclusion"]
        for section_name in section_order:
            if section_name in self.manuscript:
                section = self.manuscript[section_name]
                formatted_content.append(f"## {section.title}\n")
                formatted_content.append(f"{section.content}\n")
        
        # Write to file (markdown format for now)
        output_md = output_file.with_suffix('.md')
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write('\n'.join(formatted_content))
    
    def _create_supplements(self, specs: JournalSpecs, output_dir: Path) -> List[str]:
        """Create supplementary material files."""
        supplement_files = []
        
        # Check if methods should be in supplement (Nature requirement)
        if specs.special_requirements and specs.special_requirements.get("methods_in_supplement"):
            if "methods" in self.manuscript:
                methods_supplement = output_dir / "supplement_methods.md"
                with open(methods_supplement, 'w', encoding='utf-8') as f:
                    f.write(f"# Supplementary Methods\n\n{self.manuscript['methods'].content}")
                supplement_files.append(str(methods_supplement))
        
        return supplement_files
    
    def _generate_cover_letter(self, specs: JournalSpecs, output_file: Path) -> None:
        """Generate cover letter for journal submission."""
        title = self.manuscript.get("title", ManuscriptSection("", "Untitled Manuscript", 0, 0)).content
        
        cover_letter = f"""Dear Editor,

We are pleased to submit our manuscript entitled "{title}" for consideration for publication in {specs.name}.

This study addresses [BRIEF DESCRIPTION OF RESEARCH PROBLEM] and presents novel findings that [BRIEF DESCRIPTION OF KEY CONTRIBUTIONS]. Our work makes significant contributions to the field by [SPECIFIC CONTRIBUTIONS].

Key findings include:
- [KEY FINDING 1]
- [KEY FINDING 2]
- [KEY FINDING 3]

The manuscript complies with {specs.name} formatting requirements:
- Word count: within {specs.word_limit} word limit
- References: within {specs.reference_limit} reference limit
- Figures: within {specs.figure_limit} figure limit

We believe this work will be of broad interest to the {specs.name} readership and contributes meaningfully to [RESEARCH AREA].

All authors have read and approved the manuscript. We have no conflicts of interest to declare.

Thank you for considering our manuscript.

Sincerely,
[CORRESPONDING AUTHOR NAME]
[CORRESPONDING AUTHOR AFFILIATION]
[CORRESPONDING AUTHOR EMAIL]

Submission Date: {datetime.now().strftime('%B %d, %Y')}
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
    
    def _create_submission_checklist(self, specs: JournalSpecs, output_file: Path) -> None:
        """Create submission checklist for journal."""
        checklist_items = [
            "☐ Manuscript formatted according to journal guidelines",
            f"☐ Word count within limit ({specs.word_limit} words)",
            f"☐ Reference count within limit ({specs.reference_limit} references)",
            f"☐ Figure count within limit ({specs.figure_limit} figures)",
            "☐ All figures prepared at appropriate resolution",
            "☐ Cover letter completed",
            "☐ Author information and affiliations complete",
            "☐ Conflict of interest statements completed",
            "☐ Ethics approvals documented"
        ]
        
        # Add journal-specific requirements
        if specs.special_requirements:
            if specs.special_requirements.get("requires_clinical_trial_number"):
                checklist_items.append("☐ Clinical trial registration number included")
            if specs.special_requirements.get("requires_data_sharing"):
                checklist_items.append("☐ Data sharing statement included")
            if specs.special_requirements.get("requires_funding_statement"):
                checklist_items.append("☐ Funding statement completed")
        
        checklist_content = f"""# Submission Checklist - {specs.name}

## Pre-submission Requirements

{chr(10).join(checklist_items)}

## Additional Notes
- Double-check all author names and affiliations
- Ensure all figures and tables are referenced in text
- Verify all statistical reporting follows journal guidelines
- Confirm institutional review board approval is documented

## Submission Date: {datetime.now().strftime('%B %d, %Y')}
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(checklist_content)
    
    def _validate_figure_file(self, fig_file: Path, specs: JournalSpecs) -> Dict:
        """Validate individual figure file."""
        validation = {
            "filename": fig_file.name,
            "compliant": True,
            "issues": []
        }
        
        # Check file format
        required_formats = specs.special_requirements.get("file_formats", ["tiff", "eps", "pdf"])
        if fig_file.suffix.lower().lstrip('.') not in required_formats:
            validation["compliant"] = False
            validation["issues"].append(f"Unsupported format: {fig_file.suffix}. Required: {required_formats}")
        
        # Check file size (basic check)
        file_size_mb = fig_file.stat().st_size / (1024 * 1024)
        if file_size_mb > 50:  # Arbitrary limit
            validation["issues"].append(f"Large file size: {file_size_mb:.1f}MB")
        
        return validation
    
    def _validate_table_file(self, table_file: Path, specs: JournalSpecs) -> Dict:
        """Validate individual table file."""
        return {
            "filename": table_file.name,
            "compliant": True,
            "issues": []
        }
    
    def _generate_word_count_recommendations(self, optimization_plan: List[Dict], excess_words: int) -> List[str]:
        """Generate specific recommendations for word count reduction."""
        recommendations = [
            f"Current manuscript exceeds word limit by {excess_words} words",
            "Consider the following optimization strategies:"
        ]
        
        for plan_item in optimization_plan:
            if plan_item["action"] == "trim":
                recommendations.append(
                    f"- Trim {plan_item['section']}: reduce by ~{plan_item['suggested_reduction']} words"
                )
            elif plan_item["action"] == "move_to_supplement":
                recommendations.append(
                    f"- Move {plan_item['section']} to supplementary material"
                )
        
        recommendations.extend([
            "- Combine similar paragraphs and eliminate redundancy",
            "- Use more concise language and shorter sentences",
            "- Move detailed methodology to supplementary materials",
            "- Focus on most impactful results and discussion points"
        ])
        
        return recommendations
    
    def _generate_submission_next_steps(self, journal: str, compliant: bool) -> List[str]:
        """Generate next steps for submission process."""
        if compliant:
            return [
                f"Manuscript is ready for submission to {self.JOURNAL_SPECS[journal.lower()].name}",
                "Review cover letter and customize for specific submission",
                "Prepare author information and conflict of interest forms",
                "Upload files to journal submission system",
                "Submit manuscript and await editorial decision"
            ]
        else:
            return [
                "Resolve compliance issues identified in validation",
                "Review and revise manuscript according to journal requirements",
                "Re-run formatting and validation checks",
                "Proceed with submission once all issues are resolved"
            ]