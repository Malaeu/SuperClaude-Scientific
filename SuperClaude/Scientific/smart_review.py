"""
Smart Literature Review Engine for Medical Research

This module provides intelligent literature review capabilities with iterative
question refinement and knowledge gap identification specifically designed
for medical and scientific research.
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class SearchIteration:
    """Represents a single iteration in the smart review loop."""
    iteration_number: int
    question: str
    search_terms: List[str]
    databases: List[str]
    papers_found: int
    papers_relevant: int
    key_findings: List[str]
    knowledge_gaps: List[str]
    next_question: Optional[str] = None
    completed_at: Optional[str] = None
    

@dataclass
class ResearchGap:
    """Represents an identified knowledge gap requiring research."""
    gap_type: str  # methodological, population, temporal, geographic
    description: str
    priority: str  # high, medium, low
    research_opportunity: str
    feasibility_score: int  # 1-10 scale
    clinical_impact: int  # 1-10 scale


@dataclass
class LiteratureEvidence:
    """Represents evidence from literature review."""
    paper_id: str
    title: str
    authors: List[str]
    journal: str
    year: int
    study_type: str
    sample_size: int
    key_findings: List[str]
    quality_score: int  # 1-10 scale
    clinical_relevance: int  # 1-10 scale
    doi: Optional[str] = None


class SmartReviewEngine:
    """
    Intelligent literature review engine with iterative question refinement.
    
    This engine conducts systematic literature reviews using a smart loop
    approach, progressively refining search questions based on accumulated
    knowledge and identified gaps.
    """
    
    def __init__(self, project_name: str, domain: str = "medical", max_iterations: int = 10):
        """
        Initialize the Smart Review Engine.
        
        Args:
            project_name: Name of the research project
            domain: Research domain (medical, liver, cardiac, etc.)
            max_iterations: Maximum number of review iterations
        """
        self.project_name = project_name
        self.domain = domain
        self.max_iterations = max_iterations
        self.current_iteration = 0
        
        # Knowledge base storage
        self.iterations: List[SearchIteration] = []
        self.evidence_base: List[LiteratureEvidence] = []
        self.knowledge_gaps: List[ResearchGap] = []
        
        # Progress tracking
        self.total_papers_reviewed = 0
        self.unique_references = set()
        self.evidence_sufficiency = "insufficient"  # insufficient, approaching_complete, complete
        
        # Configuration
        self.databases = ["pubmed", "web_of_science", "cochrane", "embase"]
        self.quality_threshold = 6  # Minimum quality score for inclusion
        self.sufficiency_criteria = {
            "min_papers": 50,
            "min_high_quality": 20,
            "coverage_threshold": 0.8
        }
    
    def start_review(self, initial_question: str, research_context: Dict = None) -> Dict:
        """
        Start the smart literature review process.
        
        Args:
            initial_question: The initial broad research question
            research_context: Context including existing results, methods, domain knowledge
            
        Returns:
            Dictionary containing review initialization status and first iteration plan
        """
        self.current_iteration = 1
        
        # Generate initial search terms based on question and context
        search_terms = self._generate_initial_search_terms(initial_question, research_context)
        
        # Create first iteration
        first_iteration = SearchIteration(
            iteration_number=1,
            question=initial_question,
            search_terms=search_terms,
            databases=self.databases,
            papers_found=0,
            papers_relevant=0,
            key_findings=[],
            knowledge_gaps=[]
        )
        
        self.iterations.append(first_iteration)
        
        return {
            "status": "review_started",
            "project_name": self.project_name,
            "initial_question": initial_question,
            "search_terms": search_terms,
            "databases": self.databases,
            "next_action": "execute_search_iteration"
        }
    
    def execute_iteration(self, iteration_number: int, search_results: List[Dict]) -> Dict:
        """
        Execute a single review iteration with provided search results.
        
        Args:
            iteration_number: Current iteration number
            search_results: List of papers found in search
            
        Returns:
            Dictionary containing iteration results and next steps
        """
        if iteration_number > len(self.iterations):
            raise ValueError(f"Invalid iteration number: {iteration_number}")
        
        current_iteration = self.iterations[iteration_number - 1]
        
        # Process search results
        relevant_papers = self._filter_relevant_papers(search_results, current_iteration.question)
        high_quality_papers = self._assess_paper_quality(relevant_papers)
        
        # Extract key findings
        key_findings = self._extract_key_findings(high_quality_papers, current_iteration.question)
        
        # Identify knowledge gaps
        knowledge_gaps = self._identify_knowledge_gaps(
            high_quality_papers, 
            self._get_accumulated_knowledge()
        )
        
        # Update iteration with results
        current_iteration.papers_found = len(search_results)
        current_iteration.papers_relevant = len(relevant_papers)
        current_iteration.key_findings = key_findings
        current_iteration.knowledge_gaps = knowledge_gaps
        current_iteration.completed_at = datetime.now().isoformat()
        
        # Add evidence to base
        for paper in high_quality_papers:
            evidence = self._convert_to_evidence(paper)
            self.evidence_base.append(evidence)
            self.unique_references.add(evidence.paper_id)
        
        self.total_papers_reviewed += len(relevant_papers)
        
        # Generate next question if not at max iterations
        next_question = None
        if self.current_iteration < self.max_iterations:
            next_question = self._generate_next_question(
                current_iteration, 
                self._get_accumulated_knowledge()
            )
            current_iteration.next_question = next_question
        
        # Check evidence sufficiency
        self._update_evidence_sufficiency()
        
        return {
            "iteration": iteration_number,
            "papers_found": current_iteration.papers_found,
            "papers_relevant": current_iteration.papers_relevant,
            "key_findings": key_findings,
            "knowledge_gaps": knowledge_gaps,
            "next_question": next_question,
            "evidence_sufficiency": self.evidence_sufficiency,
            "continue_review": self._should_continue_review()
        }
    
    def generate_next_iteration(self) -> Optional[SearchIteration]:
        """
        Generate the next iteration based on current knowledge and gaps.
        
        Returns:
            Next SearchIteration or None if review should stop
        """
        if not self._should_continue_review():
            return None
        
        self.current_iteration += 1
        last_iteration = self.iterations[-1]
        
        if not last_iteration.next_question:
            return None
        
        # Generate refined search terms for next question
        search_terms = self._refine_search_terms(
            last_iteration.next_question,
            self._get_accumulated_knowledge()
        )
        
        next_iteration = SearchIteration(
            iteration_number=self.current_iteration,
            question=last_iteration.next_question,
            search_terms=search_terms,
            databases=self.databases,
            papers_found=0,
            papers_relevant=0,
            key_findings=[],
            knowledge_gaps=[]
        )
        
        self.iterations.append(next_iteration)
        return next_iteration
    
    def get_review_status(self) -> Dict:
        """Get current review status and progress."""
        return {
            "project_name": self.project_name,
            "domain": self.domain,
            "current_iteration": self.current_iteration,
            "max_iterations": self.max_iterations,
            "total_papers_reviewed": self.total_papers_reviewed,
            "unique_references": len(self.unique_references),
            "evidence_sufficiency": self.evidence_sufficiency,
            "knowledge_gaps_identified": len(self.knowledge_gaps),
            "high_priority_gaps": len([g for g in self.knowledge_gaps if g.priority == "high"]),
            "iterations_completed": len([i for i in self.iterations if i.completed_at])
        }
    
    def generate_evidence_synthesis(self) -> Dict:
        """Generate comprehensive evidence synthesis across all iterations."""
        # Organize evidence by themes
        evidence_themes = self._categorize_evidence_by_themes()
        
        # Identify research priorities
        research_priorities = self._rank_research_opportunities()
        
        # Create synthesis report
        synthesis = {
            "review_summary": {
                "total_iterations": len(self.iterations),
                "papers_reviewed": self.total_papers_reviewed,
                "unique_references": len(self.unique_references),
                "evidence_quality_distribution": self._get_quality_distribution()
            },
            "evidence_themes": evidence_themes,
            "knowledge_gaps": {
                "high_priority": [asdict(g) for g in self.knowledge_gaps if g.priority == "high"],
                "medium_priority": [asdict(g) for g in self.knowledge_gaps if g.priority == "medium"],
                "low_priority": [asdict(g) for g in self.knowledge_gaps if g.priority == "low"]
            },
            "research_priorities": research_priorities,
            "clinical_implications": self._extract_clinical_implications(),
            "methodological_insights": self._extract_methodological_insights()
        }
        
        return synthesis
    
    def save_review_state(self, filepath: str) -> None:
        """Save current review state to file."""
        review_state = {
            "project_name": self.project_name,
            "domain": self.domain,
            "max_iterations": self.max_iterations,
            "current_iteration": self.current_iteration,
            "iterations": [asdict(i) for i in self.iterations],
            "evidence_base": [asdict(e) for e in self.evidence_base],
            "knowledge_gaps": [asdict(g) for g in self.knowledge_gaps],
            "total_papers_reviewed": self.total_papers_reviewed,
            "unique_references": list(self.unique_references),
            "evidence_sufficiency": self.evidence_sufficiency,
            "saved_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(review_state, f, indent=2)
    
    def load_review_state(self, filepath: str) -> None:
        """Load review state from file."""
        with open(filepath, 'r') as f:
            review_state = json.load(f)
        
        self.project_name = review_state["project_name"]
        self.domain = review_state["domain"]
        self.max_iterations = review_state["max_iterations"]
        self.current_iteration = review_state["current_iteration"]
        
        # Reconstruct objects
        self.iterations = [SearchIteration(**i) for i in review_state["iterations"]]
        self.evidence_base = [LiteratureEvidence(**e) for e in review_state["evidence_base"]]
        self.knowledge_gaps = [ResearchGap(**g) for g in review_state["knowledge_gaps"]]
        
        self.total_papers_reviewed = review_state["total_papers_reviewed"]
        self.unique_references = set(review_state["unique_references"])
        self.evidence_sufficiency = review_state["evidence_sufficiency"]
    
    # Private methods for internal processing
    
    def _generate_initial_search_terms(self, question: str, context: Dict = None) -> List[str]:
        """Generate initial search terms based on question and context."""
        # Basic term extraction (in real implementation, use NLP)
        base_terms = question.lower().split()
        
        # Domain-specific term expansion
        if self.domain == "liver":
            domain_terms = ["liver disease", "hepatology", "transplantation", "cirrhosis"]
        elif self.domain == "cardiac":
            domain_terms = ["cardiology", "heart disease", "cardiovascular"]
        else:
            domain_terms = []
        
        # Combine and deduplicate
        all_terms = base_terms + domain_terms
        return list(set(term.strip(".,?!") for term in all_terms if len(term) > 2))
    
    def _filter_relevant_papers(self, search_results: List[Dict], question: str) -> List[Dict]:
        """Filter papers based on relevance to current question."""
        # Simplified relevance scoring (in real implementation, use ML)
        relevant_papers = []
        question_terms = set(question.lower().split())
        
        for paper in search_results:
            title_terms = set(paper.get("title", "").lower().split())
            abstract_terms = set(paper.get("abstract", "").lower().split())
            
            # Calculate overlap score
            title_overlap = len(question_terms & title_terms) / len(question_terms)
            abstract_overlap = len(question_terms & abstract_terms) / len(question_terms)
            
            relevance_score = (title_overlap * 2 + abstract_overlap) / 3
            
            if relevance_score > 0.2:  # Threshold for relevance
                paper["relevance_score"] = relevance_score
                relevant_papers.append(paper)
        
        return sorted(relevant_papers, key=lambda x: x["relevance_score"], reverse=True)
    
    def _assess_paper_quality(self, papers: List[Dict]) -> List[Dict]:
        """Assess quality of papers based on various criteria."""
        high_quality_papers = []
        
        for paper in papers:
            quality_score = self._calculate_quality_score(paper)
            if quality_score >= self.quality_threshold:
                paper["quality_score"] = quality_score
                high_quality_papers.append(paper)
        
        return high_quality_papers
    
    def _calculate_quality_score(self, paper: Dict) -> int:
        """Calculate quality score for a paper (1-10 scale)."""
        score = 5  # Base score
        
        # Journal impact factor bonus
        if paper.get("impact_factor", 0) > 10:
            score += 2
        elif paper.get("impact_factor", 0) > 5:
            score += 1
        
        # Sample size bonus
        sample_size = paper.get("sample_size", 0)
        if sample_size > 1000:
            score += 2
        elif sample_size > 100:
            score += 1
        
        # Study design bonus
        study_type = paper.get("study_type", "").lower()
        if "randomized controlled trial" in study_type:
            score += 2
        elif "cohort" in study_type:
            score += 1
        
        # Publication year penalty for old papers
        year = paper.get("year", datetime.now().year)
        if datetime.now().year - year > 10:
            score -= 1
        
        return max(1, min(10, score))
    
    def _extract_key_findings(self, papers: List[Dict], question: str) -> List[str]:
        """Extract key findings relevant to current question."""
        findings = []
        
        for paper in papers[:10]:  # Limit to top 10 papers
            # Extract key results (simplified - would use NLP in real implementation)
            abstract = paper.get("abstract", "")
            if "result" in abstract.lower():
                # Find sentences containing results
                sentences = abstract.split(".")
                for sentence in sentences:
                    if any(keyword in sentence.lower() for keyword in ["significant", "showed", "demonstrated", "found"]):
                        findings.append(f"{paper.get('title', 'Unknown')}: {sentence.strip()}")
        
        return findings[:20]  # Limit number of findings
    
    def _identify_knowledge_gaps(self, papers: List[Dict], accumulated_knowledge: Dict) -> List[str]:
        """Identify knowledge gaps based on current literature."""
        gaps = []
        
        # Methodological gaps
        study_types = [p.get("study_type", "") for p in papers]
        if "randomized controlled trial" not in " ".join(study_types).lower():
            gaps.append("Limited randomized controlled trial evidence")
        
        # Population gaps
        populations = [p.get("population", "") for p in papers]
        if not any("diverse" in pop.lower() for pop in populations):
            gaps.append("Limited diverse population representation")
        
        # Temporal gaps
        years = [p.get("year", 0) for p in papers]
        if max(years) < datetime.now().year - 2:
            gaps.append("Limited recent evidence (within 2 years)")
        
        # Sample size gaps
        sample_sizes = [p.get("sample_size", 0) for p in papers]
        if max(sample_sizes) < 500:
            gaps.append("Limited large-scale studies (>500 participants)")
        
        return gaps
    
    def _generate_next_question(self, current_iteration: SearchIteration, accumulated_knowledge: Dict) -> str:
        """Generate next question based on current findings and gaps."""
        iteration_num = current_iteration.iteration_number
        
        # Progressive question refinement based on iteration number
        if iteration_num == 1:
            return f"What specific methodologies are used in {self.domain} research?"
        elif iteration_num == 2:
            return f"What are the clinical outcomes measured in {self.domain} studies?"
        elif iteration_num == 3:
            return f"What populations are underrepresented in {self.domain} research?"
        elif iteration_num == 4:
            return f"What interventions show promise in {self.domain}?"
        elif iteration_num >= 5:
            # Focus on identified gaps
            if current_iteration.knowledge_gaps:
                main_gap = current_iteration.knowledge_gaps[0]
                return f"How can we address: {main_gap}?"
        
        return f"What are the future research priorities in {self.domain}?"
    
    def _refine_search_terms(self, question: str, accumulated_knowledge: Dict) -> List[str]:
        """Refine search terms based on question and accumulated knowledge."""
        # Extract terms from question
        base_terms = question.lower().replace("?", "").split()
        
        # Add terms from accumulated knowledge
        knowledge_terms = []
        for evidence in self.evidence_base[-10:]:  # Recent evidence
            knowledge_terms.extend(evidence.title.lower().split())
        
        # Combine and rank by frequency
        all_terms = base_terms + knowledge_terms
        term_freq = {}
        for term in all_terms:
            clean_term = term.strip(".,!?()[]")
            if len(clean_term) > 3:
                term_freq[clean_term] = term_freq.get(clean_term, 0) + 1
        
        # Return top terms
        sorted_terms = sorted(term_freq.items(), key=lambda x: x[1], reverse=True)
        return [term for term, freq in sorted_terms[:15]]
    
    def _get_accumulated_knowledge(self) -> Dict:
        """Get accumulated knowledge from all completed iterations."""
        return {
            "total_papers": self.total_papers_reviewed,
            "key_findings": [f for iteration in self.iterations for f in iteration.key_findings],
            "identified_gaps": [g for iteration in self.iterations for g in iteration.knowledge_gaps],
            "evidence_base": self.evidence_base
        }
    
    def _update_evidence_sufficiency(self) -> None:
        """Update evidence sufficiency status based on current state."""
        criteria = self.sufficiency_criteria
        
        if (self.total_papers_reviewed >= criteria["min_papers"] and
            len([e for e in self.evidence_base if e.quality_score >= 8]) >= criteria["min_high_quality"]):
            
            # Check coverage across different dimensions
            study_types = set(e.study_type for e in self.evidence_base)
            years = set(e.year for e in self.evidence_base)
            
            coverage_score = (len(study_types) / 5 + len(years) / 10) / 2  # Normalize
            
            if coverage_score >= criteria["coverage_threshold"]:
                self.evidence_sufficiency = "complete"
            else:
                self.evidence_sufficiency = "approaching_complete"
        else:
            self.evidence_sufficiency = "insufficient"
    
    def _should_continue_review(self) -> bool:
        """Determine if review should continue based on various criteria."""
        return (self.current_iteration < self.max_iterations and
                self.evidence_sufficiency != "complete" and
                len(self.iterations) > 0 and
                self.iterations[-1].papers_relevant > 0)
    
    def _convert_to_evidence(self, paper: Dict) -> LiteratureEvidence:
        """Convert paper dictionary to LiteratureEvidence object."""
        return LiteratureEvidence(
            paper_id=paper.get("id", f"paper_{len(self.evidence_base)}"),
            title=paper.get("title", ""),
            authors=paper.get("authors", []),
            journal=paper.get("journal", ""),
            year=paper.get("year", 0),
            study_type=paper.get("study_type", ""),
            sample_size=paper.get("sample_size", 0),
            key_findings=paper.get("key_findings", []),
            quality_score=paper.get("quality_score", 5),
            clinical_relevance=paper.get("clinical_relevance", 5),
            doi=paper.get("doi")
        )
    
    def _categorize_evidence_by_themes(self) -> Dict:
        """Categorize evidence by research themes."""
        themes = {
            "methodology": [],
            "outcomes": [],
            "populations": [],
            "interventions": []
        }
        
        for evidence in self.evidence_base:
            # Simple keyword-based categorization
            title_lower = evidence.title.lower()
            if any(word in title_lower for word in ["method", "approach", "technique"]):
                themes["methodology"].append(evidence.title)
            elif any(word in title_lower for word in ["outcome", "result", "effect"]):
                themes["outcomes"].append(evidence.title)
            elif any(word in title_lower for word in ["population", "cohort", "patient"]):
                themes["populations"].append(evidence.title)
            elif any(word in title_lower for word in ["intervention", "treatment", "therapy"]):
                themes["interventions"].append(evidence.title)
        
        return themes
    
    def _rank_research_opportunities(self) -> List[Dict]:
        """Rank research opportunities based on identified gaps."""
        opportunities = []
        
        for gap in self.knowledge_gaps:
            opportunity = {
                "description": gap.research_opportunity,
                "priority": gap.priority,
                "feasibility": gap.feasibility_score,
                "clinical_impact": gap.clinical_impact,
                "overall_score": (gap.feasibility_score + gap.clinical_impact) / 2
            }
            opportunities.append(opportunity)
        
        return sorted(opportunities, key=lambda x: x["overall_score"], reverse=True)
    
    def _get_quality_distribution(self) -> Dict:
        """Get distribution of evidence quality scores."""
        scores = [e.quality_score for e in self.evidence_base]
        return {
            "high_quality": len([s for s in scores if s >= 8]),
            "medium_quality": len([s for s in scores if 6 <= s < 8]),
            "low_quality": len([s for s in scores if s < 6]),
            "average_score": sum(scores) / len(scores) if scores else 0
        }
    
    def _extract_clinical_implications(self) -> List[str]:
        """Extract clinical implications from evidence base."""
        implications = []
        
        # Extract from high-quality, high-relevance papers
        for evidence in self.evidence_base:
            if evidence.quality_score >= 8 and evidence.clinical_relevance >= 8:
                implications.extend(evidence.key_findings)
        
        return implications[:10]  # Limit to top implications
    
    def _extract_methodological_insights(self) -> List[str]:
        """Extract methodological insights from evidence base."""
        insights = []
        
        # Analyze study designs and methods
        study_types = [e.study_type for e in self.evidence_base]
        sample_sizes = [e.sample_size for e in self.evidence_base]
        
        insights.append(f"Most common study design: {max(set(study_types), key=study_types.count)}")
        insights.append(f"Average sample size: {sum(sample_sizes) / len(sample_sizes):.0f}")
        
        return insights