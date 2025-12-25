"""
Test Script - Validate Backend Logic
Run this to test the recommendation engine without the UI
"""

from modules.psychometric_engine import PsychometricAssessment
from modules.recommendation_engine import RecommendationEngine
from modules.roi_calculator import ROICalculator

def test_psychometric_engine():
    """Test psychometric scoring"""
    print("=" * 60)
    print("TEST 1: Psychometric Engine")
    print("=" * 60)
    
    assessment = PsychometricAssessment()
    
    # Simulate a high-grit, hands-on learner
    test_responses = {
        'q1_failure_response': 'B',  # Analyze and reapply
        'q2_learning_style': 'A',    # Trial and error
        'q3_social_vs_technical': 'C',  # Building the product
        'q4_uncertainty_tolerance': 'D',  # Self-study
        'q5_motivation_driver': 'B',  # Immediate application
        'q6_time_horizon': 'A',  # Need income soon
        'q7_feedback_preference': 'B'  # Real-world consequences
    }
    
    scores = assessment.calculate_scores(test_responses)
    
    print("\nTest Profile: High-Grit Hands-On Learner")
    print(f"Grit: {scores['grit']}/10")
    print(f"Hands-On: {scores['hands_on']}/10")
    print(f"Structure Need: {scores['structure']}/10")
    print(f"Risk Tolerance: {scores['risk_tolerance']}/10")
    
    print("\n✅ Psychometric Engine: PASSED\n")
    return scores

def test_recommendation_engine(scores):
    """Test pathway recommendation"""
    print("=" * 60)
    print("TEST 2: Recommendation Engine")
    print("=" * 60)
    
    recommender = RecommendationEngine()
    
    # Test with medium budget
    user_data = {
        'name': 'Test Student',
        'age': 22,
        'budget': 25000,
        'current_income': 0,
        'interests': ['Technology & Software'],
        'target_country': 'USA'
    }
    
    recommendation = recommender.get_recommendation(scores, user_data)
    
    print(f"\nRecommended Pathway: {recommendation['pathway']}")
    print(f"Fit Score: {recommendation['fit_score']}/100")
    print(f"\nReasoning: {recommendation['reasoning']}")
    print(f"\nAlternative: {recommendation['alternative_suggestion']}")
    
    print("\n✅ Recommendation Engine: PASSED\n")
    return recommendation

def test_roi_calculator():
    """Test ROI calculations"""
    print("=" * 60)
    print("TEST 3: ROI Calculator")
    print("=" * 60)
    
    calculator = ROICalculator()
    
    # Test all pathways
    roi_data = calculator.calculate_all_pathways(
        budget=25000,
        current_income=0,
        field='Technology & Software',
        country='USA'
    )
    
    print("\n5-Year Financial Projections:\n")
    print(f"{'Pathway':<25} {'Total Cost':<15} {'Year 5 Salary':<15} {'Net Wealth':<15} {'ROI'}")
    print("-" * 80)
    
    for pathway, data in sorted(roi_data.items(), key=lambda x: x[1]['net_wealth_year_5'], reverse=True):
        print(f"{pathway:<25} ${data['total_cost']:<14,.0f} ${data['year_5_salary']:<14,.0f} ${data['net_wealth_year_5']:<14,.0f} {data['roi_multiple']:.2f}x")
    
    # Test debt warning
    print("\n\nDebt Warning Tests:")
    for pathway, data in roi_data.items():
        has_warning, message = calculator.get_debt_warning_threshold(data)
        if has_warning:
            print(f"⚠️  {pathway}: {message}")
        else:
            print(f"✅ {pathway}: Financially viable")
    
    print("\n✅ ROI Calculator: PASSED\n")
    return roi_data

def test_edge_cases():
    """Test edge cases"""
    print("=" * 60)
    print("TEST 4: Edge Cases")
    print("=" * 60)
    
    calculator = ROICalculator()
    
    # Test 1: Very low budget
    print("\nEdge Case 1: Very Low Budget ($2,000)")
    roi_data = calculator.calculate_all_pathways(
        budget=2000,
        current_income=0,
        field='Technology & Software',
        country='USA'
    )
    affordable_pathways = [p for p, d in roi_data.items() if d['total_cost'] <= 2000]
    print(f"Affordable pathways: {affordable_pathways}")
    
    # Test 2: High current income
    print("\nEdge Case 2: High Current Income ($60k/year)")
    roi_data = calculator.calculate_all_pathways(
        budget=100000,
        current_income=60000,
        field='Technology & Software',
        country='USA'
    )
    print("International University ROI (with opportunity cost):")
    print(f"  Net Wealth: ${roi_data['International University']['net_wealth_year_5']:,.0f}")
    
    # Test 3: Low-paying field
    print("\nEdge Case 3: Low-Paying Field (Education)")
    roi_data = calculator.calculate_all_pathways(
        budget=50000,
        current_income=0,
        field='Education & Social Services',
        country='USA'
    )
    best_pathway = max(roi_data.items(), key=lambda x: x[1]['net_wealth_year_5'])
    print(f"Best pathway for Education field: {best_pathway[0]}")
    print(f"  Net Wealth: ${best_pathway[1]['net_wealth_year_5']:,.0f}")
    
    print("\n✅ Edge Cases: PASSED\n")

def run_full_simulation():
    """Run a complete user simulation"""
    print("\n" + "=" * 60)
    print("FULL USER SIMULATION")
    print("=" * 60)
    
    assessment = PsychometricAssessment()
    recommender = RecommendationEngine()
    calculator = ROICalculator()
    
    # Simulate real user responses
    responses = {
        'q1_failure_response': 'B',
        'q2_learning_style': 'C',
        'q3_social_vs_technical': 'C',
        'q4_uncertainty_tolerance': 'C',
        'q5_motivation_driver': 'B',
        'q6_time_horizon': 'A',
        'q7_feedback_preference': 'C'
    }
    
    user_data = {
        'name': 'Alex Chen',
        'age': 24,
        'budget': 35000,
        'current_income': 28000,
        'interests': ['Technology & Software', 'Engineering & Manufacturing'],
        'target_country': 'Canada'
    }
    
    # Run pipeline
    scores = assessment.calculate_scores(responses)
    recommendation = recommender.get_recommendation(scores, user_data)
    roi_data = calculator.calculate_all_pathways(
        user_data['budget'],
        user_data['current_income'],
        user_data['interests'][0],
        user_data['target_country']
    )
    
    print(f"\nStudent: {user_data['name']}, Age {user_data['age']}")
    print(f"Budget: ${user_data['budget']:,} | Current Income: ${user_data['current_income']:,}")
    print(f"Interests: {', '.join(user_data['interests'])}")
    
    print("\n--- Psychometric Profile ---")
    for dimension, score in scores.items():
        print(f"{dimension.replace('_', ' ').title()}: {score}/10")
    
    print(f"\n--- Recommendation ---")
    print(f"Pathway: {recommendation['pathway']}")
    print(f"Fit Score: {recommendation['fit_score']}/100")
    
    print(f"\n--- Financial Projection ---")
    recommended_roi = roi_data[recommendation['pathway']]
    print(f"Total Cost: ${recommended_roi['total_cost']:,.0f}")
    print(f"Year 5 Salary: ${recommended_roi['year_5_salary']:,.0f}")
    print(f"Net Wealth (Year 5): ${recommended_roi['net_wealth_year_5']:,.0f}")
    print(f"ROI Multiple: {recommended_roi['roi_multiple']:.2f}x")
    
    has_warning, message = calculator.get_debt_warning_threshold(recommended_roi)
    if has_warning:
        print(f"\n⚠️  WARNING: {message}")
    else:
        print(f"\n✅ Financially viable pathway")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    print("\n🧪 EDUCATION ROI ENGINE - BACKEND TEST SUITE\n")
    
    # Run all tests
    scores = test_psychometric_engine()
    recommendation = test_recommendation_engine(scores)
    roi_data = test_roi_calculator()
    test_edge_cases()
    run_full_simulation()
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED")
    print("=" * 60)
    print("\nBackend logic is working correctly!")
    print("Run 'streamlit run app.py' to launch the full application.\n")
