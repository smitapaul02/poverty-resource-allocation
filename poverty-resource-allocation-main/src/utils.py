"""
Utility Functions for Poverty-Aware Resource Allocation Model

This module contains helper functions, data validation utilities,
and common operations used across the project.
"""

import pandas as pd
import numpy as np
import os
import joblib
import json
from typing import Dict, List, Tuple, Any, Optional
import warnings
warnings.filterwarnings('ignore')

class DataValidator:
    """
    Data validation utilities for ensuring data quality and consistency
    """
    
    @staticmethod
    def validate_district_data(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate district-level data for completeness and consistency
        
        Args:
            df: DataFrame to validate
            
        Returns:
            dict: Validation results
        """
        results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'summary': {}
        }
        
        # Check required columns
        required_columns = ['District', 'Literacy_Rate', 'Employment_Rate', 
                          'Clean_Water_Access', 'Electricity_Access']
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            results['errors'].append(f"Missing required columns: {missing_columns}")
            results['is_valid'] = False
        
        # Check data types
        numeric_columns = ['Literacy_Rate', 'Employment_Rate', 'Clean_Water_Access', 
                          'Electricity_Access', 'Healthcare_Index', 'Education_Index']
        
        for col in numeric_columns:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                results['errors'].append(f"Column {col} should be numeric")
                results['is_valid'] = False
        
        # Check value ranges
        percentage_columns = ['Literacy_Rate', 'Employment_Rate', 'Clean_Water_Access', 
                            'Electricity_Access', 'Urban_Population_Pct']
        
        for col in percentage_columns:
            if col in df.columns:
                if df[col].min() < 0 or df[col].max() > 100:
                    results['warnings'].append(f"Column {col} has values outside 0-100 range")
        
        # Check for missing values
        missing_values = df.isnull().sum()
        if missing_values.any():
            results['warnings'].append(f"Missing values found: {missing_values[missing_values > 0].to_dict()}")
        
        # Check for duplicates
        if df['District'].duplicated().any():
            results['errors'].append("Duplicate district names found")
            results['is_valid'] = False
        
        # Summary statistics
        results['summary'] = {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'missing_values_total': missing_values.sum(),
            'duplicate_districts': df['District'].duplicated().sum()
        }
        
        return results
    
    @staticmethod
    def validate_prediction_data(df: pd.DataFrame, required_features: List[str]) -> Dict[str, Any]:
        """
        Validate data for prediction
        
        Args:
            df: DataFrame to validate
            required_features: List of required feature columns
            
        Returns:
            dict: Validation results
        """
        results = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required features
        missing_features = [feat for feat in required_features if feat not in df.columns]
        if missing_features:
            results['errors'].append(f"Missing required features: {missing_features}")
            results['is_valid'] = False
        
        # Check for missing values in required features
        for feat in required_features:
            if feat in df.columns and df[feat].isnull().any():
                results['warnings'].append(f"Missing values in feature: {feat}")
        
        # Check data types
        for feat in required_features:
            if feat in df.columns and not pd.api.types.is_numeric_dtype(df[feat]):
                results['errors'].append(f"Feature {feat} should be numeric")
                results['is_valid'] = False
        
        return results

class ModelUtils:
    """
    Utility functions for model operations
    """
    
    @staticmethod
    def save_model_with_metadata(model: Any, model_path: str, metadata: Dict[str, Any]):
        """
        Save model with associated metadata
        
        Args:
            model: Trained model object
            model_path: Path to save the model
            metadata: Dictionary containing model metadata
        """
        # Save model
        joblib.dump(model, model_path)
        
        # Save metadata
        metadata_path = model_path.replace('.pkl', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Model saved to: {model_path}")
        print(f"Metadata saved to: {metadata_path}")
    
    @staticmethod
    def load_model_with_metadata(model_path: str) -> Tuple[Any, Dict[str, Any]]:
        """
        Load model with associated metadata
        
        Args:
            model_path: Path to the saved model
            
        Returns:
            tuple: (model, metadata)
        """
        # Load model
        model = joblib.load(model_path)
        
        # Load metadata
        metadata_path = model_path.replace('.pkl', '_metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {}
        
        return model, metadata
    
    @staticmethod
    def calculate_prediction_confidence(prediction_probs: np.ndarray) -> np.ndarray:
        """
        Calculate confidence scores for predictions
        
        Args:
            prediction_probs: Prediction probabilities from model
            
        Returns:
            numpy.ndarray: Confidence scores
        """
        # Confidence is the maximum probability
        confidence_scores = np.max(prediction_probs, axis=1)
        return confidence_scores
    
    @staticmethod
    def interpret_predictions(predictions: np.ndarray, prediction_probs: np.ndarray) -> pd.DataFrame:
        """
        Create interpretable prediction results
        
        Args:
            predictions: Predicted classes
            prediction_probs: Prediction probabilities
            
        Returns:
            pandas.DataFrame: Interpreted results
        """
        poverty_mapping = {0: 'High', 1: 'Medium', 2: 'Low'}
        
        results = pd.DataFrame({
            'Predicted_Class': predictions,
            'Predicted_Level': [poverty_mapping[pred] for pred in predictions],
            'Confidence': ModelUtils.calculate_prediction_confidence(prediction_probs),
            'High_Poverty_Prob': prediction_probs[:, 0],
            'Medium_Poverty_Prob': prediction_probs[:, 1],
            'Low_Poverty_Prob': prediction_probs[:, 2]
        })
        
        return results

class DataProcessor:
    """
    Data processing utilities
    """
    
    @staticmethod
    def create_poverty_bins(scores: pd.Series, method: str = 'quantile') -> pd.Series:
        """
        Create poverty level bins from continuous scores
        
        Args:
            scores: Poverty scores
            method: Binning method ('quantile', 'equal', 'custom')
            
        Returns:
            pandas.Series: Binned poverty levels
        """
        if method == 'quantile':
            # Equal frequency bins
            bins = pd.qcut(scores, q=3, labels=['High', 'Medium', 'Low'])
        elif method == 'equal':
            # Equal width bins
            bins = pd.cut(scores, bins=3, labels=['High', 'Medium', 'Low'])
        elif method == 'custom':
            # Custom thresholds based on domain knowledge
            bins = pd.cut(scores, bins=[0, 40, 70, 100], labels=['High', 'Medium', 'Low'])
        else:
            raise ValueError("Method must be 'quantile', 'equal', or 'custom'")
        
        return bins
    
    @staticmethod
    def normalize_features(df: pd.DataFrame, features: List[str], 
                          method: str = 'minmax') -> pd.DataFrame:
        """
        Normalize specified features
        
        Args:
            df: Input dataframe
            features: List of features to normalize
            method: Normalization method ('minmax', 'zscore')
            
        Returns:
            pandas.DataFrame: DataFrame with normalized features
        """
        df_normalized = df.copy()
        
        for feature in features:
            if feature in df.columns:
                if method == 'minmax':
                    # Min-Max normalization
                    min_val = df[feature].min()
                    max_val = df[feature].max()
                    df_normalized[feature] = (df[feature] - min_val) / (max_val - min_val)
                elif method == 'zscore':
                    # Z-score normalization
                    mean_val = df[feature].mean()
                    std_val = df[feature].std()
                    df_normalized[feature] = (df[feature] - mean_val) / std_val
                else:
                    raise ValueError("Method must be 'minmax' or 'zscore'")
        
        return df_normalized
    
    @staticmethod
    def handle_outliers(df: pd.DataFrame, columns: List[str], 
                       method: str = 'iqr', factor: float = 1.5) -> pd.DataFrame:
        """
        Handle outliers in specified columns
        
        Args:
            df: Input dataframe
            columns: Columns to process
            method: Outlier detection method ('iqr', 'zscore')
            factor: Outlier threshold factor
            
        Returns:
            pandas.DataFrame: DataFrame with outliers handled
        """
        df_clean = df.copy()
        
        for col in columns:
            if col in df.columns:
                if method == 'iqr':
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - factor * IQR
                    upper_bound = Q3 + factor * IQR
                    df_clean[col] = np.clip(df[col], lower_bound, upper_bound)
                elif method == 'zscore':
                    mean_val = df[col].mean()
                    std_val = df[col].std()
                    threshold = factor * std_val
                    df_clean[col] = np.clip(df[col], 
                                          mean_val - threshold, 
                                          mean_val + threshold)
        
        return df_clean

class ReportGenerator:
    """
    Utilities for generating reports and summaries
    """
    
    @staticmethod
    def generate_data_profile(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive data profile
        
        Args:
            df: DataFrame to profile
            
        Returns:
            dict: Data profile summary
        """
        profile = {
            'basic_info': {
                'rows': len(df),
                'columns': len(df.columns),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
            },
            'missing_values': df.isnull().sum().to_dict(),
            'data_types': df.dtypes.astype(str).to_dict(),
            'numerical_summary': {},
            'categorical_summary': {}
        }
        
        # Numerical columns summary
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            profile['numerical_summary'][col] = {
                'mean': float(df[col].mean()),
                'median': float(df[col].median()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'unique_values': int(df[col].nunique())
            }
        
        # Categorical columns summary
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            profile['categorical_summary'][col] = {
                'unique_values': int(df[col].nunique()),
                'mode': str(df[col].mode().iloc[0]) if len(df[col].mode()) > 0 else None,
                'value_counts': df[col].value_counts().head().to_dict()
            }
        
        return profile
    
    @staticmethod
    def create_model_comparison_report(model_metrics: Dict[str, Dict]) -> str:
        """
        Create a formatted model comparison report
        
        Args:
            model_metrics: Dictionary of model metrics
            
        Returns:
            str: Formatted report
        """
        report = "MODEL PERFORMANCE COMPARISON REPORT\n"
        report += "=" * 50 + "\n\n"
        
        # Overall comparison
        report += "ACCURACY COMPARISON\n"
        report += "-" * 20 + "\n"
        
        for model_name, metrics in model_metrics.items():
            accuracy = metrics['accuracy']
            report += f"{model_name}: {accuracy:.4f}\n"
        
        report += "\n"
        
        # Detailed metrics for each model
        for model_name, metrics in model_metrics.items():
            report += f"\n{model_name.upper()} DETAILED METRICS\n"
            report += "-" * (len(model_name) + 20) + "\n"
            
            class_report = metrics['classification_report']
            
            # Extract metrics for each class
            for class_label in ['0', '1', '2']:  # High, Medium, Low poverty
                if class_label in class_report:
                    class_metrics = class_report[class_label]
                    poverty_level = ['High', 'Medium', 'Low'][int(class_label)]
                    report += f"\n{poverty_level} Poverty:\n"
                    report += f"  Precision: {class_metrics['precision']:.3f}\n"
                    report += f"  Recall: {class_metrics['recall']:.3f}\n"
                    report += f"  F1-Score: {class_metrics['f1-score']:.3f}\n"
            
            # Overall metrics
            if 'macro avg' in class_report:
                macro_avg = class_report['macro avg']
                report += f"\nOverall Performance:\n"
                report += f"  Macro Precision: {macro_avg['precision']:.3f}\n"
                report += f"  Macro Recall: {macro_avg['recall']:.3f}\n"
                report += f"  Macro F1-Score: {macro_avg['f1-score']:.3f}\n"
        
        return report

class ConfigManager:
    """
    Configuration management utilities
    """
    
    @staticmethod
    def create_default_config() -> Dict[str, Any]:
        """
        Create default configuration for the project
        
        Returns:
            dict: Default configuration
        """
        config = {
            'data_collection': {
                'num_districts': 100,
                'random_seed': 42,
                'include_states': True
            },
            'preprocessing': {
                'handle_missing_values': True,
                'normalize_features': True,
                'remove_outliers': True,
                'test_size': 0.2
            },
            'model_training': {
                'algorithms': ['RandomForest', 'XGBoost'],
                'optimize_hyperparameters': False,
                'cross_validation_folds': 5,
                'random_state': 42
            },
            'resource_allocation': {
                'default_strategy': {
                    'High': 0.50,
                    'Medium': 0.30,
                    'Low': 0.20
                },
                'total_budget': 5000000000,  # 5 billion
                'allocation_method': 'weighted'
            },
            'visualization': {
                'create_interactive': True,
                'save_high_resolution': True,
                'color_scheme': 'default'
            }
        }
        
        return config
    
    @staticmethod
    def save_config(config: Dict[str, Any], config_path: str):
        """
        Save configuration to file
        
        Args:
            config: Configuration dictionary
            config_path: Path to save configuration
        """
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Configuration saved to: {config_path}")
    
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """
        Load configuration from file
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            dict: Configuration dictionary
        """
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        return config

def setup_project_directories(base_path: str) -> Dict[str, str]:
    """
    Set up project directory structure
    
    Args:
        base_path: Base project path
        
    Returns:
        dict: Dictionary mapping directory names to paths
    """
    directories = {
        'data_raw': os.path.join(base_path, 'data', 'raw'),
        'data_processed': os.path.join(base_path, 'data', 'processed'),
        'data_sample': os.path.join(base_path, 'data', 'sample'),
        'models': os.path.join(base_path, 'models'),
        'visualizations': os.path.join(base_path, 'visualizations'),
        'reports': os.path.join(base_path, 'reports'),
        'logs': os.path.join(base_path, 'logs')
    }
    
    # Create directories
    for name, path in directories.items():
        os.makedirs(path, exist_ok=True)
        print(f"Created directory: {path}")
    
    return directories

def main():
    """Demonstrate utility functions"""
    print("=== Poverty-Aware Resource Allocation: Utility Functions Demo ===")
    
    # Create default configuration
    config_manager = ConfigManager()
    default_config = config_manager.create_default_config()
    
    config_path = "/Users/smitapaul/Machine Learning/poverty-resource-allocation/config.json"
    config_manager.save_config(default_config, config_path)
    
    # Setup project directories
    base_path = "/Users/smitapaul/Machine Learning/poverty-resource-allocation"
    directories = setup_project_directories(base_path)
    
    print("\nUtility functions demonstration completed!")
    print(f"Configuration saved to: {config_path}")
    print(f"Project directories set up at: {base_path}")

if __name__ == "__main__":
    main()
