"""
Data Preprocessing Module for Poverty-Aware Resource Allocation Model

This module handles data cleaning, feature engineering, and preprocessing
for the poverty prediction machine learning model.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import os
import json
import warnings
warnings.filterwarnings('ignore')

class PovertyDataPreprocessor:
    """
    Comprehensive data preprocessing pipeline for poverty prediction
    """
    
    def __init__(self):
        """Initialize preprocessor with scalers and encoders"""
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.imputer = SimpleImputer(strategy='median')
        self.feature_names = None
        self.is_fitted = False
    
    def load_raw_data(self, file_path: str) -> pd.DataFrame:
        """
        Load raw data from CSV file
        
        Args:
            file_path: Path to the raw data CSV file
            
        Returns:
            pandas.DataFrame: Raw data
        """
        print(f"Loading raw data from: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} records with {len(df.columns)} columns")
        
        return df
    
    def explore_data(self, df: pd.DataFrame) -> dict:
        """
        Perform exploratory data analysis
        
        Args:
            df: Input dataframe
            
        Returns:
            dict: Data exploration summary
        """
        print("\n=== Data Exploration ===")
        
        # Basic info
        print(f"Dataset shape: {df.shape}")
        print(f"Memory usage: {df.memory_usage().sum() / 1024:.2f} KB")
        
        # Missing values
        missing_values = df.isnull().sum()
        missing_pct = (missing_values / len(df)) * 100
        
        print("\nMissing Values:")
        for col in df.columns:
            if missing_values[col] > 0:
                print(f"  {col}: {missing_values[col]} ({missing_pct[col]:.1f}%)")
        
        # Data types
        print(f"\nData Types:")
        print(df.dtypes)
        
        # Summary statistics for numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        print(f"\nNumerical Features Summary:")
        print(df[numerical_cols].describe())
        
        # Categorical features
        categorical_cols = df.select_dtypes(include=['object']).columns
        print(f"\nCategorical Features:")
        for col in categorical_cols:
            print(f"  {col}: {df[col].unique()}")
        
        return {
            'shape': df.shape,
            'missing_values': missing_values.to_dict(),
            'numerical_columns': numerical_cols.tolist(),
            'categorical_columns': categorical_cols.tolist()
        }
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the dataset by handling missing values, outliers, and inconsistencies
        
        Args:
            df: Input dataframe
            
        Returns:
            pandas.DataFrame: Cleaned dataframe
        """
        print("\n=== Data Cleaning ===")
        
        # Create a copy to avoid modifying original
        df_clean = df.copy()
        
        # 1. Handle missing values
        print("Handling missing values...")
        
        # For numerical columns, fill with median
        numerical_cols = df_clean.select_dtypes(include=[np.number]).columns
        numerical_cols = [col for col in numerical_cols if col not in ['Poverty_Class']]
        
        for col in numerical_cols:
            if df_clean[col].isnull().sum() > 0:
                median_val = df_clean[col].median()
                df_clean[col].fillna(median_val, inplace=True)
                print(f"  Filled {col} missing values with median: {median_val:.2f}")
        
        # For categorical columns, fill with mode
        categorical_cols = df_clean.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df_clean[col].isnull().sum() > 0:
                mode_val = df_clean[col].mode()[0]
                df_clean[col].fillna(mode_val, inplace=True)
                print(f"  Filled {col} missing values with mode: {mode_val}")
        
        # 2. Handle outliers using IQR method
        print("\nHandling outliers...")
        
        for col in numerical_cols:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define outlier bounds
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Cap outliers
            outliers_count = len(df_clean[(df_clean[col] < lower_bound) | 
                                        (df_clean[col] > upper_bound)])
            
            if outliers_count > 0:
                df_clean[col] = np.clip(df_clean[col], lower_bound, upper_bound)
                print(f"  Capped {outliers_count} outliers in {col}")
        
        # 3. Data validation
        print("\nValidating data ranges...")
        
        # Ensure percentages are within 0-100
        percentage_cols = ['Literacy_Rate', 'Female_Literacy_Rate', 'Employment_Rate', 
                          'Clean_Water_Access', 'Electricity_Access', 'Urban_Population_Pct',
                          'Toilet_Access', 'Bank_Account_Access', 'Internet_Access']
        
        for col in percentage_cols:
            if col in df_clean.columns:
                df_clean[col] = np.clip(df_clean[col], 0, 100)
        
        # Ensure indices are within 0-100
        index_cols = ['Healthcare_Index', 'Education_Index', 'Poverty_Score']
        for col in index_cols:
            if col in df_clean.columns:
                df_clean[col] = np.clip(df_clean[col], 0, 100)
        
        # Ensure household size is reasonable
        if 'Household_Size' in df_clean.columns:
            df_clean['Household_Size'] = np.clip(df_clean['Household_Size'], 1, 15)
        
        print(f"Data cleaning completed. Shape: {df_clean.shape}")
        
        return df_clean
    
    def feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create new features and transform existing ones
        
        Args:
            df: Input dataframe
            
        Returns:
            pandas.DataFrame: Enhanced dataframe with new features
        """
        print("\n=== Feature Engineering ===")
        
        df_enhanced = df.copy()
        
        # 1. Literacy Gap
        if 'Literacy_Rate' in df.columns and 'Female_Literacy_Rate' in df.columns:
            df_enhanced['Literacy_Gap'] = df_enhanced['Literacy_Rate'] - df_enhanced['Female_Literacy_Rate']
            print("Created feature: Literacy_Gap")
        
        # 2. Infrastructure Score (combined utilities access)
        if all(col in df.columns for col in ['Clean_Water_Access', 'Electricity_Access', 'Toilet_Access']):
            df_enhanced['Infrastructure_Score'] = (
                df_enhanced['Clean_Water_Access'] + 
                df_enhanced['Electricity_Access'] + 
                df_enhanced['Toilet_Access']
            ) / 3
            print("Created feature: Infrastructure_Score")
        
        # 3. Development Index (combination of key indicators)
        if all(col in df.columns for col in ['Education_Index', 'Healthcare_Index', 'Employment_Rate']):
            df_enhanced['Development_Index'] = (
                df_enhanced['Education_Index'] * 0.4 +
                df_enhanced['Healthcare_Index'] * 0.3 +
                df_enhanced['Employment_Rate'] * 0.3
            )
            print("Created feature: Development_Index")
        
        # 4. Digital Divide (access to modern services)
        if all(col in df.columns for col in ['Internet_Access', 'Bank_Account_Access']):
            df_enhanced['Digital_Access_Score'] = (
                df_enhanced['Internet_Access'] + df_enhanced['Bank_Account_Access']
            ) / 2
            print("Created feature: Digital_Access_Score")
        
        # 5. Urban Development Ratio
        if 'Urban_Population_Pct' in df.columns:
            df_enhanced['Rural_Population_Pct'] = 100 - df_enhanced['Urban_Population_Pct']
            df_enhanced['Urban_Rural_Ratio'] = df_enhanced['Urban_Population_Pct'] / (df_enhanced['Rural_Population_Pct'] + 0.1)
            print("Created features: Rural_Population_Pct, Urban_Rural_Ratio")
        
        # 6. Household Efficiency (inverse of household size)
        if 'Household_Size' in df.columns:
            df_enhanced['Household_Efficiency'] = 1 / df_enhanced['Household_Size']
            print("Created feature: Household_Efficiency")
        
        # 7. Poverty Risk Score (combination of negative indicators)
        if 'Household_Size' in df.columns and 'Literacy_Gap' in df_enhanced.columns:
            df_enhanced['Poverty_Risk_Score'] = (
                df_enhanced['Household_Size'] * 10 +  # Higher household size = more risk
                df_enhanced['Literacy_Gap'] * 2 +     # Higher gap = more risk
                (100 - df_enhanced['Employment_Rate']) # Higher unemployment = more risk
            )
            print("Created feature: Poverty_Risk_Score")
        
        print(f"Feature engineering completed. New shape: {df_enhanced.shape}")
        
        return df_enhanced
    
    def prepare_features_for_ml(self, df: pd.DataFrame, target_col: str = 'Poverty_Class') -> tuple:
        """
        Prepare features for machine learning
        
        Args:
            df: Input dataframe
            target_col: Target column name
            
        Returns:
            tuple: (X_train, X_test, y_train, y_test, feature_names)
        """
        print(f"\n=== Preparing Features for ML ===")
        
        # Separate features and target
        X = df.drop(['District', 'State', 'Poverty_Level', 'Poverty_Class', 'Poverty_Score'], 
                   axis=1, errors='ignore')
        y = df[target_col]
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        print(f"Features selected: {len(self.feature_names)}")
        print(f"Features: {self.feature_names}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        print(f"Training set: {X_train.shape}")
        print(f"Test set: {X_test.shape}")
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Convert back to DataFrames
        X_train_scaled = pd.DataFrame(X_train_scaled, columns=self.feature_names)
        X_test_scaled = pd.DataFrame(X_test_scaled, columns=self.feature_names)
        
        self.is_fitted = True
        print("Feature scaling completed")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def transform_new_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform new data using fitted preprocessor
        
        Args:
            df: New data to transform
            
        Returns:
            pandas.DataFrame: Transformed data
        """
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transforming new data")
        
        # Apply same feature engineering
        df_enhanced = self.feature_engineering(df)
        
        # Select same features as training
        X = df_enhanced[self.feature_names]
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        X_scaled = pd.DataFrame(X_scaled, columns=self.feature_names)
        
        return X_scaled
    
    def save_processed_data(self, df: pd.DataFrame, file_path: str):
        """Save processed data to CSV"""
        df.to_csv(file_path, index=False)
        print(f"Processed data saved to: {file_path}")

def main():
    """Main preprocessing pipeline"""
    print("=== Poverty-Aware Resource Allocation: Data Preprocessing ===")
    
    # Initialize preprocessor
    preprocessor = PovertyDataPreprocessor()
    
    # Resolve repo root relative to this file (repo/src/..)
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(repo_root, "data")
    raw_file = os.path.join(data_dir, "raw", "indian_districts_socioeconomic.csv")
    processed_dir = os.path.join(data_dir, "processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    # Load raw data
    raw_data = preprocessor.load_raw_data(raw_file)
    
    # Explore data
    exploration_summary = preprocessor.explore_data(raw_data)
    
    # Clean data
    clean_data = preprocessor.clean_data(raw_data)
    
    # Feature engineering
    enhanced_data = preprocessor.feature_engineering(clean_data)

    # Additional enrichment: state-level context features (does not affect existing graphs)
    try:
        if all(col in enhanced_data.columns for col in ["State", "Poverty_Score"]):
            state_stats = enhanced_data.groupby("State")["Poverty_Score"].agg(["mean", "std"]).rename(
                columns={"mean": "State_Poverty_Mean", "std": "State_Poverty_Std"}
            )
            enhanced_data = enhanced_data.merge(state_stats, on="State", how="left")
            # z-score within state (handle std=0)
            enhanced_data["State_Poverty_Z"] = (
                (enhanced_data["Poverty_Score"] - enhanced_data["State_Poverty_Mean"]) /
                enhanced_data["State_Poverty_Std"].replace(0, np.nan)
            ).fillna(0.0)
            # Fill any remaining NaNs in enrichment columns
            global_mean = enhanced_data["Poverty_Score"].mean()
            enhanced_data["State_Poverty_Mean"] = enhanced_data["State_Poverty_Mean"].fillna(global_mean)
            enhanced_data["State_Poverty_Std"] = enhanced_data["State_Poverty_Std"].fillna(0.0)
            print("Added state-level enrichment features: State_Poverty_Mean, State_Poverty_Std, State_Poverty_Z")
    except Exception as e:
        print(f"Warning: could not add state-level enrichment features: {e}")
    
    # Save processed data
    processed_file = os.path.join(processed_dir, "processed_districts_data.csv")
    preprocessor.save_processed_data(enhanced_data, processed_file)

    # Save state->districts map for UI listing
    try:
        if all(col in enhanced_data.columns for col in ["State", "District"]):
            state_districts = (
                enhanced_data[["State", "District"]]
                .dropna()
                .drop_duplicates()
                .sort_values(["State", "District"]) 
                .groupby("State")["District"].apply(list)
                .to_dict()
            )
            map_path = os.path.join(processed_dir, "state_districts.json")
            with open(map_path, "w") as f:
                json.dump(state_districts, f, indent=2)
            print(f"Saved state-to-districts map to: {map_path}")
    except Exception as e:
        print(f"Warning: could not save state_districts map: {e}")
    
    # Prepare for ML
    X_train, X_test, y_train, y_test = preprocessor.prepare_features_for_ml(enhanced_data)
    
    # Save train/test splits
    train_file = os.path.join(processed_dir, "train_data.csv")
    test_file = os.path.join(processed_dir, "test_data.csv")
    
    train_data = X_train.copy()
    train_data['Poverty_Class'] = y_train.values
    train_data.to_csv(train_file, index=False)
    
    test_data = X_test.copy()
    test_data['Poverty_Class'] = y_test.values
    test_data.to_csv(test_file, index=False)
    
    print(f"\nTrain data saved to: {train_file}")
    print(f"Test data saved to: {test_file}")
    
    print("\nData preprocessing completed successfully!")
    
    return preprocessor, enhanced_data

if __name__ == "__main__":
    main()
