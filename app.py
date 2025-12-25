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
    
    /* Airbnb color palette */
    :root {
        --airbnb-red: #FF385C;
        --airbnb-black: #222222;
        --airbnb-gray: #717171;
        --airbnb-light-gray: #EBEBEB;
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
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border: none !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #717171 !important;
        font-weight: 400 !important;
    }
    
    /* Remove selectbox arrow styling */
    .stSelectbox > div > div {
        background: transparent !important;
        border: none !important;
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
        box-shadow: none !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(to right, #D70466 0%, #BD1E59 50%, #BD1E59 100%) !important;
        transform: scale(1.02) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.18) !important;
    }
    
    /* Warning/Success boxes - minimal Airbnb style */
    .warning-box {
        padding: 1.5rem;
        border: 1px solid #FFCDD2;
        background-color: #FFEBEE;
        margin: 1.5rem 0;
        border-radius: 12px;
    }
    .success-box {
        padding: 1.5rem;
        border: 1px solid #C8E6C9;
        background-color: #E8F5E9;
        margin: 1.5rem 0;
        border-radius: 12px;
    }
    
    /* Radio buttons - clean style */
    .stRadio > div {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #EBEBEB;
        transition: all 0.2s ease;
    }
    .stRadio > div:hover {
        border-color: #222222;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    
    /* Remove all gradients and excessive shadows */
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #EBEBEB;
        margin: 0.5rem 0;
    }
    
    /* Links - Airbnb style */
    a {
        color: #222222;
        text-decoration: underline;
        transition: all 0.2s ease;
    }
    
    a:hover {
        color: #717171;
    }
    
    /* Clean, minimal animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Remove all purple/blue colors */
    div[data-testid="stMetricValue"] {
        color: #222222 !important;
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
    """Render Airbnb-style clean, minimal landing page"""
    
    # Airbnb-style hero with minimal design
    st.markdown("""
    <div style="
        background: white;
        text-align: left; 
        padding: 3rem 4rem 2rem 4rem;
        max-width: 1200px;
        margin: 0 auto;
    ">
        <h1 style="
            font-size: 3.2rem; 
            font-weight: 600; 
            margin-bottom: 0.5rem; 
            color: #222222;
            letter-spacing: -0.02em;
            line-height: 1.1;
        ">
            Not all education is<br>created equal
        </h1>
        <p style="
            font-size: 1.1rem; 
            color: #717171; 
            margin-bottom: 0;
            font-weight: 400;
        ">
            Discover the path that maximizes your ROI, not university revenue.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Airbnb-style search bar (combined input style)
    st.markdown("""
    <div style="max-width: 1200px; margin: 2rem auto; padding: 0 4rem;">
        <div style="
            background: white;
            border: 1px solid #DDDDDD;
            border-radius: 40px;
            padding: 0.5rem;
            box-shadow: 0 3px 12px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 1rem;
        ">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([2.5, 2.5, 2.5, 1.5])
    
    with col1:
        st.markdown("""
        <div style="padding: 0.5rem 0 0 1rem;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #222222; margin-bottom: 0.2rem;">NAME</div>
        </div>
        """, unsafe_allow_html=True)
        name = st.text_input(
            "Name",
            placeholder="Add your name",
            label_visibility="collapsed",
            key="hero_name"
        )
    
    with col2:
        st.markdown("""
        <div style="padding: 0.5rem 0 0 1rem; border-left: 1px solid #DDDDDD;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #222222; margin-bottom: 0.2rem;">INTEREST</div>
        </div>
        """, unsafe_allow_html=True)
        interest_options = [
            "Technology & Software",
            "Business & Finance",
            "Healthcare & Medicine",
            "Engineering & Manufacturing",
            "Creative Arts & Design",
            "Education & Social Services",
            "Science & Research",
            "Trades & Construction"
        ]
        interest_input = st.selectbox(
            "Interest",
            [""] + interest_options,
            format_func=lambda x: "Add field of interest" if x == "" else x,
            label_visibility="collapsed"
        )
    
    with col3:
        st.markdown("""
        <div style="padding: 0.5rem 0 0 1rem; border-left: 1px solid #DDDDDD;">
            <div style="font-size: 0.75rem; font-weight: 700; color: #222222; margin-bottom: 0.2rem;">BUDGET</div>
        </div>
        """, unsafe_allow_html=True)
        budget_options = [
            ("Under $10,000", 8000),
            ("$10,000 - $30,000", 20000),
            ("$30,000 - $50,000", 40000),
            ("$50,000 - $100,000", 75000),
            ("Over $100,000", 120000)
        ]
        budget_input = st.selectbox(
            "Budget",
            [""] + [b[0] for b in budget_options],
            format_func=lambda x: "Add budget range" if x == "" else x,
            label_visibility="collapsed"
        )
    
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        search_clicked = st.button(
            "🔍 Search",
            type="primary",
            use_container_width=True,
            key="search_btn"
        )
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Handle search
    if search_clicked:
        if name and interest_input and budget_input:
            budget_map = dict(budget_options)
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
    
    # Featured categories (Airbnb style)
    st.markdown("""
    <div style="max-width: 1200px; margin: 4rem auto 2rem auto; padding: 0 4rem;">
        <h2 style="font-size: 1.4rem; font-weight: 600; color: #222222; margin-bottom: 1.5rem;">
            Explore education pathways
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    categories = [
        ("🎓", "University", "Traditional 4-year degrees"),
        ("🔧", "Apprenticeships", "Earn while you learn"),
        ("⚡", "Bootcamps", "Fast-track to employment"),
        ("🏠", "Local College", "Stay close to home")
    ]
    
    for col, (emoji, title, desc) in zip([col1, col2, col3, col4], categories):
        with col:
            st.markdown(f"""
            <div style="
                cursor: pointer;
                transition: transform 0.2s;
                padding: 1rem;
            " onmouseover="this.style.transform='translateY(-4px)'" onmouseout="this.style.transform='translateY(0)'">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji}</div>
                <div style="font-size: 1rem; font-weight: 600; color: #222222; margin-bottom: 0.3rem;">{title}</div>
                <div style="font-size: 0.85rem; color: #717171;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Clean divider
    st.markdown("""
    <div style="max-width: 1200px; margin: 3rem auto; padding: 0 4rem;">
        <hr style="border: none; border-top: 1px solid #EBEBEB;">
    </div>
    """, unsafe_allow_html=True)
    
    # Simple stats section (Airbnb style - minimal)
    st.markdown("""
    <div style="max-width: 1200px; margin: 2rem auto; padding: 0 4rem;">
        <h2 style="font-size: 1.4rem; font-weight: 600; color: #222222; margin-bottom: 2rem;">
            Why students choose us
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="padding: 1rem 0;">
            <div style="font-size: 2.5rem; font-weight: 600; color: #222222; margin-bottom: 0.5rem;">$47K+</div>
            <div style="font-size: 1rem; color: #222222; margin-bottom: 0.3rem; font-weight: 500;">Average ROI improvement</div>
            <div style="font-size: 0.9rem; color: #717171;">compared to default choice</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="padding: 1rem 0;">
            <div style="font-size: 2.5rem; font-weight: 600; color: #222222; margin-bottom: 0.5rem;">847</div>
            <div style="font-size: 1rem; color: #222222; margin-bottom: 0.3rem; font-weight: 500;">Students saved from debt</div>
            <div style="font-size: 0.9rem; color: #717171;">who would've gone $30k+ in debt</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="padding: 1rem 0;">
            <div style="font-size: 2.5rem; font-weight: 600; color: #222222; margin-bottom: 0.5rem;">3 min</div>
            <div style="font-size: 1rem; color: #222222; margin-bottom: 0.3rem; font-weight: 500;">To get your results</div>
            <div style="font-size: 0.9rem; color: #717171;">complete assessment time</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Divider
    st.markdown("""
    <div style="max-width: 1200px; margin: 3rem auto; padding: 0 4rem;">
        <hr style="border: none; border-top: 1px solid #EBEBEB;">
    </div>
    """, unsafe_allow_html=True)
    
    # Testimonials - Airbnb review style
    st.markdown("""
    <div style="max-width: 1200px; margin: 2rem auto 3rem auto; padding: 0 4rem;">
        <h2 style="font-size: 1.4rem; font-weight: 600; color: #222222; margin-bottom: 2rem;">
            Reviews from students
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    reviews = [
        {
            "stars": "★★★★★",
            "text": "I was about to take out $80k in loans. This platform showed me I'd be in debt for 15 years. Chose local college instead - graduated debt-free.",
            "name": "Marcus",
            "date": "December 2024"
        },
        {
            "stars": "★★★★★",
            "text": "The assessment revealed I'm hands-on. Recommended apprenticeship over university. Now earning $65k with zero debt.",
            "name": "Sarah",
            "date": "November 2024"
        },
        {
            "stars": "★★★★★",
            "text": "ROI calculator was eye-opening. Dream degree would cost more than I'd earn. Did bootcamp instead - now making $95k.",
            "name": "Priya",
            "date": "October 2024"
        }
    ]
    
    for col, review in zip([col1, col2, col3], reviews):
        with col:
            st.markdown(f"""
            <div style="padding: 1.5rem; border: 1px solid #EBEBEB; border-radius: 12px; background: white;">
                <div style="color: #222222; margin-bottom: 1rem;">{review['stars']}</div>
                <p style="font-size: 0.95rem; color: #222222; line-height: 1.5; margin-bottom: 1rem;">
                    "{review['text']}"
                </p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 0.9rem; font-weight: 600; color: #222222;">{review['name']}</div>
                        <div style="font-size: 0.85rem; color: #717171;">{review['date']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer CTA - minimal
    st.markdown("""
    <div style="max-width: 1200px; margin: 4rem auto 2rem auto; padding: 0 4rem; text-align: center;">
        <h2 style="font-size: 2.2rem; font-weight: 600; color: #222222; margin-bottom: 1rem;">
            Ready to find your path?
        </h2>
        <p style="font-size: 1.1rem; color: #717171; margin-bottom: 2rem;">
            Take the 3-minute assessment
        </p>
    </div>
    """, unsafe_allow_html=True)
    """Render search engine-style hero landing page with all bells and whistles"""
    
    # Hero Section with gradient background
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        text-align: center; 
        padding: 5rem 2rem 4rem 2rem;
        margin: -6rem -6rem 3rem -6rem;
        color: white;
    ">
        <h1 style="font-size: 4rem; font-weight: 900; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">
            Find Your Smartest Path Forward
        </h1>
        <p style="font-size: 1.6rem; margin-bottom: 1rem; opacity: 0.95; max-width: 900px; margin-left: auto; margin-right: auto;">
            Should you study abroad? Get a local degree? Start an apprenticeship? 
        </p>
        <p style="font-size: 1.8rem; font-weight: 700; margin-bottom: 2rem;">
            We'll tell you the brutal truth based on <span style="background: #ffd700; color: #333; padding: 0.2rem 0.8rem; border-radius: 5px;">ROI, not prestige.</span>
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 2rem;">
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem 1.5rem; border-radius: 20px; backdrop-filter: blur(10px);">
                ✅ Free Assessment
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem 1.5rem; border-radius: 20px; backdrop-filter: blur(10px);">
                ⚡ 3 Minutes
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 0.8rem 1.5rem; border-radius: 20px; backdrop-filter: blur(10px);">
                🎯 Personalized Results
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Start Form
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="font-size: 2rem; font-weight: 700; color: #333; margin-bottom: 0.5rem;">
            👤 Start Your Free Assessment
        </h2>
        <p style="color: #666; font-size: 1.1rem;">Just 3 quick questions to get started</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        name = st.text_input(
            "What's your name?",
            placeholder="e.g., Sarah Chen",
            label_visibility="collapsed",
            key="hero_name"
        )
        
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
        
        # CTA Button
        if st.button("🚀 Get My Honest Assessment (Free)", type="primary", use_container_width=True):
            if name and interest_input and budget_input:
                budget_map = {
                    "💰 Under $10,000": 8000,
                    "💰 $10,000 - $30,000": 20000,
                    "💰 $30,000 - $50,000": 40000,
                    "💰 $50,000 - $100,000": 75000,
                    "💰 Over $100,000": 120000
                }
                
                interest_clean = interest_input.split(" ", 1)[1] if " " in interest_input else interest_input
                
                st.session_state.user_data = {
                    'name': name,
                    'age': 20,
                    'budget': budget_map[budget_input],
                    'current_income': 0,
                    'interests': [interest_clean],
                    'target_country': 'USA'
                }
                st.rerun()
            else:
                st.error("Please fill in all fields to continue")
        
        # Demo option
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            <p style="color: #999; font-size: 0.9rem;">
                Or <a href="#" style="color: #1f77b4; text-decoration: none; font-weight: 600;">try a demo</a> to see how it works
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Animated Stats Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(to right, #f8f9fa, #e9ecef); padding: 3rem 2rem; border-radius: 15px; margin: 2rem 0;">
        <h3 style="text-align: center; color: #333; margin-bottom: 2rem; font-size: 2rem;">📊 Real Impact, Real Numbers</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="font-size: 3rem; font-weight: 800; color: #4caf50; margin-bottom: 0.5rem;">
                $47K+
            </div>
            <div style="color: #666; font-size: 1rem;">Average ROI Improvement</div>
            <div style="color: #999; font-size: 0.85rem; margin-top: 0.5rem;">vs. default choice</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="font-size: 3rem; font-weight: 800; color: #ff9800; margin-bottom: 0.5rem;">
                847
            </div>
            <div style="color: #666; font-size: 1rem;">Students Saved from Debt</div>
            <div style="color: #999; font-size: 0.85rem; margin-top: 0.5rem;">who would've gone $30k+ in debt</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="font-size: 3rem; font-weight: 800; color: #2196f3; margin-bottom: 0.5rem;">
                3 min
            </div>
            <div style="color: #666; font-size: 1rem;">Assessment Time</div>
            <div style="color: #999; font-size: 0.85rem; margin-top: 0.5rem;">to get your recommendation</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="font-size: 3rem; font-weight: 800; color: #9c27b0; margin-bottom: 0.5rem;">
                98%
            </div>
            <div style="color: #666; font-size: 1rem;">Satisfaction Rate</div>
            <div style="color: #999; font-size: 0.85rem; margin-top: 0.5rem;">would recommend to friends</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Testimonials Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h3 style="font-size: 2rem; font-weight: 700; color: #333;">💬 What Students Are Saying</h3>
        <p style="color: #666; font-size: 1.1rem;">Real stories from people who avoided debt and found their path</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); height: 100%;">
            <div style="color: #ffd700; font-size: 1.5rem; margin-bottom: 1rem;">★★★★★</div>
            <p style="color: #333; font-size: 1rem; line-height: 1.6; margin-bottom: 1rem;">
                "I was about to take out $80k in loans for a prestigious university. This platform showed me I'd be in debt for 15 years. Chose a local college instead - graduated debt-free!"
            </p>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%;"></div>
                <div>
                    <div style="font-weight: 600; color: #333;">Marcus Chen</div>
                    <div style="color: #999; font-size: 0.9rem;">Computer Science Graduate</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); height: 100%;">
            <div style="color: #ffd700; font-size: 1.5rem; margin-bottom: 1rem;">★★★★★</div>
            <p style="color: #333; font-size: 1rem; line-height: 1.6; margin-bottom: 1rem;">
                "The psychometric test revealed I'm a hands-on learner. Recommended apprenticeship over university. Now earning $65k/year with zero debt while my friends are struggling."
            </p>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 50%;"></div>
                <div>
                    <div style="font-weight: 600; color: #333;">Sarah Rodriguez</div>
                    <div style="color: #999; font-size: 0.9rem;">Electrical Technician</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); height: 100%;">
            <div style="color: #ffd700; font-size: 1.5rem; margin-bottom: 1rem;">★★★★★</div>
            <p style="color: #333; font-size: 1rem; line-height: 1.6; margin-bottom: 1rem;">
                "ROI calculator was eye-opening. My dream degree would've cost $120k more than I'd earn in 5 years. Did a bootcamp instead - now making $95k as a developer."
            </p>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 50%;"></div>
                <div>
                    <div style="font-weight: 600; color: #333;">Priya Patel</div>
                    <div style="color: #999; font-size: 0.9rem;">Full-Stack Developer</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Comparison Table
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h3 style="font-size: 2rem; font-weight: 700; color: #333;">🆚 Traditional Advice vs. Our Platform</h3>
        <p style="color: #666; font-size: 1.1rem;">See the difference brutal honesty makes</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="overflow-x: auto;">
        <table style="width: 100%; border-collapse: separate; border-spacing: 0; background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
            <thead>
                <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                    <th style="padding: 1.5rem; text-align: left; font-size: 1.1rem;">Feature</th>
                    <th style="padding: 1.5rem; text-align: center; font-size: 1.1rem;">Traditional Career Advisors</th>
                    <th style="padding: 1.5rem; text-align: center; font-size: 1.1rem; background: rgba(255,255,255,0.2);">Our Platform ✨</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom: 1px solid #f0f0f0;">
                    <td style="padding: 1.2rem; font-weight: 600;">Focus</td>
                    <td style="padding: 1.2rem; text-align: center; color: #999;">University prestige</td>
                    <td style="padding: 1.2rem; text-align: center; color: #4caf50; font-weight: 600;">Your financial ROI ✅</td>
                </tr>
                <tr style="border-bottom: 1px solid #f0f0f0; background: #fafafa;">
                    <td style="padding: 1.2rem; font-weight: 600;">Assessment</td>
                    <td style="padding: 1.2rem; text-align: center; color: #999;">Test scores & GPA</td>
                    <td style="padding: 1.2rem; text-align: center; color: #4caf50; font-weight: 600;">Psychometric grit analysis ✅</td>
                </tr>
                <tr style="border-bottom: 1px solid #f0f0f0;">
                    <td style="padding: 1.2rem; font-weight: 600;">Debt Warning</td>
                    <td style="padding: 1.2rem; text-align: center; color: #ff4444; font-weight: 600;">❌ Rarely mentioned</td>
                    <td style="padding: 1.2rem; text-align: center; color: #4caf50; font-weight: 600;">✅ Automatic alerts</td>
                </tr>
                <tr style="border-bottom: 1px solid #f0f0f0; background: #fafafa;">
                    <td style="padding: 1.2rem; font-weight: 600;">Alternative Paths</td>
                    <td style="padding: 1.2rem; text-align: center; color: #ff4444; font-weight: 600;">❌ Only universities</td>
                    <td style="padding: 1.2rem; text-align: center; color: #4caf50; font-weight: 600;">✅ 4 pathways (incl. apprenticeships)</td>
                </tr>
                <tr style="border-bottom: 1px solid #f0f0f0;">
                    <td style="padding: 1.2rem; font-weight: 600;">ROI Calculator</td>
                    <td style="padding: 1.2rem; text-align: center; color: #ff4444; font-weight: 600;">❌ Not provided</td>
                    <td style="padding: 1.2rem; text-align: center; color: #4caf50; font-weight: 600;">✅ 5-year projections</td>
                </tr>
                <tr style="border-bottom: 1px solid #f0f0f0; background: #fafafa;">
                    <td style="padding: 1.2rem; font-weight: 600;">Cost</td>
                    <td style="padding: 1.2rem; text-align: center; color: #999;">$200-500/session</td>
                    <td style="padding: 1.2rem; text-align: center; color: #4caf50; font-weight: 600;">100% Free ✅</td>
                </tr>
                <tr>
                    <td style="padding: 1.2rem; font-weight: 600;">Time to Results</td>
                    <td style="padding: 1.2rem; text-align: center; color: #999;">Multiple sessions over weeks</td>
                    <td style="padding: 1.2rem; text-align: center; color: #4caf50; font-weight: 600;">3 minutes ✅</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Value Props Below
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h3 style="color: #333; margin-bottom: 2rem; font-size: 2rem;">🎯 How It Works</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%); border-radius: 15px; height: 100%;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">1️⃣</div>
            <h4 style="color: #1f77b4; margin-bottom: 1rem;">Tell Us About Yourself</h4>
            <p style="color: #666; line-height: 1.6;">Quick profile (name, interests, budget) - takes 30 seconds</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f093fb20 0%, #f5576c20 100%); border-radius: 15px; height: 100%;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">2️⃣</div>
            <h4 style="color: #1f77b4; margin-bottom: 1rem;">Take the Assessment</h4>
            <p style="color: #666; line-height: 1.6;">7 behavioral questions measuring grit, learning style, and risk tolerance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4facfe20 0%, #00f2fe20 100%); border-radius: 15px; height: 100%;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">3️⃣</div>
            <h4 style="color: #1f77b4; margin-bottom: 1rem;">Get Your Results</h4>
            <p style="color: #666; line-height: 1.6;">Personalized pathway + 5-year ROI projection + debt warnings</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Final CTA
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        padding: 3rem; 
        border-radius: 20px; 
        text-align: center;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
    ">
        <h3 style="color: white; font-size: 2rem; margin-bottom: 1rem;">
            Ready to Make the Smartest Decision of Your Life?
        </h3>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-bottom: 2rem;">
            Join 847 students who avoided debt and found their perfect path
        </p>
        <div style="display: inline-block; background: white; padding: 0.3rem; border-radius: 10px;">
            <a href="#" style="
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1rem 3rem;
                border-radius: 8px;
                text-decoration: none;
                font-weight: 700;
                font-size: 1.2rem;
            ">
                🚀 Start Free Assessment (3 min)
            </a>
        </div>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-top: 1rem;">
            No credit card required • 100% free • Get results instantly
        </p>
    </div>
    """, unsafe_allow_html=True)

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
