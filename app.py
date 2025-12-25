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
    page_title="Education Path Finder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Airbnb style
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Airbnb font system */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* Typography */
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        color: #222222;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .sub-header {
        font-size: 1rem;
        color: #717171;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Input styling - Airbnb search bar style */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        font-size: 0.9rem !important;
        color: #222222 !important;
        padding: 0.5rem 1rem !important;
        background: transparent !important;
    }
    
    /* Button styling - Airbnb primary button */
    .stButton > button {
        background: linear-gradient(to right, #E61E4D 0%, #E31C5F 50%, #D70466 100%) !important;
        color: white !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(to right, #D70466 0%, #BD1E59 50%, #BD1E59 100%) !important;
        transform: scale(1.02) !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #EBEBEB;
        transition: all 0.2s ease;
    }
    .stRadio > div:hover {
        border-color: #222222;
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

def render_hero_landing():
    """Render Airbnb-style landing page"""
    
    # Hero Section
    st.markdown("""
    <div style="max-width: 1200px; margin: 2rem auto; padding: 0 2rem;">
        <h1 style="font-size: 3rem; font-weight: 600; margin-bottom: 1rem; color: #222222; letter-spacing: -0.02em;">
            Not all education is<br>created equal
        </h1>
        <p style="font-size: 1.1rem; color: #717171; margin-bottom: 2rem;">
            Discover the path that maximizes your ROI, not university revenue.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Airbnb-style search bar
    st.markdown("""
    <div style="max-width: 1200px; margin: 2rem auto; padding: 0 2rem;">
        <div style="background: white; border: 1px solid #DDDDDD; border-radius: 40px; padding: 0.5rem; box-shadow: 0 3px 12px rgba(0,0,0,0.1);">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2.5, 2.5, 2.5, 1.5])
    
    with col1:
        st.markdown('<div style="padding: 0.5rem 0 0 1rem;"><div style="font-size: 0.75rem; font-weight: 700; color: #222222;">NAME</div></div>', unsafe_allow_html=True)
        name = st.text_input("Name", placeholder="Add your name", label_visibility="collapsed", key="name_input")
    
    with col2:
        st.markdown('<div style="padding: 0.5rem 0 0 1rem; border-left: 1px solid #DDDDDD;"><div style="font-size: 0.75rem; font-weight: 700; color: #222222;">INTEREST</div></div>', unsafe_allow_html=True)
        interest_input = st.selectbox(
            "Interest",
            [""] + ["Technology & Software", "Business & Finance", "Healthcare & Medicine", "Engineering & Manufacturing", "Creative Arts & Design", "Education & Social Services", "Science & Research", "Trades & Construction"],
            format_func=lambda x: "Add field of interest" if x == "" else x,
            label_visibility="collapsed",
            key="interest_select"
        )
    
    with col3:
        st.markdown('<div style="padding: 0.5rem 0 0 1rem; border-left: 1px solid #DDDDDD;"><div style="font-size: 0.75rem; font-weight: 700; color: #222222;">BUDGET</div></div>', unsafe_allow_html=True)
        budget_input = st.selectbox(
            "Budget",
            [""] + ["Under $10,000", "$10,000 - $30,000", "$30,000 - $50,000", "$50,000 - $100,000", "Over $100,000"],
            format_func=lambda x: "Add budget range" if x == "" else x,
            label_visibility="collapsed",
            key="budget_select"
        )
    
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    if search_clicked:
        if name and interest_input and budget_input:
            budget_map = {"Under $10,000": 8000, "$10,000 - $30,000": 20000, "$30,000 - $50,000": 40000, "$50,000 - $100,000": 75000, "Over $100,000": 120000}
            st.session_state.user_data = {
                'name': name,
                'age': 20,
                'budget': budget_map.get(budget_input, 20000),
                'current_income': 0,
                'interests': [interest_input],
                'target_country': 'USA'
            }
            st.rerun()
        else:
            st.error("Please fill in all fields")
    
    # Stats
    st.markdown("""
    <div style="max-width: 1200px; margin: 4rem auto 2rem auto; padding: 0 2rem;">
        <h2 style="font-size: 1.4rem; font-weight: 600; color: #222222; margin-bottom: 2rem;">Why students choose us</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div style="padding: 1rem;"><div style="font-size: 2.5rem; font-weight: 600; color: #222222; margin-bottom: 0.5rem;">$47K+</div><div style="font-size: 1rem; color: #222222; font-weight: 500;">Average ROI improvement</div><div style="font-size: 0.9rem; color: #717171;">compared to default choice</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="padding: 1rem;"><div style="font-size: 2.5rem; font-weight: 600; color: #222222; margin-bottom: 0.5rem;">847</div><div style="font-size: 1rem; color: #222222; font-weight: 500;">Students saved from debt</div><div style="font-size: 0.9rem; color: #717171;">who would\'ve gone $30k+ in debt</div></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div style="padding: 1rem;"><div style="font-size: 2.5rem; font-weight: 600; color: #222222; margin-bottom: 0.5rem;">3 min</div><div style="font-size: 1rem; color: #222222; font-weight: 500;">To get your results</div><div style="font-size: 0.9rem; color: #717171;">complete assessment time</div></div>', unsafe_allow_html=True)

def render_assessment():
    """Render psychometric assessment"""
    st.markdown(f'<div style="text-align: center; padding: 2rem 0;"><div style="display: inline-block; padding: 0.5rem 1.5rem; background: #e3f2fd; border-radius: 20px; color: #1976d2;">Step 2 of 3: Assessment</div></div>', unsafe_allow_html=True)
    st.markdown(f'<p class="main-header">Hi {st.session_state.user_data["name"]}! Let\'s Find Your Best Path</p>', unsafe_allow_html=True)
    
    assessment = PsychometricAssessment()
    
    with st.form("psychometric_form"):
        responses = {}
        
        for i, question in enumerate(assessment.questions, 1):
            st.markdown(f'<div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0;"><h4 style="color: #1f77b4;">Question {i} of {len(assessment.questions)}</h4><p style="font-size: 1.1rem; color: #333;">{question["text"]}</p></div>', unsafe_allow_html=True)
            
            responses[question['id']] = st.radio(
                f"Q{i}",
                options=list(question['options'].keys()),
                format_func=lambda x: question['options'][x],
                key=f"q_{question['id']}",
                label_visibility="collapsed"
            )
        
        submitted = st.form_submit_button("📊 Get My Results", type="primary", use_container_width=True)
        
        if submitted:
            scores = assessment.calculate_scores(responses)
            st.session_state.assessment_scores = scores
            st.session_state.assessment_complete = True
            st.rerun()

def render_results():
    """Render results with ROI analysis"""
    st.markdown('<div style="text-align: center; padding: 2rem 0;"><div style="display: inline-block; padding: 0.5rem 1.5rem; background: #e8f5e9; border-radius: 20px; color: #2e7d32;">✅ Step 3 of 3: Your Results</div></div>', unsafe_allow_html=True)
    
    user_data = st.session_state.user_data
    scores = st.session_state.assessment_scores
    
    st.markdown(f'<p class="main-header">Results for {user_data["name"]}</p>', unsafe_allow_html=True)
    
    # Psychometric Profile
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Grit", f"{scores['grit']}/10")
    with col2:
        st.metric("Hands-On", f"{scores['hands_on']}/10")
    with col3:
        st.metric("Structure Need", f"{scores['structure']}/10")
    with col4:
        st.metric("Risk Tolerance", f"{scores['risk_tolerance']}/10")
    
    # Get recommendation
    recommender = RecommendationEngine()
    recommendation = recommender.get_recommendation(scores, user_data)
    
    st.markdown(f"### 🎓 Recommended: **{recommendation['pathway']}**")
    st.write(f"**Reasoning:** {recommendation['reasoning']}")
    
    # ROI Analysis
    st.markdown("### 💰 5-Year Financial Projection")
    
    roi_calc = ROICalculator()
    roi_data = roi_calc.calculate_all_pathways(user_data['budget'], user_data['current_income'], user_data['interests'][0] if user_data['interests'] else 'Technology & Software', user_data['target_country'])
    
    df = pd.DataFrame(roi_data).T.sort_values('net_wealth_year_5', ascending=False)
    
    # Visualize
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Net Wealth (Year 5)',
        x=df.index,
        y=df['net_wealth_year_5'],
        marker_color=['#44ff44' if x > 0 else '#ff4444' for x in df['net_wealth_year_5']],
        text=[f"${x:,.0f}" for x in df['net_wealth_year_5']],
        textposition='outside'
    ))
    fig.update_layout(title="5-Year Net Wealth by Pathway", xaxis_title="Pathway", yaxis_title="Net Wealth (USD)", height=500)
    fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Warnings
    recommended_roi = roi_data[recommendation['pathway']]
    if recommended_roi['net_wealth_year_5'] < 0:
        st.error(f"⚠️ **DEBT WARNING**: {recommendation['pathway']} will leave you with **${abs(recommended_roi['net_wealth_year_5']):,.0f} in debt** after 5 years.")
    elif recommended_roi['roi_multiple'] < 1.5:
        st.warning(f"⚠️ **LOW ROI**: ROI is only {recommended_roi['roi_multiple']:.2f}x")
    else:
        st.success(f"✅ **STRONG ROI**: Projected ${recommended_roi['net_wealth_year_5']:,.0f} net wealth after 5 years")
    
    if st.button("🔄 Start New Assessment"):
        st.session_state.clear()
        st.rerun()

def main():
    initialize_session_state()
    
    if not st.session_state.user_data:
        render_hero_landing()
    elif not st.session_state.assessment_complete:
        render_assessment()
    else:
        render_results()

if __name__ == "__main__":
    main()
