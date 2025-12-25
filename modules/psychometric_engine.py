"""
Psychometric Assessment Engine
Measures: Grit, Hands-on Preference, Structure Need, Risk Tolerance
"""

class PsychometricAssessment:
    def __init__(self):
        self.questions = [
            {
                'id': 'q1_failure_response',
                'text': 'You spent 6 months learning to code but failed your first technical interview. What do you do?',
                'options': {
                    'A': 'Take a break and reconsider if coding is right for me',
                    'B': 'Analyze what went wrong, practice more, and reapply',
                    'C': 'Look for a bootcamp or structured course to fill gaps',
                    'D': 'Switch to a different career path that might be easier'
                },
                'weights': {
                    'grit': {'A': 3, 'B': 9, 'C': 6, 'D': 1},
                    'hands_on': {'A': 5, 'B': 8, 'C': 4, 'D': 5},
                    'structure': {'A': 5, 'B': 3, 'C': 9, 'D': 7},
                    'risk_tolerance': {'A': 4, 'B': 8, 'C': 5, 'D': 2}
                }
            },
            {
                'id': 'q2_learning_style',
                'text': 'Which learning experience sounds MOST appealing to you?',
                'options': {
                    'A': 'Building projects and learning by trial and error',
                    'B': 'Following a structured curriculum with clear milestones',
                    'C': 'Working under an experienced mentor in a real work environment',
                    'D': 'Watching online courses and reading documentation at my own pace'
                },
                'weights': {
                    'grit': {'A': 8, 'B': 6, 'C': 7, 'D': 4},
                    'hands_on': {'A': 9, 'B': 4, 'C': 10, 'D': 3},
                    'structure': {'A': 3, 'B': 10, 'C': 6, 'D': 5},
                    'risk_tolerance': {'A': 7, 'B': 5, 'C': 6, 'D': 6}
                }
            },
            {
                'id': 'q3_social_vs_technical',
                'text': 'In a group project, you naturally gravitate toward:',
                'options': {
                    'A': 'Coordinating the team and managing timelines',
                    'B': 'Doing deep technical work alone and presenting results',
                    'C': 'Building the actual product/deliverable',
                    'D': 'Researching best practices and creating documentation'
                },
                'weights': {
                    'grit': {'A': 6, 'B': 7, 'C': 8, 'D': 5},
                    'hands_on': {'A': 4, 'B': 6, 'C': 10, 'D': 3},
                    'structure': {'A': 7, 'B': 5, 'C': 4, 'D': 8},
                    'risk_tolerance': {'A': 7, 'B': 5, 'C': 8, 'D': 4}
                }
            },
            {
                'id': 'q4_uncertainty_tolerance',
                'text': 'You have $20,000. Which option appeals most?',
                'options': {
                    'A': 'Attend a prestigious university program ($20k/year for 4 years) - go into debt but get the degree',
                    'B': 'Attend a local state university ($8k/year) and graduate debt-free',
                    'C': 'Do a 6-month coding bootcamp ($15k) then start job hunting',
                    'D': 'Self-study with free resources and build a portfolio, keeping the $20k'
                },
                'weights': {
                    'grit': {'A': 5, 'B': 6, 'C': 8, 'D': 9},
                    'hands_on': {'A': 3, 'B': 4, 'C': 9, 'D': 10},
                    'structure': {'A': 9, 'B': 8, 'C': 6, 'D': 2},
                    'risk_tolerance': {'A': 3, 'B': 5, 'C': 7, 'D': 9}
                }
            },
            {
                'id': 'q5_motivation_driver',
                'text': 'What motivates you MOST to pursue further education?',
                'options': {
                    'A': 'The credential/degree itself (family expectations, visa requirements)',
                    'B': 'Learning skills I can immediately apply to earn money',
                    'C': 'Gaining deep theoretical knowledge in a field I love',
                    'D': 'Making professional connections and building a network'
                },
                'weights': {
                    'grit': {'A': 4, 'B': 8, 'C': 7, 'D': 6},
                    'hands_on': {'A': 2, 'B': 10, 'C': 4, 'D': 5},
                    'structure': {'A': 9, 'B': 4, 'C': 8, 'D': 6},
                    'risk_tolerance': {'A': 3, 'B': 8, 'C': 5, 'D': 7}
                }
            },
            {
                'id': 'q6_time_horizon',
                'text': 'When do you need to see results from your education investment?',
                'options': {
                    'A': 'Within 6-12 months (I need income soon)',
                    'B': '2-3 years (willing to invest time for better long-term outcome)',
                    'C': '4+ years (I can afford to take the traditional path)',
                    'D': "It doesn't matter - I'm learning for personal growth"
                },
                'weights': {
                    'grit': {'A': 7, 'B': 8, 'C': 5, 'D': 6},
                    'hands_on': {'A': 9, 'B': 7, 'C': 4, 'D': 5},
                    'structure': {'A': 4, 'B': 6, 'C': 9, 'D': 3},
                    'risk_tolerance': {'A': 8, 'B': 6, 'C': 4, 'D': 7}
                }
            },
            {
                'id': 'q7_feedback_preference',
                'text': 'How do you prefer to receive feedback on your work?',
                'options': {
                    'A': 'Regular structured assessments (exams, grades, formal reviews)',
                    'B': 'Real-world consequences (client reactions, product metrics)',
                    'C': 'Continuous feedback from a mentor or supervisor',
                    'D': 'Self-assessment based on my own standards'
                },
                'weights': {
                    'grit': {'A': 5, 'B': 9, 'C': 7, 'D': 8},
                    'hands_on': {'A': 3, 'B': 10, 'C': 8, 'D': 6},
                    'structure': {'A': 10, 'B': 4, 'C': 7, 'D': 2},
                    'risk_tolerance': {'A': 4, 'B': 8, 'C': 6, 'D': 7}
                }
            }
        ]
    
    def calculate_scores(self, responses):
        """
        Calculate psychometric scores based on responses
        
        Args:
            responses: Dict mapping question_id to selected option (A/B/C/D)
        
        Returns:
            Dict with scores for each dimension (normalized to 0-10)
        """
        scores = {
            'grit': 0,
            'hands_on': 0,
            'structure': 0,
            'risk_tolerance': 0
        }
        
        # Accumulate weighted scores
        for question in self.questions:
            q_id = question['id']
            if q_id in responses:
                selected_option = responses[q_id]
                weights = question['weights']
                
                for dimension in scores.keys():
                    scores[dimension] += weights[dimension][selected_option]
        
        # Normalize to 0-10 scale
        # Max possible score per dimension: 7 questions × 10 points = 70
        for dimension in scores.keys():
            scores[dimension] = round((scores[dimension] / 70) * 10, 1)
        
        return scores
    
    def get_profile_interpretation(self, scores):
        """Generate human-readable interpretation of scores"""
        interpretations = []
        
        if scores['grit'] >= 7:
            interpretations.append("High Grit: You have exceptional perseverance and will push through obstacles.")
        elif scores['grit'] >= 4:
            interpretations.append("Moderate Grit: You persist through challenges but may need external motivation.")
        else:
            interpretations.append("Lower Grit: You may benefit from highly structured environments with clear milestones.")
        
        if scores['hands_on'] >= 7:
            interpretations.append("Hands-On Learner: You learn best by building and doing, not passive study.")
        elif scores['hands_on'] >= 4:
            interpretations.append("Balanced Learner: You can adapt to both theoretical and practical learning.")
        else:
            interpretations.append("Theoretical Learner: You prefer conceptual understanding before application.")
        
        if scores['structure'] >= 7:
            interpretations.append("Structure-Seeking: You thrive in formal education with clear expectations.")
        elif scores['structure'] >= 4:
            interpretations.append("Flexible Structure Needs: You can work in both structured and self-directed environments.")
        else:
            interpretations.append("Independent Learner: You prefer self-directed learning over rigid curriculums.")
        
        if scores['risk_tolerance'] >= 7:
            interpretations.append("High Risk Tolerance: You're comfortable with uncertainty and non-traditional paths.")
        elif scores['risk_tolerance'] >= 4:
            interpretations.append("Moderate Risk Tolerance: You balance security with opportunity.")
        else:
            interpretations.append("Risk-Averse: You prefer established, proven pathways.")
        
        return "\n".join(interpretations)
