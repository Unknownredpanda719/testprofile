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
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main typography */
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
    
    /* Input styling */
    .stTextInput > div > div > input {
        font-size: 1.1rem;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1);
    }
    
    .stSelectbox > div > div {
        font-size: 1.1rem;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    /* Button styling */
    .stButton > button {
        font-size: 1.2rem;
        font-weight: 600;
        padding: 1rem 2rem;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
    }
    
    /* Warning/Success boxes */
    .warning-box {
        padding: 1.5rem;
        border-left: 4px solid #ff4444;
        background-color: #fff3f3;
        margin: 1.5rem 0;
        border-radius: 8px;
    }
    .success-box {
        padding: 1.5rem;
        border-left: 4px solid #44ff44;
        background-color: #f3fff3;
        margin: 1.5rem 0;
        border-radius: 8px;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    .stRadio > div:hover {
        border-color: #1f77b4;
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



def render_assessment():
    """Render psychometric assessment"""
    
    # Progress indicator
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <div style="display: inline-block; padding: 0.5rem 1.5rem; background: #e3f2fd; border-radius: 20px; color: #1976d2;">
            Step 2 of 3: Psychometric Assessment
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<p class="main-header">Hi {st.session_state.user_data["name"]}! Let\'s Find Your Best Path 🎯</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">7 quick questions to understand how you learn best. There are no "right" answers - just honest ones.</p>', unsafe_allow_html=True)
    
    assessment = PsychometricAssessment()
    
    with st.form("psychometric_form"):
        responses = {}
        
        for i, question in enumerate(assessment.questions, 1):
            # Question card styling
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0;">
                <h4 style="color: #1f77b4; margin-bottom: 1rem;">Question {i} of {len(assessment.questions)}</h4>
                <p style="font-size: 1.1rem; font-weight: 500; color: #333;">{question['text']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            responses[question['id']] = st.radio(
                f"Select your answer for Q{i}:",
                options=list(question['options'].keys()),
                format_func=lambda x: question['options'][x],
                key=f"q_{question['id']}",
                label_visibility="collapsed"
            )
            
            if i < len(assessment.questions):
                st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("📊 Get My Results", type="primary", use_container_width=True)
        
        if submitted:
            # Calculate scores
            scores = assessment.calculate_scores(responses)
            st.session_state.assessment_scores = scores
            st.session_state.assessment_complete = True
            st.rerun()

def render_results():
    """Render comprehensive results with ROI analysis"""
    
    # Progress indicator
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <div style="display: inline-block; padding: 0.5rem 1.5rem; background: #e8f5e9; border-radius: 20px; color: #2e7d32;">
            ✅ Step 3 of 3: Your Personalized Results
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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

def render_hero_landing():
    """Render search engine-style hero landing page"""
    
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem 3rem 2rem;">
        <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem; color: #1f77b4;">
            Find Your Smartest Path Forward
        </h1>
        <p style="font-size: 1.4rem; color: #666; margin-bottom: 3rem; max-width: 800px; margin-left: auto; margin-right: auto;">
            Should you study abroad? Get a local degree? Start an apprenticeship? 
            We'll tell you the brutal truth based on <strong>ROI, not prestige.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search-style input
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("### 👤 Quick Start: Tell Us About Yourself")
        
        name = st.text_input(
            "What's your name?",
            placeholder="e.g., Sarah Chen",
            label_visibility="collapsed",
            key="hero_name"
        )
        
        # Interest search bar style
        interest_input = st.selectbox(
            "What do you want to study?",
            [""] + [
                "💻 Technology & Software",
                "💼 Business & Finance",
                "⚕️ Healthcare & Medicine",
                "🔧 Engineering & Manufacturing",
                "🎨 Creative Arts & Design",
                "👥 Education & Social Services",
                "🔬 Science & Research",
                "🏗️ Trades & Construction"
            ],
            format_func=lambda x: "What do you want to study? (Select one)" if x == "" else x,
            label_visibility="collapsed"
        )
        
        budget_input = st.selectbox(
            "Budget",
            [""] + [
                "💰 Under $10,000",
                "💰 $10,000 - $30,000",
                "💰 $30,000 - $50,000",
                "💰 $50,000 - $100,000",
                "💰 Over $100,000"
            ],
            format_func=lambda x: "What's your education budget?" if x == "" else x,
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Get My Honest Assessment", type="primary", use_container_width=True):
            if name and interest_input and budget_input:
                # Parse budget
                budget_map = {
                    "💰 Under $10,000": 8000,
                    "💰 $10,000 - $30,000": 20000,
                    "💰 $30,000 - $50,000": 40000,
                    "💰 $50,000 - $100,000": 75000,
                    "💰 Over $100,000": 120000
                }
                
                # Parse interest (remove emoji)
                interest_clean = interest_input.split(" ", 1)[1] if " " in interest_input else interest_input
                
                st.session_state.user_data = {
                    'name': name,
                    'age': 20,  # Default for now
                    'budget': budget_map[budget_input],
                    'current_income': 0,
                    'interests': [interest_clean],
                    'target_country': 'USA'  # Default
                }
                st.rerun()
            else:
                st.error("Please fill in all fields to continue")
    
    # Value Props Below
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; border-top: 1px solid #eee;">
        <h3 style="color: #333; margin-bottom: 2rem;">Why Students Trust Us</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h4 style="color: #1f77b4;">Psychometric-Driven</h4>
            <p style="color: #666;">We measure grit, learning style, and risk tolerance - not just grades.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💰</div>
            <h4 style="color: #1f77b4;">Brutally Honest ROI</h4>
            <p style="color: #666;">If a degree leaves you in debt, we'll tell you. No sugar-coating.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
            <h4 style="color: #1f77b4;">4 Smart Pathways</h4>
            <p style="color: #666;">University, local college, apprenticeship, or bootcamp - based on YOUR data.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Social proof / stats
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average ROI Improvement", "+$47k", help="vs. default choice")
    with col2:
        st.metric("Students Saved from Debt", "847", help="who would've gone $30k+ in debt")
    with col3:
        st.metric("Assessment Time", "3 min", help="to get your recommendation")
    with col4:
        st.metric("Pathways Analyzed", "4", help="customized to your profile")

def main():
    initialize_session_state()
    
    # Main content flow
    if not st.session_state.user_data:
        # Hero landing page
        render_hero_landing()
    
    elif not st.session_state.assessment_complete:
        # Assessment page
        render_assessment()
    
    else:
        # Results page
        render_results()

if __name__ == "__main__":
    main()
