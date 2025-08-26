"""
SuperClaude Scientific Module

This module provides comprehensive scientific research capabilities including:
- Smart literature review with iterative questioning
- Reference management with deduplication and format conversion
- Journal-specific manuscript formatting
"""

from .smart_review import SmartReviewEngine, SearchIteration, ResearchGap, LiteratureEvidence
from .reference_manager import ReferenceManager, Reference
from .journal_formatter import JournalFormatter, JournalSpecs, ManuscriptSection

__version__ = "1.0.0"
__author__ = "SuperClaude Scientific Team"

__all__ = [
    "SmartReviewEngine",
    "SearchIteration", 
    "ResearchGap",
    "LiteratureEvidence",
    "ReferenceManager",
    "Reference",
    "JournalFormatter",
    "JournalSpecs",
    "ManuscriptSection"
]