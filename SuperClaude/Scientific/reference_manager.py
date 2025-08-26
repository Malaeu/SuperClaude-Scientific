"""
Reference Manager for Scientific Literature

This module provides comprehensive reference management capabilities including
deduplication, format conversion, and integration with reference management software
like EndNote, Mendeley, and Zotero.
"""

import json
import re
import hashlib
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import csv


@dataclass
class Reference:
    """Represents a single scientific reference with all metadata."""
    
    # Required fields
    title: str
    authors: List[str]
    year: int
    
    # Optional fields
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    url: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = None
    
    # Publication type
    publication_type: str = "journal_article"  # journal_article, conference, book, thesis, etc.
    
    # Quality metrics
    impact_factor: Optional[float] = None
    citation_count: Optional[int] = None
    quality_score: Optional[int] = None  # 1-10 scale
    
    # Internal tracking
    reference_id: Optional[str] = None
    added_date: Optional[str] = None
    source_iteration: Optional[int] = None  # Which review iteration found this
    
    def __post_init__(self):
        """Generate reference ID and set added date if not provided."""
        if not self.reference_id:
            self.reference_id = self._generate_id()
        if not self.added_date:
            self.added_date = datetime.now().isoformat()
    
    def _generate_id(self) -> str:
        """Generate unique ID based on title, authors, and year."""
        id_string = f"{self.title}{','.join(self.authors)}{self.year}"
        return hashlib.md5(id_string.encode()).hexdigest()[:12]


class ReferenceManager:
    """
    Comprehensive reference management system for scientific literature.
    
    Features:
    - Automatic deduplication based on DOI, title, and author matching
    - Multiple export formats (RIS, BibTeX, EndNote, CSV)
    - Quality assessment and ranking
    - Integration with literature review workflows
    - Citation network analysis
    """
    
    def __init__(self, project_name: str = "default"):
        """
        Initialize reference manager.
        
        Args:
            project_name: Name of the research project
        """
        self.project_name = project_name
        self.references: Dict[str, Reference] = {}
        self.duplicate_groups: List[List[str]] = []  # Groups of duplicate reference IDs
        
        # Deduplication settings
        self.doi_weight = 1.0  # Perfect match if DOIs match
        self.title_similarity_threshold = 0.85
        self.author_overlap_threshold = 0.7
        
        # Quality settings
        self.min_quality_score = 5
        self.high_impact_threshold = 5.0  # Journal impact factor
        
    def add_reference(self, reference_data: Dict) -> str:
        """
        Add a new reference with automatic deduplication.
        
        Args:
            reference_data: Dictionary containing reference information
            
        Returns:
            Reference ID of the added or existing reference
        """
        # Create reference object
        ref = self._create_reference_from_dict(reference_data)
        
        # Check for duplicates
        duplicate_id = self._find_duplicate(ref)
        if duplicate_id:
            # Update existing reference with any new information
            self._merge_references(duplicate_id, ref)
            return duplicate_id
        
        # Add new reference
        self.references[ref.reference_id] = ref
        return ref.reference_id
    
    def add_references_batch(self, references_list: List[Dict]) -> List[str]:
        """
        Add multiple references in batch with progress tracking.
        
        Args:
            references_list: List of reference dictionaries
            
        Returns:
            List of reference IDs (new or existing)
        """
        added_ids = []
        duplicates_found = 0
        
        for ref_data in references_list:
            ref_id = self.add_reference(ref_data)
            added_ids.append(ref_id)
            
            # Track if this was a duplicate
            if ref_id in [r.reference_id for r in self.references.values() 
                         if r.added_date != datetime.now().isoformat()[:10]]:
                duplicates_found += 1
        
        print(f"Added {len(references_list)} references ({duplicates_found} duplicates found)")
        return added_ids
    
    def get_reference(self, reference_id: str) -> Optional[Reference]:
        """Get reference by ID."""
        return self.references.get(reference_id)
    
    def search_references(self, query: str, fields: List[str] = None) -> List[Reference]:
        """
        Search references by text query in specified fields.
        
        Args:
            query: Search query string
            fields: List of fields to search in (default: title, abstract, keywords)
            
        Returns:
            List of matching references
        """
        if fields is None:
            fields = ["title", "abstract", "keywords"]
        
        query_lower = query.lower()
        matching_refs = []
        
        for ref in self.references.values():
            for field in fields:
                field_value = getattr(ref, field, None)
                if field_value:
                    if isinstance(field_value, str) and query_lower in field_value.lower():
                        matching_refs.append(ref)
                        break
                    elif isinstance(field_value, list) and any(query_lower in item.lower() for item in field_value):
                        matching_refs.append(ref)
                        break
        
        return matching_refs
    
    def filter_references(self, 
                         min_year: Optional[int] = None,
                         max_year: Optional[int] = None,
                         min_quality: Optional[int] = None,
                         publication_types: Optional[List[str]] = None,
                         has_doi: Optional[bool] = None) -> List[Reference]:
        """
        Filter references based on various criteria.
        
        Args:
            min_year: Minimum publication year
            max_year: Maximum publication year
            min_quality: Minimum quality score
            publication_types: List of acceptable publication types
            has_doi: Whether reference must have DOI
            
        Returns:
            List of references meeting criteria
        """
        filtered_refs = []
        
        for ref in self.references.values():
            # Year filter
            if min_year and ref.year < min_year:
                continue
            if max_year and ref.year > max_year:
                continue
            
            # Quality filter
            if min_quality and (ref.quality_score is None or ref.quality_score < min_quality):
                continue
            
            # Publication type filter
            if publication_types and ref.publication_type not in publication_types:
                continue
            
            # DOI filter
            if has_doi is not None:
                if has_doi and not ref.doi:
                    continue
                if not has_doi and ref.doi:
                    continue
            
            filtered_refs.append(ref)
        
        return filtered_refs
    
    def get_high_quality_references(self, limit: Optional[int] = None) -> List[Reference]:
        """Get highest quality references sorted by quality score."""
        quality_refs = [ref for ref in self.references.values() 
                       if ref.quality_score and ref.quality_score >= self.min_quality_score]
        
        # Sort by quality score, then by impact factor, then by citation count
        quality_refs.sort(key=lambda r: (
            r.quality_score or 0,
            r.impact_factor or 0,
            r.citation_count or 0
        ), reverse=True)
        
        return quality_refs[:limit] if limit else quality_refs
    
    def export_ris(self, filepath: str, reference_ids: Optional[List[str]] = None) -> None:
        """
        Export references in RIS format for EndNote/Mendeley.
        
        Args:
            filepath: Output file path
            reference_ids: Specific reference IDs to export (default: all)
        """
        if reference_ids:
            refs_to_export = [self.references[rid] for rid in reference_ids if rid in self.references]
        else:
            refs_to_export = list(self.references.values())
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for ref in refs_to_export:
                f.write(self._format_ris(ref))
                f.write("\n")
        
        print(f"Exported {len(refs_to_export)} references to {filepath}")
    
    def export_bibtex(self, filepath: str, reference_ids: Optional[List[str]] = None) -> None:
        """
        Export references in BibTeX format.
        
        Args:
            filepath: Output file path
            reference_ids: Specific reference IDs to export (default: all)
        """
        if reference_ids:
            refs_to_export = [self.references[rid] for rid in reference_ids if rid in self.references]
        else:
            refs_to_export = list(self.references.values())
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for ref in refs_to_export:
                f.write(self._format_bibtex(ref))
                f.write("\n")
        
        print(f"Exported {len(refs_to_export)} references to {filepath}")
    
    def export_csv(self, filepath: str, reference_ids: Optional[List[str]] = None) -> None:
        """
        Export references in CSV format for analysis.
        
        Args:
            filepath: Output file path
            reference_ids: Specific reference IDs to export (default: all)
        """
        if reference_ids:
            refs_to_export = [self.references[rid] for rid in reference_ids if rid in self.references]
        else:
            refs_to_export = list(self.references.values())
        
        if not refs_to_export:
            print("No references to export")
            return
        
        # Get all possible fields
        fieldnames = list(asdict(refs_to_export[0]).keys())
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for ref in refs_to_export:
                ref_dict = asdict(ref)
                # Convert lists to strings
                for key, value in ref_dict.items():
                    if isinstance(value, list):
                        ref_dict[key] = '; '.join(map(str, value))
                writer.writerow(ref_dict)
        
        print(f"Exported {len(refs_to_export)} references to {filepath}")
    
    def generate_statistics(self) -> Dict:
        """Generate comprehensive statistics about the reference collection."""
        total_refs = len(self.references)
        
        if total_refs == 0:
            return {"message": "No references in collection"}
        
        # Year distribution
        years = [ref.year for ref in self.references.values() if ref.year]
        year_stats = {
            "min_year": min(years) if years else None,
            "max_year": max(years) if years else None,
            "recent_5_years": len([y for y in years if y >= (datetime.now().year - 5)])
        }
        
        # Publication type distribution
        pub_types = [ref.publication_type for ref in self.references.values()]
        type_counts = {ptype: pub_types.count(ptype) for ptype in set(pub_types)}
        
        # Quality distribution
        quality_scores = [ref.quality_score for ref in self.references.values() if ref.quality_score]
        quality_stats = {
            "high_quality": len([q for q in quality_scores if q >= 8]),
            "medium_quality": len([q for q in quality_scores if 6 <= q < 8]),
            "low_quality": len([q for q in quality_scores if q < 6]),
            "average_quality": sum(quality_scores) / len(quality_scores) if quality_scores else 0
        }
        
        # DOI and metadata completeness
        completeness = {
            "with_doi": len([ref for ref in self.references.values() if ref.doi]),
            "with_abstract": len([ref for ref in self.references.values() if ref.abstract]),
            "with_keywords": len([ref for ref in self.references.values() if ref.keywords]),
            "with_impact_factor": len([ref for ref in self.references.values() if ref.impact_factor])
        }
        
        # Top journals
        journals = [ref.journal for ref in self.references.values() if ref.journal]
        journal_counts = {}
        for journal in journals:
            journal_counts[journal] = journal_counts.get(journal, 0) + 1
        top_journals = sorted(journal_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_references": total_refs,
            "year_distribution": year_stats,
            "publication_types": type_counts,
            "quality_distribution": quality_stats,
            "metadata_completeness": completeness,
            "top_journals": top_journals,
            "duplicate_groups": len(self.duplicate_groups)
        }
    
    def save_database(self, filepath: str) -> None:
        """Save reference database to JSON file."""
        database = {
            "project_name": self.project_name,
            "references": {rid: asdict(ref) for rid, ref in self.references.items()},
            "duplicate_groups": self.duplicate_groups,
            "saved_at": datetime.now().isoformat(),
            "total_references": len(self.references)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.references)} references to {filepath}")
    
    def load_database(self, filepath: str) -> None:
        """Load reference database from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            database = json.load(f)
        
        self.project_name = database.get("project_name", "loaded_project")
        self.duplicate_groups = database.get("duplicate_groups", [])
        
        # Reconstruct reference objects
        self.references = {}
        for rid, ref_data in database.get("references", {}).items():
            ref = Reference(**ref_data)
            self.references[rid] = ref
        
        print(f"Loaded {len(self.references)} references from {filepath}")
    
    def find_citation_opportunities(self, manuscript_text: str) -> List[Dict]:
        """
        Find references that could be cited in manuscript text.
        
        Args:
            manuscript_text: Text of manuscript to analyze
            
        Returns:
            List of potential citation opportunities
        """
        opportunities = []
        text_lower = manuscript_text.lower()
        
        for ref in self.references.values():
            # Check if reference keywords appear in text
            if ref.keywords:
                for keyword in ref.keywords:
                    if keyword.lower() in text_lower:
                        opportunities.append({
                            "reference_id": ref.reference_id,
                            "title": ref.title,
                            "matched_keyword": keyword,
                            "relevance_score": self._calculate_relevance(ref, manuscript_text)
                        })
                        break
        
        # Sort by relevance score
        opportunities.sort(key=lambda x: x["relevance_score"], reverse=True)
        return opportunities[:20]  # Return top 20 opportunities
    
    # Private helper methods
    
    def _create_reference_from_dict(self, ref_data: Dict) -> Reference:
        """Create Reference object from dictionary data."""
        # Clean and validate data
        cleaned_data = {}
        
        # Required fields
        cleaned_data["title"] = str(ref_data.get("title", "")).strip()
        cleaned_data["authors"] = self._parse_authors(ref_data.get("authors", []))
        cleaned_data["year"] = self._parse_year(ref_data.get("year"))
        
        # Optional fields
        optional_fields = ["journal", "volume", "issue", "pages", "doi", "pmid", 
                          "url", "abstract", "publication_type", "impact_factor",
                          "citation_count", "quality_score", "source_iteration"]
        
        for field in optional_fields:
            if field in ref_data:
                cleaned_data[field] = ref_data[field]
        
        # Special handling for keywords
        if "keywords" in ref_data:
            cleaned_data["keywords"] = self._parse_keywords(ref_data["keywords"])
        
        return Reference(**cleaned_data)
    
    def _parse_authors(self, authors_input) -> List[str]:
        """Parse authors from various input formats."""
        if isinstance(authors_input, list):
            return [str(author).strip() for author in authors_input if author]
        elif isinstance(authors_input, str):
            # Split by common separators
            if ';' in authors_input:
                return [author.strip() for author in authors_input.split(';') if author.strip()]
            elif ',' in authors_input and ' and ' not in authors_input:
                return [author.strip() for author in authors_input.split(',') if author.strip()]
            else:
                return [authors_input.strip()]
        else:
            return []
    
    def _parse_year(self, year_input) -> int:
        """Parse year from various input formats."""
        if isinstance(year_input, int):
            return year_input
        elif isinstance(year_input, str):
            # Extract 4-digit year from string
            year_match = re.search(r'\b(19|20)\d{2}\b', year_input)
            return int(year_match.group()) if year_match else datetime.now().year
        else:
            return datetime.now().year
    
    def _parse_keywords(self, keywords_input) -> List[str]:
        """Parse keywords from various input formats."""
        if isinstance(keywords_input, list):
            return [str(kw).strip() for kw in keywords_input if kw]
        elif isinstance(keywords_input, str):
            # Split by common separators
            separators = [';', ',', '|', '\n']
            for sep in separators:
                if sep in keywords_input:
                    return [kw.strip() for kw in keywords_input.split(sep) if kw.strip()]
            return [keywords_input.strip()]
        else:
            return []
    
    def _find_duplicate(self, new_ref: Reference) -> Optional[str]:
        """Find duplicate reference based on DOI, title, and author similarity."""
        for existing_ref in self.references.values():
            # Perfect match: same DOI
            if new_ref.doi and existing_ref.doi and new_ref.doi == existing_ref.doi:
                return existing_ref.reference_id
            
            # Title and author similarity matching
            title_sim = self._calculate_title_similarity(new_ref.title, existing_ref.title)
            author_overlap = self._calculate_author_overlap(new_ref.authors, existing_ref.authors)
            
            if (title_sim > self.title_similarity_threshold and 
                author_overlap > self.author_overlap_threshold and
                abs(new_ref.year - existing_ref.year) <= 1):  # Allow 1 year difference
                return existing_ref.reference_id
        
        return None
    
    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        """Calculate similarity between two titles."""
        # Simple word-based similarity
        words1 = set(title1.lower().split())
        words2 = set(title2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_author_overlap(self, authors1: List[str], authors2: List[str]) -> float:
        """Calculate overlap between two author lists."""
        if not authors1 or not authors2:
            return 0.0
        
        # Normalize author names (last name only for comparison)
        norm_authors1 = set()
        norm_authors2 = set()
        
        for author in authors1:
            last_name = author.split()[-1].lower() if author else ""
            if len(last_name) > 2:  # Avoid initials
                norm_authors1.add(last_name)
        
        for author in authors2:
            last_name = author.split()[-1].lower() if author else ""
            if len(last_name) > 2:  # Avoid initials
                norm_authors2.add(last_name)
        
        if not norm_authors1 or not norm_authors2:
            return 0.0
        
        intersection = len(norm_authors1.intersection(norm_authors2))
        min_length = min(len(norm_authors1), len(norm_authors2))
        
        return intersection / min_length
    
    def _merge_references(self, existing_id: str, new_ref: Reference) -> None:
        """Merge new reference data into existing reference."""
        existing_ref = self.references[existing_id]
        
        # Update fields that are missing or have better quality in new reference
        merge_fields = ["doi", "pmid", "url", "abstract", "keywords", "impact_factor", 
                       "citation_count", "volume", "issue", "pages"]
        
        for field in merge_fields:
            existing_value = getattr(existing_ref, field)
            new_value = getattr(new_ref, field)
            
            if not existing_value and new_value:
                setattr(existing_ref, field, new_value)
            elif field == "keywords" and existing_value and new_value:
                # Merge keyword lists
                combined_keywords = list(set(existing_value + new_value))
                setattr(existing_ref, field, combined_keywords)
    
    def _format_ris(self, ref: Reference) -> str:
        """Format reference in RIS format."""
        ris_lines = []
        
        # Publication type
        type_mapping = {
            "journal_article": "JOUR",
            "conference": "CONF",
            "book": "BOOK",
            "thesis": "THES"
        }
        pub_type = type_mapping.get(ref.publication_type, "JOUR")
        ris_lines.append(f"TY  - {pub_type}")
        
        # Authors
        for author in ref.authors:
            ris_lines.append(f"AU  - {author}")
        
        # Title
        ris_lines.append(f"TI  - {ref.title}")
        
        # Journal
        if ref.journal:
            ris_lines.append(f"JO  - {ref.journal}")
        
        # Year
        ris_lines.append(f"PY  - {ref.year}")
        
        # Volume, Issue, Pages
        if ref.volume:
            ris_lines.append(f"VL  - {ref.volume}")
        if ref.issue:
            ris_lines.append(f"IS  - {ref.issue}")
        if ref.pages:
            ris_lines.append(f"SP  - {ref.pages}")
        
        # DOI
        if ref.doi:
            ris_lines.append(f"DO  - {ref.doi}")
        
        # URL
        if ref.url:
            ris_lines.append(f"UR  - {ref.url}")
        
        # Abstract
        if ref.abstract:
            ris_lines.append(f"AB  - {ref.abstract}")
        
        # Keywords
        if ref.keywords:
            ris_lines.append(f"KW  - {'; '.join(ref.keywords)}")
        
        # End record
        ris_lines.append("ER  - ")
        
        return '\n'.join(ris_lines)
    
    def _format_bibtex(self, ref: Reference) -> str:
        """Format reference in BibTeX format."""
        # Generate citation key
        first_author = ref.authors[0].split()[-1] if ref.authors else "Unknown"
        citation_key = f"{first_author}{ref.year}"
        
        bibtex_lines = [f"@article{{{citation_key},"]
        
        # Title
        bibtex_lines.append(f"  title={{{ref.title}}},")
        
        # Authors
        if ref.authors:
            authors_str = " and ".join(ref.authors)
            bibtex_lines.append(f"  author={{{authors_str}}},")
        
        # Journal
        if ref.journal:
            bibtex_lines.append(f"  journal={{{ref.journal}}},")
        
        # Year
        bibtex_lines.append(f"  year={{{ref.year}}},")
        
        # Volume, Issue, Pages
        if ref.volume:
            bibtex_lines.append(f"  volume={{{ref.volume}}},")
        if ref.issue:
            bibtex_lines.append(f"  number={{{ref.issue}}},")
        if ref.pages:
            bibtex_lines.append(f"  pages={{{ref.pages}}},")
        
        # DOI
        if ref.doi:
            bibtex_lines.append(f"  doi={{{ref.doi}}},")
        
        # URL
        if ref.url:
            bibtex_lines.append(f"  url={{{ref.url}}},")
        
        bibtex_lines.append("}")
        
        return '\n'.join(bibtex_lines)
    
    def _calculate_relevance(self, ref: Reference, text: str) -> float:
        """Calculate relevance score of reference to given text."""
        text_lower = text.lower()
        score = 0.0
        
        # Title word matches
        title_words = ref.title.lower().split()
        title_matches = sum(1 for word in title_words if word in text_lower)
        score += (title_matches / len(title_words)) * 0.4
        
        # Keyword matches
        if ref.keywords:
            keyword_matches = sum(1 for kw in ref.keywords if kw.lower() in text_lower)
            score += (keyword_matches / len(ref.keywords)) * 0.4
        
        # Quality bonus
        if ref.quality_score:
            score += (ref.quality_score / 10) * 0.2
        
        return min(1.0, score)