"""
Main Execution Script for Poverty-Aware Resource Allocation Model

This script orchestrates the complete machine learning pipeline:
1. Data Collection & Generation
2. Data Preprocessing & Feature Engineering  
3. Model Training & Evaluation
4. Resource Allocation Calculation
5. Visualization & Reporting

Run this script to execute the complete pipeline end-to-end.
"""

import os
import sys
import time
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import project modules
try:
    from src.data_collection import collect_and_save_data
    from src.data_preprocessing import main as preprocess_data
    from src.model_training import main as train_models
    from src.resource_allocation import main as allocate_resources
    from src.visualization import main as create_visualizations
    from src.utils import ConfigManager, setup_project_directories
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required packages are installed: pip install -r requirements.txt")
    sys.exit(1)

class PovertyAllocationPipeline:
    """
    Main pipeline orchestrator for the poverty-aware resource allocation system
    """
    
    def __init__(self, project_path: str):
        """
        Initialize the pipeline
        
        Args:
            project_path: Root path of the project
        """
        self.project_path = project_path
        self.config = None
        self.execution_log = []
        
        # Set up logging
        self.log_file = os.path.join(project_path, 'pipeline_execution.log')
    
    def log_step(self, step_name: str, status: str, duration: float = None, details: str = None):
        """
        Log pipeline execution steps
        
        Args:
            step_name: Name of the pipeline step
            status: Status (SUCCESS, ERROR, WARNING)
            duration: Execution time in seconds
            details: Additional details
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = {
            'timestamp': timestamp,
            'step': step_name,
            'status': status,
            'duration': duration,
            'details': details
        }
        
        self.execution_log.append(log_entry)
        
        # Print to console
        duration_str = f" ({duration:.2f}s)" if duration else ""
        details_str = f" - {details}" if details else ""
        print(f"[{timestamp}] {step_name}: {status}{duration_str}{details_str}")
        
        # Write to log file
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {step_name}: {status}{duration_str}{details_str}\n")
    
    def setup_environment(self):
        """Set up the project environment and configuration"""
        print("="*80)
        print("POVERTY-AWARE RESOURCE ALLOCATION MODEL")
        print("="*80)
        print(f"Project Path: {self.project_path}")
        print(f"Execution Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        start_time = time.time()
        
        try:
            # Setup project directories
            setup_project_directories(self.project_path)
            
            # Load or create configuration
            config_path = os.path.join(self.project_path, 'config.json')
            
            if os.path.exists(config_path):
                self.config = ConfigManager.load_config(config_path)
                self.log_step("Environment Setup", "SUCCESS", 
                            time.time() - start_time, "Configuration loaded")
            else:
                self.config = ConfigManager.create_default_config()
                ConfigManager.save_config(self.config, config_path)
                self.log_step("Environment Setup", "SUCCESS", 
                            time.time() - start_time, "Default configuration created")
                
        except Exception as e:
            self.log_step("Environment Setup", "ERROR", 
                        time.time() - start_time, str(e))
            raise
    
    def run_data_collection(self):
        """Execute data collection step"""
        print("\n" + "="*50)
        print("STEP 1: DATA COLLECTION")
        print("="*50)
        
        start_time = time.time()
        
        try:
            # Run data collection
            district_data = collect_and_save_data()
            
            duration = time.time() - start_time
            self.log_step("Data Collection", "SUCCESS", duration, 
                        f"Generated {len(district_data)} district records")
            
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_step("Data Collection", "ERROR", duration, str(e))
            print(f"Error in data collection: {e}")
            return False
    
    def run_data_preprocessing(self):
        """Execute data preprocessing step"""
        print("\n" + "="*50)
        print("STEP 2: DATA PREPROCESSING")
        print("="*50)
        
        start_time = time.time()
        
        try:
            # Run data preprocessing
            preprocessor, processed_data = preprocess_data()
            
            duration = time.time() - start_time
            self.log_step("Data Preprocessing", "SUCCESS", duration,
                        f"Processed {len(processed_data)} records with {len(processed_data.columns)} features")
            
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_step("Data Preprocessing", "ERROR", duration, str(e))
            print(f"Error in data preprocessing: {e}")
            return False
    
    def run_model_training(self):
        """Execute model training step"""
        print("\n" + "="*50)
        print("STEP 3: MODEL TRAINING")
        print("="*50)
        
        start_time = time.time()
        
        try:
            # Run model training
            trainer = train_models()
            
            duration = time.time() - start_time
            best_accuracy = trainer.model_metrics[trainer.best_model_name]['accuracy']
            self.log_step("Model Training", "SUCCESS", duration,
                        f"Best model: {trainer.best_model_name} (Accuracy: {best_accuracy:.4f})")
            
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_step("Model Training", "ERROR", duration, str(e))
            print(f"Error in model training: {e}")
            return False
    
    def run_resource_allocation(self):
        """Execute resource allocation step"""
        print("\n" + "="*50)
        print("STEP 4: RESOURCE ALLOCATION")
        print("="*50)
        
        start_time = time.time()
        
        try:
            # Run resource allocation
            allocate_resources()
            
            duration = time.time() - start_time
            budget = self.config['resource_allocation']['total_budget']
            self.log_step("Resource Allocation", "SUCCESS", duration,
                        f"Allocated budget: ₹{budget:,.0f}")
            
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_step("Resource Allocation", "ERROR", duration, str(e))
            print(f"Error in resource allocation: {e}")
            return False
    
    def run_visualization(self):
        """Execute visualization generation step"""
        print("\n" + "="*50)
        print("STEP 5: VISUALIZATION & REPORTING")
        print("="*50)
        
        start_time = time.time()
        
        try:
            # Run visualization generation
            create_visualizations()
            
            duration = time.time() - start_time
            viz_dir = os.path.join(self.project_path, 'visualizations')
            viz_files = [f for f in os.listdir(viz_dir) if f.endswith(('.png', '.html'))]
            
            self.log_step("Visualization", "SUCCESS", duration,
                        f"Generated {len(viz_files)} visualization files")
            
            return True
            
        except Exception as e:
            duration = time.time() - start_time
            self.log_step("Visualization", "ERROR", duration, str(e))
            print(f"Error in visualization generation: {e}")
            return False
    
    def generate_final_report(self):
        """Generate final execution report"""
        print("\n" + "="*50)
        print("GENERATING FINAL REPORT")
        print("="*50)
        
        # Calculate total execution time
        total_duration = sum([log['duration'] for log in self.execution_log if log['duration']])
        
        # Count successes and failures
        successes = len([log for log in self.execution_log if log['status'] == 'SUCCESS'])
        errors = len([log for log in self.execution_log if log['status'] == 'ERROR'])
        
        # Generate report
        report_path = os.path.join(self.project_path, 'execution_report.txt')
        
        with open(report_path, 'w') as f:
            f.write("POVERTY-AWARE RESOURCE ALLOCATION MODEL\n")
            f.write("EXECUTION REPORT\n")
            f.write("="*50 + "\n\n")
            
            f.write(f"Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Project Path: {self.project_path}\n")
            f.write(f"Total Duration: {total_duration:.2f} seconds\n")
            f.write(f"Steps Completed: {successes}\n")
            f.write(f"Errors Encountered: {errors}\n\n")
            
            f.write("STEP-BY-STEP EXECUTION LOG\n")
            f.write("-"*30 + "\n")
            
            for log in self.execution_log:
                f.write(f"{log['timestamp']} - {log['step']}: {log['status']}")
                if log['duration']:
                    f.write(f" ({log['duration']:.2f}s)")
                if log['details']:
                    f.write(f" - {log['details']}")
                f.write("\n")
            
            f.write("\nPROJECT OUTPUTS\n")
            f.write("-"*15 + "\n")
            
            # List generated files
            data_dir = os.path.join(self.project_path, 'data')
            models_dir = os.path.join(self.project_path, 'models')
            viz_dir = os.path.join(self.project_path, 'visualizations')
            
            if os.path.exists(data_dir):
                data_files = []
                for root, dirs, files in os.walk(data_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            data_files.append(file)
                f.write(f"Data Files: {len(data_files)} CSV files\n")
            
            if os.path.exists(models_dir):
                model_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl')]
                f.write(f"Model Files: {len(model_files)} saved models\n")
            
            if os.path.exists(viz_dir):
                viz_files = [f for f in os.listdir(viz_dir) if f.endswith(('.png', '.html'))]
                f.write(f"Visualization Files: {len(viz_files)} charts and dashboards\n")
            
            f.write("\nRECOMMENDations\n")
            f.write("-"*15 + "\n")
            f.write("1. Review model performance metrics in visualizations/\n")
            f.write("2. Analyze resource allocation results in data/allocation_results.csv\n")
            f.write("3. Use the trained model for new district predictions\n")
            f.write("4. Consider running with hyperparameter optimization for better accuracy\n")
            f.write("5. Validate results with domain experts before deployment\n")
        
        print(f"Final report saved to: {report_path}")
        
        return report_path
    
    def run_complete_pipeline(self):
        """Execute the complete machine learning pipeline"""
        
        # Setup environment
        self.setup_environment()
        
        # Execute pipeline steps
        steps = [
            ("Data Collection", self.run_data_collection),
            ("Data Preprocessing", self.run_data_preprocessing),
            ("Model Training", self.run_model_training),
            ("Resource Allocation", self.run_resource_allocation),
            ("Visualization", self.run_visualization)
        ]
        
        pipeline_success = True
        
        for step_name, step_function in steps:
            success = step_function()
            if not success:
                print(f"\n❌ Pipeline failed at step: {step_name}")
                pipeline_success = False
                break
        
        # Generate final report
        report_path = self.generate_final_report()
        
        # Final summary
        print("\n" + "="*80)
        if pipeline_success:
            print("✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
            print("="*80)
            print("📊 OUTPUTS GENERATED:")
            print(f"   • District data with poverty predictions")
            print(f"   • Trained ML models (Random Forest & XGBoost)")
            print(f"   • Resource allocation recommendations")
            print(f"   • Comprehensive visualizations and dashboards")
            print(f"   • Detailed execution report: {os.path.basename(report_path)}")
            print("="*80)
            print("🚀 NEXT STEPS:")
            print("   • Review visualizations in the 'visualizations/' folder")
            print("   • Check resource allocation in 'data/allocation_results.csv'")
            print("   • Launch Streamlit app: 'streamlit run streamlit_app.py'")
            print("   • Validate results with domain experts")
        else:
            print("❌ PIPELINE EXECUTION FAILED!")
            print("="*80)
            print("📋 CHECK:")
            print(f"   • Execution log: {os.path.basename(self.log_file)}")
            print(f"   • Error details in: {os.path.basename(report_path)}")
            print("   • Required dependencies: pip install -r requirements.txt")
        
        print("="*80)
        
        return pipeline_success

def main():
    """Main execution function"""
    
    # Get project path
    project_path = "/Users/smitapaul/Machine Learning/poverty-resource-allocation"
    
    # Initialize and run pipeline
    pipeline = PovertyAllocationPipeline(project_path)
    success = pipeline.run_complete_pipeline()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
