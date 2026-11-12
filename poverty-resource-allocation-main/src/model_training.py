"""
Model Training Module for Poverty-Aware Resource Allocation Model

This module implements and trains machine learning models for poverty classification
using Random Forest and XGBoost algorithms.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score, GridSearchCV
import xgboost as xgb
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class PovertyPredictionModel:
    """
    Machine learning model for poverty level prediction and evaluation
    """
    
    def __init__(self):
        """Initialize the model trainer"""
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.feature_importance = None
        self.model_metrics = {}
    
    def load_preprocessed_data(self, train_path: str, test_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Load preprocessed training and testing data
        
        Args:
            train_path: Path to training data CSV
            test_path: Path to testing data CSV
            
        Returns:
            tuple: X_train, X_test, y_train, y_test
        """
        print("Loading preprocessed data...")
        
        # Load training data
        train_data = pd.read_csv(train_path)
        X_train = train_data.drop('Poverty_Class', axis=1)
        y_train = train_data['Poverty_Class']
        
        # Load testing data
        test_data = pd.read_csv(test_path)
        X_test = test_data.drop('Poverty_Class', axis=1)
        y_test = test_data['Poverty_Class']
        
        print(f"Training set: {X_train.shape}")
        print(f"Test set: {X_test.shape}")
        print(f"Class distribution in training: {y_train.value_counts().to_dict()}")
        
        return X_train, X_test, y_train, y_test
    
    def train_random_forest(self, X_train: pd.DataFrame, y_train: pd.Series, 
                           optimize: bool = True) -> RandomForestClassifier:
        """
        Train Random Forest model with optional hyperparameter optimization
        
        Args:
            X_train: Training features
            y_train: Training labels
            optimize: Whether to perform hyperparameter optimization
            
        Returns:
            RandomForestClassifier: Trained model
        """
        print("\n=== Training Random Forest Model ===")
        
        if optimize:
            print("Performing hyperparameter optimization...")
            
            # Define parameter grid
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, 30, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'max_features': ['sqrt', 'log2', None]
            }
            
            # Grid search with cross-validation
            rf_base = RandomForestClassifier(random_state=42, n_jobs=-1)
            grid_search = GridSearchCV(
                estimator=rf_base,
                param_grid=param_grid,
                cv=5,
                scoring='accuracy',
                n_jobs=-1,
                verbose=1
            )
            
            grid_search.fit(X_train, y_train)
            
            print(f"Best parameters: {grid_search.best_params_}")
            print(f"Best cross-validation score: {grid_search.best_score_:.4f}")
            
            rf_model = grid_search.best_estimator_
        else:
            # Use default parameters
            rf_model = RandomForestClassifier(
                n_estimators=200,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                max_features='sqrt',
                random_state=42,
                n_jobs=-1
            )
            rf_model.fit(X_train, y_train)
        
        # Cross-validation score
        cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5, scoring='accuracy')
        print(f"Cross-validation accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        self.models['RandomForest'] = rf_model
        
        return rf_model
    
    def train_xgboost(self, X_train: pd.DataFrame, y_train: pd.Series, 
                      optimize: bool = True) -> xgb.XGBClassifier:
        """
        Train XGBoost model with optional hyperparameter optimization
        
        Args:
            X_train: Training features
            y_train: Training labels
            optimize: Whether to perform hyperparameter optimization
            
        Returns:
            XGBClassifier: Trained model
        """
        print("\n=== Training XGBoost Model ===")
        
        if optimize:
            print("Performing hyperparameter optimization...")
            
            # Define parameter grid
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 0.9, 1.0],
                'colsample_bytree': [0.8, 0.9, 1.0]
            }
            
            # Grid search with cross-validation
            xgb_base = xgb.XGBClassifier(random_state=42, eval_metric='logloss')
            grid_search = GridSearchCV(
                estimator=xgb_base,
                param_grid=param_grid,
                cv=5,
                scoring='accuracy',
                n_jobs=-1,
                verbose=1
            )
            
            grid_search.fit(X_train, y_train)
            
            print(f"Best parameters: {grid_search.best_params_}")
            print(f"Best cross-validation score: {grid_search.best_score_:.4f}")
            
            xgb_model = grid_search.best_estimator_
        else:
            # Use default parameters
            xgb_model = xgb.XGBClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.9,
                colsample_bytree=0.9,
                random_state=42,
                eval_metric='logloss'
            )
            xgb_model.fit(X_train, y_train)
        
        # Cross-validation score
        cv_scores = cross_val_score(xgb_model, X_train, y_train, cv=5, scoring='accuracy')
        print(f"Cross-validation accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        self.models['XGBoost'] = xgb_model
        
        return xgb_model
    
    def evaluate_models(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Dict]:
        """
        Evaluate all trained models on test data
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            dict: Evaluation metrics for each model
        """
        print("\n=== Model Evaluation ===")
        
        self.model_metrics = {}
        
        for model_name, model in self.models.items():
            print(f"\nEvaluating {model_name}...")
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)
            
            # Metrics
            accuracy = accuracy_score(y_test, y_pred)
            
            # Classification report
            class_report = classification_report(y_test, y_pred, 
                                               target_names=['High Poverty', 'Medium Poverty', 'Low Poverty'],
                                               output_dict=True)
            
            # Confusion matrix
            conf_matrix = confusion_matrix(y_test, y_pred)
            
            self.model_metrics[model_name] = {
                'accuracy': accuracy,
                'classification_report': class_report,
                'confusion_matrix': conf_matrix,
                'predictions': y_pred,
                'prediction_probabilities': y_pred_proba
            }
            
            print(f"Accuracy: {accuracy:.4f}")
            print(f"Classification Report:")
            print(classification_report(y_test, y_pred, 
                                      target_names=['High Poverty', 'Medium Poverty', 'Low Poverty']))
        
        # Select best model
        best_accuracy = 0
        for model_name, metrics in self.model_metrics.items():
            if metrics['accuracy'] > best_accuracy:
                best_accuracy = metrics['accuracy']
                self.best_model_name = model_name
                self.best_model = self.models[model_name]
        
        print(f"\nBest Model: {self.best_model_name} (Accuracy: {best_accuracy:.4f})")
        
        return self.model_metrics
    
    def analyze_feature_importance(self, X_train: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze feature importance for the best model
        
        Args:
            X_train: Training features for feature names
            
        Returns:
            pandas.DataFrame: Feature importance rankings
        """
        print(f"\n=== Feature Importance Analysis ({self.best_model_name}) ===")
        
        if self.best_model is None:
            raise ValueError("No model has been trained yet")
        
        # Get feature importance
        if hasattr(self.best_model, 'feature_importances_'):
            importance_scores = self.best_model.feature_importances_
        else:
            raise ValueError("Model does not support feature importance analysis")
        
        # Create DataFrame
        self.feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': importance_scores
        }).sort_values('importance', ascending=False)
        
        print("Top 10 Most Important Features:")
        print(self.feature_importance.head(10))
        
        return self.feature_importance
    
    def create_model_visualizations(self, output_dir: str):
        """
        Create visualizations for model performance and feature importance
        
        Args:
            output_dir: Directory to save visualizations
        """
        print(f"\n=== Creating Model Visualizations ===")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Model Comparison
        plt.figure(figsize=(10, 6))
        model_names = list(self.model_metrics.keys())
        accuracies = [self.model_metrics[name]['accuracy'] for name in model_names]
        
        bars = plt.bar(model_names, accuracies, color=['skyblue', 'lightcoral'])
        plt.title('Model Performance Comparison', fontsize=16, fontweight='bold')
        plt.ylabel('Accuracy', fontsize=12)
        plt.ylim(0, 1)
        
        # Add value labels on bars
        for bar, acc in zip(bars, accuracies):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'model_comparison.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Confusion Matrix for Best Model
        plt.figure(figsize=(8, 6))
        conf_matrix = self.model_metrics[self.best_model_name]['confusion_matrix']
        
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
                   xticklabels=['High Poverty', 'Medium Poverty', 'Low Poverty'],
                   yticklabels=['High Poverty', 'Medium Poverty', 'Low Poverty'])
        plt.title(f'Confusion Matrix - {self.best_model_name}', fontsize=16, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'confusion_matrix.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Feature Importance
        if self.feature_importance is not None:
            plt.figure(figsize=(12, 8))
            top_features = self.feature_importance.head(15)
            
            bars = plt.barh(range(len(top_features)), top_features['importance'])
            plt.yticks(range(len(top_features)), top_features['feature'])
            plt.xlabel('Feature Importance', fontsize=12)
            plt.title(f'Top 15 Feature Importance - {self.best_model_name}', 
                     fontsize=16, fontweight='bold')
            plt.gca().invert_yaxis()
            
            # Color bars by importance
            colors = plt.cm.viridis(top_features['importance'] / top_features['importance'].max())
            for bar, color in zip(bars, colors):
                bar.set_color(color)
            
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'feature_importance.png'), dpi=300, bbox_inches='tight')
            plt.close()
        
        print(f"Visualizations saved to: {output_dir}")
    
    def save_models(self, model_dir: str):
        """
        Save trained models to disk
        
        Args:
            model_dir: Directory to save models
        """
        print(f"\n=== Saving Models ===")
        
        os.makedirs(model_dir, exist_ok=True)
        
        for model_name, model in self.models.items():
            model_path = os.path.join(model_dir, f"{model_name.lower()}_model.pkl")
            joblib.dump(model, model_path)
            print(f"Saved {model_name} to: {model_path}")
        
        # Save best model separately
        if self.best_model is not None:
            best_model_path = os.path.join(model_dir, "best_model.pkl")
            joblib.dump(self.best_model, best_model_path)
            
            # Save model metadata
            metadata = {
                'best_model_name': self.best_model_name,
                'best_model_accuracy': self.model_metrics[self.best_model_name]['accuracy'],
                'feature_names': list(self.feature_importance['feature']) if self.feature_importance is not None else None
            }
            
            metadata_path = os.path.join(model_dir, "model_metadata.pkl")
            joblib.dump(metadata, metadata_path)
            
            print(f"Saved best model to: {best_model_path}")
            print(f"Saved metadata to: {metadata_path}")
    
    def predict_poverty_level(self, X_new: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict poverty levels for new data
        
        Args:
            X_new: New data to predict
            
        Returns:
            tuple: (predictions, prediction_probabilities)
        """
        if self.best_model is None:
            raise ValueError("No model has been trained yet")
        
        predictions = self.best_model.predict(X_new)
        prediction_probs = self.best_model.predict_proba(X_new)
        
        return predictions, prediction_probs

def main():
    """Main model training pipeline"""
    print("=== Poverty-Aware Resource Allocation: Model Training ===")
    
    # Initialize model trainer
    trainer = PovertyPredictionModel()
    
    # Resolve project-relative paths
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(repo_root, "data", "processed")
    train_path = os.path.join(data_dir, "train_data.csv")
    test_path = os.path.join(data_dir, "test_data.csv")
    model_dir = os.path.join(repo_root, "models")
    viz_dir = os.path.join(repo_root, "visualizations")
    
    # Load data
    X_train, X_test, y_train, y_test = trainer.load_preprocessed_data(train_path, test_path)
    
    # Train models (enable optimization for more advanced training)
    trainer.train_random_forest(X_train, y_train, optimize=True)
    trainer.train_xgboost(X_train, y_train, optimize=True)
    
    # Evaluate models
    trainer.evaluate_models(X_test, y_test)
    
    # Analyze feature importance
    trainer.analyze_feature_importance(X_train)
    
    # Create visualizations
    trainer.create_model_visualizations(viz_dir)
    
    # Save models
    trainer.save_models(model_dir)
    
    print("\nModel training completed successfully!")
    print(f"Best model: {trainer.best_model_name}")
    print(f"Best accuracy: {trainer.model_metrics[trainer.best_model_name]['accuracy']:.4f}")
    
    return trainer

if __name__ == "__main__":
    main()
