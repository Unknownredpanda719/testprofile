"""
UK Programme Database
Real universities, bootcamps, and apprenticeships for each pathway
"""

UK_PROGRAMMES = {
    'International University': [
        {
            'name': 'University of Oxford - Computer Science',
            'type': 'University',
            'location': 'Oxford, UK',
            'duration': '3 years',
            'cost': 27750,  # £9,250/year × 3
            'entry_requirements': 'A*A*A',
            'starting_salary': 35000,
            'application_link': 'https://www.ox.ac.uk',
            'fit_tags': ['high_structure', 'theoretical', 'prestige'],
            'ranking': 1
        },
        {
            'name': 'Imperial College London - Engineering',
            'type': 'University',
            'location': 'London, UK',
            'duration': '4 years (MEng)',
            'cost': 37000,
            'entry_requirements': 'A*A*A',
            'starting_salary': 34000,
            'application_link': 'https://www.imperial.ac.uk',
            'fit_tags': ['high_structure', 'technical', 'prestige'],
            'ranking': 2
        },
        {
            'name': 'London School of Economics - Economics',
            'type': 'University',
            'location': 'London, UK',
            'duration': '3 years',
            'cost': 27750,
            'entry_requirements': 'A*AA',
            'starting_salary': 33000,
            'application_link': 'https://www.lse.ac.uk',
            'fit_tags': ['high_structure', 'theoretical', 'business'],
            'ranking': 3
        }
    ],
    
    'Local University': [
        {
            'name': 'University of Bristol - Computer Science',
            'type': 'University',
            'location': 'Bristol, UK',
            'duration': '3 years',
            'cost': 27750,
            'entry_requirements': 'AAB',
            'starting_salary': 29000,
            'application_link': 'https://www.bristol.ac.uk',
            'fit_tags': ['high_structure', 'balanced', 'russell_group'],
            'ranking': 'Russell Group'
        },
        {
            'name': 'University of Manchester - Engineering',
            'type': 'University',
            'location': 'Manchester, UK',
            'duration': '3 years',
            'cost': 27750,
            'entry_requirements': 'AAA',
            'starting_salary': 28000,
            'application_link': 'https://www.manchester.ac.uk',
            'fit_tags': ['high_structure', 'technical', 'russell_group'],
            'ranking': 'Russell Group'
        },
        {
            'name': 'University of Birmingham - Business',
            'type': 'University',
            'location': 'Birmingham, UK',
            'duration': '3 years',
            'cost': 27750,
            'entry_requirements': 'ABB',
            'starting_salary': 27000,
            'application_link': 'https://www.birmingham.ac.uk',
            'fit_tags': ['high_structure', 'business', 'russell_group'],
            'ranking': 'Russell Group'
        },
        {
            'name': 'Nottingham Trent University - Computing',
            'type': 'University',
            'location': 'Nottingham, UK',
            'duration': '3 years',
            'cost': 27750,
            'entry_requirements': 'BBC',
            'starting_salary': 25000,
            'application_link': 'https://www.ntu.ac.uk',
            'fit_tags': ['moderate_structure', 'practical', 'modern'],
            'ranking': 'Modern University'
        },
        {
            'name': 'Open University - Computing & IT',
            'type': 'Distance Learning',
            'location': 'Online',
            'duration': '3-6 years (part-time)',
            'cost': 18000,
            'entry_requirements': 'None',
            'starting_salary': 26000,
            'application_link': 'https://www.open.ac.uk',
            'fit_tags': ['flexible', 'self_directed', 'work_friendly'],
            'ranking': 'Distance Learning'
        }
    ],
    
    'Apprenticeship': [
        {
            'name': 'Google Software Engineering Apprenticeship',
            'type': 'Apprenticeship',
            'location': 'London, UK',
            'duration': '2 years',
            'cost': -24000,  # Earn £12k/year
            'entry_requirements': 'A-Levels or equivalent',
            'starting_salary': 28000,  # After completion
            'application_link': 'https://careers.google.com/apprenticeships',
            'fit_tags': ['hands_on', 'high_grit', 'tech'],
            'ranking': 'Big Tech'
        },
        {
            'name': 'IBM Digital Technology Solutions Apprenticeship',
            'type': 'Apprenticeship',
            'location': 'Multiple UK locations',
            'duration': '2 years',
            'cost': -22000,
            'entry_requirements': '5 GCSEs grade 4+',
            'starting_salary': 26000,
            'application_link': 'https://www.ibm.com/uk-en/employment/apprenticeships',
            'fit_tags': ['hands_on', 'tech', 'structured'],
            'ranking': 'Big Tech'
        },
        {
            'name': 'Rolls-Royce Engineering Apprenticeship',
            'type': 'Apprenticeship',
            'location': 'Derby, UK',
            'duration': '4 years',
            'cost': -56000,  # Earn £14k/year
            'entry_requirements': '5 GCSEs grade 5+ (Maths & Science)',
            'starting_salary': 30000,
            'application_link': 'https://careers.rolls-royce.com/apprenticeships',
            'fit_tags': ['hands_on', 'engineering', 'prestigious'],
            'ranking': 'Engineering'
        },
        {
            'name': 'PwC Flying Start Degree Apprenticeship',
            'type': 'Degree Apprenticeship',
            'location': 'Multiple UK locations',
            'duration': '5 years',
            'cost': -75000,  # Earn £15k/year + degree
            'entry_requirements': 'ABB at A-Level',
            'starting_salary': 32000,
            'application_link': 'https://www.pwc.co.uk/careers/school-jobs/flying-start-programmes.html',
            'fit_tags': ['hands_on', 'business', 'degree_included'],
            'ranking': 'Big 4'
        },
        {
            'name': 'BAE Systems Engineering Apprenticeship',
            'type': 'Apprenticeship',
            'location': 'Various UK',
            'duration': '4 years',
            'cost': -52000,
            'entry_requirements': '5 GCSEs grade 5+',
            'starting_salary': 29000,
            'application_link': 'https://www.baesystems.com/apprenticeships',
            'fit_tags': ['hands_on', 'engineering', 'defence'],
            'ranking': 'Defence'
        },
        {
            'name': 'Amazon Software Development Apprenticeship',
            'type': 'Apprenticeship',
            'location': 'London, UK',
            'duration': '2 years',
            'cost': -24000,
            'entry_requirements': 'A-Levels or equivalent',
            'starting_salary': 27000,
            'application_link': 'https://www.amazon.jobs/apprenticeships',
            'fit_tags': ['hands_on', 'tech', 'fast_paced'],
            'ranking': 'Big Tech'
        }
    ],
    
    'Micro-Credentials': [
        {
            'name': 'Le Wagon - Full Stack Web Development',
            'type': 'Bootcamp',
            'location': 'London (+ Remote)',
            'duration': '9 weeks',
            'cost': 7000,
            'entry_requirements': 'None',
            'starting_salary': 28000,
            'application_link': 'https://www.lewagon.com/london',
            'fit_tags': ['intensive', 'hands_on', 'career_switcher'],
            'ranking': '4.9/5 (Switchup)'
        },
        {
            'name': 'Makers Academy - Software Engineering',
            'type': 'Bootcamp',
            'location': 'London (+ Remote)',
            'duration': '16 weeks',
            'cost': 8000,
            'entry_requirements': 'None',
            'starting_salary': 30000,
            'application_link': 'https://www.makers.tech',
            'fit_tags': ['intensive', 'career_switcher', 'job_guarantee'],
            'ranking': '4.8/5 (Course Report)'
        },
        {
            'name': 'General Assembly - Data Science',
            'type': 'Bootcamp',
            'location': 'London',
            'duration': '12 weeks',
            'cost': 11000,
            'entry_requirements': 'Basic programming',
            'starting_salary': 32000,
            'application_link': 'https://generalassemb.ly/locations/london',
            'fit_tags': ['intensive', 'data_science', 'global_network'],
            'ranking': '4.5/5 (Switchup)'
        },
        {
            'name': 'Northcoders - Software Development',
            'type': 'Bootcamp',
            'location': 'Manchester (+ Remote)',
            'duration': '13 weeks',
            'cost': 6500,
            'entry_requirements': 'None',
            'starting_salary': 26000,
            'application_link': 'https://www.northcoders.com',
            'fit_tags': ['intensive', 'northern', 'affordable'],
            'ranking': '4.9/5 (Course Report)'
        },
        {
            'name': 'CodeClan - Software Development',
            'type': 'Bootcamp',
            'location': 'Edinburgh/Glasgow',
            'duration': '16 weeks',
            'cost': 5500,
            'entry_requirements': 'None',
            'starting_salary': 25000,
            'application_link': 'https://www.codeclan.com',
            'fit_tags': ['intensive', 'scotland', 'affordable'],
            'ranking': '4.8/5 (Switchup)'
        },
        {
            'name': 'HyperionDev - Data Science',
            'type': 'Online Bootcamp',
            'location': 'Fully Remote',
            'duration': '3-6 months (part-time)',
            'cost': 4000,
            'entry_requirements': 'None',
            'starting_salary': 27000,
            'application_link': 'https://www.hyperiondev.com',
            'fit_tags': ['flexible', 'work_friendly', 'affordable'],
            'ranking': '4.7/5 (Trustpilot)'
        }
    ]
}

def get_programmes_for_pathway(pathway, limit=3):
    """Get top programmes for a specific pathway"""
    programmes = UK_PROGRAMMES.get(pathway, [])
    return programmes[:limit]

def get_all_programmes_for_pathway(pathway):
    """Get all programmes for a specific pathway"""
    return UK_PROGRAMMES.get(pathway, [])
