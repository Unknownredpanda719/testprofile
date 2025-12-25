# 🎓 Education ROI Engine - MVP

## The Human Capital De-risking Platform

### What This Is
An "Airbnb for Education" that disrupts the international student recruitment market by prioritizing **student financial outcomes** over institutional revenue. This platform uses psychometric assessment and ROI modeling to determine if a student should pursue:

1. **International University** - Traditional 4-year degree abroad
2. **Local University** - Domestic degree program
3. **Apprenticeship** - Earn-while-you-learn vocational training
4. **Micro-Credentials** - Bootcamps, certificates, self-directed learning

### The Innovation
- **Grit Engine**: Measures perseverance, learning style, and risk tolerance - not just "what do you want to study"
- **Honesty Filter**: If a degree costs more than projected 5-year salary growth, the system triggers a **Debt Warning**
- **ROI-First**: Every recommendation is backed by financial projections showing net wealth after 5 years

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Terminal/Command Prompt access

### Installation

1. **Clone or download this repository**
```bash
cd education_roi_engine
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Access in browser**
The app will automatically open at `http://localhost:8501`

---

## 📊 How It Works

### Step 1: User Intake
Students fill out a profile in the sidebar:
- Name, age
- Available education budget
- Current income (if any)
- Areas of interest (up to 3)
- Preferred study location

### Step 2: Psychometric Assessment
7 high-signal behavioral questions that measure:
- **Grit**: Perseverance through obstacles
- **Hands-On Preference**: Learning by doing vs. theory
- **Structure Need**: Formal education vs. self-directed
- **Risk Tolerance**: Comfort with non-traditional paths

**Example Question:**
> "You spent 6 months learning to code but failed your first technical interview. What do you do?"
> - A: Take a break and reconsider
> - B: Analyze what went wrong and reapply (HIGH GRIT)
> - C: Look for a structured course
> - D: Switch careers

### Step 3: Recommendation Engine
The system calculates a **fit score** (0-100) for each pathway based on:
- Psychometric profile alignment
- Budget constraints
- Field of interest

**Routing Logic:**
- High grit + hands-on → **Apprenticeship**
- High structure need + theoretical → **University**
- High grit + low structure need → **Micro-Credentials**
- Budget < $30k → **NOT** International University

### Step 4: ROI Projection
For each pathway, the system calculates:
- **Total Cost**: Tuition + living + opportunity cost
- **5-Year Earnings**: Realistic salary trajectory by field
- **Net Wealth (Year 5)**: Earnings - Total Cost
- **ROI Multiple**: How much you earn per $1 invested

**Debt Warning Triggers:**
- Net wealth < $0 after 5 years
- ROI multiple < 1.5x
- Total cost > 5-year earnings

---

## 🏗️ Architecture

### Project Structure
```
education_roi_engine/
├── app.py                          # Main Streamlit application
├── modules/
│   ├── __init__.py
│   ├── psychometric_engine.py      # Assessment logic
│   ├── recommendation_engine.py    # Pathway routing
│   └── roi_calculator.py           # Financial modeling
├── requirements.txt
└── README.md
```

### Module Breakdown

#### `psychometric_engine.py`
- 7 carefully designed behavioral questions
- Weighted scoring system (each dimension scored 0-10)
- Questions target real-world scenarios, not academic hypotheticals

#### `recommendation_engine.py`
- Fit score calculation for each pathway
- Budget eligibility filtering
- Alternative pathway suggestions
- Actionable next steps generation

#### `roi_calculator.py`
- **Salary data** by field and pathway (8 fields × 4 pathways)
- **Education costs** by country (6 countries × 2 university types)
- **5-year projections** with realistic growth rates
- **Opportunity cost** calculation (income lost during study)

---

## 💰 Sample ROI Calculations

### Example 1: Tech Student with $50k Budget
**Profile**: High grit (8/10), hands-on (9/10), low structure need (4/10)

| Pathway | Total Cost | Year 5 Salary | Net Wealth | ROI |
|---------|-----------|---------------|------------|-----|
| **Micro-Credentials** | $12,000 | $95,000 | **$283,000** | **24.6x** |
| Apprenticeship | $0 | $78,000 | $258,000 | ∞ |
| Local University | $96,000 | $82,000 | $134,000 | 2.4x |
| International University | $252,000 | $95,000 | $-27,000 | 0.9x ⚠️ |

**Recommendation**: Micro-Credentials (bootcamp path)
**Warning**: International University leaves you $27k in debt!

### Example 2: Healthcare Student with $20k Budget
**Profile**: Moderate grit (6/10), low hands-on (4/10), high structure (8/10)

| Pathway | Total Cost | Year 5 Salary | Net Wealth | ROI |
|---------|-----------|---------------|------------|-----|
| **Local University** | $80,000 | $75,000 | **$115,000** | **2.4x** |
| Micro-Credentials | $12,000 | $62,000 | $146,000 | 13.2x |
| Apprenticeship | $0 | $58,000 | $146,000 | ∞ |
| International University | N/A | N/A | N/A | Unaffordable |

**Recommendation**: Local University (fits structure need + budget)

---

## 🎯 Key Features

### 1. Brutal Honesty
- If a pathway leads to debt, **we say it explicitly**
- No sugar-coating for prestigious universities
- ROI warnings for <1.5x returns

### 2. Personalization
- Recommendations based on psychometrics, not just test scores
- Considers budget, field of interest, location preferences
- Suggests alternatives if primary path has negative ROI

### 3. Actionable Next Steps
Each recommendation includes 5 concrete action items:
- For universities: Visa requirements, scholarship research
- For apprenticeships: Where to find programs, portfolio tips
- For micro-credentials: Free resources to try first

### 4. Data Visualization
- Interactive bar charts showing net wealth by pathway
- Color coding: Green for positive ROI, red for debt
- Detailed comparison tables

---

## 🔧 Customization

### Adding New Fields of Interest
Edit `roi_calculator.py`:
```python
self.salary_data['Your New Field'] = {
    'International University': {'starting': 70000, 'growth_rate': 0.10},
    'Local University': {'starting': 60000, 'growth_rate': 0.09},
    'Apprenticeship': {'starting': 45000, 'growth_rate': 0.12},
    'Micro-Credentials': {'starting': 55000, 'growth_rate': 0.15}
}
```

### Modifying Assessment Questions
Edit `psychometric_engine.py`:
- Update the `questions` list in `__init__()`
- Each question needs `id`, `text`, `options`, and `weights`
- Weights are scored 1-10 for each dimension

### Adjusting Education Costs
Edit `roi_calculator.py` → `self.education_costs`:
```python
'Local University': {
    'USA': {'tuition': 12000, 'living': 12000, 'duration_years': 4}
}
```

---

## 📈 Future Enhancements

### Phase 2 (Next Sprint)
- [ ] User accounts and progress tracking
- [ ] Export recommendations as PDF
- [ ] Integration with real university pricing APIs
- [ ] Scholarship matching engine

### Phase 3 (Marketplace)
- [ ] University/bootcamp listings
- [ ] Student-mentor matching
- [ ] Visa application tracking
- [ ] ROI-based financing options

---

## 🧪 Testing

### Manual Test Scenarios

**Test 1: High-Risk Student**
- Budget: $100k
- Interests: Creative Arts
- Profile: Low grit (3/10), low hands-on (4/10)
- **Expected**: Local University with debt warnings

**Test 2: Self-Starter**
- Budget: $15k
- Interests: Technology
- Profile: High grit (9/10), high hands-on (9/10)
- **Expected**: Micro-Credentials or Apprenticeship

**Test 3: Budget-Constrained**
- Budget: $5k
- Interests: Any
- **Expected**: Apprenticeship only (others filtered out)

---

## 🤝 Contributing

This is an MVP. Priority improvements:
1. **Data accuracy**: Validate salary projections with labor market data
2. **Question refinement**: A/B test psychometric questions for predictive power
3. **Cost modeling**: Add regional variation in living costs
4. **Outcome tracking**: Long-term validation of recommendations

---

## ⚖️ Ethical Considerations

This platform makes **life-altering recommendations**. Key safeguards:
- Always show multiple pathways (never lock users into one option)
- Debt warnings are prominent and unavoidable
- Alternative suggestions included even for "optimal" paths
- Encourage users to validate with real advisors

**Limitations:**
- ROI projections are estimates, not guarantees
- Psychometric assessment is simplified (not clinical-grade)
- Salary data is US-centric and may not generalize globally

---

## 📞 Support

For questions or issues:
1. Check the FAQ section (coming soon)
2. Review sample test scenarios above
3. Contact: [Your contact info]

---

## 📄 License

MIT License - Free to use and modify

---

## 🎓 Philosophy

**Traditional education marketplaces optimize for:**
- University revenue
- Application volume
- Prestige signals

**This platform optimizes for:**
- Student financial outcomes
- Honest career guidance
- ROI transparency

*"If a degree leaves you in debt with no earnings premium, we'll tell you - even if it upsets universities."*
