"""
Recommendation Engine
Routes students to: International University, Local University, Apprenticeship, or Micro-Credentials
Based on psychometric scores and financial context
"""

class RecommendationEngine:
    def __init__(self):
        self.pathways = {
            'International University': {
                'ideal_profile': {
                    'grit': (5, 10),
                    'hands_on': (0, 6),
                    'structure': (6, 10),
                    'risk_tolerance': (3, 7)
                },
                'min_budget': 30000,
                'description': 'Traditional 4-year international degree program'
            },
            'Local University': {
                'ideal_profile': {
                    'grit': (4, 10),
                    'hands_on': (0, 7),
                    'structure': (5, 10),
                    'risk_tolerance': (4, 8)
                },
                'min_budget': 10000,
                'description': 'Domestic 4-year degree program with lower costs'
            },
            'Apprenticeship': {
                'ideal_profile': {
                    'grit': (6, 10),
                    'hands_on': (7, 10),
                    'structure': (4, 9),
                    'risk_tolerance': (5, 10)
                },
                'min_budget': 0,
                'description': 'Earn while you learn - paid work-based training'
            },
            'Micro-Credentials': {
                'ideal_profile': {
                    'grit': (7, 10),
                    'hands_on': (6, 10),
                    'structure': (0, 6),
                    'risk_tolerance': (6, 10)
                },
                'min_budget': 5000,
                'description': 'Bootcamps, certificates, and project-based learning'
            }
        }
    
    def calculate_fit_score(self, scores, pathway_profile):
        """
        Calculate how well a student's scores match a pathway's ideal profile
        Returns score from 0-100
        """
        fit_score = 0
        dimensions = ['grit', 'hands_on', 'structure', 'risk_tolerance']
        
        for dimension in dimensions:
            student_score = scores[dimension]
            ideal_range = pathway_profile[dimension]
            
            # Check if score is in ideal range
            if ideal_range[0] <= student_score <= ideal_range[1]:
                # Perfect fit - in ideal range
                fit_score += 25
            else:
                # Calculate distance from ideal range
                if student_score < ideal_range[0]:
                    distance = ideal_range[0] - student_score
                else:
                    distance = student_score - ideal_range[1]
                
                # Deduct points based on distance (max 10 points away)
                penalty = min(distance * 2.5, 25)
                fit_score += (25 - penalty)
        
        return round(fit_score, 1)
    
    def get_recommendation(self, scores, user_data):
        """
        Generate pathway recommendation based on psychometric scores and budget
        
        Args:
            scores: Dict with psychometric scores
            user_data: Dict with user profile (budget, interests, etc.)
        
        Returns:
            Dict with recommended pathway and reasoning
        """
        budget = user_data['budget']
        
        # Calculate fit scores for each pathway
        fit_scores = {}
        for pathway, config in self.pathways.items():
            # Check budget eligibility
            if budget >= config['min_budget']:
                fit_scores[pathway] = self.calculate_fit_score(
                    scores, 
                    config['ideal_profile']
                )
            else:
                fit_scores[pathway] = 0  # Not affordable
        
        # Get best fitting pathway
        recommended_pathway = max(fit_scores, key=fit_scores.get)
        fit_score = fit_scores[recommended_pathway]
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            recommended_pathway, 
            scores, 
            user_data,
            fit_score
        )
        
        # Generate alternative suggestion
        alternative = self._generate_alternative(
            recommended_pathway,
            scores,
            user_data,
            fit_scores
        )
        
        # Generate next steps
        next_steps = self._generate_next_steps(recommended_pathway, user_data)
        
        return {
            'pathway': recommended_pathway,
            'fit_score': fit_score,
            'reasoning': reasoning,
            'alternative_suggestion': alternative,
            'next_steps': next_steps,
            'all_fit_scores': fit_scores
        }
    
    def _generate_reasoning(self, pathway, scores, user_data, fit_score):
        """Generate explanation for why this pathway was recommended"""
        reasons = []
        
        # Psychometric-based reasoning
        if pathway == 'International University':
            if scores['structure'] >= 6:
                reasons.append("You thrive in structured academic environments")
            if scores['hands_on'] <= 6:
                reasons.append("You prefer theoretical learning over hands-on work")
            if user_data['budget'] >= 50000:
                reasons.append("Your budget supports international education costs")
        
        elif pathway == 'Local University':
            if scores['structure'] >= 5:
                reasons.append("You benefit from formal academic structure")
            if user_data['budget'] < 50000:
                reasons.append("Local university optimizes ROI within your budget")
            if scores['risk_tolerance'] >= 4 and scores['risk_tolerance'] <= 8:
                reasons.append("You seek a balanced risk-reward profile")
        
        elif pathway == 'Apprenticeship':
            if scores['hands_on'] >= 7:
                reasons.append("You're a hands-on learner who learns by doing")
            if scores['grit'] >= 6:
                reasons.append("Your high grit will help you excel in work-based learning")
            if user_data['current_income'] == 0 or user_data['budget'] < 20000:
                reasons.append("Earning while learning addresses your financial constraints")
        
        elif pathway == 'Micro-Credentials':
            if scores['grit'] >= 7:
                reasons.append("Your self-motivation suits independent learning")
            if scores['structure'] <= 6:
                reasons.append("You don't need rigid academic structure to succeed")
            if scores['risk_tolerance'] >= 6:
                reasons.append("You're comfortable with non-traditional career paths")
            if scores['hands_on'] >= 6:
                reasons.append("You prefer project-based learning over lectures")
        
        # Add fit score context
        if fit_score >= 80:
            reasons.append(f"This pathway is an excellent match (fit score: {fit_score}/100)")
        elif fit_score >= 60:
            reasons.append(f"This pathway is a good match (fit score: {fit_score}/100)")
        else:
            reasons.append(f"This is your best option given constraints, but consider alternatives")
        
        return " • ".join(reasons) if reasons else "Based on your profile and budget constraints"
    
    def _generate_alternative(self, primary_pathway, scores, user_data, fit_scores):
        """Generate alternative pathway suggestion"""
        # Remove primary pathway from consideration
        alternative_scores = {k: v for k, v in fit_scores.items() if k != primary_pathway and v > 0}
        
        if not alternative_scores:
            return "No viable alternatives within budget constraints. Consider increasing budget or pursuing primary recommendation."
        
        # Get second-best option
        alternative_pathway = max(alternative_scores, key=alternative_scores.get)
        alternative_score = alternative_scores[alternative_pathway]
        
        return f"Alternative: {alternative_pathway} (fit score: {alternative_score}/100) - Consider if primary path shows negative ROI"
    
    def _generate_next_steps(self, pathway, user_data):
        """Generate actionable next steps"""
        steps = []
        
        if pathway == 'International University':
            steps.append("1. Research visa requirements for your target country")
            steps.append("2. Identify 5-10 universities with strong programs in your interest areas")
            steps.append("3. Calculate total cost of attendance including living expenses")
            steps.append("4. Apply for scholarships and financial aid")
            steps.append("5. Verify post-graduation work authorization policies")
        
        elif pathway == 'Local University':
            steps.append("1. Compare programs at local universities in your area")
            steps.append("2. Check eligibility for in-state tuition rates")
            steps.append("3. Apply for local scholarships and grants")
            steps.append("4. Consider part-time work during studies")
            steps.append("5. Network with alumni in your target industry")
        
        elif pathway == 'Apprenticeship':
            steps.append("1. Research registered apprenticeship programs in your interest areas")
            steps.append("2. Identify companies offering apprenticeships (check trade associations)")
            steps.append("3. Build a basic portfolio of relevant projects")
            steps.append("4. Prepare for employer interviews (they're evaluating work ethic)")
            steps.append("5. Consider hybrid: part-time apprenticeship + online courses")
        
        elif pathway == 'Micro-Credentials':
            steps.append("1. Identify top bootcamps/programs in your interest area (check reviews carefully)")
            steps.append("2. Build a portfolio of 3-5 projects BEFORE spending money")
            steps.append("3. Join online communities in your target field")
            steps.append("4. Start networking on LinkedIn (50+ connections in target industry)")
            steps.append("5. Consider: Free resources first (freeCodeCamp, Coursera audit) before paid programs")
        
        return "\n".join(steps)
