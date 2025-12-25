# 🚀 QUICK START GUIDE

## Installation & Launch (3 Steps)

### Option 1: Using the run script (Recommended)
```bash
cd education_roi_engine
./run.sh
```

### Option 2: Manual launch
```bash
cd education_roi_engine
pip install -r requirements.txt
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

---

## How to Use the Platform

### Step 1: Fill Out Your Profile (Sidebar)
- Enter your name and age
- Input your education budget
- Select your areas of interest (max 3)
- Choose preferred study location

Click **"Save Profile & Start Assessment"**

### Step 2: Take the Assessment
- 7 behavioral questions
- Answer honestly - there are no "right" answers
- Focus on what you'd *actually* do, not what sounds impressive

Click **"Generate My Recommendation"**

### Step 3: Review Your Results
You'll see:
- Your psychometric profile (4 scores out of 10)
- Recommended education pathway
- 5-year financial projection for ALL pathways
- Debt warnings (if applicable)
- Specific next steps to take

---

## Understanding Your Results

### Psychometric Scores

**Grit (0-10)**
- Low (0-4): Need external motivation, benefit from structure
- Medium (5-6): Balanced perseverance
- High (7-10): Self-motivated, push through obstacles

**Hands-On Preference (0-10)**
- Low (0-4): Prefer theory and conceptual learning
- Medium (5-6): Can do both
- High (7-10): Learn by building and doing

**Structure Need (0-10)**
- Low (0-4): Self-directed learner
- Medium (5-6): Flexible
- High (7-10): Thrive in formal education

**Risk Tolerance (0-10)**
- Low (0-4): Prefer proven, traditional paths
- Medium (5-6): Balanced approach
- High (7-10): Comfortable with uncertainty

### The Four Pathways

**International University**
- 4-year degree abroad
- High cost, high structure
- Best for: Strong budget + formal education preference

**Local University**
- 4-year domestic degree
- Moderate cost, high structure
- Best for: Limited budget + need for credentials

**Apprenticeship**
- 2-year earn-while-you-learn
- Zero cost (you get paid!)
- Best for: High grit + hands-on learners + limited budget

**Micro-Credentials**
- 6-month bootcamp/certificates
- Low cost, low structure
- Best for: Self-motivated + quick income need + hands-on

### ROI Metrics Explained

**Total Cost**
- Tuition + living expenses + opportunity cost (income lost during study)

**Year 5 Salary**
- Projected annual salary 5 years after starting

**Net Wealth (Year 5)**
- Total earnings - Total costs
- This is the actual money in your pocket after 5 years

**ROI Multiple**
- How much you earn per $1 invested
- 1.0x = break even
- 2.0x = you earn $2 for every $1 spent
- <1.0x = you're losing money (debt)

### Warning Flags

🔴 **SEVERE WARNING**: Net wealth is negative (you'll be in debt)
🟡 **CAUTION**: ROI < 1.5x (barely profitable)
🟢 **GOOD**: Positive net wealth with decent ROI

---

## Sample Test Scenarios

Try these profiles to see different recommendations:

### Scenario 1: Self-Starter Tech Student
- Budget: $20,000
- Interests: Technology & Software
- Assessment: Answer with high independence, hands-on learning
- **Expected**: Micro-Credentials or Apprenticeship

### Scenario 2: Traditional Academic
- Budget: $100,000
- Interests: Science & Research
- Assessment: Answer with preference for structure, theory
- **Expected**: International or Local University

### Scenario 3: Budget-Constrained
- Budget: $5,000
- Any interests
- **Expected**: Apprenticeship (only affordable option)

---

## Troubleshooting

### App won't start
```bash
# Reinstall dependencies
pip install --upgrade streamlit pandas plotly

# Try running directly
python -m streamlit run app.py
```

### Browser doesn't open automatically
Manually navigate to: `http://localhost:8501`

### Port already in use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Module import errors
Make sure you're in the correct directory:
```bash
cd education_roi_engine
python test_backend.py  # Should pass all tests
```

---

## Key Principles

1. **Honesty Over Prestige**: We recommend what's financially smart, not what sounds impressive

2. **ROI First**: If a pathway leads to debt, we'll tell you directly

3. **Personalization**: Your psychometric profile matters more than test scores

4. **Alternatives Always Shown**: Even if we recommend one path, you see all options

---

## Need Help?

1. Run the backend tests: `python test_backend.py`
2. Check the full README.md for detailed documentation
3. Review the sample test scenarios above
4. Make sure all dependencies are installed

---

## What Makes This Different?

**Traditional platforms ask:**
- "What do you want to study?"
- "What's your GPA?"
- "Where do you want to go?"

**We ask:**
- "How do you handle failure?"
- "What's your budget vs expected ROI?"
- "Can you afford this degree based on salary projections?"

**Result**: Recommendations that protect your financial future, not just please universities.
