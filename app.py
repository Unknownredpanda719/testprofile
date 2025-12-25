import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys
import requests
import json

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.psychometric_engine import PsychometricAssessment
from modules.recommendation_engine import RecommendationEngine
from modules.roi_calculator import ROICalculator
from modules.uk_programmes import get_programmes_for_pathway
from modules.uk_careers import get_careers_for_field

# ============= GOOGLE SHEETS INTEGRATION =============
# Replace this URL with your Google Apps Script Web App URL
GOOGLE_SHEETS_URL = "https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec"

def capture_email_to_sheet(email, name="", interest="", budget="", capture_point="", recommended_pathway="", roi_result=""):
    """Send email data to Google Sheets"""
    try:
        payload = {
            "email": email,
            "name": name,
            "interest": interest,
            "budget": budget,
            "capture_point": capture_point,
            "recommended_pathway": recommended_pathway,
            "roi_result": roi_result
        }
        
        response = requests.post(
            GOOGLE_SHEETS_URL,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error capturing email: {e}")
        return False

# Page config
st.set_page_config(
    page_title="Education Path Finder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============= GOOGLE ANALYTICS 4 =============
# Replace with your GA4 Measurement ID from Google Analytics
GA_MEASUREMENT_ID = "G-XXXXXXXXXX"  # TODO: Replace this!

# Only load GA4 if user has accepted analytics cookies
if GA_MEASUREMENT_ID != "G-XXXXXXXXXX" and st.session_state.get('analytics_enabled', False):
    st.markdown(f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA_MEASUREMENT_ID}', {{
        'anonymize_ip': true,
        'cookie_flags': 'SameSite=None;Secure'
      }});
    </script>
    """, unsafe_allow_html=True)

def track_event(event_name, event_params=None):
    """Track custom events in GA4 - only if analytics enabled"""
    if GA_MEASUREMENT_ID == "G-XXXXXXXXXX":
        return  # Skip if GA not configured
    
    if not st.session_state.get('analytics_enabled', False):
        return  # Skip if user hasn't consented to analytics
    
    if event_params is None:
        event_params = {}
    
    params_str = ", ".join([f"'{k}': '{v}'" for k, v in event_params.items()])
    
    st.markdown(f"""
    <script>
      gtag('event', '{event_name}', {{{params_str}}});
    </script>
    """, unsafe_allow_html=True)

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
    if 'cookies_accepted' not in st.session_state:
        st.session_state.cookies_accepted = False
    if 'analytics_enabled' not in st.session_state:
        st.session_state.analytics_enabled = False

def render_cookie_banner():
    """Render GDPR-compliant cookie consent banner"""
    if not st.session_state.cookies_accepted:
        st.markdown("""
        <div style="
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #222222;
            color: white;
            padding: 1.5rem;
            z-index: 9999;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
        ">
            <div style="max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div style="flex: 1; min-width: 300px;">
                    <strong>🍪 We use cookies</strong><br>
                    <span style="font-size: 0.9rem; color: #ccc;">
                        We use necessary cookies for site functionality and optional analytics cookies to improve our service.
                        See our <a href="#privacy-policy" style="color: #4fc3f7; text-decoration: underline;">Privacy Policy</a>.
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("✅ Accept All", key="accept_all_cookies", type="primary"):
                st.session_state.cookies_accepted = True
                st.session_state.analytics_enabled = True
                st.rerun()
        
        with col2:
            if st.button("⚙️ Necessary Only", key="necessary_only_cookies"):
                st.session_state.cookies_accepted = True
                st.session_state.analytics_enabled = False
                st.rerun()
        
        with col3:
            if st.button("❌ Reject All", key="reject_all_cookies"):
                st.session_state.cookies_accepted = True
                st.session_state.analytics_enabled = False
                st.rerun()

def render_privacy_policy_link():
    """Render privacy policy and terms links in footer"""
    st.markdown("""
    <div style="
        text-align: center;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid #EBEBEB;
        margin-top: 3rem;
        font-size: 0.85rem;
        color: #717171;
    ">
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Privacy Policy", key="privacy_footer", use_container_width=True):
            st.switch_page("pages/Privacy_Policy.py")
    
    with col2:
        if st.button("Terms of Service", key="terms_footer", use_container_width=True):
            st.info("Terms coming soon")
    
    with col3:
        if st.button("Cookie Settings", key="cookies_footer", use_container_width=True):
            st.session_state.cookies_accepted = False
            st.rerun()
    
    with col4:
        st.markdown("""
        <a href="mailto:your.email@example.com" style="
            display: inline-block;
            padding: 0.5rem 1rem;
            text-decoration: none;
            color: #717171;
            text-align: center;
            width: 100%;
        ">Contact</a>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; font-size: 0.75rem; color: #999; margin-top: 1rem;">
        © 2025 Education Path Finder. Registered in England and Wales. ICO: [Your Number]
    </div>
    """, unsafe_allow_html=True)

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
            [""] + ["Under £10,000", "£10,000 - £30,000", "£30,000 - £50,000", "£50,000 - £75,000", "Over £75,000"],
            format_func=lambda x: "Add budget range" if x == "" else x,
            label_visibility="collapsed",
            key="budget_select"
        )
    
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        search_clicked = st.button("🔍 Search", type="primary", width='stretch')
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    if search_clicked:
        if name and interest_input and budget_input:
            budget_map = {"Under £10,000": 8000, "£10,000 - £30,000": 20000, "£30,000 - £50,000": 40000, "£50,000 - £75,000": 62500, "Over £75,000": 90000}
            
            # Track assessment started
            track_event('assessment_started', {
                'interest': interest_input,
                'budget_range': budget_input
            })
            
            st.session_state.user_data = {
                'name': name,
                'age': 20,
                'budget': budget_map.get(budget_input, 20000),
                'current_income': 0,
                'interests': [interest_input],
                'target_country': 'UK'  # Default to UK
            }
            st.rerun()
        else:
            st.error("Please fill in all fields")
    
    # ============= EMAIL CAPTURE - TOP OF PAGE =============
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="max-width: 1200px; margin: 2rem auto; padding: 0 4rem;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2.5rem 2rem; border-radius: 20px; text-align: center; box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);">
            <h3 style="color: white; font-size: 1.6rem; margin-bottom: 0.75rem; font-weight: 600;">
                📧 Get Your Free Results + Curated Programme List
            </h3>
            <p style="color: rgba(255,255,255,0.9); font-size: 1rem; margin-bottom: 1.5rem;">
                Save your spot and receive your personalized pathway recommendations via email
            </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        early_email = st.text_input(
            "Email",
            placeholder="your.email@example.com",
            label_visibility="collapsed",
            key="early_email_capture_top"
        )
        
        # GDPR Consent Checkboxes
        email_consent_top = st.checkbox(
            "✓ I agree to receive my assessment results and programme recommendations",
            key="landing_email_consent_top"
        )
        
        marketing_consent_top = st.checkbox(
            "Send me scholarship opportunities and application deadlines (optional)",
            key="landing_marketing_consent_top"
        )
        
        st.markdown("""
        <div style="font-size: 0.75rem; color: rgba(255,255,255,0.8); margin-top: 0.5rem; text-align: center;">
            <a href="#privacy-policy" style="color: #fff; text-decoration: underline;">Privacy Policy</a> • 
            Unsubscribe anytime • We never sell your data
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✨ Save My Spot", type="primary", width='stretch', key="email_submit_top"):
            if not email_consent_top:
                st.error("Please agree to receive your assessment results")
            elif early_email and "@" in early_email:
                # Capture to Google Sheets with consent flags
                success = capture_email_to_sheet(
                    email=early_email,
                    name=name if name else "",
                    interest=interest_input if interest_input else "",
                    budget=budget_input if budget_input else "",
                    capture_point="landing_page_top",
                    recommended_pathway=f"Consent: {email_consent_top}, Marketing: {marketing_consent_top}",
                    roi_result=""
                )
                
                st.session_state['user_email'] = early_email
                st.session_state['marketing_consent'] = marketing_consent_top
                st.success("✅ Saved! Now fill in the search bar above and click 🔍 Search to start")
                
                # Track email capture
                track_event('email_captured', {
                    'capture_point': 'landing_page_top',
                    'marketing_consent': str(marketing_consent_top)
                })
                
                if not success:
                    st.warning("Note: Email saved locally but may not have synced to our system")
            else:
                st.error("Please enter a valid email")
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    st.markdown("""
    <div style="max-width: 1200px; margin: 4rem auto 2rem auto; padding: 0 2rem;">
        <h2 style="font-size: 1.4rem; font-weight: 600; color: #222222; margin-bottom: 2rem;">Why UK students choose us</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div style="padding: 1rem;"><div style="font-size: 2.5rem; font-weight: 600; color: #222222; margin-bottom: 0.5rem;">£38K+</div><div style="font-size: 1rem; color: #222222; font-weight: 500;">Average ROI improvement</div><div style="font-size: 0.9rem; color: #717171;">compared to default choice</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="padding: 1rem;"><div style="font-size: 2.5rem; font-weight: 600; color: #222222; margin-bottom: 0.5rem;">847</div><div style="font-size: 1rem; color: #222222; font-weight: 500;">Students saved from debt</div><div style="font-size: 0.9rem; color: #717171;">who would\'ve gone £25k+ in debt</div></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div style="padding: 1rem;"><div style="font-size: 2.5rem; font-weight: 600; color: #222222; margin-bottom: 0.5rem;">3 min</div><div style="font-size: 1rem; color: #222222; font-weight: 500;">To get your results</div><div style="font-size: 0.9rem; color: #717171;">complete assessment time</div></div>', unsafe_allow_html=True)
    
    # Programme Preview Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="max-width: 1200px; margin: 3rem auto 2rem auto; padding: 0 2rem;">
        <h2 style="font-size: 1.8rem; font-weight: 600; color: #222222; margin-bottom: 0.5rem;">
            Programmes We Recommend
        </h2>
        <p style="font-size: 1.1rem; color: #717171; margin-bottom: 2rem;">
            Real universities, apprenticeships, and bootcamps - tailored to your profile
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="padding: 2rem; border: 1px solid #EBEBEB; border-radius: 12px; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🎓</div>
            <h4 style="color: #222222; margin-bottom: 0.5rem;">Russell Group Universities</h4>
            <p style="color: #717171; font-size: 0.95rem; margin-bottom: 1rem;">
                Oxford, Imperial, Manchester, Bristol and more
            </p>
            <div style="color: #E31C5F; font-weight: 600;">From £27,750 total</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="padding: 2rem; border: 1px solid #EBEBEB; border-radius: 12px; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔧</div>
            <h4 style="color: #222222; margin-bottom: 0.5rem;">Top Apprenticeships</h4>
            <p style="color: #717171; font-size: 0.95rem; margin-bottom: 1rem;">
                Google, IBM, Rolls-Royce, PwC, BAE Systems
            </p>
            <div style="color: #4CAF50; font-weight: 600;">Earn £12-15k while learning</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="padding: 2rem; border: 1px solid #EBEBEB; border-radius: 12px; height: 100%;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">⚡</div>
            <h4 style="color: #222222; margin-bottom: 0.5rem;">Coding Bootcamps</h4>
            <p style="color: #717171; font-size: 0.95rem; margin-bottom: 1rem;">
                Le Wagon, Makers, General Assembly, Northcoders
            </p>
            <div style="color: #E31C5F; font-weight: 600;">From £4,000 (9-16 weeks)</div>
        </div>
        """, unsafe_allow_html=True)

def render_assessment():
    """Render psychometric assessment"""
    st.markdown(f'<div style="text-align: center; padding: 2rem 0;"><div style="display: inline-block; padding: 0.5rem 1.5rem; background: #e3f2fd; border-radius: 20px; color: #1976d2;">Step 2 of 3: Assessment</div></div>', unsafe_allow_html=True)
    st.markdown(f'<p class="main-header">Hi {st.session_state.user_data["name"]}! Let\'s Find Your Best Path</p>', unsafe_allow_html=True)
    
    # Premium features reminder
    st.info("💎 **After this assessment, you'll get:** Top 3 curated programmes • 5 career paths with UK salaries • ROI calculator • Scholarship opportunities")
    
    # NEW: Optional text box for achievements/experience
    st.markdown("---")
    st.markdown("### 📄 Boost Your Profile (Optional)")
    
    tab1, tab2 = st.tabs(["✍️ Type Your Experience", "📎 Upload CV"])
    
    with tab1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <p style="color: #717171; font-size: 0.95rem; margin: 0;">
                Share your achievements, projects, or work experience to get more accurate recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        user_text = st.text_area(
            "Your achievements, projects, or experience",
            placeholder="""Example: "Built a website for a local charity using HTML/CSS. Worked part-time at Tesco for 6 months. Captain of school football team for 2 years. Completed a 10km charity run."
            
Tell us about:
• Projects you've built or created
• Work experience (part-time jobs, internships)
• Leadership roles (captain, prefect, club president)
• Awards or achievements
• Skills you've developed
• Challenges you've overcome""",
            height=200,
            key="user_achievements_text",
            help="We'll analyze this to better understand your hands-on skills, perseverance, and leadership"
        )
        
        if user_text and len(user_text.strip()) > 20:
            # Show quick preview
            from modules.cv_analyzer import get_cv_insights
            
            with st.spinner("Analyzing your experience..."):
                cv_analysis = get_cv_insights(user_text)
                
                if cv_analysis['total_matches'] > 0:
                    st.success(f"✅ Found {cv_analysis['total_matches']} relevant skills/experiences!")
                    
                    with st.expander("🔍 What we detected"):
                        for insight in cv_analysis['insights'][:3]:
                            category = insight['category'].replace('_', ' ').title()
                            examples = ', '.join(insight['examples'][:3])
                            st.write(f"**{category}:** {examples}")
                else:
                    st.info("💡 Tip: Include words like 'built', 'led', 'created', or 'worked at' for better analysis")
            
            # Store for later
            st.session_state['user_achievements_text'] = user_text
    
    with tab2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <p style="color: #717171; font-size: 0.95rem; margin: 0;">
                Upload your CV (PDF or Word) and we'll automatically extract your skills and experience.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose your CV file",
            type=['pdf', 'docx', 'doc'],
            help="We'll extract text from your CV to analyze your skills and experience. Your file is processed securely and not stored.",
            key="cv_upload"
        )
        
        if uploaded_file:
            try:
                # Extract text from uploaded file
                if uploaded_file.name.endswith('.pdf'):
                    import PyPDF2
                    from io import BytesIO
                    
                    pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
                    cv_text = ""
                    for page in pdf_reader.pages:
                        cv_text += page.extract_text()
                
                elif uploaded_file.name.endswith(('.docx', '.doc')):
                    from docx import Document
                    from io import BytesIO
                    
                    doc = Document(BytesIO(uploaded_file.read()))
                    cv_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                
                if cv_text and len(cv_text.strip()) > 50:
                    st.success(f"✅ CV uploaded! Extracted {len(cv_text.split())} words")
                    
                    # Analyze the CV
                    from modules.cv_analyzer import get_cv_insights
                    
                    with st.spinner("Analyzing your CV..."):
                        cv_analysis = get_cv_insights(cv_text)
                        
                        if cv_analysis['total_matches'] > 0:
                            st.success(f"🎯 Found {cv_analysis['total_matches']} relevant skills/experiences in your CV!")
                            
                            with st.expander("🔍 Key skills detected"):
                                for insight in cv_analysis['insights'][:5]:
                                    category = insight['category'].replace('_', ' ').title()
                                    score = insight['score']
                                    examples = ', '.join(insight['examples'][:3])
                                    st.write(f"**{category}** ({score}/10): {examples}")
                        else:
                            st.warning("We couldn't detect many skills. Your CV might be in an unusual format. Try the text box instead!")
                    
                    # Store extracted text
                    st.session_state['user_achievements_text'] = cv_text
                else:
                    st.error("Could not extract text from this file. Please try a different format or use the text box.")
                    
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                st.info("💡 Try using the text box instead, or upload a different CV format")
    
    st.markdown("---")
    
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
        
        submitted = st.form_submit_button("📊 Get My Results", type="primary", width='stretch')
        
        if submitted:
            # Calculate base quiz scores
            base_scores = assessment.calculate_scores(responses)
            
            # Check if user provided additional text
            user_text = st.session_state.get('user_achievements_text', '')
            
            if user_text and len(user_text.strip()) > 20:
                # Merge quiz scores with CV text analysis
                from modules.cv_analyzer import merge_cv_with_quiz
                
                merged_scores, cv_analysis = merge_cv_with_quiz(base_scores, user_text)
                
                # Store both for results page
                st.session_state.assessment_scores = merged_scores
                st.session_state.cv_analysis = cv_analysis
                st.session_state.used_text_boost = True
            else:
                # Just use quiz scores
                st.session_state.assessment_scores = base_scores
                st.session_state.cv_analysis = None
                st.session_state.used_text_boost = False
            
            st.session_state.assessment_complete = True
            
            # Track assessment completion
            track_event('assessment_completed', {
                'grit_score': str(st.session_state.assessment_scores['grit']),
                'hands_on_score': str(st.session_state.assessment_scores['hands_on']),
                'text_analysis_used': str(st.session_state.get('used_text_boost', False))
            })
            
            st.rerun()

def render_results():
    """Render results with ROI analysis, programmes, and careers"""
    st.markdown('<div style="text-align: center; padding: 2rem 0;"><div style="display: inline-block; padding: 0.5rem 1.5rem; background: #e8f5e9; border-radius: 20px; color: #2e7d32;">✅ Step 3 of 3: Your Complete Results</div></div>', unsafe_allow_html=True)
    
    user_data = st.session_state.user_data
    scores = st.session_state.assessment_scores
    
    st.markdown(f'<p class="main-header">Results for {user_data["name"]}</p>', unsafe_allow_html=True)
    
    # Quick navigation to premium features
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #E31C5F;">
        <div style="font-weight: 600; color: #222222; margin-bottom: 0.5rem;">📋 Your Complete Report Includes:</div>
        <div style="display: flex; gap: 2rem; flex-wrap: wrap; font-size: 0.9rem; color: #717171;">
            <div>✅ Psychometric Profile</div>
            <div>✅ ROI Calculator</div>
            <div>✅ Top 3 Programmes</div>
            <div>✅ 5 Career Paths</div>
            <div>✅ Email Report Option</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Psychometric Profile
    st.markdown("### 📊 Your Psychometric Profile")
    
    # Show if text analysis was used
    if st.session_state.get('used_text_boost', False):
        st.markdown("""
        <div style="background: #e8f5e9; padding: 1rem; border-radius: 10px; border-left: 4px solid #4caf50; margin-bottom: 1rem;">
            <strong>✨ Enhanced Profile</strong><br>
            <span style="color: #717171; font-size: 0.9rem;">
                We analyzed your achievements and experience to give you more accurate scores below.
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Grit", f"{scores['grit']}/10")
    with col2:
        st.metric("Hands-On", f"{scores['hands_on']}/10")
    with col3:
        st.metric("Structure Need", f"{scores['structure']}/10")
    with col4:
        st.metric("Risk Tolerance", f"{scores['risk_tolerance']}/10")
    
    # Show insights from CV analysis if available
    if st.session_state.get('cv_analysis') and st.session_state.cv_analysis['total_matches'] > 0:
        with st.expander("🔍 What We Found in Your Experience", expanded=False):
            cv_analysis = st.session_state.cv_analysis
            
            st.markdown("Based on your text, we detected:")
            
            for insight in cv_analysis['insights'][:5]:
                category = insight['category'].replace('_', ' ').title()
                level = insight['level'].title()
                score = insight['score']
                examples = insight['examples'][:3]
                
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 0.75rem; border-radius: 8px; margin: 0.5rem 0;">
                    <strong>{category}:</strong> {level} ({score}/10)<br>
                    <span style="color: #717171; font-size: 0.85rem;">
                        Keywords: {', '.join(examples)}
                    </span>
                </div>
                """, unsafe_allow_html=True)
    
    # Get recommendation
    recommender = RecommendationEngine()
    recommendation = recommender.get_recommendation(scores, user_data)
    
    st.markdown("---")
    st.markdown(f"### 🎓 Recommended Path: **{recommendation['pathway']}**")
    st.write(f"**Why:** {recommendation['reasoning']}")
    
    # ROI Analysis
    st.markdown("---")
    st.markdown("### 💰 5-Year Financial Projection (UK)")
    
    roi_calc = ROICalculator()
    roi_data = roi_calc.calculate_all_pathways(
        user_data['budget'], 
        user_data['current_income'], 
        user_data['interests'][0] if user_data['interests'] else 'Technology & Software', 
        user_data['target_country']
    )
    
    df = pd.DataFrame(roi_data).T.sort_values('net_wealth_year_5', ascending=False)
    
    # Visualize with £ symbols
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Net Wealth (Year 5)',
        x=df.index,
        y=df['net_wealth_year_5'],
        marker_color=['#44ff44' if x > 0 else '#ff4444' for x in df['net_wealth_year_5']],
        text=[f"£{x:,.0f}" for x in df['net_wealth_year_5']],
        textposition='outside'
    ))
    fig.update_layout(
        title="5-Year Net Wealth by Pathway", 
        xaxis_title="Pathway", 
        yaxis_title="Net Wealth (£)", 
        height=500
    )
    fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)
    
    st.plotly_chart(fig, width='stretch')
    
    # Detailed table with £
    st.markdown("### 📈 Pathway Comparison")
    display_df = df.copy()
    display_df['total_cost'] = display_df['total_cost'].apply(lambda x: f"£{x:,.0f}")
    display_df['year_5_salary'] = display_df['year_5_salary'].apply(lambda x: f"£{x:,.0f}")
    display_df['net_wealth_year_5'] = display_df['net_wealth_year_5'].apply(lambda x: f"£{x:,.0f}")
    display_df['roi_multiple'] = display_df['roi_multiple'].apply(lambda x: f"{x:.2f}x")
    display_df['total_earnings_5yr'] = display_df['total_earnings_5yr'].apply(lambda x: f"£{x:,.0f}")
    display_df['education_duration'] = display_df['education_duration'].apply(lambda x: f"{x} years")
    display_df.columns = ['Total Cost', 'Year 5 Salary', 'Net Wealth', 'ROI Multiple', 'Total Earnings (5yr)', 'Duration']
    st.dataframe(display_df, width='stretch')
    
    # Warnings with £
    recommended_roi = roi_data[recommendation['pathway']]
    if recommended_roi['net_wealth_year_5'] < 0:
        st.error(f"⚠️ **DEBT WARNING**: {recommendation['pathway']} will leave you with **£{abs(recommended_roi['net_wealth_year_5']):,.0f} in debt** after 5 years.")
    elif recommended_roi['roi_multiple'] < 1.5:
        st.warning(f"⚠️ **LOW ROI**: ROI is only {recommended_roi['roi_multiple']:.2f}x")
    else:
        st.success(f"✅ **STRONG ROI**: Projected £{recommended_roi['net_wealth_year_5']:,.0f} net wealth after 5 years")
    
    # ============= NEW: TOP 3 PROGRAMMES =============
    st.markdown("---")
    st.markdown(f"### 🎓 Top 3 {recommendation['pathway']} Programmes For You")
    
    programmes = get_programmes_for_pathway(recommendation['pathway'], limit=3)
    
    if programmes:
        for prog in programmes:
            with st.expander(f"**{prog['name']}** - {prog['location']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Type:** {prog['type']}")
                    st.write(f"**Duration:** {prog['duration']}")
                    if 'entry_requirements' in prog:
                        st.write(f"**Entry Requirements:** {prog['entry_requirements']}")
                    
                    cost_display = f"£{abs(prog['cost']):,.0f}"
                    if prog['cost'] < 0:
                        st.write(f"**Salary While Training:** {cost_display}/year 💰")
                    else:
                        st.write(f"**Total Cost:** {cost_display}")
                    
                    st.write(f"**Starting Salary (after completion):** £{prog['starting_salary']:,.0f}")
                
                with col2:
                    if 'ranking' in prog:
                        st.info(f"🏆 {prog['ranking']}")
                    
                    st.link_button("📝 Apply Now", prog['application_link'], width='stretch')
    else:
        st.info("Programme database coming soon for this pathway.")
    
    # ============= NEW: CAREER PATHS =============
    st.markdown("---")
    st.markdown(f"### 💼 Career Paths in {user_data['interests'][0]}")
    
    careers = get_careers_for_field(user_data['interests'][0], limit=5)
    
    if careers:
        st.write("Based on your field of interest, here are career paths you could pursue:")
        
        for career in careers:
            with st.expander(f"**{career['title']}** - Entry: £{career['entry_salary']:,.0f} → Year 5: £{career['year_5_salary']:,.0f}", expanded=False):
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    st.write(f"**5-Year Salary Growth:** £{career['entry_salary']:,.0f} → £{career['year_5_salary']:,.0f}")
                    st.write(f"**Senior Salary Potential:** £{career['senior_salary']:,.0f}")
                    st.write(f"**Annual Growth Rate:** {career['growth_rate']*100:.0f}%")
                    st.write(f"**Job Demand:** {career['demand']}")
                    st.write(f"**Remote Work:** {'✅ Yes' if career['remote_friendly'] else '❌ No'}")
                
                with col2:
                    st.write("**Top Employers:**")
                    for company in career['top_companies'][:3]:
                        st.write(f"• {company}")
                    
                    st.write("**Required Skills:**")
                    for skill in career['skills'][:3]:
                        st.write(f"• {skill}")
                    
                    st.metric("UK Job Openings", career['job_openings_uk'])
    else:
        st.info("Career data coming soon for this field.")
    
    # ============= EMAIL CAPTURE - MORE PROMINENT =============
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem 2rem; border-radius: 20px; text-align: center; margin: 2rem 0;">
        <h3 style="color: white; font-size: 2rem; margin-bottom: 1rem;">
            📧 Get Your Full Report + Programme Guide Sent to Your Inbox
        </h3>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-bottom: 1.5rem;">
            We'll email you this full report plus scholarship opportunities, application deadlines, and interview tips
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        email = st.text_input(
            "Email address",
            placeholder="your.email@example.com",
            label_visibility="collapsed",
            key="email_capture",
            value=st.session_state.get('user_email', '')
        )
        
        # GDPR Consent Checkboxes
        results_consent = st.checkbox(
            "I agree to receive my full report and programme recommendations via email",
            value=True,  # Default checked since they already gave consent
            key="results_email_consent"
        )
        
        results_marketing = st.checkbox(
            "Yes, send me scholarship deadlines and education opportunities (optional)",
            value=st.session_state.get('marketing_consent', False),
            key="results_marketing_consent"
        )
        
        st.markdown("""
        <div style="font-size: 0.75rem; color: rgba(255,255,255,0.8); margin-top: 0.5rem; text-align: center;">
            See our <a href="#privacy-policy" style="color: #4fc3f7;">Privacy Policy</a>. 
            Unsubscribe anytime. Your data is secure and never sold.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📨 Email Me My Full Report", type="primary", width='stretch', key="send_report"):
            if not results_consent:
                st.error("Please agree to receive your report to continue")
            elif email and "@" in email:
                # Capture to Google Sheets with full context and consent
                success = capture_email_to_sheet(
                    email=email,
                    name=user_data.get('name', ''),
                    interest=user_data['interests'][0] if user_data.get('interests') else '',
                    budget=str(user_data.get('budget', '')),
                    capture_point="results_page_with_consent",
                    recommended_pathway=f"{recommendation['pathway']} | Consent: {results_consent}, Marketing: {results_marketing}",
                    roi_result=f"£{recommended_roi['net_wealth_year_5']:,.0f}"
                )
                
                st.success("✅ Report sent! Check your inbox in the next few minutes.")
                st.balloons()
                st.session_state['user_email'] = email
                st.session_state['marketing_consent'] = results_marketing
                
                # Track email capture event
                track_event('email_captured', {
                    'capture_point': 'results_page',
                    'marketing_consent': str(results_marketing)
                })
                
                if not success:
                    st.warning("Note: You'll receive your report, but it may take a bit longer to process")
            else:
                st.error("Please enter a valid email address")
    
    st.markdown("""
        <p style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-top: 1rem;">
            ✅ No spam • ✅ Unsubscribe anytime • ✅ We'll also send scholarship deadlines
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ============= NEW: ACTION BUTTONS =============
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download Full Report (PDF)", width='stretch'):
            st.info("PDF download coming soon!")
    
    with col2:
        if st.button("💬 Book Free Consultation", width='stretch'):
            st.info("Booking system coming soon!")
    
    with col3:
        if st.button("🔄 Start New Assessment", width='stretch'):
            st.session_state.clear()
            st.rerun()

def main():
    initialize_session_state()
    
    # Render cookie consent banner (GDPR requirement)
    render_cookie_banner()
    
    # Main content flow
    if not st.session_state.user_data:
        render_hero_landing()
    elif not st.session_state.assessment_complete:
        render_assessment()
    else:
        render_results()
    
    # Privacy policy footer (always visible)
    render_privacy_policy_link()

if __name__ == "__main__":
    main()
