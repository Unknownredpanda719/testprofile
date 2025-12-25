"""
UK Careers Database
Career paths with UK salary data, growth rates, and job market insights
"""

UK_CAREERS = {
    'Technology & Software': [
        {
            'title': 'Software Developer',
            'entry_salary': 28000,
            'year_5_salary': 45000,
            'senior_salary': 65000,
            'growth_rate': 0.15,
            'required_education': ['Bootcamp', 'Degree', 'Apprenticeship'],
            'top_companies': ['Google', 'Amazon', 'Sky', 'BBC', 'Monzo'],
            'demand': 'Very High',
            'remote_friendly': True,
            'skills': ['JavaScript', 'Python', 'React', 'Git'],
            'job_openings_uk': '15,000+'
        },
        {
            'title': 'Data Analyst',
            'entry_salary': 26000,
            'year_5_salary': 42000,
            'senior_salary': 60000,
            'growth_rate': 0.14,
            'required_education': ['Bootcamp', 'Degree'],
            'top_companies': ['Deloitte', 'KPMG', 'British Airways', 'HSBC'],
            'demand': 'High',
            'remote_friendly': True,
            'skills': ['SQL', 'Python', 'Excel', 'Tableau'],
            'job_openings_uk': '8,000+'
        },
        {
            'title': 'DevOps Engineer',
            'entry_salary': 32000,
            'year_5_salary': 52000,
            'senior_salary': 75000,
            'growth_rate': 0.16,
            'required_education': ['Degree', 'Apprenticeship', 'Self-taught'],
            'top_companies': ['Amazon Web Services', 'Google Cloud', 'Cloudflare'],
            'demand': 'Very High',
            'remote_friendly': True,
            'skills': ['AWS', 'Docker', 'Kubernetes', 'CI/CD'],
            'job_openings_uk': '6,000+'
        },
        {
            'title': 'Cloud Architect',
            'entry_salary': 40000,
            'year_5_salary': 65000,
            'senior_salary': 90000,
            'growth_rate': 0.15,
            'required_education': ['Degree', 'Self-taught with certs'],
            'top_companies': ['Accenture', 'Capgemini', 'AWS', 'Microsoft'],
            'demand': 'High',
            'remote_friendly': True,
            'skills': ['AWS', 'Azure', 'Architecture', 'Security'],
            'job_openings_uk': '4,000+'
        },
        {
            'title': 'Cybersecurity Analyst',
            'entry_salary': 30000,
            'year_5_salary': 48000,
            'senior_salary': 70000,
            'growth_rate': 0.14,
            'required_education': ['Degree', 'Apprenticeship', 'Certifications'],
            'top_companies': ['GCHQ', 'BAE Systems', 'Darktrace', 'NCC Group'],
            'demand': 'Very High',
            'remote_friendly': False,
            'skills': ['Network Security', 'Penetration Testing', 'CISSP'],
            'job_openings_uk': '5,500+'
        }
    ],
    
    'Business & Finance': [
        {
            'title': 'Accountant (ACCA/CIMA)',
            'entry_salary': 24000,
            'year_5_salary': 38000,
            'senior_salary': 55000,
            'growth_rate': 0.12,
            'required_education': ['Degree', 'Apprenticeship + ACCA'],
            'top_companies': ['PwC', 'Deloitte', 'EY', 'KPMG'],
            'demand': 'High',
            'remote_friendly': True,
            'skills': ['Financial Reporting', 'Tax', 'Audit', 'Excel'],
            'job_openings_uk': '12,000+'
        },
        {
            'title': 'Financial Analyst',
            'entry_salary': 28000,
            'year_5_salary': 45000,
            'senior_salary': 65000,
            'growth_rate': 0.13,
            'required_education': ['Degree', 'CFA'],
            'top_companies': ['JP Morgan', 'Barclays', 'HSBC', 'Goldman Sachs'],
            'demand': 'Medium',
            'remote_friendly': True,
            'skills': ['Financial Modelling', 'Excel', 'Bloomberg', 'Valuation'],
            'job_openings_uk': '4,500+'
        },
        {
            'title': 'Management Consultant',
            'entry_salary': 32000,
            'year_5_salary': 55000,
            'senior_salary': 85000,
            'growth_rate': 0.15,
            'required_education': ['Degree (Russell Group preferred)'],
            'top_companies': ['McKinsey', 'BCG', 'Bain', 'Accenture'],
            'demand': 'Medium',
            'remote_friendly': False,
            'skills': ['Problem Solving', 'Excel', 'PowerPoint', 'Strategy'],
            'job_openings_uk': '3,000+'
        },
        {
            'title': 'Business Analyst',
            'entry_salary': 26000,
            'year_5_salary': 40000,
            'senior_salary': 58000,
            'growth_rate': 0.11,
            'required_education': ['Degree', 'Bootcamp'],
            'top_companies': ['Lloyds Banking Group', 'Tesco', 'BT'],
            'demand': 'High',
            'remote_friendly': True,
            'skills': ['Requirements Gathering', 'SQL', 'Agile', 'Stakeholder Management'],
            'job_openings_uk': '9,000+'
        }
    ],
    
    'Engineering & Manufacturing': [
        {
            'title': 'Mechanical Engineer',
            'entry_salary': 27000,
            'year_5_salary': 42000,
            'senior_salary': 60000,
            'growth_rate': 0.12,
            'required_education': ['Degree (MEng)', 'Apprenticeship'],
            'top_companies': ['Rolls-Royce', 'BAE Systems', 'Airbus', 'JLR'],
            'demand': 'High',
            'remote_friendly': False,
            'skills': ['CAD', 'SolidWorks', 'FEA', 'Manufacturing'],
            'job_openings_uk': '6,500+'
        },
        {
            'title': 'Electrical Engineer',
            'entry_salary': 28000,
            'year_5_salary': 44000,
            'senior_salary': 62000,
            'growth_rate': 0.13,
            'required_education': ['Degree', 'Apprenticeship'],
            'top_companies': ['National Grid', 'Siemens', 'ABB', 'Schneider Electric'],
            'demand': 'High',
            'remote_friendly': False,
            'skills': ['Circuit Design', 'PLC Programming', 'AutoCAD', 'Testing'],
            'job_openings_uk': '5,000+'
        },
        {
            'title': 'Civil Engineer',
            'entry_salary': 26000,
            'year_5_salary': 40000,
            'senior_salary': 55000,
            'growth_rate': 0.11,
            'required_education': ['Degree (BEng/MEng)'],
            'top_companies': ['Arup', 'Mott MacDonald', 'Balfour Beatty', 'HS2'],
            'demand': 'High',
            'remote_friendly': False,
            'skills': ['Structural Analysis', 'AutoCAD', 'Project Management'],
            'job_openings_uk': '7,000+'
        }
    ],
    
    'Healthcare & Medicine': [
        {
            'title': 'Registered Nurse',
            'entry_salary': 25000,
            'year_5_salary': 32000,
            'senior_salary': 42000,
            'growth_rate': 0.07,
            'required_education': ['Nursing Degree', 'Apprenticeship (Nursing Associate)'],
            'top_companies': ['NHS', 'Private Hospitals', 'Care Homes'],
            'demand': 'Very High',
            'remote_friendly': False,
            'skills': ['Patient Care', 'Clinical Skills', 'Compassion'],
            'job_openings_uk': '40,000+'
        },
        {
            'title': 'Physiotherapist',
            'entry_salary': 24000,
            'year_5_salary': 32000,
            'senior_salary': 44000,
            'growth_rate': 0.08,
            'required_education': ['Degree (BSc Physiotherapy)'],
            'top_companies': ['NHS', 'Nuffield Health', 'Bupa'],
            'demand': 'High',
            'remote_friendly': False,
            'skills': ['Manual Therapy', 'Rehabilitation', 'Patient Assessment'],
            'job_openings_uk': '5,000+'
        },
        {
            'title': 'Dental Nurse',
            'entry_salary': 20000,
            'year_5_salary': 25000,
            'senior_salary': 30000,
            'growth_rate': 0.06,
            'required_education': ['Apprenticeship', 'Diploma'],
            'top_companies': ['NHS Dentists', 'Private Practices', 'Bupa Dental'],
            'demand': 'High',
            'remote_friendly': False,
            'skills': ['Dental Procedures', 'Sterilization', 'Patient Care'],
            'job_openings_uk': '8,000+'
        }
    ],
    
    'Trades & Construction': [
        {
            'title': 'Electrician',
            'entry_salary': 22000,
            'year_5_salary': 35000,
            'senior_salary': 45000,
            'growth_rate': 0.14,
            'required_education': ['Apprenticeship (Level 3)'],
            'top_companies': ['Self-employed', 'Balfour Beatty', 'Laing O\'Rourke'],
            'demand': 'Very High',
            'remote_friendly': False,
            'skills': ['Wiring', '18th Edition', 'Testing & Inspection'],
            'job_openings_uk': '15,000+'
        },
        {
            'title': 'Plumber',
            'entry_salary': 21000,
            'year_5_salary': 33000,
            'senior_salary': 42000,
            'growth_rate': 0.13,
            'required_education': ['Apprenticeship (Level 3)'],
            'top_companies': ['Self-employed', 'British Gas', 'Pimlico Plumbers'],
            'demand': 'Very High',
            'remote_friendly': False,
            'skills': ['Pipework', 'Gas Safe', 'Central Heating'],
            'job_openings_uk': '12,000+'
        },
        {
            'title': 'Carpenter',
            'entry_salary': 20000,
            'year_5_salary': 30000,
            'senior_salary': 38000,
            'growth_rate': 0.12,
            'required_education': ['Apprenticeship'],
            'top_companies': ['Self-employed', 'Wates', 'Morgan Sindall'],
            'demand': 'High',
            'remote_friendly': False,
            'skills': ['Joinery', 'Site Carpentry', 'Reading Drawings'],
            'job_openings_uk': '10,000+'
        }
    ]
}

def get_careers_for_field(field, limit=5):
    """Get top careers for a specific field"""
    careers = UK_CAREERS.get(field, [])
    return careers[:limit]

def get_career_by_title(title):
    """Get specific career by title"""
    for field, careers in UK_CAREERS.items():
        for career in careers:
            if career['title'].lower() == title.lower():
                return career
    return None
