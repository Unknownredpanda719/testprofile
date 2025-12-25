"""
CV & Text Analysis Module
Extracts skills, achievements, and personality traits from user-provided text or CVs
Uses keyword matching (no LLM = zero API costs)
"""

class CVAnalyzer:
    def __init__(self):
        # Keyword dictionaries mapped to psychometric dimensions
        self.keyword_categories = {
            'hands_on': {
                'keywords': [
                    # Making/Building
                    'built', 'created', 'designed', 'developed', 'constructed', 'assembled',
                    'made', 'crafted', 'engineered', 'fabricated', 'installed', 'repaired',
                    'fixed', 'maintained', 'renovated', 'restored',
                    
                    # Technical/Practical
                    'arduino', 'raspberry pi', ' 3d print', 'cnc', 'laser cut',
                    'woodwork', 'metalwork', 'electronics', 'robotics', 'mechanics',
                    'plumbing', 'electrical', 'carpentry', 'welding', 'soldering',
                    
                    # DIY/Maker
                    'workshop', 'garage', 'prototype', 'hack', 'mod', 'custom',
                    'hands-on', 'practical', 'physical', 'manual', 'technical'
                ],
                'weight': 1.5  # How much each match boosts the score
            },
            
            'grit': {
                'keywords': [
                    # Perseverance
                    'persevered', 'overcame', 'despite', 'challenge', 'difficult',
                    'struggled', 'failed', 'tried again', 'persisted', 'determined',
                    'resilient', 'tenacious', 'dedication', 'commitment',
                    
                    # Long-term effort
                    'marathon', 'years of', 'self-taught', 'practiced', 'trained',
                    'improved', 'progressed', 'developed over', 'journey',
                    
                    # Achievements through effort
                    'award', 'achievement', 'competition', 'championship', 'medal',
                    'distinction', 'honors', 'scholarship', 'recognition',
                    
                    # Recovery/Growth
                    'setback', 'obstacle', 'barrier', 'difficulty', 'adversity'
                ],
                'weight': 1.0
            },
            
            'structure': {
                'keywords': [
                    # Organized/Planning
                    'organized', 'planned', 'scheduled', 'structured', 'systematic',
                    'process', 'procedure', 'framework', 'methodology', 'strategy',
                    'agenda', 'timeline', 'roadmap', 'checklist', 'protocol',
                    
                    # Academic/Formal
                    'research', 'thesis', 'dissertation', 'paper', 'study',
                    'analysis', 'methodology', 'framework', 'academic',
                    
                    # Compliance/Rules
                    'policy', 'regulation', 'compliance', 'standard', 'guideline',
                    'certification', 'accredited', 'qualified', 'licensed'
                ],
                'weight': 1.0
            },
            
            'risk_tolerance': {
                'keywords': [
                    # Entrepreneurial
                    'startup', 'founded', 'launched', 'business', 'venture',
                    'entrepreneur', 'self-employed', 'freelance', 'independent',
                    
                    # Innovation/Creativity
                    'innovative', 'experimental', 'novel', 'creative', 'original',
                    'unique', 'unconventional', 'pioneered', 'first to',
                    
                    # Risk-taking
                    'risk', 'bold', 'ambitious', 'challenged', 'pushed boundaries',
                    'explored', 'ventured', 'gamble', 'uncertain',
                    
                    # Change/Adaptability
                    'changed', 'adapted', 'flexible', 'pivoted', 'transformed',
                    'evolved', 'adjusted', 'dynamic'
                ],
                'weight': 1.0
            },
            
            'leadership': {
                'keywords': [
                    # Leadership roles
                    'led', 'managed', 'supervised', 'directed', 'coordinated',
                    'captain', 'president', 'chair', 'head', 'chief', 'leader',
                    'founder', 'co-founder', 'director', 'manager',
                    
                    # Team influence
                    'mentored', 'coached', 'trained', 'taught', 'guided',
                    'motivated', 'inspired', 'delegated', 'organized team',
                    
                    # Initiative
                    'initiated', 'established', 'created team', 'recruited',
                    'mobilized', 'rallied', 'united'
                ],
                'weight': 1.2
            },
            
            'academic_strength': {
                'keywords': [
                    # Academic achievements
                    'grade a', 'a*', 'distinction', 'first class', 'honors',
                    'scholarship', 'academic award', 'dean\'s list',
                    
                    # Research/Writing
                    'research', 'published', 'thesis', 'dissertation', 'paper',
                    'journal', 'conference', 'presentation', 'analysis',
                    
                    # Advanced study
                    'advanced', 'higher level', 'university course', 'ap',
                    'extension', 'enrichment', 'gifted'
                ],
                'weight': 1.0
            },
            
            'work_experience': {
                'keywords': [
                    # Employment
                    'worked', 'employed', 'job', 'position', 'role',
                    'internship', 'placement', 'apprenticeship', 'work experience',
                    
                    # Responsibilities
                    'responsible for', 'duties', 'tasks', 'managed',
                    'handled', 'operated', 'served', 'assisted',
                    
                    # Duration indicators
                    'part-time', 'full-time', 'summer job', 'weekend',
                    'months', 'years', 'currently working'
                ],
                'weight': 1.0
            }
        }
        
    def analyze_text(self, text):
        """
        Analyze free-form text or CV content
        Returns scores and insights
        """
        if not text or len(text.strip()) < 10:
            return {
                'scores': {},
                'insights': [],
                'keywords_found': {},
                'total_matches': 0
            }
        
        text_lower = text.lower()
        
        scores = {}
        keywords_found = {}
        insights = []
        
        for category, data in self.keyword_categories.items():
            matches = []
            for keyword in data['keywords']:
                if keyword in text_lower:
                    matches.append(keyword)
            
            if matches:
                # Calculate score (capped at 10)
                raw_score = len(matches) * data['weight']
                score = min(raw_score / 2, 10)  # Normalize to 0-10 scale
                
                scores[category] = round(score, 1)
                keywords_found[category] = matches[:5]  # Store first 5 matches
                
                # Generate insight
                if score >= 7:
                    level = "strong"
                elif score >= 4:
                    level = "moderate"
                else:
                    level = "some"
                
                insights.append({
                    'category': category,
                    'level': level,
                    'score': score,
                    'examples': matches[:3]  # First 3 examples
                })
        
        return {
            'scores': scores,
            'insights': insights,
            'keywords_found': keywords_found,
            'total_matches': sum(len(v) for v in keywords_found.values())
        }
    
    def merge_with_quiz_scores(self, quiz_scores, cv_scores):
        """
        Intelligently merge quiz scores with CV-derived scores
        CV scores boost quiz scores but don't replace them
        """
        merged = quiz_scores.copy()
        
        # Map CV categories to quiz dimensions
        category_mapping = {
            'hands_on': 'hands_on',
            'grit': 'grit',
            'structure': 'structure',
            'risk_tolerance': 'risk_tolerance'
        }
        
        for cv_category, quiz_dimension in category_mapping.items():
            if cv_category in cv_scores:
                cv_score = cv_scores[cv_category]
                quiz_score = merged.get(quiz_dimension, 5)  # Default 5 if missing
                
                # Weighted average: 70% quiz, 30% CV
                # This ensures quiz is primary but CV provides supporting evidence
                merged[quiz_dimension] = round((quiz_score * 0.7) + (cv_score * 0.3), 1)
        
        return merged
    
    def generate_profile_summary(self, analysis_results):
        """
        Generate human-readable summary of CV analysis
        """
        insights = analysis_results['insights']
        
        if not insights:
            return "No additional profile information detected."
        
        # Sort by score
        insights_sorted = sorted(insights, key=lambda x: x['score'], reverse=True)
        
        summary_parts = []
        
        for insight in insights_sorted[:3]:  # Top 3 traits
            category = insight['category'].replace('_', ' ').title()
            level = insight['level']
            examples = insight['examples'][:2]
            
            if examples:
                example_text = f"(e.g., {', '.join(examples)})"
            else:
                example_text = ""
            
            summary_parts.append(f"**{level.title()} {category}** {example_text}")
        
        return " • ".join(summary_parts)


# Convenience functions for easy import
def analyze_cv_text(text):
    """Quick function to analyze text and return scores"""
    analyzer = CVAnalyzer()
    result = analyzer.analyze_text(text)
    return result['scores']

def get_cv_insights(text):
    """Get full analysis with insights"""
    analyzer = CVAnalyzer()
    return analyzer.analyze_text(text)

def merge_cv_with_quiz(quiz_scores, cv_text):
    """Analyze CV and merge with quiz scores"""
    analyzer = CVAnalyzer()
    cv_analysis = analyzer.analyze_text(cv_text)
    merged_scores = analyzer.merge_with_quiz_scores(quiz_scores, cv_analysis['scores'])
    return merged_scores, cv_analysis
