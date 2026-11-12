"""
Resource Allocation Module for Poverty-Aware Resource Allocation Model

This module implements logic for distributing aid/resources based on predicted poverty levels
and provides optimization strategies for maximum impact.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ResourceAllocationEngine:
    """
    Engine for calculating optimal resource allocation based on poverty predictions
    """
    
    def __init__(self):
        """Initialize the resource allocation engine"""
        # Default allocation strategy (can be customized)
        self.allocation_strategy = {
            'High': 0.50,    # 50% of resources to high poverty areas
            'Medium': 0.30,  # 30% of resources to medium poverty areas
            'Low': 0.20      # 20% of resources to low poverty areas
        }
        
        # Poverty class mapping
        self.poverty_mapping = {
            0: 'High',
            1: 'Medium', 
            2: 'Low'
        }
        
        self.allocation_results = None
    
    def set_allocation_strategy(self, strategy: Dict[str, float]):
        """
        Set custom allocation strategy
        
        Args:
            strategy: Dictionary mapping poverty levels to allocation percentages
        """
        # Validate strategy
        if not np.isclose(sum(strategy.values()), 1.0, rtol=1e-05):
            raise ValueError("Allocation percentages must sum to 1.0")
        
        for level in ['High', 'Medium', 'Low']:
            if level not in strategy:
                raise ValueError(f"Strategy must include allocation for '{level}' poverty level")
        
        self.allocation_strategy = strategy
        print(f"Updated allocation strategy: {strategy}")
    
    def calculate_basic_allocation(self, districts_df: pd.DataFrame, 
                                 total_budget: float = 1000000000) -> pd.DataFrame:
        """
        Calculate basic resource allocation based on poverty predictions
        
        Args:
            districts_df: DataFrame with districts and their poverty predictions
            total_budget: Total budget to allocate (default: 1 billion)
            
        Returns:
            pandas.DataFrame: Districts with allocated resources
        """
        print("=== Calculating Basic Resource Allocation ===")
        
        # Ensure we have required columns
        required_cols = ['District', 'Poverty_Class']
        for col in required_cols:
            if col not in districts_df.columns:
                raise ValueError(f"Required column '{col}' not found in data")
        
        # Create a copy for allocation
        allocation_df = districts_df.copy()
        
        # Map poverty classes to levels
        allocation_df['Poverty_Level'] = allocation_df['Poverty_Class'].map(self.poverty_mapping)
        
        # Count districts by poverty level
        poverty_counts = allocation_df['Poverty_Level'].value_counts()
        print(f"District distribution: {poverty_counts.to_dict()}")
        
        # Calculate allocation per district for each poverty level
        allocation_per_district = {}
        
        for level, percentage in self.allocation_strategy.items():
            budget_for_level = total_budget * percentage
            districts_in_level = poverty_counts.get(level, 0)
            
            if districts_in_level > 0:
                allocation_per_district[level] = budget_for_level / districts_in_level
            else:
                allocation_per_district[level] = 0
            
            print(f"{level} Poverty: {districts_in_level} districts, "
                  f"₹{budget_for_level:,.0f} total, "
                  f"₹{allocation_per_district[level]:,.0f} per district")
        
        # Assign allocations to districts
        allocation_df['Allocated_Amount'] = allocation_df['Poverty_Level'].map(allocation_per_district)
        allocation_df['Allocation_Percentage'] = allocation_df['Poverty_Level'].map(self.allocation_strategy)
        
        # Calculate allocation metrics
        total_allocated = allocation_df['Allocated_Amount'].sum()
        allocation_df['District_Share'] = (allocation_df['Allocated_Amount'] / total_allocated) * 100
        
        print(f"\nTotal Budget: ₹{total_budget:,.0f}")
        print(f"Total Allocated: ₹{total_allocated:,.0f}")
        print(f"Allocation Coverage: {(total_allocated/total_budget)*100:.1f}%")
        
        self.allocation_results = allocation_df
        
        return allocation_df
    
    def calculate_weighted_allocation(self, districts_df: pd.DataFrame, 
                                    total_budget: float = 1000000000,
                                    weight_factors: Dict[str, str] = None) -> pd.DataFrame:
        """
        Calculate weighted resource allocation considering additional factors
        
        Args:
            districts_df: DataFrame with districts and their features
            total_budget: Total budget to allocate
            weight_factors: Additional factors to consider for weighting
            
        Returns:
            pandas.DataFrame: Districts with weighted allocations
        """
        print("=== Calculating Weighted Resource Allocation ===")
        
        # Default weight factors
        if weight_factors is None:
            weight_factors = {
                'population_proxy': 'Household_Size',  # Proxy for population
                'infrastructure_need': 'Infrastructure_Score',  # Infrastructure deficit
                'development_deficit': 'Development_Index'  # Overall development gap
            }
        
        allocation_df = districts_df.copy()
        allocation_df['Poverty_Level'] = allocation_df['Poverty_Class'].map(self.poverty_mapping)
        
        # Calculate base weights for each district
        base_weights = []
        
        for _, row in allocation_df.iterrows():
            poverty_level = row['Poverty_Level']
            base_weight = self.allocation_strategy[poverty_level]
            
            # Apply weight factors
            weight_multiplier = 1.0
            
            # Population weight (higher household size = more people affected)
            if weight_factors['population_proxy'] in allocation_df.columns:
                pop_proxy = row[weight_factors['population_proxy']]
                # Normalize to 0.8-1.2 range
                pop_weight = 0.8 + (pop_proxy - allocation_df[weight_factors['population_proxy']].min()) / \
                           (allocation_df[weight_factors['population_proxy']].max() - 
                            allocation_df[weight_factors['population_proxy']].min()) * 0.4
                weight_multiplier *= pop_weight
            
            # Infrastructure need weight (lower score = higher need)
            if weight_factors['infrastructure_need'] in allocation_df.columns:
                infra_score = row[weight_factors['infrastructure_need']]
                # Invert score so lower infrastructure gets higher weight
                infra_weight = 1.5 - (infra_score / 100)  # Normalize to 0.5-1.5 range
                weight_multiplier *= infra_weight
            
            # Development deficit weight (lower development = higher allocation)
            if weight_factors['development_deficit'] in allocation_df.columns:
                dev_score = row[weight_factors['development_deficit']]
                # Invert score so lower development gets higher weight
                dev_weight = 1.3 - (dev_score / 100)  # Normalize to 0.3-1.3 range
                weight_multiplier *= dev_weight
            
            final_weight = base_weight * weight_multiplier
            base_weights.append(final_weight)
        
        allocation_df['Allocation_Weight'] = base_weights
        
        # Normalize weights to sum to 1
        total_weight = sum(base_weights)
        allocation_df['Normalized_Weight'] = allocation_df['Allocation_Weight'] / total_weight
        
        # Calculate final allocations
        allocation_df['Allocated_Amount'] = allocation_df['Normalized_Weight'] * total_budget
        allocation_df['District_Share'] = allocation_df['Normalized_Weight'] * 100
        
        # Add allocation category based on amount
        allocation_df['Allocation_Category'] = pd.cut(
            allocation_df['Allocated_Amount'], 
            bins=3, 
            labels=['Standard', 'Enhanced', 'Priority']
        )
        
        print(f"Weighted allocation completed")
        print(f"Total Budget: ₹{total_budget:,.0f}")
        print(f"Average allocation per district: ₹{allocation_df['Allocated_Amount'].mean():,.0f}")
        
        self.allocation_results = allocation_df
        
        return allocation_df
    
    def optimize_allocation_impact(self, districts_df: pd.DataFrame, 
                                 total_budget: float = 1000000000) -> pd.DataFrame:
        """
        Optimize allocation for maximum poverty reduction impact
        
        Args:
            districts_df: DataFrame with districts and their features
            total_budget: Total budget to allocate
            
        Returns:
            pandas.DataFrame: Optimized allocation results
        """
        print("=== Optimizing Allocation for Maximum Impact ===")
        
        allocation_df = districts_df.copy()
        allocation_df['Poverty_Level'] = allocation_df['Poverty_Class'].map(self.poverty_mapping)
        
        # Calculate impact potential for each district
        impact_scores = []
        
        for _, row in allocation_df.iterrows():
            # Factors that indicate high impact potential
            impact_score = 0
            
            # Base impact by poverty level (higher poverty = higher impact potential)
            poverty_impact = {'High': 1.0, 'Medium': 0.7, 'Low': 0.4}
            impact_score += poverty_impact[row['Poverty_Level']] * 40
            
            # Literacy gap impact (larger gap = higher impact potential for education investment)
            if 'Literacy_Gap' in allocation_df.columns:
                literacy_impact = row['Literacy_Gap'] * 0.5
                impact_score += literacy_impact
            
            # Infrastructure deficit impact
            if 'Infrastructure_Score' in allocation_df.columns:
                infra_impact = (100 - row['Infrastructure_Score']) * 0.3
                impact_score += infra_impact
            
            # Employment impact (lower employment = higher impact potential)
            if 'Employment_Rate' in allocation_df.columns:
                employ_impact = (100 - row['Employment_Rate']) * 0.2
                impact_score += employ_impact
            
            # Healthcare deficit impact
            if 'Healthcare_Index' in allocation_df.columns:
                health_impact = (100 - row['Healthcare_Index']) * 0.15
                impact_score += health_impact
            
            impact_scores.append(impact_score)
        
        allocation_df['Impact_Score'] = impact_scores
        
        # Normalize impact scores
        max_impact = max(impact_scores)
        allocation_df['Normalized_Impact'] = allocation_df['Impact_Score'] / max_impact
        
        # Allocate based on impact potential
        total_impact = allocation_df['Normalized_Impact'].sum()
        allocation_df['Impact_Weight'] = allocation_df['Normalized_Impact'] / total_impact
        allocation_df['Allocated_Amount'] = allocation_df['Impact_Weight'] * total_budget
        allocation_df['District_Share'] = allocation_df['Impact_Weight'] * 100
        
        # Calculate expected impact metrics
        allocation_df['Expected_Poverty_Reduction'] = (
            allocation_df['Normalized_Impact'] * 
            allocation_df['Impact_Weight'] * 100
        )
        
        print(f"Impact-optimized allocation completed")
        print(f"Top 5 highest impact districts:")
        top_impact = allocation_df.nlargest(5, 'Expected_Poverty_Reduction')[
            ['District', 'Poverty_Level', 'Allocated_Amount', 'Expected_Poverty_Reduction']
        ]
        print(top_impact.to_string(index=False))
        
        self.allocation_results = allocation_df
        
        return allocation_df
    
    def generate_allocation_summary(self) -> Dict:
        """
        Generate summary statistics for the allocation results
        
        Returns:
            dict: Summary statistics
        """
        if self.allocation_results is None:
            raise ValueError("No allocation results available. Run allocation calculation first.")
        
        df = self.allocation_results
        
        summary = {
            'total_districts': len(df),
            'total_budget': df['Allocated_Amount'].sum(),
            'average_allocation': df['Allocated_Amount'].mean(),
            'median_allocation': df['Allocated_Amount'].median(),
            'allocation_by_poverty_level': {},
            'top_allocated_districts': df.nlargest(5, 'Allocated_Amount')[['District', 'Allocated_Amount']].to_dict('records'),
            'allocation_distribution': {
                'std': df['Allocated_Amount'].std(),
                'min': df['Allocated_Amount'].min(),
                'max': df['Allocated_Amount'].max()
            }
        }
        
        # Allocation by poverty level
        for level in ['High', 'Medium', 'Low']:
            level_data = df[df['Poverty_Level'] == level]
            if len(level_data) > 0:
                summary['allocation_by_poverty_level'][level] = {
                    'districts': len(level_data),
                    'total_allocation': level_data['Allocated_Amount'].sum(),
                    'average_allocation': level_data['Allocated_Amount'].mean(),
                    'percentage_of_budget': (level_data['Allocated_Amount'].sum() / df['Allocated_Amount'].sum()) * 100
                }
        
        return summary
    
    def create_allocation_visualizations(self, output_dir: str):
        """
        Create visualizations for resource allocation results
        
        Args:
            output_dir: Directory to save visualizations
        """
        if self.allocation_results is None:
            raise ValueError("No allocation results available. Run allocation calculation first.")
        
        print("=== Creating Allocation Visualizations ===")
        
        os.makedirs(output_dir, exist_ok=True)
        df = self.allocation_results
        
        # 1. Allocation by Poverty Level (Pie Chart)
        plt.figure(figsize=(10, 8))
        poverty_allocation = df.groupby('Poverty_Level')['Allocated_Amount'].sum()
        
        colors = ['#ff6b6b', '#feca57', '#48cae4']  # Red, Yellow, Blue
        plt.pie(poverty_allocation.values, labels=poverty_allocation.index, autopct='%1.1f%%',
                startangle=90, colors=colors)
        plt.title('Resource Allocation by Poverty Level', fontsize=16, fontweight='bold')
        plt.axis('equal')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'allocation_by_poverty_level.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. District-wise Allocation (Top 20)
        plt.figure(figsize=(15, 10))
        top_districts = df.nlargest(20, 'Allocated_Amount')
        
        bars = plt.bar(range(len(top_districts)), top_districts['Allocated_Amount'] / 1e6)
        plt.xticks(range(len(top_districts)), top_districts['District'], rotation=45, ha='right')
        plt.ylabel('Allocation (Million ₹)', fontsize=12)
        plt.title('Top 20 Districts by Resource Allocation', fontsize=16, fontweight='bold')
        
        # Color bars by poverty level
        colors_map = {'High': '#ff6b6b', 'Medium': '#feca57', 'Low': '#48cae4'}
        for bar, poverty_level in zip(bars, top_districts['Poverty_Level']):
            bar.set_color(colors_map[poverty_level])
        
        # Add legend
        handles = [plt.Rectangle((0,0),1,1, color=colors_map[level]) for level in ['High', 'Medium', 'Low']]
        plt.legend(handles, ['High Poverty', 'Medium Poverty', 'Low Poverty'], loc='upper right')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'top_districts_allocation.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Allocation Distribution Histogram
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.hist(df['Allocated_Amount'] / 1e6, bins=20, color='skyblue', alpha=0.7, edgecolor='black')
        plt.xlabel('Allocation (Million ₹)', fontsize=12)
        plt.ylabel('Number of Districts', fontsize=12)
        plt.title('Distribution of Allocations', fontsize=14, fontweight='bold')
        
        plt.subplot(1, 2, 2)
        box_data = [df[df['Poverty_Level'] == level]['Allocated_Amount'] / 1e6 
                   for level in ['High', 'Medium', 'Low']]
        plt.boxplot(box_data, labels=['High', 'Medium', 'Low'])
        plt.ylabel('Allocation (Million ₹)', fontsize=12)
        plt.xlabel('Poverty Level', fontsize=12)
        plt.title('Allocation by Poverty Level', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'allocation_distribution.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. State-wise Allocation Summary (if State column exists)
        if 'State' in df.columns:
            plt.figure(figsize=(15, 8))
            state_allocation = df.groupby('State')['Allocated_Amount'].sum().sort_values(ascending=False)
            
            plt.bar(range(len(state_allocation)), state_allocation.values / 1e6)
            plt.xticks(range(len(state_allocation)), state_allocation.index, rotation=45, ha='right')
            plt.ylabel('Total Allocation (Million ₹)', fontsize=12)
            plt.title('State-wise Resource Allocation', fontsize=16, fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'state_wise_allocation.png'), dpi=300, bbox_inches='tight')
            plt.close()
        
        print(f"Allocation visualizations saved to: {output_dir}")
    
    def export_allocation_results(self, output_path: str):
        """
        Export allocation results to CSV
        
        Args:
            output_path: Path to save the results CSV
        """
        if self.allocation_results is None:
            raise ValueError("No allocation results available. Run allocation calculation first.")
        
        # Select relevant columns for export
        export_columns = ['District', 'State', 'Poverty_Level', 'Poverty_Class', 
                         'Allocated_Amount', 'District_Share']
        
        # Add optional columns if they exist
        optional_columns = ['Allocation_Weight', 'Normalized_Weight', 'Impact_Score', 
                           'Expected_Poverty_Reduction', 'Allocation_Category']
        
        for col in optional_columns:
            if col in self.allocation_results.columns:
                export_columns.append(col)
        
        export_df = self.allocation_results[export_columns].copy()
        
        # Format currency values
        export_df['Allocated_Amount_Formatted'] = export_df['Allocated_Amount'].apply(
            lambda x: f"₹{x:,.0f}"
        )
        
        export_df.to_csv(output_path, index=False)
        print(f"Allocation results exported to: {output_path}")

def main():
    """Main resource allocation pipeline"""
    print("=== Poverty-Aware Resource Allocation: Resource Distribution ===")
    
    # This would typically load results from the model prediction
    # For demo purposes, we'll create sample data
    
    # Initialize allocation engine
    allocator = ResourceAllocationEngine()
    
    # Load districts with predictions (this would come from model predictions)
    processed_data_path = "/Users/smitapaul/Machine Learning/poverty-resource-allocation/data/processed/processed_districts_data.csv"
    
    if os.path.exists(processed_data_path):
        districts_df = pd.read_csv(processed_data_path)
        print(f"Loaded {len(districts_df)} districts for allocation")
        
        # Run different allocation strategies
        
        # 1. Basic allocation
        print("\n1. Basic Allocation Strategy")
        basic_allocation = allocator.calculate_basic_allocation(districts_df, total_budget=5000000000)  # 5 billion
        
        # 2. Weighted allocation
        print("\n2. Weighted Allocation Strategy")
        weighted_allocation = allocator.calculate_weighted_allocation(districts_df, total_budget=5000000000)
        
        # 3. Impact-optimized allocation
        print("\n3. Impact-Optimized Allocation Strategy")
        impact_allocation = allocator.optimize_allocation_impact(districts_df, total_budget=5000000000)
        
        # Generate summary
        summary = allocator.generate_allocation_summary()
        print(f"\nAllocation Summary:")
        print(f"Total Districts: {summary['total_districts']}")
        print(f"Total Budget: ₹{summary['total_budget']:,.0f}")
        print(f"Average Allocation: ₹{summary['average_allocation']:,.0f}")
        
        # Create visualizations
        viz_dir = "/Users/smitapaul/Machine Learning/poverty-resource-allocation/visualizations"
        allocator.create_allocation_visualizations(viz_dir)
        
        # Export results
        results_path = "/Users/smitapaul/Machine Learning/poverty-resource-allocation/data/allocation_results.csv"
        allocator.export_allocation_results(results_path)
        
        print("\nResource allocation completed successfully!")
        
    else:
        print(f"Processed data not found at: {processed_data_path}")
        print("Please run data collection and preprocessing first.")

if __name__ == "__main__":
    main()
