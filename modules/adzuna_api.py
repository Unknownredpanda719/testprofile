"""
Adzuna Jobs API Integration
Real-time UK job market data for career recommendations

Free tier: 5,000 requests/month
Sign up: https://developer.adzuna.com/
"""

import requests
from typing import Dict, List, Optional

class AdzunaAPI:
    def __init__(self, app_id: str, app_key: str):
        """
        Initialize Adzuna API client
        
        Args:
            app_id: Your Adzuna App ID
            app_key: Your Adzuna API Key
        """
        self.app_id = app_id
        self.app_key = app_key
        self.base_url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"
    
    def get_job_demand(self, 
                       job_title: str, 
                       location: str = 'UK',
                       results_per_page: int = 100) -> Dict:
        """
        Get job demand statistics for a specific role
        
        Returns:
            {
                'total_jobs': int,
                'avg_salary': float,
                'salary_min': float,
                'salary_max': float,
                'top_companies': List[str],
                'locations': List[str],
                'updated_at': str
            }
        """
        
        params = {
            'app_id': self.app_id,
            'app_key': self.app_key,
            'what': job_title,
            'where': location,
            'results_per_page': results_per_page,
            'sort_by': 'salary'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract insights
            total_jobs = data.get('count', 0)
            results = data.get('results', [])
            
            # Calculate salary stats
            salaries = [
                job.get('salary_max', 0) 
                for job in results 
                if job.get('salary_max')
            ]
            
            avg_salary = sum(salaries) / len(salaries) if salaries else 0
            salary_min = min(salaries) if salaries else 0
            salary_max = max(salaries) if salaries else 0
            
            # Top companies
            companies = list(set([
                job['company']['display_name'] 
                for job in results 
                if job.get('company', {}).get('display_name')
            ]))[:10]
            
            # Top locations
            locations = list(set([
                job.get('location', {}).get('display_name', '')
                for job in results
                if job.get('location', {}).get('display_name')
            ]))[:10]
            
            return {
                'total_jobs': total_jobs,
                'avg_salary': round(avg_salary, 0),
                'salary_min': round(salary_min, 0),
                'salary_max': round(salary_max, 0),
                'top_companies': companies,
                'locations': locations,
                'updated_at': 'Today',
                'success': True
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'total_jobs': 0,
                'avg_salary': 0,
                'salary_min': 0,
                'salary_max': 0,
                'top_companies': [],
                'locations': [],
                'updated_at': 'N/A',
                'success': False,
                'error': str(e)
            }
    
    def get_skills_demand(self, skill: str) -> Dict:
        """
        Get demand for a specific skill
        
        Args:
            skill: e.g., 'Python', 'React', 'AWS'
            
        Returns:
            Demand level and job count
        """
        
        result = self.get_job_demand(skill)
        total_jobs = result['total_jobs']
        
        # Categorize demand
        if total_jobs > 10000:
            demand_level = 'Very High'
        elif total_jobs > 5000:
            demand_level = 'High'
        elif total_jobs > 2000:
            demand_level = 'Medium'
        elif total_jobs > 500:
            demand_level = 'Low'
        else:
            demand_level = 'Very Low'
        
        return {
            'skill': skill,
            'total_jobs': total_jobs,
            'demand_level': demand_level,
            'avg_salary': result['avg_salary']
        }
    
    def compare_careers(self, career_titles: List[str]) -> List[Dict]:
        """
        Compare multiple careers by job availability
        
        Args:
            career_titles: List of job titles to compare
            
        Returns:
            Sorted list by demand
        """
        
        comparisons = []
        
        for title in career_titles:
            data = self.get_job_demand(title)
            comparisons.append({
                'career': title,
                'total_jobs': data['total_jobs'],
                'avg_salary': data['avg_salary'],
                'demand_level': 'High' if data['total_jobs'] > 5000 else 'Medium' if data['total_jobs'] > 2000 else 'Low'
            })
        
        # Sort by total jobs (demand)
        comparisons.sort(key=lambda x: x['total_jobs'], reverse=True)
        
        return comparisons


# Example usage
if __name__ == "__main__":
    # Get your free API keys from https://developer.adzuna.com/
    api = AdzunaAPI(
        app_id='YOUR_APP_ID',  # Replace with your Adzuna App ID
        app_key='YOUR_API_KEY'  # Replace with your Adzuna API Key
    )
    
    # Example 1: Get software developer demand
    print("=" * 60)
    print("SOFTWARE DEVELOPER DEMAND (UK)")
    print("=" * 60)
    
    dev_demand = api.get_job_demand('Software Developer', 'UK')
    
    if dev_demand['success']:
        print(f"Total jobs: {dev_demand['total_jobs']:,}")
        print(f"Average salary: £{dev_demand['avg_salary']:,.0f}")
        print(f"Salary range: £{dev_demand['salary_min']:,.0f} - £{dev_demand['salary_max']:,.0f}")
        print(f"Top companies: {', '.join(dev_demand['top_companies'][:5])}")
        print(f"Top locations: {', '.join(dev_demand['locations'][:5])}")
    
    # Example 2: Compare career options
    print("\n" + "=" * 60)
    print("CAREER COMPARISON")
    print("=" * 60)
    
    careers = [
        'Software Developer',
        'Data Analyst',
        'Web Developer',
        'DevOps Engineer',
        'UX Designer'
    ]
    
    comparison = api.compare_careers(careers)
    
    for i, career in enumerate(comparison, 1):
        print(f"{i}. {career['career']}")
        print(f"   Jobs: {career['total_jobs']:,} | Salary: £{career['avg_salary']:,.0f} | Demand: {career['demand_level']}")
    
    # Example 3: Skills demand
    print("\n" + "=" * 60)
    print("SKILLS DEMAND")
    print("=" * 60)
    
    skills = ['Python', 'JavaScript', 'React', 'AWS', 'Docker']
    
    for skill in skills:
        skill_data = api.get_skills_demand(skill)
        print(f"{skill}: {skill_data['total_jobs']:,} jobs ({skill_data['demand_level']} demand)")
