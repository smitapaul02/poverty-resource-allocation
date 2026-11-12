"""
Advanced Model Training Module for Poverty-Aware Resource Allocation
Includes ensemble methods, hyperparameter optimization, and model interpretability
"""

import pandas as pd
import numpy as np
import json
import logging
import joblib
import shap
from datetime import datetime
from typing import Dict, List, Tuple, Any
from pathlib import Path

# ML Libraries
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
from sklearn.preprocessing import LabelEncoder

# Optional imports with fallbacks
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️ XGBoost not available, using sklearn models only")

try:
    import lightgbm as lgb
    from optuna.integration import LightGBMPruningCallback
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    print("⚠️ LightGBM not available, using sklearn models only")

try:
    import catboost as cb
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False
    print("⚠️ CatBoost not available, using sklearn models only")

try:
    import optuna
    OPTUNA_AVAILABLE = True
except ImportError:
    OPTUNA_AVAILABLE = False
    print("⚠️ Optuna not available, using basic hyperparameter tuning")

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    print("⚠️ SHAP not available, using basic feature importance")

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class AdvancedPovertyPredictionModel:
    """Advanced ML model with ensemble methods and hyperparameter optimization"""
    
    def __init__(self, config_path: str = 'config.json'):
        self.config = self._load_config(config_path)
        self.models = {}
        self.best_model = None
        self.best_score = 0
        self.feature_importance = None
        self.shap_explainer = None
        self.ensemble_model = None
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def train_ensemble_models(self, X_train: pd.DataFrame, y_train: pd.Series, 
                            X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Dict]:
        """Train multiple models and create ensemble"""
        
        self.logger.info("Starting advanced model training with ensemble methods...")
        
        # Define models - only include available ones
        models_config = {
            'RandomForest': {
                'model': RandomForestClassifier(random_state=42, n_jobs=-1),
                'params': {
                    'n_estimators': [100, 200, 300],
                    'max_depth': [10, 15, 20, None],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                }
            },
            'ExtraTrees': {
                'model': ExtraTreesClassifier(random_state=42, n_jobs=-1),
                'params': {
                    'n_estimators': [100, 200, 300],
                    'max_depth': [10, 15, 20],
                    'min_samples_split': [2, 5, 10]
                }
            },
            'GradientBoosting': {
                'model': GradientBoostingClassifier(random_state=42),
                'params': {
                    'n_estimators': [100, 200],
                    'max_depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.1, 0.2]
                }
            }
        }
        
        # Add optional models if available
        if XGBOOST_AVAILABLE:
            models_config['XGBoost'] = {
                'model': xgb.XGBClassifier(random_state=42, eval_metric='mlogloss'),
                'params': {
                    'n_estimators': [100, 200, 300],
                    'max_depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'subsample': [0.8, 0.9, 1.0]
                }
            }
        
        if LIGHTGBM_AVAILABLE:
            models_config['LightGBM'] = {
                'model': lgb.LGBMClassifier(random_state=42, verbose=-1),
                'params': {
                    'n_estimators': [100, 200, 300],
                    'max_depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'num_leaves': [31, 50, 100]
                }
            }
        
        if CATBOOST_AVAILABLE:
            models_config['CatBoost'] = {
                'model': cb.CatBoostClassifier(random_state=42, verbose=False),
                'params': {
                    'iterations': [100, 200, 300],
                    'depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.1, 0.2]
                }
            }
        
        results = {}
        
        # Train each model
        for model_name, model_config in models_config.items():
            self.logger.info(f"Training {model_name}...")
            
            if self.config['model_training']['optimize_hyperparameters']:
                # Hyperparameter optimization
                best_model = self._optimize_hyperparameters(
                    model_config['model'], 
                    model_config['params'],
                    X_train, y_train, 
                    model_name
                )
            else:
                best_model = model_config['model']
                best_model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = best_model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(
                best_model, X_train, y_train, 
                cv=self.config['model_training']['cross_validation_folds'],
                scoring='accuracy'
            )
            
            # Store results
            results[model_name] = {
                'model': best_model,
                'accuracy': accuracy,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'predictions': y_pred,
                'classification_report': classification_report(y_test, y_pred, output_dict=True)
            }
            
            self.models[model_name] = best_model
            
            # Update best model
            if accuracy > self.best_score:
                self.best_score = accuracy
                self.best_model = best_model
                self.best_model_name = model_name
            
            self.logger.info(f"{model_name} - Accuracy: {accuracy:.4f}, CV: {cv_scores.mean():.4f}±{cv_scores.std():.4f}")
        
        # Create ensemble model
        self._create_ensemble_model(X_train, y_train, X_test, y_test)
        
        return results
    
    def _optimize_hyperparameters(self, model, param_grid: Dict, 
                                 X_train: pd.DataFrame, y_train: pd.Series, 
                                 model_name: str):
        """Optimize hyperparameters using Optuna"""
        
        def objective(trial):
            params = {}
            for param, values in param_grid.items():
                if isinstance(values[0], int):
                    params[param] = trial.suggest_int(param, min(values), max(values))
                elif isinstance(values[0], float):
                    params[param] = trial.suggest_float(param, min(values), max(values))
                else:
                    params[param] = trial.suggest_categorical(param, values)
            
            # Create model with suggested parameters
            if model_name == 'RandomForest':
                clf = RandomForestClassifier(**params, random_state=42, n_jobs=-1)
            elif model_name == 'XGBoost':
                clf = xgb.XGBClassifier(**params, random_state=42, eval_metric='mlogloss')
            elif model_name == 'LightGBM':
                clf = lgb.LGBMClassifier(**params, random_state=42, verbose=-1)
            elif model_name == 'CatBoost':
                clf = cb.CatBoostClassifier(**params, random_state=42, verbose=False)
            elif model_name == 'ExtraTrees':
                clf = ExtraTreesClassifier(**params, random_state=42, n_jobs=-1)
            else:
                clf = GradientBoostingClassifier(**params, random_state=42)
            
            # Cross-validation score
            cv_scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy')
            return cv_scores.mean()
        
        # Optimize
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=50)
        
        # Get best parameters
        best_params = study.best_params
        self.logger.info(f"Best parameters for {model_name}: {best_params}")
        
        # Train final model with best parameters
        if model_name == 'RandomForest':
            best_model = RandomForestClassifier(**best_params, random_state=42, n_jobs=-1)
        elif model_name == 'XGBoost':
            best_model = xgb.XGBClassifier(**best_params, random_state=42, eval_metric='mlogloss')
        elif model_name == 'LightGBM':
            best_model = lgb.LGBMClassifier(**best_params, random_state=42, verbose=-1)
        elif model_name == 'CatBoost':
            best_model = cb.CatBoostClassifier(**best_params, random_state=42, verbose=False)
        elif model_name == 'ExtraTrees':
            best_model = ExtraTreesClassifier(**best_params, random_state=42, n_jobs=-1)
        else:
            best_model = GradientBoostingClassifier(**best_params, random_state=42)
        
        best_model.fit(X_train, y_train)
        return best_model
    
    def _create_ensemble_model(self, X_train: pd.DataFrame, y_train: pd.Series,
                              X_test: pd.DataFrame, y_test: pd.Series):
        """Create ensemble model using voting"""
        from sklearn.ensemble import VotingClassifier
        
        # Select top 3 models for ensemble
        model_scores = [(name, results['accuracy']) for name, results in 
                       [(name, {'accuracy': accuracy_score(y_test, model.predict(X_test))}) 
                        for name, model in self.models.items()]]
        model_scores.sort(key=lambda x: x[1], reverse=True)
        top_models = model_scores[:3]
        
        # Create ensemble
        estimators = [(name, self.models[name]) for name, _ in top_models]
        self.ensemble_model = VotingClassifier(estimators=estimators, voting='soft')
        self.ensemble_model.fit(X_train, y_train)
        
        # Evaluate ensemble
        ensemble_pred = self.ensemble_model.predict(X_test)
        ensemble_accuracy = accuracy_score(y_test, ensemble_pred)
        
        self.logger.info(f"Ensemble Model Accuracy: {ensemble_accuracy:.4f}")
        
        if ensemble_accuracy > self.best_score:
            self.best_score = ensemble_accuracy
            self.best_model = self.ensemble_model
            self.best_model_name = "Ensemble"
    
    def create_model_interpretability(self, X_train: pd.DataFrame, feature_names: List[str]):
        """Create SHAP explainer for model interpretability"""
        
        self.logger.info("Creating model interpretability with SHAP...")
        
        # Create SHAP explainer
        if hasattr(self.best_model, 'predict_proba'):
            self.shap_explainer = shap.Explainer(self.best_model, X_train)
        else:
            self.shap_explainer = shap.Explainer(self.best_model)
        
        # Calculate SHAP values
        shap_values = self.shap_explainer(X_train.iloc[:100])  # Sample for efficiency
        
        # Feature importance from SHAP
        self.feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': np.abs(shap_values.values).mean(0)
        }).sort_values('importance', ascending=False)
        
        return shap_values
    
    def create_advanced_visualizations(self, X_test: pd.DataFrame, y_test: pd.Series,
                                     results: Dict, save_path: str = 'visualizations/'):
        """Create comprehensive model visualizations"""
        
        save_path = Path(save_path)
        save_path.mkdir(exist_ok=True)
        
        # 1. Model Comparison Dashboard
        self._create_model_comparison_dashboard(results, save_path)
        
        # 2. Feature Importance Visualization
        self._create_feature_importance_viz(save_path)
        
        # 3. SHAP Visualizations
        if self.shap_explainer:
            self._create_shap_visualizations(X_test, save_path)
        
        # 4. Confusion Matrix Heatmap
        self._create_confusion_matrix_viz(X_test, y_test, save_path)
        
        # 5. ROC Curves (for binary classification adaptation)
        self._create_performance_curves(X_test, y_test, save_path)
        
        self.logger.info(f"Advanced visualizations saved to {save_path}")
    
    def _create_model_comparison_dashboard(self, results: Dict, save_path: Path):
        """Create interactive model comparison dashboard"""
        
        # Prepare data
        model_names = list(results.keys())
        accuracies = [results[name]['accuracy'] for name in model_names]
        cv_means = [results[name]['cv_mean'] for name in model_names]
        cv_stds = [results[name]['cv_std'] for name in model_names]
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Model Accuracy Comparison', 'Cross-Validation Scores',
                          'Model Performance Metrics', 'Training vs Validation'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Accuracy comparison
        fig.add_trace(
            go.Bar(x=model_names, y=accuracies, name='Test Accuracy',
                  marker_color='lightblue'),
            row=1, col=1
        )
        
        # CV scores with error bars
        fig.add_trace(
            go.Bar(x=model_names, y=cv_means, 
                  error_y=dict(type='data', array=cv_stds),
                  name='CV Mean ± Std', marker_color='orange'),
            row=1, col=2
        )
        
        # Performance metrics heatmap data
        metrics_data = []
        for name in model_names:
            report = results[name]['classification_report']
            metrics_data.append([
                report['weighted avg']['precision'],
                report['weighted avg']['recall'], 
                report['weighted avg']['f1-score']
            ])
        
        fig.add_trace(
            go.Heatmap(
                z=metrics_data,
                x=['Precision', 'Recall', 'F1-Score'],
                y=model_names,
                colorscale='Viridis',
                name='Metrics'
            ),
            row=2, col=1
        )
        
        # Model complexity vs performance
        complexity_scores = [0.8, 0.9, 0.85, 0.95, 0.75, 0.88]  # Example scores
        fig.add_trace(
            go.Scatter(x=complexity_scores, y=accuracies,
                      mode='markers+text', text=model_names,
                      textposition="top center", name='Complexity vs Accuracy',
                      marker=dict(size=10, color='red')),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Advanced Model Performance Dashboard",
            showlegend=True,
            height=800
        )
        
        # Save
        fig.write_html(str(save_path / 'advanced_model_comparison.html'))
    
    def _create_feature_importance_viz(self, save_path: Path):
        """Create advanced feature importance visualizations"""
        
        if self.feature_importance is None:
            return
        
        # Top 20 features
        top_features = self.feature_importance.head(20)
        
        # Create interactive plot
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_features['feature'],
            x=top_features['importance'],
            orientation='h',
            marker=dict(
                color=top_features['importance'],
                colorscale='Viridis',
                showscale=True
            )
        ))
        
        fig.update_layout(
            title='Top 20 Feature Importance (SHAP Values)',
            xaxis_title='Importance Score',
            yaxis_title='Features',
            height=600,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        fig.write_html(str(save_path / 'advanced_feature_importance.html'))
    
    def _create_shap_visualizations(self, X_test: pd.DataFrame, save_path: Path):
        """Create SHAP-based interpretability visualizations"""
        
        # Sample for visualization
        sample_data = X_test.iloc[:50]
        shap_values = self.shap_explainer(sample_data)
        
        # Summary plot
        plt.figure(figsize=(12, 8))
        shap.summary_plot(shap_values, sample_data, show=False)
        plt.tight_layout()
        plt.savefig(str(save_path / 'shap_summary_plot.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # Waterfall plot for first prediction
        plt.figure(figsize=(12, 8))
        shap.waterfall_plot(shap_values[0], show=False)
        plt.tight_layout()
        plt.savefig(str(save_path / 'shap_waterfall_plot.png'), dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_confusion_matrix_viz(self, X_test: pd.DataFrame, y_test: pd.Series, save_path: Path):
        """Create advanced confusion matrix visualization"""
        
        y_pred = self.best_model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        
        # Get unique labels
        labels = sorted(y_test.unique())
        label_names = ['Critical', 'High', 'Medium', 'Low'][:len(labels)]
        
        # Create interactive heatmap
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=label_names,
            y=label_names,
            colorscale='Blues',
            text=cm,
            texttemplate="%{text}",
            textfont={"size": 16},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Confusion Matrix - Best Model',
            xaxis_title='Predicted Label',
            yaxis_title='True Label'
        )
        
        fig.write_html(str(save_path / 'confusion_matrix_interactive.html'))
    
    def _create_performance_curves(self, X_test: pd.DataFrame, y_test: pd.Series, save_path: Path):
        """Create performance curves visualization"""
        
        # Get prediction probabilities
        y_pred_proba = self.best_model.predict_proba(X_test)
        
        # Create confidence distribution plot
        max_proba = np.max(y_pred_proba, axis=1)
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=max_proba,
            nbinsx=30,
            name='Prediction Confidence',
            opacity=0.7
        ))
        
        fig.update_layout(
            title='Prediction Confidence Distribution',
            xaxis_title='Maximum Probability',
            yaxis_title='Count',
            showlegend=True
        )
        
        fig.write_html(str(save_path / 'prediction_confidence.html'))
    
    def save_models(self, save_path: str = 'models/'):
        """Save all trained models"""
        
        save_path = Path(save_path)
        save_path.mkdir(exist_ok=True)
        
        # Save individual models
        for name, model in self.models.items():
            joblib.dump(model, save_path / f'{name.lower()}_model_advanced.pkl')
        
        # Save best model
        if self.best_model:
            joblib.dump(self.best_model, save_path / 'best_model_advanced.pkl')
        
        # Save ensemble model
        if self.ensemble_model:
            joblib.dump(self.ensemble_model, save_path / 'ensemble_model_advanced.pkl')
        
        # Save feature importance
        if self.feature_importance is not None:
            self.feature_importance.to_csv(save_path / 'feature_importance_advanced.csv', index=False)
        
        # Save metadata
        metadata = {
            'best_model_name': getattr(self, 'best_model_name', 'Unknown'),
            'best_score': self.best_score,
            'training_date': datetime.now().isoformat(),
            'config': self.config,
            'models_trained': list(self.models.keys())
        }
        
        with open(save_path / 'model_metadata_advanced.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.logger.info(f"All models saved to {save_path}")
    
    def load_model(self, model_path: str):
        """Load a saved model"""
        self.best_model = joblib.load(model_path)
        return self.best_model
    
    def predict_with_confidence(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions with confidence scores"""
        
        if self.best_model is None:
            raise ValueError("No model trained. Please train a model first.")
        
        predictions = self.best_model.predict(X)
        
        if hasattr(self.best_model, 'predict_proba'):
            probabilities = self.best_model.predict_proba(X)
            confidence = np.max(probabilities, axis=1)
        else:
            confidence = np.ones(len(predictions))  # Default confidence
        
        return predictions, confidence

def main():
    """Main function to demonstrate advanced model training"""
    
    # Load data (assuming preprocessed data exists)
    try:
        X_train = pd.read_csv('data/processed/train_data.csv')
        y_train = X_train.pop('Poverty_Class')
        
        X_test = pd.read_csv('data/processed/test_data.csv') 
        y_test = X_test.pop('Poverty_Class')
        
        # Initialize advanced model
        advanced_model = AdvancedPovertyPredictionModel()
        
        # Train ensemble models
        results = advanced_model.train_ensemble_models(X_train, y_train, X_test, y_test)
        
        # Create interpretability
        shap_values = advanced_model.create_model_interpretability(X_train, X_train.columns.tolist())
        
        # Create visualizations
        advanced_model.create_advanced_visualizations(X_test, y_test, results)
        
        # Save models
        advanced_model.save_models()
        
        print("✅ Advanced model training completed successfully!")
        print(f"🏆 Best Model: {advanced_model.best_model_name}")
        print(f"📊 Best Accuracy: {advanced_model.best_score:.4f}")
        
    except FileNotFoundError:
        print("❌ Training data not found. Please run data preprocessing first.")
    except Exception as e:
        print(f"❌ Error during training: {str(e)}")

if __name__ == "__main__":
    main()
