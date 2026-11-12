# Poverty-Aware Resource Allocation Model

A machine learning project to predict poverty levels across Indian districts and recommend optimal resource allocation based on socio-economic indicators.

## Project Overview

This project uses district-wise socio-economic data to:
1. Predict poverty levels (High, Medium, Low) using machine learning
2. Recommend resource allocation percentages based on poverty predictions
3. Visualize regional poverty distribution and aid allocation
4. Provide a web interface for real-time predictions

## Features

- **Data Collection**: Aggregated data from Census of India and open sources
- **ML Models**: Random Forest and XGBoost for poverty classification
- **Resource Allocation**: Logic-based aid distribution system
- **Visualizations**: Interactive maps and charts
- **Web Interface**: Streamlit app for user interaction

## Project Structure

```
poverty-resource-allocation/
├── data/
│   ├── raw/                    # Raw datasets
│   ├── processed/              # Cleaned datasets
│   └── sample/                 # Sample data for testing
├── src/
│   ├── data_collection.py      # Data gathering and synthesis
│   ├── data_preprocessing.py   # Data cleaning and feature engineering
│   ├── model_training.py       # ML model training and evaluation
│   ├── resource_allocation.py  # Aid distribution logic
│   ├── visualization.py        # Charts and maps
│   └── utils.py               # Helper functions
├── models/
│   └── trained_models/         # Saved ML models
├── visualizations/             # Generated plots and maps
├── streamlit_app.py           # Web interface
├── main.py                    # Main execution script
└── requirements.txt           # Dependencies
```

## Installation

1. Clone or download this project
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Run the complete pipeline:
```bash
python main.py
```

### 2. Run individual components:
```bash
# Data collection and preprocessing
python src/data_collection.py
python src/data_preprocessing.py

# Model training
python src/model_training.py

# Generate visualizations
python src/visualization.py
```

### 3. Launch web interface:
```bash
streamlit run streamlit_app.py
```

## Data Sources

- Census of India (simulated district-level data)
- Socio-economic indicators based on real Indian development patterns
- Poverty proxies using literacy, employment, and infrastructure access

## Model Features

### Input Features:
- Literacy Rate (%)
- Employment Rate (%)
- Access to Clean Water (%)
- Electricity Access (%)
- Healthcare Index (0-100)
- Education Index (0-100)
- Household Size (average)
- Female Literacy Rate (%)

### Output:
- Poverty Classification: High (0), Medium (1), Low (2)
- Resource Allocation Percentage

## Results

The model achieves good performance in classifying poverty levels and provides actionable insights for resource allocation across different regions.

## Contributing

Feel free to contribute by:
- Adding more data sources
- Improving model accuracy
- Enhancing visualizations
- Expanding the web interface

## License

This project is for educational and research purposes.
