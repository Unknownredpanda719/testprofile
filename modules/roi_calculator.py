"""
ROI Calculator
Calculates 5-year financial projections for each education pathway
Brutally honest - factors in debt, opportunity cost, realistic salary growth
"""

class ROICalculator:
    def __init__(self):
        # Base salary data by field and pathway (GBP £, annual - UK market)
        self.salary_data = {
            'Technology & Software': {
                'International University': {'starting': 32000, 'growth_rate': 0.12},
                'Local University': {'starting': 28000, 'growth_rate': 0.11},
                'Apprenticeship': {'starting': 22000, 'growth_rate': 0.16},
                'Micro-Credentials': {'starting': 26000, 'growth_rate': 0.18}
            },
            'Business & Finance': {
                'International University': {'starting': 30000, 'growth_rate': 0.10},
                'Local University': {'starting': 26000, 'growth_rate': 0.09},
                'Apprenticeship': {'starting': 20000, 'growth_rate': 0.12},
                'Micro-Credentials': {'starting': 24000, 'growth_rate': 0.14}
            },
            'Healthcare & Medicine': {
                'International University': {'starting': 28000, 'growth_rate': 0.08},
                'Local University': {'starting': 26000, 'growth_rate': 0.08},
                'Apprenticeship': {'starting': 21000, 'growth_rate': 0.10},
                'Micro-Credentials': {'starting': 23000, 'growth_rate': 0.11}
            },
            'Engineering & Manufacturing': {
                'International University': {'starting': 31000, 'growth_rate': 0.09},
                'Local University': {'starting': 28000, 'growth_rate': 0.09},
                'Apprenticeship': {'starting': 23000, 'growth_rate': 0.14},
                'Micro-Credentials': {'starting': 25000, 'growth_rate': 0.13}
            },
            'Creative Arts & Design': {
                'International University': {'starting': 22000, 'growth_rate': 0.07},
                'Local University': {'starting': 20000, 'growth_rate': 0.06},
                'Apprenticeship': {'starting': 18000, 'growth_rate': 0.11},
                'Micro-Credentials': {'starting': 20000, 'growth_rate': 0.13}
            },
            'Education & Social Services': {
                'International University': {'starting': 24000, 'growth_rate': 0.06},
                'Local University': {'starting': 23000, 'growth_rate': 0.06},
                'Apprenticeship': {'starting': 19000, 'growth_rate': 0.08},
                'Micro-Credentials': {'starting': 21000, 'growth_rate': 0.09}
            },
            'Science & Research': {
                'International University': {'starting': 27000, 'growth_rate': 0.08},
                'Local University': {'starting': 25000, 'growth_rate': 0.08},
                'Apprenticeship': {'starting': 21000, 'growth_rate': 0.10},
                'Micro-Credentials': {'starting': 23000, 'growth_rate': 0.11}
            },
            'Trades & Construction': {
                'International University': {'starting': 24000, 'growth_rate': 0.07},
                'Local University': {'starting': 23000, 'growth_rate': 0.07},
                'Apprenticeship': {'starting': 21000, 'growth_rate': 0.15},
                'Micro-Credentials': {'starting': 22000, 'growth_rate': 0.13}
            }
        }
        
        # Education costs by pathway (GBP £, annual - UK market)
        self.education_costs = {
            'International University': {
                'USA': {'tuition': 35000, 'living': 14000, 'duration_years': 4},
                'UK': {'tuition': 9250, 'living': 9000, 'duration_years': 3},  # Home fees
                'Canada': {'tuition': 18000, 'living': 11000, 'duration_years': 4},
                'Australia': {'tuition': 20000, 'living': 12000, 'duration_years': 3},
                'Germany': {'tuition': 2000, 'living': 9000, 'duration_years': 3},
                'Local/Home Country': {'tuition': 9250, 'living': 9000, 'duration_years': 3}  # UK home fees
            },
            'Local University': {
                'USA': {'tuition': 9000, 'living': 9000, 'duration_years': 4},
                'UK': {'tuition': 9250, 'living': 7000, 'duration_years': 3},  # Home fees, living at home
                'Canada': {'tuition': 6000, 'living': 8000, 'duration_years': 4},
                'Australia': {'tuition': 7000, 'living': 8500, 'duration_years': 3},
                'Germany': {'tuition': 400, 'living': 8000, 'duration_years': 3},
                'Local/Home Country': {'tuition': 9250, 'living': 7000, 'duration_years': 3}
            },
            'Apprenticeship': {
                'default': {'tuition': -12000, 'living': 0, 'duration_years': 2}  # Negative = earning £12k/year
            },
            'Micro-Credentials': {
                'default': {'tuition': 9000, 'living': 0, 'duration_years': 0.5}  # 6 months bootcamp
            }
        }
    
    def calculate_pathway_roi(self, pathway, budget, current_income, field, country):
        """
        Calculate 5-year ROI for a specific pathway
        
        Returns:
            Dict with total_cost, year_5_salary, net_wealth_year_5, roi_multiple
        """
        # Get education costs
        if pathway in ['Apprenticeship', 'Micro-Credentials']:
            cost_data = self.education_costs[pathway]['default']
        else:
            cost_data = self.education_costs[pathway].get(country, 
                                                          self.education_costs[pathway]['Local/Home Country'])
        
        # Calculate total education cost
        duration_years = cost_data['duration_years']
        annual_cost = cost_data['tuition'] + cost_data['living']
        total_education_cost = annual_cost * duration_years
        
        # Get salary trajectory
        salary_info = self.salary_data.get(field, self.salary_data['Technology & Software'])[pathway]
        starting_salary = salary_info['starting']
        growth_rate = salary_info['growth_rate']
        
        # Calculate earnings over 5 years
        total_earnings = 0
        year_5_salary = 0
        
        # Year-by-year calculation
        for year in range(1, 6):
            if year <= duration_years:
                # Still in education
                if pathway == 'Apprenticeship':
                    # Earning during apprenticeship
                    yearly_salary = abs(cost_data['tuition'])  # Convert negative to positive
                    total_earnings += yearly_salary
                else:
                    # Not earning, just costs
                    yearly_salary = 0
            else:
                # Working after graduation
                years_working = year - duration_years
                yearly_salary = starting_salary * ((1 + growth_rate) ** (years_working - 1))
                total_earnings += yearly_salary
            
            if year == 5:
                year_5_salary = yearly_salary if yearly_salary > 0 else starting_salary
        
        # Calculate opportunity cost (income lost during education)
        opportunity_cost = 0
        if current_income > 0 and duration_years > 0:
            if pathway != 'Apprenticeship':  # Apprenticeship doesn't have opportunity cost
                opportunity_cost = current_income * duration_years
        
        # Calculate net wealth after 5 years
        total_cost = max(total_education_cost, 0) + opportunity_cost
        net_wealth_year_5 = total_earnings - total_cost
        
        # Calculate ROI multiple
        if total_cost > 0:
            roi_multiple = total_earnings / total_cost
        else:
            roi_multiple = float('inf') if total_earnings > 0 else 0
        
        # Cap ROI multiple for display
        roi_multiple = min(roi_multiple, 99.99)
        
        return {
            'total_cost': round(total_cost, 0),
            'year_5_salary': round(year_5_salary, 0),
            'net_wealth_year_5': round(net_wealth_year_5, 0),
            'roi_multiple': round(roi_multiple, 2),
            'total_earnings_5yr': round(total_earnings, 0),
            'education_duration': duration_years
        }
    
    def calculate_all_pathways(self, budget, current_income, field, country):
        """
        Calculate ROI for all four pathways
        
        Returns:
            Dict mapping pathway name to ROI metrics
        """
        pathways = [
            'International University',
            'Local University', 
            'Apprenticeship',
            'Micro-Credentials'
        ]
        
        results = {}
        for pathway in pathways:
            results[pathway] = self.calculate_pathway_roi(
                pathway, budget, current_income, field, country
            )
        
        return results
    
    def get_debt_warning_threshold(self, pathway_data):
        """
        Determine if pathway triggers debt warning
        Returns: (has_warning, warning_message)
        """
        net_wealth = pathway_data['net_wealth_year_5']
        roi_multiple = pathway_data['roi_multiple']
        
        if net_wealth < 0:
            return (True, f"You will be ${abs(net_wealth):,.0f} in debt after 5 years")
        elif roi_multiple < 1.2:
            return (True, f"Low ROI: Only ${roi_multiple:.2f} earned per $1 invested")
        elif pathway_data['total_cost'] > pathway_data['total_earnings_5yr']:
            return (True, "Total cost exceeds 5-year earnings")
        else:
            return (False, "Financially viable pathway")
    
    def compare_pathways(self, roi_data):
        """
        Generate comparison summary
        Returns: Dict with best/worst pathways and recommendations
        """
        # Sort by net wealth
        sorted_pathways = sorted(
            roi_data.items(),
            key=lambda x: x[1]['net_wealth_year_5'],
            reverse=True
        )
        
        best_pathway = sorted_pathways[0]
        worst_pathway = sorted_pathways[-1]
        
        # Calculate delta
        wealth_delta = best_pathway[1]['net_wealth_year_5'] - worst_pathway[1]['net_wealth_year_5']
        
        return {
            'best_pathway': best_pathway[0],
            'best_net_wealth': best_pathway[1]['net_wealth_year_5'],
            'worst_pathway': worst_pathway[0],
            'worst_net_wealth': worst_pathway[1]['net_wealth_year_5'],
            'wealth_delta': wealth_delta,
            'recommendation': f"Choosing {best_pathway[0]} over {worst_pathway[0]} results in ${wealth_delta:,.0f} more wealth after 5 years"
        }
