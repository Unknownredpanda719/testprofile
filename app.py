"""
Education Path Finder - Modules
Contains all backend logic for assessments, recommendations, and data tracking
"""

from .psychometric_engine import PsychometricAssessment
from .recommendation_engine import RecommendationEngine
from .roi_calculator import ROICalculator
from .uk_programmes import get_programmes_for_pathway, get_all_programmes_for_pathway
from .uk_careers import get_careers_for_field, get_career_by_title
from .cv_analyzer import CVAnalyzer, analyze_cv_text, get_cv_insights, merge_cv_with_quiz
from .outcome_tracker import OutcomeTracker, create_outcome_tracking_link, generate_follow_up_email_template

__all__ = [
    # Core engines
    'PsychometricAssessment',
    'RecommendationEngine',
    'ROICalculator',
    
    # UK data
    'get_programmes_for_pathway',
    'get_all_programmes_for_pathway',
    'get_careers_for_field',
    'get_career_by_title',
    
    # CV analysis
    'CVAnalyzer',
    'analyze_cv_text',
    'get_cv_insights',
    'merge_cv_with_quiz',
    
    # Outcome tracking (THE MOAT)
    'OutcomeTracker',
    'create_outcome_tracking_link',
    'generate_follow_up_email_template'
]

__version__ = '2.0.0'
