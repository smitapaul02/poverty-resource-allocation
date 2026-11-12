"""
Visualization Module for Poverty-Aware Resource Allocation Model

This module creates comprehensive visualizations for poverty analysis,
model performance, and resource allocation insights.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

class PovertyVisualizationEngine:
    """
    Comprehensive visualization engine for poverty analysis and resource allocation
    """
    
    def __init__(self):
        """Initialize the visualization engine"""
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Color schemes
        self.poverty_colors = {
            'High': '#e74c3c',    # Red
            'Medium': '#f39c12',  # Orange  
            'Low': '#27ae60'      # Green
        }
        
        self.state_colors = plt.cm.Set3(np.linspace(0, 1, 20))
    
    def create_poverty_overview_dashboard(self, df: pd.DataFrame, output_dir: str):
        """
        Create comprehensive poverty overview dashboard
        
        Args:
            df: DataFrame with district data
            output_dir: Directory to save visualizations
        """
        print("=== Creating Poverty Overview Dashboard ===")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Poverty Distribution Overview
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Poverty Analysis Overview Dashboard', fontsize=20, fontweight='bold')
        
        # Poverty level distribution
        poverty_counts = df['Poverty_Level'].value_counts()
        colors = [self.poverty_colors[level] for level in poverty_counts.index]
        
        axes[0, 0].pie(poverty_counts.values, labels=poverty_counts.index, autopct='%1.1f%%',
                      colors=colors, startangle=90)
        axes[0, 0].set_title('Distribution of Poverty Levels', fontweight='bold')
        
        # Poverty score distribution
        axes[0, 1].hist(df['Poverty_Score'], bins=20, color='skyblue', alpha=0.7, edgecolor='black')
        axes[0, 1].set_xlabel('Poverty Score')
        axes[0, 1].set_ylabel('Number of Districts')
        axes[0, 1].set_title('Distribution of Poverty Scores', fontweight='bold')
        axes[0, 1].axvline(df['Poverty_Score'].mean(), color='red', linestyle='--', 
                          label=f'Mean: {df["Poverty_Score"].mean():.1f}')
        axes[0, 1].legend()
        
        # Key indicators by poverty level
        key_indicators = ['Literacy_Rate', 'Employment_Rate', 'Clean_Water_Access', 'Healthcare_Index']
        poverty_means = df.groupby('Poverty_Level')[key_indicators].mean()
        
        x_pos = np.arange(len(key_indicators))
        width = 0.25
        
        for i, level in enumerate(['High', 'Medium', 'Low']):
            if level in poverty_means.index:
                axes[1, 0].bar(x_pos + (i * width), poverty_means.loc[level], width, 
                              label=level, color=self.poverty_colors[level], alpha=0.8)
        
        axes[1, 0].set_xlabel('Indicators')
        axes[1, 0].set_ylabel('Average Value')
        axes[1, 0].set_title('Key Indicators by Poverty Level', fontweight='bold')
        axes[1, 0].set_xticks(x_pos + width)
        axes[1, 0].set_xticklabels(key_indicators, rotation=45)
        axes[1, 0].legend()
        
        # State-wise poverty distribution
        if 'State' in df.columns:
            state_poverty = df.groupby(['State', 'Poverty_Level']).size().unstack(fill_value=0)
            state_poverty_pct = state_poverty.div(state_poverty.sum(axis=1), axis=0) * 100
            
            # Select top 10 states by total districts
            top_states = df['State'].value_counts().head(10).index
            state_poverty_pct_top = state_poverty_pct.loc[top_states]
            
            state_poverty_pct_top.plot(kind='bar', stacked=True, ax=axes[1, 1], 
                                     color=[self.poverty_colors[col] for col in state_poverty_pct_top.columns])
            axes[1, 1].set_xlabel('State')
            axes[1, 1].set_ylabel('Percentage of Districts')
            axes[1, 1].set_title('Poverty Distribution by State (Top 10)', fontweight='bold')
            axes[1, 1].legend(title='Poverty Level')
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'poverty_overview_dashboard.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Poverty overview dashboard created")
    
    def create_correlation_analysis(self, df: pd.DataFrame, output_dir: str):
        """
        Create correlation analysis visualizations
        
        Args:
            df: DataFrame with district data
            output_dir: Directory to save visualizations
        """
        print("=== Creating Correlation Analysis ===")
        
        # Select numerical columns for correlation
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        numerical_cols = [col for col in numerical_cols if col not in ['Poverty_Class']]
        
        # 1. Correlation Heatmap
        plt.figure(figsize=(14, 12))
        correlation_matrix = df[numerical_cols].corr()
        
        # Create mask for upper triangle
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='RdYlBu_r', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, fmt='.2f')
        plt.title('Feature Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'correlation_heatmap.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Poverty Score Correlation
        plt.figure(figsize=(12, 8))
        poverty_corr = df[numerical_cols].corrwith(df['Poverty_Score']).sort_values(ascending=False)
        
        colors = ['green' if x > 0 else 'red' for x in poverty_corr.values]
        bars = plt.barh(range(len(poverty_corr)), poverty_corr.values, color=colors, alpha=0.7)
        plt.yticks(range(len(poverty_corr)), poverty_corr.index)
        plt.xlabel('Correlation with Poverty Score', fontsize=12)
        plt.title('Feature Correlation with Poverty Score', fontsize=16, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, poverty_corr.values):
            plt.text(value + 0.01 if value > 0 else value - 0.01, bar.get_y() + bar.get_height()/2, 
                    f'{value:.2f}', ha='left' if value > 0 else 'right', va='center')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'poverty_score_correlation.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Correlation analysis created")
    
    def create_geographic_analysis(self, df: pd.DataFrame, output_dir: str):
        """
        Create geographic analysis visualizations
        
        Args:
            df: DataFrame with district data
            output_dir: Directory to save visualizations
        """
        print("=== Creating Geographic Analysis ===")
        
        if 'State' not in df.columns:
            print("State information not available for geographic analysis")
            return
        
        # 1. State-wise Statistics
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Geographic Analysis of Poverty Indicators', fontsize=20, fontweight='bold')
        
        # Average poverty score by state
        state_poverty = df.groupby('State')['Poverty_Score'].mean().sort_values()
        state_poverty.plot(kind='barh', ax=axes[0, 0], color='coral')
        axes[0, 0].set_title('Average Poverty Score by State', fontweight='bold')
        axes[0, 0].set_xlabel('Average Poverty Score')
        
        # Literacy rate by state
        state_literacy = df.groupby('State')['Literacy_Rate'].mean().sort_values(ascending=False)
        state_literacy.plot(kind='bar', ax=axes[0, 1], color='lightblue')
        axes[0, 1].set_title('Average Literacy Rate by State', fontweight='bold')
        axes[0, 1].set_ylabel('Literacy Rate (%)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Employment rate by state
        state_employment = df.groupby('State')['Employment_Rate'].mean().sort_values(ascending=False)
        state_employment.plot(kind='bar', ax=axes[1, 0], color='lightgreen')
        axes[1, 0].set_title('Average Employment Rate by State', fontweight='bold')
        axes[1, 0].set_ylabel('Employment Rate (%)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Infrastructure score by state
        if 'Infrastructure_Score' in df.columns:
            state_infra = df.groupby('State')['Infrastructure_Score'].mean().sort_values(ascending=False)
            state_infra.plot(kind='bar', ax=axes[1, 1], color='gold')
            axes[1, 1].set_title('Average Infrastructure Score by State', fontweight='bold')
            axes[1, 1].set_ylabel('Infrastructure Score')
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'geographic_analysis.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Regional Development Comparison
        plt.figure(figsize=(14, 8))
        
        # Create scatter plot of states
        state_summary = df.groupby('State').agg({
            'Poverty_Score': 'mean',
            'Literacy_Rate': 'mean',
            'Employment_Rate': 'mean',
            'Healthcare_Index': 'mean'
        }).reset_index()
        
        # Calculate overall development index
        state_summary['Development_Index'] = (
            state_summary['Literacy_Rate'] * 0.3 +
            state_summary['Employment_Rate'] * 0.3 +
            state_summary['Healthcare_Index'] * 0.4
        )
        
        scatter = plt.scatter(state_summary['Development_Index'], state_summary['Poverty_Score'], 
                            s=100, alpha=0.7, c=range(len(state_summary)), cmap='viridis')
        
        # Add state labels
        for i, state in enumerate(state_summary['State']):
            plt.annotate(state, (state_summary['Development_Index'].iloc[i], 
                               state_summary['Poverty_Score'].iloc[i]),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.xlabel('Development Index', fontsize=12)
        plt.ylabel('Poverty Score', fontsize=12)
        plt.title('State Development vs Poverty Score', fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'state_development_comparison.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Geographic analysis created")
    
    def create_feature_analysis(self, df: pd.DataFrame, output_dir: str):
        """
        Create detailed feature analysis visualizations
        
        Args:
            df: DataFrame with district data
            output_dir: Directory to save visualizations
        """
        print("=== Creating Feature Analysis ===")
        
        # 1. Distribution of key features by poverty level
        key_features = ['Literacy_Rate', 'Employment_Rate', 'Clean_Water_Access', 
                       'Electricity_Access', 'Healthcare_Index', 'Education_Index']
        
        available_features = [f for f in key_features if f in df.columns]
        
        if len(available_features) >= 4:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            axes = axes.flatten()
            fig.suptitle('Feature Distributions by Poverty Level', fontsize=20, fontweight='bold')
            
            for i, feature in enumerate(available_features[:4]):
                for level in ['High', 'Medium', 'Low']:
                    if level in df['Poverty_Level'].values:
                        data = df[df['Poverty_Level'] == level][feature]
                        axes[i].hist(data, alpha=0.6, label=level, bins=15, 
                                   color=self.poverty_colors[level])
                
                axes[i].set_xlabel(feature.replace('_', ' '))
                axes[i].set_ylabel('Frequency')
                axes[i].set_title(f'Distribution of {feature.replace("_", " ")}', fontweight='bold')
                axes[i].legend()
                axes[i].grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'feature_distributions.png'), 
                       dpi=300, bbox_inches='tight')
            plt.close()
        
        # 2. Box plots for key features
        plt.figure(figsize=(15, 10))
        
        # Create box plots for each feature by poverty level
        n_features = min(6, len(available_features))
        for i, feature in enumerate(available_features[:n_features]):
            plt.subplot(2, 3, i+1)
            
            # Prepare data for box plot
            box_data = []
            labels = []
            for level in ['High', 'Medium', 'Low']:
                if level in df['Poverty_Level'].values:
                    box_data.append(df[df['Poverty_Level'] == level][feature])
                    labels.append(level)
            
            box_plot = plt.boxplot(box_data, labels=labels, patch_artist=True)
            
            # Color the boxes
            for patch, label in zip(box_plot['boxes'], labels):
                patch.set_facecolor(self.poverty_colors[label])
                patch.set_alpha(0.7)
            
            plt.title(feature.replace('_', ' '), fontweight='bold')
            plt.ylabel('Value')
            plt.grid(True, alpha=0.3)
        
        plt.suptitle('Box Plots of Key Features by Poverty Level', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'feature_boxplots.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Feature analysis created")
    
    def create_interactive_dashboard(self, df: pd.DataFrame, output_dir: str):
        """
        Create interactive Plotly dashboard
        
        Args:
            df: DataFrame with district data
            output_dir: Directory to save visualizations
        """
        print("=== Creating Interactive Dashboard ===")
        
        # 1. Interactive Scatter Plot Matrix
        numerical_features = ['Literacy_Rate', 'Employment_Rate', 'Clean_Water_Access', 
                            'Healthcare_Index', 'Poverty_Score']
        available_features = [f for f in numerical_features if f in df.columns]
        
        if len(available_features) >= 3:
            fig = px.scatter_matrix(df, dimensions=available_features[:4], 
                                  color='Poverty_Level',
                                  color_discrete_map=self.poverty_colors,
                                  title='Interactive Feature Correlation Matrix')
            fig.update_layout(height=800, width=1000)
            fig.write_html(os.path.join(output_dir, 'interactive_scatter_matrix.html'))
        
        # 2. Interactive 3D Scatter Plot
        if all(col in df.columns for col in ['Literacy_Rate', 'Employment_Rate', 'Healthcare_Index']):
            fig = px.scatter_3d(df, x='Literacy_Rate', y='Employment_Rate', z='Healthcare_Index',
                              color='Poverty_Level', size='Poverty_Score',
                              hover_data=['District', 'State'] if 'State' in df.columns else ['District'],
                              color_discrete_map=self.poverty_colors,
                              title='3D Poverty Indicators Analysis')
            fig.update_layout(height=700)
            fig.write_html(os.path.join(output_dir, 'interactive_3d_scatter.html'))
        
        # 3. Interactive Bar Chart
        if 'State' in df.columns:
            state_summary = df.groupby(['State', 'Poverty_Level']).size().reset_index(name='Count')
            fig = px.bar(state_summary, x='State', y='Count', color='Poverty_Level',
                        color_discrete_map=self.poverty_colors,
                        title='Districts by State and Poverty Level')
            fig.update_layout(xaxis_tickangle=-45, height=600)
            fig.write_html(os.path.join(output_dir, 'interactive_state_analysis.html'))
        
        print("Interactive dashboard created")
    
    def create_allocation_visualizations(self, allocation_df: pd.DataFrame, output_dir: str):
        """
        Create resource allocation visualizations
        
        Args:
            allocation_df: DataFrame with allocation results
            output_dir: Directory to save visualizations
        """
        print("=== Creating Resource Allocation Visualizations ===")
        
        # 1. Allocation Summary Dashboard
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Resource Allocation Analysis Dashboard', fontsize=20, fontweight='bold')
        
        # Total allocation by poverty level
        poverty_allocation = allocation_df.groupby('Poverty_Level')['Allocated_Amount'].sum()
        colors = [self.poverty_colors[level] for level in poverty_allocation.index]
        
        axes[0, 0].pie(poverty_allocation.values, labels=poverty_allocation.index, 
                      autopct='%1.1f%%', colors=colors, startangle=90)
        axes[0, 0].set_title('Resource Allocation by Poverty Level', fontweight='bold')
        
        # Top 15 districts by allocation
        top_districts = allocation_df.nlargest(15, 'Allocated_Amount')
        bars = axes[0, 1].barh(range(len(top_districts)), top_districts['Allocated_Amount'] / 1e6)
        axes[0, 1].set_yticks(range(len(top_districts)))
        axes[0, 1].set_yticklabels(top_districts['District'])
        axes[0, 1].set_xlabel('Allocation (Million ₹)')
        axes[0, 1].set_title('Top 15 Districts by Allocation', fontweight='bold')
        
        # Color bars by poverty level
        for bar, poverty_level in zip(bars, top_districts['Poverty_Level']):
            bar.set_color(self.poverty_colors[poverty_level])
        
        # Allocation distribution
        axes[1, 0].hist(allocation_df['Allocated_Amount'] / 1e6, bins=20, 
                       color='skyblue', alpha=0.7, edgecolor='black')
        axes[1, 0].set_xlabel('Allocation (Million ₹)')
        axes[1, 0].set_ylabel('Number of Districts')
        axes[1, 0].set_title('Distribution of Allocations', fontweight='bold')
        
        # Average allocation by poverty level
        avg_allocation = allocation_df.groupby('Poverty_Level')['Allocated_Amount'].mean()
        bars = axes[1, 1].bar(avg_allocation.index, avg_allocation.values / 1e6,
                             color=[self.poverty_colors[level] for level in avg_allocation.index])
        axes[1, 1].set_ylabel('Average Allocation (Million ₹)')
        axes[1, 1].set_title('Average Allocation by Poverty Level', fontweight='bold')
        
        # Add value labels on bars
        for bar, value in zip(bars, avg_allocation.values):
            axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                           f'₹{value/1e6:.1f}M', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'allocation_dashboard.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. State-wise allocation analysis
        if 'State' in allocation_df.columns:
            plt.figure(figsize=(15, 8))
            state_allocation = allocation_df.groupby('State')['Allocated_Amount'].sum().sort_values(ascending=False)
            
            plt.bar(range(len(state_allocation)), state_allocation.values / 1e6, color='coral')
            plt.xticks(range(len(state_allocation)), state_allocation.index, rotation=45, ha='right')
            plt.ylabel('Total Allocation (Million ₹)')
            plt.title('State-wise Resource Allocation', fontsize=16, fontweight='bold')
            plt.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'state_allocation_analysis.png'), 
                       dpi=300, bbox_inches='tight')
            plt.close()
        
        print("Resource allocation visualizations created")
    
    def generate_summary_report(self, df: pd.DataFrame, allocation_df: Optional[pd.DataFrame], 
                              output_dir: str):
        """
        Generate a comprehensive summary report
        
        Args:
            df: Main dataset
            allocation_df: Allocation results (optional)
            output_dir: Directory to save the report
        """
        print("=== Generating Summary Report ===")
        
        report_path = os.path.join(output_dir, 'poverty_analysis_report.txt')
        
        with open(report_path, 'w') as f:
            f.write("POVERTY-AWARE RESOURCE ALLOCATION MODEL\n")
            f.write("="*50 + "\n\n")
            
            # Data Overview
            f.write("DATA OVERVIEW\n")
            f.write("-"*20 + "\n")
            f.write(f"Total Districts Analyzed: {len(df)}\n")
            f.write(f"States Covered: {df['State'].nunique() if 'State' in df.columns else 'N/A'}\n")
            f.write(f"Features Analyzed: {len(df.columns) - 3}\n\n")  # Excluding District, State, target
            
            # Poverty Distribution
            f.write("POVERTY LEVEL DISTRIBUTION\n")
            f.write("-"*30 + "\n")
            poverty_dist = df['Poverty_Level'].value_counts()
            for level, count in poverty_dist.items():
                pct = (count / len(df)) * 100
                f.write(f"{level} Poverty: {count} districts ({pct:.1f}%)\n")
            f.write("\n")
            
            # Key Statistics
            f.write("KEY STATISTICS\n")
            f.write("-"*20 + "\n")
            f.write(f"Average Poverty Score: {df['Poverty_Score'].mean():.2f}\n")
            f.write(f"Average Literacy Rate: {df['Literacy_Rate'].mean():.2f}%\n")
            f.write(f"Average Employment Rate: {df['Employment_Rate'].mean():.2f}%\n")
            f.write(f"Average Healthcare Index: {df['Healthcare_Index'].mean():.2f}\n\n")
            
            # Poverty Correlations
            f.write("TOP POVERTY CORRELATIONS\n")
            f.write("-"*30 + "\n")
            numerical_cols = df.select_dtypes(include=[np.number]).columns
            numerical_cols = [col for col in numerical_cols if col not in ['Poverty_Class', 'Poverty_Score']]
            correlations = df[numerical_cols].corrwith(df['Poverty_Score']).sort_values(ascending=False)
            
            for feature, corr in correlations.head(5).items():
                f.write(f"{feature}: {corr:.3f}\n")
            f.write("\n")
            
            # Resource Allocation Summary
            if allocation_df is not None:
                f.write("RESOURCE ALLOCATION SUMMARY\n")
                f.write("-"*35 + "\n")
                total_budget = allocation_df['Allocated_Amount'].sum()
                f.write(f"Total Budget Allocated: ₹{total_budget:,.0f}\n")
                f.write(f"Average per District: ₹{allocation_df['Allocated_Amount'].mean():,.0f}\n")
                
                poverty_allocation = allocation_df.groupby('Poverty_Level')['Allocated_Amount'].sum()
                for level, amount in poverty_allocation.items():
                    pct = (amount / total_budget) * 100
                    f.write(f"{level} Poverty Regions: ₹{amount:,.0f} ({pct:.1f}%)\n")
                f.write("\n")
            
            # Recommendations
            f.write("KEY RECOMMENDATIONS\n")
            f.write("-"*25 + "\n")
            f.write("1. Focus on improving literacy rates in high poverty districts\n")
            f.write("2. Invest in healthcare infrastructure for maximum impact\n")
            f.write("3. Prioritize employment generation programs\n")
            f.write("4. Enhance access to clean water and electricity\n")
            f.write("5. Implement targeted interventions based on regional needs\n\n")
            
            f.write("Report generated by Poverty-Aware Resource Allocation Model\n")
            f.write(f"Analysis Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"Summary report saved to: {report_path}")

def main():
    """Main visualization pipeline"""
    print("=== Poverty-Aware Resource Allocation: Visualization Generation ===")
    
    # Initialize visualization engine
    viz_engine = PovertyVisualizationEngine()
    
    # File paths
    data_path = "/Users/smitapaul/Machine Learning/poverty-resource-allocation/data/processed/processed_districts_data.csv"
    allocation_path = "/Users/smitapaul/Machine Learning/poverty-resource-allocation/data/allocation_results.csv"
    output_dir = "/Users/smitapaul/Machine Learning/poverty-resource-allocation/visualizations"
    
    # Load data
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        print(f"Loaded {len(df)} districts for visualization")
        
        # Create all visualizations
        viz_engine.create_poverty_overview_dashboard(df, output_dir)
        viz_engine.create_correlation_analysis(df, output_dir)
        viz_engine.create_geographic_analysis(df, output_dir)
        viz_engine.create_feature_analysis(df, output_dir)
        viz_engine.create_interactive_dashboard(df, output_dir)
        
        # Load allocation results if available
        allocation_df = None
        if os.path.exists(allocation_path):
            allocation_df = pd.read_csv(allocation_path)
            viz_engine.create_allocation_visualizations(allocation_df, output_dir)
        
        # Generate summary report
        viz_engine.generate_summary_report(df, allocation_df, output_dir)
        
        print(f"\nAll visualizations saved to: {output_dir}")
        print("Visualization generation completed successfully!")
        
    else:
        print(f"Data file not found: {data_path}")
        print("Please run data preprocessing first.")

if __name__ == "__main__":
    main()
