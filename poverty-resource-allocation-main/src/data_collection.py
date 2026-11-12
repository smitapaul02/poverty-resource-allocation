"""
Data Collection Module for Poverty-Aware Resource Allocation Model

This module generates synthetic district-level data based on real Indian socio-economic patterns.
In a production environment, this would connect to APIs from Census of India, World Bank, etc.
"""

import pandas as pd
import numpy as np
import random
from typing import List, Tuple
import os

class IndianDistrictDataGenerator:
    """
    Generates realistic synthetic data for Indian districts based on actual patterns
    """
    
    def __init__(self, seed: int = 42):
        """Initialize the data generator with a random seed for reproducibility"""
        np.random.seed(seed)
        random.seed(seed)
        
        # Real Indian district names (sample from different states)
        self.district_names = [
            # Uttar Pradesh
            "Agra", "Lucknow", "Kanpur", "Varanasi", "Allahabad", "Meerut", "Bareilly", "Aligarh",
            # Maharashtra
            "Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur", "Amravati", "Kolhapur",
            # Bihar
            "Patna", "Gaya", "Bhagalpur", "Darbhanga", "Muzaffarpur", "Purnia", "Araria", "Begusarai",
            # West Bengal
            "Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Malda", "Bardhaman", "Kharagpur",
            # Tamil Nadu
            "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Erode", "Vellore",
            # Karnataka
            "Bangalore", "Mysore", "Hubli", "Dharwad", "Mangalore", "Belgaum", "Gulbarga", "Davanagere",
            # Gujarat
            "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Gandhinagar", "Anand",
            # Rajasthan
            "Jaipur", "Jodhpur", "Udaipur", "Kota", "Bikaner", "Ajmer", "Bharatpur", "Alwar",
            # Madhya Pradesh
            "Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain", "Sagar", "Dewas", "Satna",
            # Andhra Pradesh
            "Hyderabad", "Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Rajahmundry", "Tirupati",
            # Assam
            "Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Tinsukia", "Tezpur", "Bongaigaon",
            # Punjab
            "Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Mohali", "Hoshiarpur", "Batala",
            # Haryana
            "Faridabad", "Gurgaon", "Panipat", "Ambala", "Yamunanagar", "Rohtak", "Hisar", "Karnal",
            # Kerala
            "Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Palakkad", "Alappuzha", "Malappuram",
            # Odisha
            "Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur", "Puri", "Balasore", "Baripada"
        ]
        
        # State mappings for regional variations
        self.state_mapping = {
            # Developed states (higher indices)
            "Mumbai": "Maharashtra", "Pune": "Maharashtra", "Bangalore": "Karnataka", 
            "Chennai": "Tamil Nadu", "Hyderabad": "Andhra Pradesh", "Ahmedabad": "Gujarat",
            "Surat": "Gujarat", "Kochi": "Kerala", "Thiruvananthapuram": "Kerala",
            
            # Moderately developed states
            "Jaipur": "Rajasthan", "Bhopal": "Madhya Pradesh", "Lucknow": "Uttar Pradesh",
            "Kolkata": "West Bengal", "Guwahati": "Assam", "Ludhiana": "Punjab",
            
            # Less developed regions
            "Patna": "Bihar", "Gaya": "Bihar", "Bhagalpur": "Bihar", "Darbhanga": "Bihar"
        }
    
    def generate_district_data(self, num_districts: int = 100) -> pd.DataFrame:
        """
        Generate synthetic district-level socio-economic data
        
        Args:
            num_districts: Number of districts to generate data for
            
        Returns:
            pandas.DataFrame: Generated district data with poverty indicators
        """
        print(f"Generating synthetic data for {num_districts} Indian districts...")
        
        # Select districts (repeat if needed)
        districts = (self.district_names * ((num_districts // len(self.district_names)) + 1))[:num_districts]
        
        data = []
        
        for i, district in enumerate(districts):
            # Get state for regional variation
            state = self.state_mapping.get(district, "Other")
            
            # Base development level (affects all indicators)
            if state in ["Maharashtra", "Karnataka", "Tamil Nadu", "Gujarat", "Kerala"]:
                base_development = np.random.normal(0.7, 0.1)  # Higher development
            elif state in ["Rajasthan", "Madhya Pradesh", "Uttar Pradesh", "West Bengal", "Punjab"]:
                base_development = np.random.normal(0.5, 0.1)  # Medium development
            else:
                base_development = np.random.normal(0.3, 0.1)  # Lower development
            
            base_development = np.clip(base_development, 0.1, 0.9)
            
            # Generate correlated features based on development level
            literacy_rate = self._generate_correlated_feature(base_development, 40, 95, 0.8)
            female_literacy_rate = literacy_rate * np.random.uniform(0.7, 0.95)  # Generally lower than overall
            
            employment_rate = self._generate_correlated_feature(base_development, 30, 80, 0.7)
            clean_water_access = self._generate_correlated_feature(base_development, 20, 95, 0.75)
            electricity_access = self._generate_correlated_feature(base_development, 25, 98, 0.8)
            
            # Healthcare and education indices (0-100 scale)
            healthcare_index = self._generate_correlated_feature(base_development, 20, 90, 0.7) 
            education_index = self._generate_correlated_feature(base_development, 25, 95, 0.8)
            
            # Household size (inversely correlated with development)
            household_size = 8 - (base_development * 3) + np.random.normal(0, 0.5)
            household_size = np.clip(household_size, 2.5, 8.0)
            
            # Urban/Rural ratio
            urban_population_pct = self._generate_correlated_feature(base_development, 10, 85, 0.6)
            
            # Additional poverty proxies
            toilet_access = self._generate_correlated_feature(base_development, 15, 90, 0.7)
            bank_account_access = self._generate_correlated_feature(base_development, 25, 95, 0.75)
            internet_access = self._generate_correlated_feature(base_development, 5, 80, 0.8)
            
            # Create poverty score based on multiple indicators (for supervised learning)
            poverty_score = self._calculate_poverty_score(
                literacy_rate, employment_rate, clean_water_access, 
                electricity_access, healthcare_index, education_index,
                household_size, toilet_access, bank_account_access
            )
            
            # Classify poverty level with balanced distribution
            if poverty_score >= 65:
                poverty_level = "Low"
                poverty_class = 2
            elif poverty_score >= 35:
                poverty_level = "Medium" 
                poverty_class = 1
            else:
                poverty_level = "High"
                poverty_class = 0
            
            data.append({
                'District': district,
                'State': state,
                'Literacy_Rate': round(literacy_rate, 2),
                'Female_Literacy_Rate': round(female_literacy_rate, 2),
                'Employment_Rate': round(employment_rate, 2),
                'Clean_Water_Access': round(clean_water_access, 2),
                'Electricity_Access': round(electricity_access, 2),
                'Healthcare_Index': round(healthcare_index, 2),
                'Education_Index': round(education_index, 2),
                'Household_Size': round(household_size, 2),
                'Urban_Population_Pct': round(urban_population_pct, 2),
                'Toilet_Access': round(toilet_access, 2),
                'Bank_Account_Access': round(bank_account_access, 2),
                'Internet_Access': round(internet_access, 2),
                'Poverty_Score': round(poverty_score, 2),
                'Poverty_Level': poverty_level,
                'Poverty_Class': poverty_class
            })
        
        df = pd.DataFrame(data)
        print(f"Generated data for {len(df)} districts")
        print(f"Poverty distribution: {df['Poverty_Level'].value_counts().to_dict()}")
        
        return df
    
    def _generate_correlated_feature(self, base_value: float, min_val: float, 
                                   max_val: float, correlation: float) -> float:
        """Generate a feature correlated with base development level"""
        # Scale base_value to the target range
        target_mean = min_val + (max_val - min_val) * base_value
        
        # Add some noise while maintaining correlation
        noise_std = (max_val - min_val) * (1 - correlation) * 0.2
        value = np.random.normal(target_mean, noise_std)
        
        return np.clip(value, min_val, max_val)
    
    def _calculate_poverty_score(self, literacy: float, employment: float, 
                               water: float, electricity: float, healthcare: float,
                               education: float, household_size: float, 
                               toilet: float, bank: float) -> float:
        """
        Calculate poverty score based on multiple indicators
        Higher score = Lower poverty
        """
        # Normalize household size (smaller = better)
        normalized_household = (8 - household_size) / 5.5 * 100
        
        # Weighted average of all positive indicators
        weights = {
            'literacy': 0.15,
            'employment': 0.15, 
            'water': 0.1,
            'electricity': 0.1,
            'healthcare': 0.15,
            'education': 0.15,
            'household': 0.1,
            'toilet': 0.05,
            'bank': 0.05
        }
        
        score = (weights['literacy'] * literacy +
                weights['employment'] * employment +
                weights['water'] * water +
                weights['electricity'] * electricity +
                weights['healthcare'] * healthcare +
                weights['education'] * education +
                weights['household'] * normalized_household +
                weights['toilet'] * toilet +
                weights['bank'] * bank)
        
        return np.clip(score, 0, 100)

def collect_and_save_data():
    """Main function to generate and save district data"""
    print("=== Poverty-Aware Resource Allocation: Data Collection ===")
    
    # Create data directories
    raw_data_dir = "/Users/smitapaul/Machine Learning/poverty-resource-allocation/data/raw"
    os.makedirs(raw_data_dir, exist_ok=True)
    
    # Generate district data
    generator = IndianDistrictDataGenerator()
    district_data = generator.generate_district_data(num_districts=5000)
    
    # Save raw data
    raw_file_path = os.path.join(raw_data_dir, "indian_districts_socioeconomic.csv")
    district_data.to_csv(raw_file_path, index=False)
    print(f"\nRaw data saved to: {raw_file_path}")
    
    # Display summary statistics
    print("\n=== Data Summary ===")
    print(f"Total districts: {len(district_data)}")
    print(f"Features: {len(district_data.columns)}")
    print("\nPoverty Level Distribution:")
    print(district_data['Poverty_Level'].value_counts())
    
    print("\nSample data (first 5 rows):")
    print(district_data.head())
    
    print("\nData collection completed successfully!")
    return district_data

if __name__ == "__main__":
    collect_and_save_data()
