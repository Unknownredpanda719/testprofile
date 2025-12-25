import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.psychometric_engine import PsychometricAssessment
from modules.recommendation_engine import RecommendationEngine
from modules.roi_calculator import ROICalculator

# Page config
st.set_page_config(
    page_title="Education ROI Engine",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UX
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .warning-box {
        padding: 1rem;
        border-left: 4px solid #ff4444;
        background-color: #fff3f3;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-left: 4px solid #44ff44;
        background-color: #f3fff3;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'assessment_complete' not in st.session_state:
        st.session_state.assessment_complete = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'assessment_scores' not in st.session_state:
        st.session_state.assessment_scores = {}

def render_sidebar():
    """Render sidebar with user intake form"""
    with st.sidebar:
        st.markdown("### 👤 Student Profile")
        
        name = st.text_input("Full Name", placeholder="Enter your name")
        age = st.number_input("Age", min_value=16, max_value=35, value=18)
        
        st.markdown("### 💰 Financial Context")
        available_budget = st.number_input(
            "Available Education Budget (USD)",
            min_value=0,
            max_value=500000,
            value=20000,
            step=5000,
            help="Total amount you can invest in education"
        )
        
        current_income = st.number_input(
            "Current Annual Income (USD)",
            min_value=0,
            max_value=200000,
            value=0,
            step=5000,
            help="If currently employed, enter annual income. Otherwise leave at 0."
        )
        
        st.markdown("### 🎯 Areas of Interest")
        interest_areas = st.multiselect(
            "Select up to 3 areas",
            [
                "Technology & Software",
                "Business & Finance",
                "Healthcare & Medicine",
                "Engineering & Manufacturing",
                "Creative Arts & Design",
                "Education & Social Services",
                "Science & Research",
                "Trades & Construction"
            ],
            max_selections=3
        )
        
        target_country = st.selectbox(
            "Preferred Study Location",
            ["USA", "UK", "Canada", "Australia", "Germany", "Local/Home Country"]
        )
        
        if st.button("💾 Save Profile & Start Assessment", type="primary", use_container_width=True):
            if name and interest_areas:
                st.session_state.user_data = {
                    'name': name,
                    'age': age,
                    'budget': available_budget,
                    'current_income': current_income,
                    'interests': interest_areas,
                    'target_country': target_country
                }
                st.success("✅ Profile saved! Scroll down to start assessment.")
                st.rerun()
            else:
                st.error("Please fill in your name and select at least one interest area.")

def render_assessment():
    """Render psychometric assessment"""
    st.markdown('<p class="main-header">📋 Psychometric Assessment</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Answer honestly - this determines your optimal path, not what sounds impressive.</p>', unsafe_allow_html=True)
    
    assessment = PsychometricAssessment()
    
    with st.form("psychometric_form"):
        responses = {}
        
        for i, question in enumerate(assessment.questions, 1):
            st.markdown(f"**Question {i}: {question['text']}**")
            
            responses[question['id']] = st.radio(
                f"Select your answer for Q{i}:",
                options=list(question['options'].keys()),
                format_func=lambda x: question['options'][x],
                key=f"q_{question['id']}",
                label_visibility="collapsed"
            )
            st.markdown("---")
        
        submitted = st.form_submit_button("📊 Generate My Recommendation", type="primary", use_container_width=True)
        
        if submitted:
            # Calculate scores
            scores = assessment.calculate_scores(responses)
            st.session_state.assessment_scores = scores
            st.session_state.assessment_complete = True
            st.rerun()

def render_results():
    """Render comprehensive results with ROI analysis"""
    user_data = st.session_state.user_data
    scores = st.session_state.assessment_scores
    
    st.markdown(f'<p class="main-header">🎯 Results for {user_data["name"]}</p>', unsafe_allow_html=True)
    
    # Psychometric Profile
    st.markdown("### 📊 Your Psychometric Profile")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Grit Score", f"{scores['grit']}/10", help="Perseverance and resilience")
    with col2:
        st.metric("Hands-On Preference", f"{scores['hands_on']}/10", help="Practical vs theoretical learning")
    with col3:
        st.metric("Structure Need", f"{scores['structure']}/10", help="Need for formal education framework")
    with col4:
        st.metric("Risk Tolerance", f"{scores['risk_tolerance']}/10", help="Comfort with uncertainty")
    
    # Get recommendation
    recommender = RecommendationEngine()
    recommendation = recommender.get_recommendation(scores, user_data)
    
    st.markdown("---")
    st.markdown(f"### 🎓 Recommended Path: **{recommendation['pathway']}**")
    st.markdown(f"**Reasoning:** {recommendation['reasoning']}")
    
    # ROI Analysis
    st.markdown("---")
    st.markdown("### 💰 5-Year Financial Projection (The Brutal Truth)")
    
    roi_calc = ROICalculator()
    roi_data = roi_calc.calculate_all_pathways(
        user_data['budget'],
        user_data['current_income'],
        user_data['interests'][0] if user_data['interests'] else 'Technology & Software',
        user_data['target_country']
    )
    
    # Create comparison DataFrame
    df = pd.DataFrame(roi_data).T
    df = df.sort_values('net_wealth_year_5', ascending=False)
    
    # Visualize ROI
    fig = go.Figure()
    
    # Net Wealth bars
    fig.add_trace(go.Bar(
        name='Net Wealth (Year 5)',
        x=df.index,
        y=df['net_wealth_year_5'],
        marker_color=['#44ff44' if x > 0 else '#ff4444' for x in df['net_wealth_year_5']],
        text=[f"${x:,.0f}" for x in df['net_wealth_year_5']],
        textposition='outside',
    ))
    
    fig.update_layout(
        title="5-Year Net Wealth by Education Pathway",
        xaxis_title="Education Pathway",
        yaxis_title="Net Wealth (USD)",
        height=500,
        showlegend=False,
        hovermode='x unified'
    )
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed breakdown table
    st.markdown("### 📈 Detailed Pathway Comparison")
    
    display_df = df.copy()
    display_df['total_cost'] = display_df['total_cost'].apply(lambda x: f"${x:,.0f}")
    display_df['year_5_salary'] = display_df['year_5_salary'].apply(lambda x: f"${x:,.0f}")
    display_df['net_wealth_year_5'] = display_df['net_wealth_year_5'].apply(lambda x: f"${x:,.0f}")
    display_df['roi_multiple'] = display_df['roi_multiple'].apply(lambda x: f"{x:.2f}x")
    
    display_df.columns = ['Total Cost', 'Year 5 Salary', 'Net Wealth', 'ROI Multiple']
    st.dataframe(display_df, use_container_width=True)
    
    # Warning System
    recommended_pathway = recommendation['pathway']
    recommended_roi = roi_data[recommended_pathway]
    
    if recommended_roi['net_wealth_year_5'] < 0:
        st.markdown(f"""
        <div class="warning-box">
            <h3>⚠️ DEBT WARNING</h3>
            <p><strong>{recommended_pathway}</strong> will leave you with <strong>${abs(recommended_roi['net_wealth_year_5']):,.0f} in debt</strong> after 5 years.</p>
            <p><strong>Recommendation:</strong> {recommendation['alternative_suggestion']}</p>
        </div>
        """, unsafe_allow_html=True)
    elif recommended_roi['roi_multiple'] < 1.5:
        st.markdown(f"""
        <div class="warning-box">
            <h3>⚠️ LOW ROI WARNING</h3>
            <p>Your recommended path has an ROI of only <strong>{recommended_roi['roi_multiple']:.2f}x</strong>.</p>
            <p>This means you'll earn ${recommended_roi['roi_multiple']:.2f} for every $1 invested - barely above break-even.</p>
            <p><strong>Consider:</strong> {recommendation['alternative_suggestion']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-box">
            <h3>✅ STRONG ROI PROJECTION</h3>
            <p>Your recommended path projects <strong>${recommended_roi['net_wealth_year_5']:,.0f}</strong> in net wealth after 5 years.</p>
            <p>ROI Multiple: <strong>{recommended_roi['roi_multiple']:.2f}x</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Action items
    st.markdown("---")
    st.markdown("### 📝 Next Steps")
    st.markdown(recommendation['next_steps'])
    
    # Reset button
    if st.button("🔄 Start New Assessment", use_container_width=True):
        st.session_state.clear()
        st.rerun()

def main():
    initialize_session_state()
    
    # Header
    st.markdown('<p class="main-header">🎓 Education ROI Engine</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">The Human Capital De-risking Platform - Brutally Honest Career Guidance</p>', unsafe_allow_html=True)
    
    # Sidebar
    render_sidebar()
    
    # Main content
    if not st.session_state.user_data:
        st.info("👈 Start by filling out your profile in the sidebar.")
        
        # Show value proposition
        st.markdown("### Why This Platform is Different")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🎯 Psychometric-Driven**")
            st.write("We measure grit, learning style, and risk tolerance - not just academic scores.")
        
        with col2:
            st.markdown("**💰 ROI-First Approach**")
            st.write("If a degree costs more than it earns, we'll tell you. No sugar-coating.")
        
        with col3:
            st.markdown("**🔍 Four Pathways**")
            st.write("International university, local university, apprenticeship, or micro-credentials - based on YOUR data.")
    
    elif not st.session_state.assessment_complete:
        render_assessment()
    
    else:
        render_results()

if __name__ == "__main__":
    main()
