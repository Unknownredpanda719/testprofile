"""
Outcome Tracking System
Follows up with users to build proprietary dataset: Profile → Pathway → Outcome

This is THE moat. The data that makes you irreplaceable.
"""

from datetime import datetime, timedelta
import json

class OutcomeTracker:
    def __init__(self):
        """Initialize outcome tracking system"""
        self.tracking_enabled = True
    
    def capture_initial_decision(self, user_data, assessment_scores, recommendation, roi_data):
        """
        Capture student's initial state when they complete assessment
        This is the baseline we'll compare outcomes against
        
        Returns: Dictionary to store in Google Sheets
        """
        
        pathway_chosen = recommendation['pathway']
        
        # Calculate predicted outcomes
        predicted_roi = roi_data[pathway_chosen]
        
        tracking_data = {
            # User identification
            'timestamp': datetime.now().isoformat(),
            'email': user_data.get('email', ''),
            'name': user_data.get('name', ''),
            
            # Psychometric profile (anonymized for research)
            'grit_score': assessment_scores.get('grit', 0),
            'hands_on_score': assessment_scores.get('hands_on', 0),
            'structure_score': assessment_scores.get('structure', 0),
            'risk_tolerance_score': assessment_scores.get('risk_tolerance', 0),
            
            # Context
            'interest_field': user_data.get('interests', ['Unknown'])[0],
            'budget': user_data.get('budget', 0),
            'age': user_data.get('age', 18),
            'location': user_data.get('location', 'UK'),
            
            # Decision
            'recommended_pathway': pathway_chosen,
            'predicted_roi': predicted_roi['net_wealth_year_5'],
            'predicted_salary_year_5': predicted_roi['year_5_salary'],
            
            # Follow-up schedule
            'follow_up_6_months': (datetime.now() + timedelta(days=180)).isoformat(),
            'follow_up_12_months': (datetime.now() + timedelta(days=365)).isoformat(),
            'follow_up_24_months': (datetime.now() + timedelta(days=730)).isoformat(),
            
            # Tracking status
            'outcome_captured': False,
            'consent_to_follow_up': False
        }
        
        return tracking_data
    
    def generate_follow_up_questions(self, months_elapsed=6):
        """
        Generate questions for follow-up survey
        These build the proprietary outcome dataset
        """
        
        if months_elapsed == 6:
            return {
                'pathway_questions': [
                    {
                        'id': 'pathway_followed',
                        'question': 'Which pathway did you ultimately choose?',
                        'type': 'single_choice',
                        'options': [
                            'International University',
                            'Local University',
                            'Apprenticeship',
                            'Bootcamp/Micro-Credential',
                            'Took a gap year',
                            'Went straight to work',
                            'Still deciding'
                        ]
                    },
                    {
                        'id': 'pathway_same_as_recommended',
                        'question': 'Did you follow our recommendation?',
                        'type': 'boolean',
                        'options': ['Yes', 'No, I chose differently']
                    },
                    {
                        'id': 'if_different_why',
                        'question': 'If you chose differently, why?',
                        'type': 'text',
                        'optional': True
                    }
                ],
                
                'satisfaction_questions': [
                    {
                        'id': 'satisfaction_score',
                        'question': 'How satisfied are you with your choice? (1-10)',
                        'type': 'scale',
                        'range': [1, 10]
                    },
                    {
                        'id': 'regret_score',
                        'question': 'Do you have any regrets about your decision? (1-10, 1=no regrets)',
                        'type': 'scale',
                        'range': [1, 10]
                    },
                    {
                        'id': 'would_recommend',
                        'question': 'Would you recommend this pathway to someone similar to you?',
                        'type': 'boolean',
                        'options': ['Yes', 'No']
                    }
                ],
                
                'financial_questions': [
                    {
                        'id': 'current_debt',
                        'question': 'How much student debt do you currently have? (£)',
                        'type': 'number',
                        'optional': True
                    },
                    {
                        'id': 'current_earnings',
                        'question': 'If you\'re earning, what\'s your current salary? (£)',
                        'type': 'number',
                        'optional': True
                    }
                ],
                
                'outcome_questions': [
                    {
                        'id': 'current_status',
                        'question': 'What are you doing now?',
                        'type': 'single_choice',
                        'options': [
                            'Studying (university)',
                            'In apprenticeship',
                            'Completed bootcamp, now job hunting',
                            'Employed in my field',
                            'Employed, but not in my field',
                            'Still searching for opportunities',
                            'Took different path entirely'
                        ]
                    },
                    {
                        'id': 'biggest_surprise',
                        'question': 'What surprised you most about your chosen path?',
                        'type': 'text'
                    }
                ]
            }
        
        elif months_elapsed == 12:
            return {
                'employment_questions': [
                    {
                        'id': 'employment_status',
                        'question': 'What\'s your current employment status?',
                        'type': 'single_choice',
                        'options': [
                            'Employed full-time in my field',
                            'Employed full-time, different field',
                            'Employed part-time',
                            'Still studying',
                            'Unemployed, job hunting',
                            'Self-employed/Freelance'
                        ]
                    },
                    {
                        'id': 'current_salary',
                        'question': 'Current annual salary? (£, or "Still studying")',
                        'type': 'number'
                    },
                    {
                        'id': 'job_satisfaction',
                        'question': 'Job satisfaction (1-10)',
                        'type': 'scale',
                        'range': [1, 10]
                    }
                ],
                
                'roi_validation': [
                    {
                        'id': 'total_cost_so_far',
                        'question': 'Total education cost so far (tuition + living)? (£)',
                        'type': 'number'
                    },
                    {
                        'id': 'total_debt',
                        'question': 'Total student debt? (£)',
                        'type': 'number'
                    },
                    {
                        'id': 'roi_vs_predicted',
                        'question': 'How does your financial situation compare to what we predicted?',
                        'type': 'single_choice',
                        'options': [
                            'Much better than predicted',
                            'Slightly better',
                            'About the same',
                            'Slightly worse',
                            'Much worse than predicted'
                        ]
                    }
                ]
            }
        
        elif months_elapsed == 24:
            return {
                'final_outcome': [
                    {
                        'id': 'final_employment',
                        'question': 'Current employment?',
                        'type': 'text'
                    },
                    {
                        'id': 'final_salary',
                        'question': 'Current salary? (£)',
                        'type': 'number'
                    },
                    {
                        'id': 'total_debt_final',
                        'question': 'Total remaining debt? (£)',
                        'type': 'number'
                    },
                    {
                        'id': 'net_wealth',
                        'question': 'Approximate net wealth (assets - debts)? (£)',
                        'type': 'number'
                    },
                    {
                        'id': 'overall_satisfaction',
                        'question': 'Overall satisfaction with pathway choice (1-10)',
                        'type': 'scale',
                        'range': [1, 10]
                    },
                    {
                        'id': 'advice_to_past_self',
                        'question': 'Knowing what you know now, what would you tell your 18-year-old self?',
                        'type': 'text'
                    }
                ]
            }
    
    def calculate_prediction_accuracy(self, initial_data, outcome_data):
        """
        Calculate how accurate our predictions were
        This is the metric that proves your moat's value
        """
        
        predicted_roi = initial_data.get('predicted_roi', 0)
        predicted_salary = initial_data.get('predicted_salary_year_5', 0)
        
        actual_net_wealth = outcome_data.get('net_wealth', 0)
        actual_salary = outcome_data.get('final_salary', 0)
        
        roi_accuracy = 1 - abs(predicted_roi - actual_net_wealth) / max(abs(predicted_roi), 1)
        salary_accuracy = 1 - abs(predicted_salary - actual_salary) / max(predicted_salary, 1)
        
        return {
            'roi_accuracy': max(0, min(roi_accuracy, 1)),  # Clamp 0-1
            'salary_accuracy': max(0, min(salary_accuracy, 1)),
            'predicted_roi': predicted_roi,
            'actual_roi': actual_net_wealth,
            'predicted_salary': predicted_salary,
            'actual_salary': actual_salary,
            'prediction_error': abs(predicted_roi - actual_net_wealth)
        }
    
    def build_evidence_statement(self, profile_type, pathway, outcomes_data):
        """
        Generate evidence-based recommendation from outcome data
        This is what Claude CAN'T do - you have real evidence
        
        Example: "83% of high-grit, hands-on students who chose apprenticeships
                 report 9/10 satisfaction after 12 months, with average salary of £28k"
        """
        
        if not outcomes_data or len(outcomes_data) < 10:
            return None  # Need minimum 10 data points
        
        # Filter outcomes for similar profiles
        similar_outcomes = [
            o for o in outcomes_data 
            if o['pathway'] == pathway 
            and abs(o['grit_score'] - profile_type['grit']) < 2
            and abs(o['hands_on_score'] - profile_type['hands_on']) < 2
        ]
        
        if len(similar_outcomes) < 5:
            return None
        
        # Calculate statistics
        avg_satisfaction = sum(o['satisfaction_score'] for o in similar_outcomes) / len(similar_outcomes)
        avg_salary = sum(o['current_salary'] for o in similar_outcomes if o.get('current_salary')) / len([o for o in similar_outcomes if o.get('current_salary')])
        success_rate = len([o for o in similar_outcomes if o['satisfaction_score'] >= 7]) / len(similar_outcomes)
        
        evidence = {
            'sample_size': len(similar_outcomes),
            'avg_satisfaction': round(avg_satisfaction, 1),
            'avg_salary': round(avg_salary, 0),
            'success_rate': round(success_rate * 100, 0),
            'confidence': 'high' if len(similar_outcomes) > 20 else 'moderate',
            
            'statement': f"""
            Based on {len(similar_outcomes)} students with similar profiles who chose {pathway}:
            
            • {round(success_rate * 100)}% report high satisfaction (7+/10)
            • Average salary after 12 months: £{int(avg_salary):,}
            • Average satisfaction score: {avg_satisfaction}/10
            
            This is real evidence from students like you, not predictions.
            """
        }
        
        return evidence


def create_outcome_tracking_link(user_email, tracking_id):
    """
    Generate unique tracking link for follow-up
    Example: https://yourapp.com/outcome-survey?id=abc123
    """
    import hashlib
    
    # Create unique ID
    unique_id = hashlib.sha256(f"{user_email}{tracking_id}".encode()).hexdigest()[:12]
    
    return f"https://education-path-finder.streamlit.app/outcome-survey?id={unique_id}"


def generate_follow_up_email_template(user_name, pathway_chosen, months_elapsed=6):
    """
    Email template for outcome tracking
    Critical: This builds your data moat
    """
    
    if months_elapsed == 6:
        subject = f"Quick check-in: How's {pathway_chosen.lower()} going?"
        
        body = f"""
        Hi {user_name},
        
        It's been 6 months since you used Education Path Finder. We recommended 
        {pathway_chosen} based on your profile, and we'd love to know how it's going!
        
        WHY WE'RE ASKING:
        Your feedback helps future students like you make better decisions. We're 
        building the UK's first evidence-based pathway recommendation system - and 
        your real outcomes are the evidence.
        
        TAKES 2 MINUTES:
        → Did you follow our recommendation?
        → How satisfied are you? (1-10)
        → What surprised you most?
        
        [Take 2-min survey]
        
        WHAT YOU GET:
        • See how your outcome compares to others
        • Early access to our jobs-of-the-future predictor (coming soon!)
        • Entered to win £100 Amazon voucher
        
        Thanks for helping future students,
        Education Path Finder Team
        
        P.S. Your data is anonymized for research. We'll never share your personal details.
        """
    
    elif months_elapsed == 12:
        subject = "One year on: Share your journey (+ see our predictions vs reality)"
        
        body = f"""
        Hi {user_name},
        
        A year ago, we predicted {pathway_chosen} would work well for you.
        
        Were we right?
        
        We'd love to compare our predictions to your actual outcomes. This helps us 
        improve our recommendations for thousands of students.
        
        QUICK SURVEY (3 minutes):
        → Current salary/employment status
        → Satisfaction vs. expectations
        → Financial situation vs. what we predicted
        
        [Share your 12-month update]
        
        YOU'LL GET:
        • Personalized report: Our predictions vs. your reality
        • Access to aggregate data: "Students like you who chose X earn Y"
        • First look at our UK jobs predictor tool
        
        Your honest feedback makes this tool better for everyone.
        
        Cheers,
        Education Path Finder Team
        """
    
    return {
        'subject': subject,
        'body': body,
        'send_date': datetime.now() + timedelta(days=30 * months_elapsed)
    }
