from dataclasses import dataclass
from typing import Dict, List, Optional
import re

@dataclass
class JournalGuideline:
    journal: str
    word_counts: Dict[str, Optional[int]]
    refs_style: str
    figures_limits: Dict[str, Optional[int]]
    tables_limits: Dict[str, Optional[int]]
    image_specs: Dict[str, Optional[int]]
    sections: List[str]
    supplement_rules: List[str]
    source_url: str
    source_hash: str
    retrieved_at: str
    publisher: Optional[str] = None

def normalize_guidelines(text: str) -> Dict:
    """
    Input: raw guideline text (HTML→text, PDF→text)
    Output: dict, совместимый с JournalGuideline schema
    """
    # TODO: реализовать набор регексов/эвристик по семействам издателей
    return {
        "word_counts": _extract_word_counts(text),
        "refs_style": _extract_refs_style(text),
        "figures_limits": _extract_fig_limits(text),
        "tables_limits": _extract_table_limits(text),
        "image_specs": _extract_image_specs(text),
        "sections": _extract_sections(text),
        "supplement_rules": _extract_supplement_rules(text),
    }

def _extract_word_counts(text: str) -> Dict[str, Optional[int]]:
    """Extract word count limits from guideline text"""
    word_counts = {}
    
    # Common patterns for word counts
    patterns = [
        (r"abstract(?:\s+(?:up\s+to|no\s+more\s+than|maximum|limit|should\s+be))?\s*:?\s*(\d+)\s*word", "abstract"),
        (r"main\s+text(?:\s+(?:up\s+to|no\s+more\s+than|maximum|limit|should\s+be))?\s*:?\s*(\d+)\s*word", "main"),
        (r"manuscript(?:\s+(?:up\s+to|no\s+more\s+than|maximum|limit|should\s+be))?\s*:?\s*(\d+)\s*word", "main"),
        (r"(\d+)\s*word.*?abstract", "abstract"),
        (r"(\d+)\s*word.*?main", "main"),
        (r"references?\s*:?\s*(\d+)", "refs"),
    ]
    
    text_lower = text.lower()
    for pattern, field in patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                word_counts[field] = int(match.group(1))
            except (ValueError, IndexError):
                pass
    
    return word_counts

def _extract_refs_style(text: str) -> str:
    """Extract reference style from guideline text"""
    text_lower = text.lower()
    
    # Reference style patterns
    if re.search(r'vancouver.*superscript|superscript.*vancouver|numbered.*superscript', text_lower):
        return "Vancouver superscript"
    elif re.search(r'vancouver.*bracket|bracket.*vancouver|numbered.*bracket', text_lower):
        return "Vancouver bracket"
    elif re.search(r'harvard|author.year|author-year|\(author.*year\)', text_lower):
        return "Harvard author-year"
    elif re.search(r'ama\s+style|american\s+medical\s+association', text_lower):
        return "AMA"
    elif re.search(r'apa\s+style|american\s+psychological', text_lower):
        return "APA"
    elif re.search(r'vancouver', text_lower):
        return "Vancouver"
    else:
        return "Unknown"

def _extract_fig_limits(text: str) -> Dict[str, Optional[int]]:
    """Extract figure limits from guideline text"""
    fig_limits = {}
    
    patterns = [
        r'(?:up\s+to|maximum|no\s+more\s+than|limit)\s*(\d+)\s*figure',
        r'(\d+)\s*figure.*(?:maximum|allowed|permitted)',
        r'figure.*limit.*?(\d+)',
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                fig_limits["max"] = int(match.group(1))
                break
            except (ValueError, IndexError):
                pass
    
    return fig_limits

def _extract_table_limits(text: str) -> Dict[str, Optional[int]]:
    """Extract table limits from guideline text"""
    table_limits = {}
    
    patterns = [
        r'(?:up\s+to|maximum|no\s+more\s+than|limit)\s*(\d+)\s*table',
        r'(\d+)\s*table.*(?:maximum|allowed|permitted)',
        r'table.*limit.*?(\d+)',
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                table_limits["max"] = int(match.group(1))
                break
            except (ValueError, IndexError):
                pass
    
    return table_limits

def _extract_image_specs(text: str) -> Dict[str, Optional[int]]:
    """Extract image specifications from guideline text"""
    image_specs = {}
    
    # DPI patterns
    dpi_patterns = [
        r'(\d+)\s*dpi',
        r'resolution.*?(\d+)',
        r'(\d+).*resolution',
    ]
    
    # Width patterns  
    width_patterns = [
        r'width.*?(\d+)\s*mm',
        r'(\d+)\s*mm.*width',
        r'width.*?(\d+)\s*cm',
    ]
    
    text_lower = text.lower()
    
    for pattern in dpi_patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                image_specs["dpi"] = int(match.group(1))
                break
            except (ValueError, IndexError):
                pass
    
    for pattern in width_patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                width = int(match.group(1))
                # Convert cm to mm if needed
                if 'cm' in match.group(0):
                    width *= 10
                image_specs["width_mm"] = width
                break
            except (ValueError, IndexError):
                pass
    
    return image_specs

def _extract_sections(text: str) -> List[str]:
    """Extract required sections from guideline text"""
    # Common section patterns
    common_sections = [
        "Abstract", "Introduction", "Methods", "Results", 
        "Discussion", "Conclusion", "References", "Acknowledgments",
        "Supplementary Information", "Supporting Information",
        "Materials and Methods", "Background"
    ]
    
    found_sections = []
    text_lower = text.lower()
    
    for section in common_sections:
        if section.lower() in text_lower:
            found_sections.append(section)
    
    return found_sections

def _extract_supplement_rules(text: str) -> List[str]:
    """Extract supplementary material rules from guideline text"""
    supplement_rules = []
    text_lower = text.lower()
    
    # Common supplement patterns
    if re.search(r'methods.*supplement|supplement.*methods', text_lower):
        supplement_rules.append("methods online")
    
    if re.search(r'detailed.*protocol.*supplement', text_lower):
        supplement_rules.append("detailed protocols online")
        
    if re.search(r'statistical.*supplement', text_lower):
        supplement_rules.append("statistical methods online")
    
    if re.search(r'extended.*data|extended.*figure', text_lower):
        supplement_rules.append("extended data allowed")
    
    return supplement_rules