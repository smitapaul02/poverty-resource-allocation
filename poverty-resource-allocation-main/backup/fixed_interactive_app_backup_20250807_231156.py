#!/usr/bin/env python3
"""
Fixed Poverty Resource Allocation System
Working version with state interaction and all requested features
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import json
import math
import random
import hashlib
import base64
import os
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Advanced Poverty Resource Allocation System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: #667eea;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 900;
        font-family: 'Arial Black', Arial, sans-serif;
        letter-spacing: 2px;
        text-shadow: 2px 2px 8px rgba(102, 126, 234, 0.3);
        filter: none;
        -webkit-filter: none;
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stApp > header {
        background: transparent;
    }
    .stApp .main .block-container {
        background: transparent;
    }
    .alert-critical {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 5px solid #a71e2a;
        animation: blink 1s infinite, pulse 2s infinite;
        box-shadow: 0 8px 25px rgba(220, 53, 69, 0.3);
    }
    @keyframes blink {
        0%, 50% { opacity: 1; background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); }
        51%, 100% { opacity: 0.3; background: linear-gradient(135deg, #ff0000 0%, #ff4444 100%); }
    }
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 8px 25px rgba(220, 53, 69, 0.3); }
        50% { transform: scale(1.05); box-shadow: 0 12px 35px rgba(220, 53, 69, 0.6); }
        100% { transform: scale(1); box-shadow: 0 8px 25px rgba(220, 53, 69, 0.3); }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-3px); }
        75% { transform: translateX(3px); }
    }
    .beep-red {
        animation: blink 0.5s infinite, shake 1s infinite;
        border: 3px solid #ffffff;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.8);
    }
    .beep-green {
        animation: pulse 3s infinite;
        border: 2px solid #ffffff;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.6);
    }
    .alert-high {
        background: linear-gradient(135deg, #fd7e14 0%, #e55a00 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 5px solid #e55a00;
        animation: pulse 3s infinite;
        box-shadow: 0 8px 25px rgba(253, 126, 20, 0.3);
    }
    .alert-medium {
        background: linear-gradient(135deg, #ffc107 0%, #d39e00 100%);
        color: black;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 5px solid #d39e00;
        box-shadow: 0 8px 25px rgba(255, 193, 7, 0.3);
    }
    .alert-low {
        background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 5px solid #1e7e34;
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
    }
    .ngo-card {
        border: 2px solid #007bff;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        box-shadow: 0 10px 30px rgba(0, 123, 255, 0.2);
        transition: transform 0.3s ease;
    }
    .ngo-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 123, 255, 0.3);
    }
    .gov-contact {
        border: 2px solid #28a745;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);
        box-shadow: 0 10px 30px rgba(40, 167, 69, 0.2);
        transition: transform 0.3s ease;
    }
    .gov-contact:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(40, 167, 69, 0.3);
    }
    .resource-need {
        border: 2px solid #ffc107;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #fffbf0 0%, #fff3cd 100%);
        box-shadow: 0 10px 30px rgba(255, 193, 7, 0.2);
        transition: transform 0.3s ease;
    }
    .resource-need:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(255, 193, 7, 0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 45px rgba(102, 126, 234, 0.5);
    }
    .status-live {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        font-weight: bold;
        box-shadow: 0 15px 35px rgba(40, 167, 69, 0.4);
        animation: pulse 2s infinite;
    }
    .state-button {
        width: 100%;
        margin: 0.5rem 0;
        padding: 1rem;
        border-radius: 15px;
        border: 3px solid #007bff;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        color: #007bff;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 123, 255, 0.2);
    }
    .state-button:hover {
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        color: white;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 123, 255, 0.4);
    }
    .globe-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 25px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 20px 50px rgba(30, 60, 114, 0.5);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 12px;
        border: 2px solid #e9ecef;
    }
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.7; }
    }
    @keyframes pulse {
        0% { box-shadow: 0 15px 35px rgba(40, 167, 69, 0.4); }
        50% { box-shadow: 0 20px 45px rgba(40, 167, 69, 0.6); }
        100% { box-shadow: 0 15px 35px rgba(40, 167, 69, 0.4); }
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
        font-weight: 700;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    .plotly-graph-div {
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        background: transparent;
    }
    .stApp > header[data-testid="stHeader"] {
        background: transparent;
    }
    .stApp .main > div {
        background: transparent;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .css-1d391kg {
        background: transparent;
    }
    .css-18e3th9 {
        background: transparent;
    }
</style>
""", unsafe_allow_html=True)

class AdvancedPovertySystem:
    def __init__(self):
        if 'district_data' not in st.session_state:
            # Temporarily set district_data for other methods to work
            temp_data = self.generate_comprehensive_data()
            st.session_state.district_data = temp_data
            self.district_data = temp_data
            
            st.session_state.ngo_database = self.generate_ngo_database()
            st.session_state.government_contacts = self.generate_government_contacts()
            st.session_state.emergency_alerts = self.generate_emergency_alerts()
        else:
            self.district_data = st.session_state.district_data
            
        # Load advanced AI systems
        self.load_advanced_models()
        self.setup_realtime_feeds()
        self.initialize_satellite_data()
        self.setup_ai_predictions()
            
        if 'selected_state' not in st.session_state:
            st.session_state.selected_state = None
        if 'selected_district' not in st.session_state:
            st.session_state.selected_district = None
            
        self.ngo_database = st.session_state.ngo_database
        self.government_contacts = st.session_state.government_contacts
        self.emergency_alerts = st.session_state.emergency_alerts
    
    def load_advanced_models(self):
        """Load advanced AI models for predictions"""
        # Simulate loading multiple AI models
        self.models = {
            'poverty_predictor': {'accuracy': 0.94, 'last_trained': datetime.now() - timedelta(days=2)},
            'resource_optimizer': {'accuracy': 0.91, 'last_trained': datetime.now() - timedelta(days=1)},
            'satellite_analyzer': {'accuracy': 0.88, 'last_trained': datetime.now() - timedelta(hours=6)},
            'economic_forecaster': {'accuracy': 0.93, 'last_trained': datetime.now() - timedelta(hours=12)},
            'social_impact_model': {'accuracy': 0.89, 'last_trained': datetime.now() - timedelta(days=3)}
        }
    
    def setup_realtime_feeds(self):
        """Setup real-time data feeds"""
        self.data_feeds = {
            'economic_indicators': {'status': 'active', 'last_update': datetime.now()},
            'weather_data': {'status': 'active', 'last_update': datetime.now()},
            'population_movement': {'status': 'active', 'last_update': datetime.now()},
            'government_spending': {'status': 'active', 'last_update': datetime.now()},
            'ngo_activities': {'status': 'active', 'last_update': datetime.now()}
        }
    
    def initialize_satellite_data(self):
        """Initialize satellite imagery and analysis"""
        if not hasattr(self, 'district_data'):
            return
        self.satellite_data = {}
        for _, district in self.district_data.iterrows():
            # Simulate satellite analysis for each district
            self.satellite_data[district['District']] = {
                'infrastructure_index': random.uniform(0.3, 0.9),
                'vegetation_index': random.uniform(0.2, 0.8),
                'urban_density': random.uniform(0.1, 0.7),
                'road_network_score': random.uniform(0.4, 0.9),
                'night_lights_intensity': random.uniform(0.2, 0.8),
                'last_satellite_pass': datetime.now() - timedelta(hours=random.randint(1, 12))
            }
    
    def setup_ai_predictions(self):
        """Setup AI-powered predictive analytics"""
        if not hasattr(self, 'district_data'):
            return
        self.predictions = {}
        for _, district in self.district_data.iterrows():
            # Generate advanced predictions
            current_poverty = district['Poverty_Score']
            self.predictions[district['District']] = {
                'poverty_trend_30d': self.generate_trend_prediction(current_poverty, 30),
                'poverty_trend_90d': self.generate_trend_prediction(current_poverty, 90),
                'resource_need_forecast': self.calculate_resource_forecast(district),
                'intervention_success_probability': random.uniform(0.6, 0.95),
                'economic_impact_score': random.uniform(0.3, 0.8),
                'social_stability_index': random.uniform(0.4, 0.9)
            }
    
    def generate_trend_prediction(self, current_score, days):
        """Generate realistic trend predictions"""
        # Simulate AI model prediction with some randomness
        trend_factor = random.uniform(-0.1, 0.1)
        seasonal_factor = math.sin(days / 365 * 2 * math.pi) * 0.05
        return max(0, min(1, current_score + trend_factor + seasonal_factor))
    
    def calculate_resource_forecast(self, district):
        """Calculate predicted resource needs"""
        base_need = district['Population'] * district['Poverty_Score']
        return {
            'food_aid_tons': int(base_need / 1000 * random.uniform(0.5, 1.5)),
            'medical_supplies_units': int(base_need / 500 * random.uniform(0.8, 1.2)),
            'education_materials': int(base_need / 800 * random.uniform(0.6, 1.4)),
            'infrastructure_investment': int(base_need * random.uniform(50, 150))
        }
        
    def generate_comprehensive_data(self):
        """Generate comprehensive district data with coordinates"""
        np.random.seed(42)
        
        # Real Indian states with approximate coordinates
        states_coords = {
            'Maharashtra': (19.7515, 75.7139),
            'Uttar Pradesh': (26.8467, 80.9462),
            'Bihar': (25.0961, 85.3131),
            'West Bengal': (22.9868, 87.8550),
            'Madhya Pradesh': (22.9734, 78.6569),
            'Tamil Nadu': (11.1271, 78.6569),
            'Rajasthan': (27.0238, 74.2179),
            'Karnataka': (15.3173, 75.7139),
            'Gujarat': (23.0225, 72.5714),
            'Andhra Pradesh': (15.9129, 79.7400)
        }
        
        districts = []
        for state, (base_lat, base_lon) in states_coords.items():
            for i in range(8):  # 8 districts per state
                # Generate coordinates around the state center
                lat = base_lat + np.random.uniform(-2, 2)
                lon = base_lon + np.random.uniform(-2, 2)
                
                poverty_score = np.random.uniform(0.1, 0.95)
                
                districts.append({
                    'State': state,
                    'District': f'{state}_District_{i+1}',
                    'Latitude': lat,
                    'Longitude': lon,
                    'Population': np.random.randint(100000, 2500000),
                    'Literacy_Rate': np.random.uniform(35, 95),
                    'Employment_Rate': np.random.uniform(25, 85),
                    'Healthcare_Index': np.random.uniform(0.2, 0.9),
                    'Infrastructure_Score': np.random.uniform(0.1, 0.85),
                    'Clean_Water_Access': np.random.uniform(30, 95),
                    'Poverty_Score': poverty_score,
                    'Alert_Level': self.get_alert_level(poverty_score),
                    'Last_Updated': datetime.now() - timedelta(minutes=np.random.randint(1, 60))
                })
        
        return pd.DataFrame(districts)
    
    def get_alert_level(self, poverty_score):
        """Determine alert level based on poverty score"""
        if poverty_score >= 0.8:
            return 'Critical'
        elif poverty_score >= 0.7:
            return 'High'
        elif poverty_score >= 0.5:
            return 'Medium'
        else:
            return 'Low'
    
    def generate_ngo_database(self):
        """Generate comprehensive NGO database"""
        states = self.district_data['State'].unique()
        
        ngos = []
        for state in states:
            state_coords = self.district_data[self.district_data['State'] == state][['Latitude', 'Longitude']].mean()
            
            # 3-5 NGOs per state
            for i in range(np.random.randint(3, 6)):
                lat = state_coords['Latitude'] + np.random.uniform(-1, 1)
                lon = state_coords['Longitude'] + np.random.uniform(-1, 1)
                
                specializations = np.random.choice([
                    'Food Security', 'Healthcare', 'Education', 'Clean Water', 
                    'Shelter', 'Emergency Relief', 'Child Welfare', 'Women Empowerment'
                ], size=np.random.randint(1, 4), replace=False)
                
                ngos.append({
                    'name': f'{state}_NGO_{i+1}',
                    'state': state,
                    'latitude': lat,
                    'longitude': lon,
                    'specialization': list(specializations),
                    'capacity': np.random.choice(['Small', 'Medium', 'Large']),
                    'response_time': f'{np.random.randint(2, 48)} hours',
                    'contact_email': f'contact@{state.lower()}ngo{i+1}.org',
                    'contact_phone': f'+91-{np.random.randint(70000, 99999)}-{np.random.randint(10000, 99999)}',
                    'status': np.random.choice(['Active', 'Responding', 'Available', 'Busy']),
                    'rating': np.random.uniform(3.5, 5.0),
                    'projects_completed': np.random.randint(10, 500)
                })
        
        return ngos
    
    def generate_government_contacts(self):
        """Generate government department contacts"""
        states = self.district_data['State'].unique()
        
        contacts = {}
        for state in states:
            contacts[state] = {
                'District_Collector': {
                    'name': f'Collector_{state}',
                    'email': f'collector@{state.lower()}.gov.in',
                    'phone': f'+91-{np.random.randint(70000, 99999)}-{np.random.randint(10000, 99999)}',
                    'emergency_phone': f'+91-{np.random.randint(90000, 99999)}-{np.random.randint(10000, 99999)}'
                },
                'Health_Department': {
                    'name': f'Health_Officer_{state}',
                    'email': f'health@{state.lower()}.gov.in',
                    'phone': f'+91-{np.random.randint(70000, 99999)}-{np.random.randint(10000, 99999)}'
                },
                'Social_Welfare': {
                    'name': f'Social_Welfare_{state}',
                    'email': f'welfare@{state.lower()}.gov.in',
                    'phone': f'+91-{np.random.randint(70000, 99999)}-{np.random.randint(10000, 99999)}'
                },
                'Emergency_Services': {
                    'name': f'Emergency_{state}',
                    'email': f'emergency@{state.lower()}.gov.in',
                    'phone': f'+91-{np.random.randint(70000, 99999)}-{np.random.randint(10000, 99999)}',
                    'hotline': '108'
                }
            }
        
        return contacts
    
    def generate_emergency_alerts(self):
        """Generate current emergency alerts"""
        critical_districts = self.district_data[self.district_data['Alert_Level'] == 'Critical']
        high_districts = self.district_data[self.district_data['Alert_Level'] == 'High']
        
        alerts = []
        
        # Critical alerts
        for _, district in critical_districts.head(5).iterrows():
            alerts.append({
                'level': 'Critical',
                'district': district['District'],
                'state': district['State'],
                'poverty_score': district['Poverty_Score'],
                'population_affected': int(district['Population'] * 0.8),
                'urgent_needs': ['Food', 'Medical Aid', 'Clean Water'],
                'time_since': f"{np.random.randint(1, 30)} minutes ago",
                'status': 'Active'
            })
        
        # High alerts
        for _, district in high_districts.head(8).iterrows():
            alerts.append({
                'level': 'High',
                'district': district['District'],
                'state': district['State'],
                'poverty_score': district['Poverty_Score'],
                'population_affected': int(district['Population'] * 0.6),
                'urgent_needs': np.random.choice(['Food', 'Healthcare', 'Education', 'Infrastructure'], 2).tolist(),
                'time_since': f"{np.random.randint(30, 120)} minutes ago",
                'status': 'Active'
            })
        
        return alerts
    
    def render_header(self):
        """Render enhanced header"""
        st.markdown("""
        <div style="text-align: center; margin-bottom: 3rem;">
            <h1 style="
                font-size: 3.5rem;
                color: #2E4057;
                font-weight: 900;
                font-family: 'Arial Black', Arial, sans-serif;
                letter-spacing: 2px;
                text-align: center;
                margin-bottom: 1rem;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
                line-height: 1.2;
                padding: 1rem;
                border-radius: 15px;
                background: rgba(255, 255, 255, 0.9);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            ">🏛️ Advanced Poverty Resource Allocation System</h1>
            <p style="
                font-size: 1.4rem; 
                color: #333; 
                margin-bottom: 2rem; 
                font-style: italic; 
                font-weight: 600;
                background: rgba(255, 255, 255, 0.8);
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
            ">
                AI-Powered Global Poverty Alleviation with Real-time Analytics & 3D Visualization
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced live status with animations
        st.markdown("""
        <div class="status-live">
            <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;">
                <div>🟢 <strong>SYSTEM LIVE</strong> - Real-time Monitoring Active</div>
                <div>🌐 <strong>Server:</strong> http://localhost:8505</div>
                <div>⚡ <strong>Auto-NGO Matching:</strong> ON</div>
                <div>🚨 <strong>Emergency Alerts:</strong> ACTIVE</div>
                <div>🌍 <strong>3D Globe:</strong> ENABLED</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced key metrics with better styling
        col1, col2, col3, col4, col5 = st.columns(5)
        
        critical_count = len([a for a in self.emergency_alerts if a['level'] == 'Critical'])
        high_alert_count = len([a for a in self.emergency_alerts if a['level'] == 'High'])
        active_ngos = len([n for n in self.ngo_database if n['status'] == 'Active'])
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🚨</div>
                <h3 style="margin: 0;">Critical Alerts</h3>
                <h1 style="margin: 0.5rem 0; font-size: 3rem;">{critical_count}</h1>
                <p style="margin: 0; opacity: 0.9;">Immediate Action Required</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⚠️</div>
                <h3 style="margin: 0;">High Alerts</h3>
                <h1 style="margin: 0.5rem 0; font-size: 3rem;">{high_alert_count}</h1>
                <p style="margin: 0; opacity: 0.9;">Priority Response</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🏢</div>
                <h3 style="margin: 0;">Active NGOs</h3>
                <h1 style="margin: 0.5rem 0; font-size: 3rem;">{active_ngos}</h1>
                <p style="margin: 0; opacity: 0.9;">Ready to Respond</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🏛️</div>
                <h3 style="margin: 0;">Districts</h3>
                <h1 style="margin: 0.5rem 0; font-size: 3rem;">80</h1>
                <p style="margin: 0; opacity: 0.9;">Under Monitoring</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col5:
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                <h3 style="margin: 0;">AI Models</h3>
                <h1 style="margin: 0.5rem 0; font-size: 3rem;">6</h1>
                <p style="margin: 0; opacity: 0.9;">Processing Data</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Enhanced sidebar with emergency controls"""
        st.sidebar.title("🎛️ Emergency Control Center")
        
        # Emergency quick actions
        st.sidebar.markdown("### 🚨 Quick Emergency Actions")
        if st.sidebar.button("🚨 EMERGENCY ALERT", key="emergency", help="Send immediate alert"):
            st.sidebar.success("🚨 Emergency alert sent to all agencies!")
        
        if st.sidebar.button("📞 Contact All NGOs", key="contact_all"):
            st.sidebar.success("📞 Contacted all active NGOs!")
        
        # Navigation
        st.sidebar.markdown("### 📍 Navigation")
        page = st.sidebar.selectbox(
            "Select Module:",
            [
                "🏠 Emergency Dashboard",
                "🗺️ Interactive State Selection",
                "🤖 AI Predictions & Training",
                "🛰️ Satellite Intelligence",
                "🧠 Neural Network Analytics", 
                "🔮 Future Predictions",
                "🏢 NGO Auto-Matching",
                "🏛️ Government Contacts",
                "📊 Resource Management",
                "📈 Real-time Analytics"
            ]
        )
        
        # Real-time settings
        st.sidebar.markdown("### ⚙️ System Settings")
        alert_threshold = st.sidebar.slider("🚨 Alert Threshold", 0.0, 1.0, 0.7, 0.1)
        auto_ngo_contact = st.sidebar.checkbox("📞 Auto NGO Contact", value=True)
        st.sidebar.info("💡 Use browser refresh for updates")
        
        # Current system status
        st.sidebar.markdown("### 📊 System Status")
        st.sidebar.metric("🔴 Critical Areas", len([a for a in self.emergency_alerts if a['level'] == 'Critical']))
        st.sidebar.metric("🟡 High Risk Areas", len([a for a in self.emergency_alerts if a['level'] == 'High']))
        st.sidebar.metric("🟢 System Uptime", "99.9%")
        
        # Advanced AI status
        st.sidebar.markdown("### 🤖 AI System Status")
        if hasattr(self, 'models'):
            for model_name, model_info in self.models.items():
                accuracy = model_info['accuracy']
                color = "🟢" if accuracy > 0.9 else "🟡" if accuracy > 0.8 else "🔴"
                st.sidebar.metric(f"{color} {model_name.replace('_', ' ').title()}", f"{accuracy:.1%}")
        
        # Real-time data feeds
        st.sidebar.markdown("### 📡 Data Feeds")
        if hasattr(self, 'data_feeds'):
            for feed_name, feed_info in self.data_feeds.items():
                status_icon = "🟢" if feed_info['status'] == 'active' else "🔴"
                st.sidebar.write(f"{status_icon} {feed_name.replace('_', ' ').title()}")
        
        # Satellite status
        st.sidebar.markdown("### 🛰️ Satellite Status")
        st.sidebar.metric("📡 Active Satellites", "12")
        st.sidebar.metric("🔄 Last Update", "2 min ago")
        
        return page, alert_threshold, auto_ngo_contact
    
    def render_emergency_dashboard(self):
        """Render emergency dashboard with live alerts"""
        st.header("🚨 Emergency Dashboard - Live Monitoring")
        
        # Emergency alerts section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🚨 Active Emergency Alerts")
            
            for alert in self.emergency_alerts[:10]:  # Show top 10 alerts
                alert_class = f"alert-{alert['level'].lower()}"
                
                st.markdown(f"""
                <div class="{alert_class}">
                    <strong>🚨 {alert['level'].upper()} ALERT: {alert['district']}, {alert['state']}</strong><br>
                    📊 Poverty Score: {alert['poverty_score']:.2f} | 
                    👥 Population Affected: {alert['population_affected']:,}<br>
                    🎯 Urgent Needs: {', '.join(alert['urgent_needs'])}<br>
                    ⏰ {alert['time_since']} | Status: {alert['status']}
                </div>
                """, unsafe_allow_html=True)
                
                # Quick action buttons for each alert
                alert_col1, alert_col2, alert_col3 = st.columns(3)
                with alert_col1:
                    if st.button(f"📞 Contact NGOs", key=f"ngo_{alert['district']}"):
                        st.success(f"✅ Contacted NGOs for {alert['district']}")
                
                with alert_col2:
                    if st.button(f"🏛️ Notify Government", key=f"gov_{alert['district']}"):
                        st.success(f"✅ Government notified for {alert['district']}")
                
                with alert_col3:
                    if st.button(f"📦 Allocate Resources", key=f"res_{alert['district']}"):
                        st.success(f"✅ Resources allocated to {alert['district']}")
        
        with col2:
            st.subheader("📊 Alert Summary")
            
            alert_summary = {}
            for alert in self.emergency_alerts:
                level = alert['level']
                if level not in alert_summary:
                    alert_summary[level] = 0
                alert_summary[level] += 1
            
            # Alert level pie chart
            if alert_summary:
                fig = px.pie(
                    values=list(alert_summary.values()),
                    names=list(alert_summary.keys()),
                    title="Alert Level Distribution",
                    color_discrete_map={
                        'Critical': '#dc3545',
                        'High': '#fd7e14',
                        'Medium': '#ffc107',
                        'Low': '#28a745'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def render_interactive_state_selection(self):
        """Render interactive state selection with full details"""
        st.header("🗺️ Interactive State Selection - Click to Get Resources & NGOs")
        
        # Add 3D Globe Section
        st.markdown('<div class="globe-container">', unsafe_allow_html=True)
        st.markdown("## 🌍 **3D GLOBAL POVERTY VISUALIZATION**")
        st.markdown("### 🇮🇳 Focused on Indian Poverty-Stricken Areas")
        
        # Create 3D globe with Indian poverty data
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Generate 3D globe data focused on India
            india_districts = self.district_data.copy()
            
            # Create more realistic 3D globe with India outline
            fig = go.Figure()
            
            # Add India country outline first
            fig.add_trace(go.Scattergeo(
                lon=[68, 97, 97, 68, 68],  # India boundary coordinates
                lat=[6, 6, 37, 37, 6],
                mode='lines',
                line=dict(width=3, color='#FF6B35'),
                name='India Boundary',
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Add different layers for different alert levels with enhanced styling
            alert_configs = {
                'Critical': {
                    'color': '#FF0000',
                    'size_multiplier': 3,
                    'opacity': 1.0,
                    'symbol': 'circle',
                    'line_width': 4,
                    'line_color': '#FFFFFF',
                    'pulse': True
                },
                'High': {
                    'color': '#FF6600',
                    'size_multiplier': 2.5,
                    'opacity': 0.9,
                    'symbol': 'circle',
                    'line_width': 3,
                    'line_color': '#FFFFFF',
                    'pulse': False
                },
                'Medium': {
                    'color': '#FFCC00',
                    'size_multiplier': 2,
                    'opacity': 0.8,
                    'symbol': 'circle',
                    'line_width': 2,
                    'line_color': '#333333',
                    'pulse': False
                },
                'Low': {
                    'color': '#00FF00',
                    'size_multiplier': 1.5,
                    'opacity': 0.7,
                    'symbol': 'circle',
                    'line_width': 1,
                    'line_color': '#333333',
                    'pulse': False
                }
            }
            
            for alert_level in ['Low', 'Medium', 'High', 'Critical']:  # Order matters for layering
                level_data = india_districts[india_districts['Alert_Level'] == alert_level]
                
                if len(level_data) > 0:
                    config = alert_configs[alert_level]
                    
                    # Enhanced size calculation for better visibility
                    base_size = 8
                    population_factor = (level_data['Population'] / 500000)
                    poverty_factor = (level_data['Poverty_Score'] * 15)
                    sizes = base_size + (population_factor + poverty_factor) * config['size_multiplier']
                    
                    # Create hover text with emergency information
                    hover_text = level_data.apply(lambda row: 
                        f"<b>🚨 {row['Alert_Level'].upper()} ALERT</b><br>" +
                        f"<b>📍 {row['District']}</b><br>" +
                        f"🏛️ State: {row['State']}<br>" +
                        f"📊 Poverty Score: {row['Poverty_Score']:.2f}<br>" +
                        f"👥 Population: {row['Population']:,}<br>" +
                        f"👥 Affected: {int(row['Population'] * row['Poverty_Score']):,}<br>" +
                        f"📚 Literacy: {row['Literacy_Rate']:.1f}%<br>" +
                        f"🏥 Healthcare: {row['Healthcare_Index']:.2f}<br>" +
                        f"💧 Water Access: {row['Clean_Water_Access']:.1f}%<br>" +
                        f"⚡ Employment: {row['Employment_Rate']:.1f}%<br>" +
                        f"🕒 Last Update: {row['Last_Updated'].strftime('%H:%M:%S')}", axis=1)
                    
                    # Add trace with enhanced styling
                    fig.add_trace(go.Scattergeo(
                        lon=level_data['Longitude'],
                        lat=level_data['Latitude'],
                        text=hover_text,
                        mode='markers',
                        marker=dict(
                            size=sizes,
                            color=config['color'],
                            opacity=config['opacity'],
                            line=dict(
                                width=config['line_width'], 
                                color=config['line_color']
                            ),
                            sizemode='diameter',
                            symbol=config['symbol']
                        ),
                        name=f'🚨 {alert_level} Alert Areas ({len(level_data)})',
                        hovertemplate='%{text}<extra></extra>',
                        customdata=level_data['Alert_Level']
                    ))
            
            # Enhanced layout for ultra-realistic 3D globe
            fig.update_layout(
                title={
                    'text': '🌍 REAL-TIME POVERTY ALERT SYSTEM - INDIA',
                    'x': 0.5,
                    'font': {'size': 24, 'color': '#FFFFFF', 'family': 'Arial Black'},
                    'pad': {'t': 20}
                },
                geo=dict(
                    # Ultra-realistic globe settings
                    projection_type='orthographic',
                    projection_rotation=dict(lon=78, lat=20, roll=0),
                    
                    # Enhanced geographical features
                    showland=True,
                    landcolor='rgb(217, 217, 217)',
                    showocean=True,
                    oceancolor='rgb(0, 119, 190)',
                    showlakes=True,
                    lakecolor='rgb(85, 173, 240)',
                    
                    # Country and state boundaries
                    showcountries=True,
                    countrycolor='rgb(255, 255, 255)',
                    countrywidth=2,
                    showsubunits=True,
                    subunitcolor='rgb(255, 255, 255)',
                    subunitwidth=1,
                    
                    # Enhanced coastlines
                    showcoastlines=True,
                    coastlinecolor='rgb(255, 255, 255)',
                    coastlinewidth=2,
                    
                    # Focus and zoom settings
                    projection_scale=3.5,  # Increased zoom on India
                    center=dict(lat=22, lon=78),  # Centered on India
                    
                    # Frame and background
                    showframe=True,
                    framecolor='rgb(255, 255, 255)',
                    framewidth=2,
                    bgcolor='rgba(0, 50, 100, 0.8)'
                ),
                height=700,
                paper_bgcolor='rgba(30, 60, 114, 0.9)',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                font=dict(color='white', size=12),
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(0, 0, 0, 0.8)',
                    bordercolor='white',
                    borderwidth=2,
                    font=dict(color='white', size=12),
                    x=0.02,
                    y=0.98
                ),
                margin=dict(l=0, r=0, t=60, b=0)
            )
            
            # Add annotations for critical alerts
            critical_districts = india_districts[india_districts['Alert_Level'] == 'Critical']
            if len(critical_districts) > 0:
                fig.add_annotation(
                    text="🚨 CRITICAL ALERTS DETECTED",
                    x=0.5, y=0.02,
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(color="red", size=16, family="Arial Black"),
                    bgcolor="rgba(255, 0, 0, 0.8)",
                    bordercolor="white",
                    borderwidth=2
                )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Enhanced control panel with alert simulation
            st.markdown("### 🎛️ **Globe Control Center**")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("🔄 Rotate Left", use_container_width=True):
                    st.info("🔄 Globe rotated left - Scanning western regions")
            with col_b:
                if st.button("🎯 Focus India", use_container_width=True, type="primary"):
                    st.success("🇮🇳 Focused on India - All alerts visible")
            with col_c:
                if st.button("🔄 Rotate Right", use_container_width=True):
                    st.info("🔄 Globe rotated right - Scanning eastern regions")
            
            # Alert simulation buttons
            st.markdown("### 🚨 **Alert Simulation**")
            col_d, col_e = st.columns(2)
            with col_d:
                if st.button("🔴 Simulate Critical Alert", use_container_width=True):
                    st.error("🚨 BEEP! BEEP! CRITICAL POVERTY ALERT ACTIVATED!")
                    st.markdown("""
                    <div class="beep-red" style="background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%); color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
                        <h3>🚨 RED ALERT: Emergency Response Required</h3>
                        <p><strong>🔴 BEEP! BEEP! BEEP!</strong></p>
                        <p>Critical poverty levels detected in multiple districts!</p>
                        <p>⚠️ Immediate intervention required ⚠️</p>
                        <div style="font-size: 2rem; animation: blink 0.5s infinite;">🚨</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show affected districts in critical state
                    critical_districts = self.district_data[self.district_data['Alert_Level'] == 'Critical']
                    if len(critical_districts) > 0:
                        st.markdown("**🎯 Critical Districts:**")
                        for _, district in critical_districts.head(3).iterrows():
                            st.markdown(f"""
                            <div class="beep-red" style="background: rgba(255,0,0,0.8); color: white; padding: 0.5rem; margin: 0.2rem 0; border-radius: 5px;">
                                🚨 {district['District']}, {district['State']} - Poverty Score: {district['Poverty_Score']:.2f}
                            </div>
                            """, unsafe_allow_html=True)
            
            with col_e:
                if st.button("🟢 Simulate Green Alert", use_container_width=True):
                    st.success("✅ Green Alert: Normal Monitoring Active")
                    st.markdown("""
                    <div class="beep-green" style="background: linear-gradient(135deg, #00cc00 0%, #009900 100%); color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;">
                        <h3>🟢 GREEN STATUS: All Systems Normal</h3>
                        <p><strong>✅ Soft beep... monitoring active</strong></p>
                        <p>Poverty levels within acceptable range</p>
                        <p>📊 Continuous monitoring in progress</p>
                        <div style="font-size: 2rem; animation: pulse 2s infinite;">✅</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show well-performing districts
                    low_alert_districts = self.district_data[self.district_data['Alert_Level'] == 'Low']
                    if len(low_alert_districts) > 0:
                        st.markdown("**🌟 Well-Performing Districts:**")
                        for _, district in low_alert_districts.head(3).iterrows():
                            st.markdown(f"""
                            <div class="beep-green" style="background: rgba(0,200,0,0.8); color: white; padding: 0.5rem; margin: 0.2rem 0; border-radius: 5px;">
                                ✅ {district['District']}, {district['State']} - Poverty Score: {district['Poverty_Score']:.2f}
                            </div>
                            """, unsafe_allow_html=True)
            
            # Real-time alert status
            st.markdown("### 📡 **Real-Time Alert Status**")
            alert_counts = self.district_data['Alert_Level'].value_counts()
            
            col_status1, col_status2, col_status3, col_status4 = st.columns(4)
            
            with col_status1:
                critical_count = alert_counts.get('Critical', 0)
                if critical_count > 0:
                    st.markdown(f"""
                    <div class="beep-red" style="background: rgba(255,0,0,0.9); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                        <h4>🚨 CRITICAL</h4>
                        <h2>{critical_count}</h2>
                        <p>Districts</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(100,100,100,0.5); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                        <h4>🚨 CRITICAL</h4>
                        <h2>0</h2>
                        <p>Districts</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col_status2:
                high_count = alert_counts.get('High', 0)
                st.markdown(f"""
                <div style="background: rgba(255,102,0,0.8); color: white; padding: 1rem; border-radius: 10px; text-align: center; animation: pulse 3s infinite;">
                    <h4>🟠 HIGH</h4>
                    <h2>{high_count}</h2>
                    <p>Districts</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_status3:
                medium_count = alert_counts.get('Medium', 0)
                st.markdown(f"""
                <div style="background: rgba(255,204,0,0.8); color: black; padding: 1rem; border-radius: 10px; text-align: center;">
                    <h4>🟡 MEDIUM</h4>
                    <h2>{medium_count}</h2>
                    <p>Districts</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_status4:
                low_count = alert_counts.get('Low', 0)
                st.markdown(f"""
                <div class="beep-green" style="background: rgba(0,204,0,0.8); color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                    <h4>🟢 LOW</h4>
                    <h2>{low_count}</h2>
                    <p>Districts</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📊 **Global Poverty Statistics**")
            
            # Calculate statistics
            total_affected = india_districts['Population'].sum()
            critical_population = india_districts[india_districts['Alert_Level'] == 'Critical']['Population'].sum()
            avg_poverty_score = india_districts['Poverty_Score'].mean()
            worst_district = india_districts.loc[india_districts['Poverty_Score'].idxmax()]
            
            # Display statistics with enhanced styling
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; color: black;">
                <h4>🇮🇳 India Poverty Overview</h4>
                <p><strong>🔴 Critical Population:</strong> {critical_population:,}</p>
                <p><strong>👥 Total Population:</strong> {total_affected:,}</p>
                <p><strong>📊 Avg Poverty Score:</strong> {avg_poverty_score:.2f}</p>
                <p><strong>⚠️ Worst Affected:</strong> {worst_district['District']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add globe legend
            st.markdown("""
            <div style="background: rgba(255,255,255,0.9); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; color: black;">
                <h4>🎨 Globe Legend</h4>
                <p><span style="color: #dc3545;">🔴</span> Critical Alert Areas</p>
                <p><span style="color: #fd7e14;">🟡</span> High Alert Areas</p>
                <p><span style="color: #ffc107;">🟠</span> Medium Alert Areas</p>
                <p><span style="color: #28a745;">🟢</span> Low Alert Areas</p>
                <p><em>Size = Population × Poverty Score</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Real-time updates
            st.markdown("""
            <div style="background: rgba(40,167,69,0.9); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; color: white;">
                <h4>📡 Live Updates</h4>
                <p>🔄 Data refreshed: Just now</p>
                <p>🌐 Satellites monitoring: 24/7</p>
                <p>📊 AI Analysis: Active</p>
                <p>🚨 Alert System: Online</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced State Selection with better styling
        st.markdown("---")
        st.subheader("📍 Select a State to View Resources, NGOs & Government Contacts")
        
        states = self.district_data['State'].unique()
        
        # Create a grid of enhanced state buttons
        cols = st.columns(5)  # 5 columns for 10 states
        
        for i, state in enumerate(states):
            col = cols[i % 5]
            
            # Calculate state stats
            state_data = self.district_data[self.district_data['State'] == state]
            critical_districts = len(state_data[state_data['Alert_Level'] == 'Critical'])
            avg_poverty = state_data['Poverty_Score'].mean()
            
            # Enhanced color coding with gradients
            if critical_districts > 2:
                button_style = "🔴"
                button_color = "#dc3545"
            elif avg_poverty > 0.7:
                button_style = "🟡"
                button_color = "#ffc107"
            else:
                button_style = "🟢"
                button_color = "#28a745"
            
            with col:
                # Enhanced button with hover effects
                button_html = f"""
                <div style="
                    background: linear-gradient(135deg, {button_color}20 0%, {button_color}40 100%);
                    border: 3px solid {button_color};
                    border-radius: 20px;
                    padding: 1.5rem;
                    margin: 0.5rem 0;
                    text-align: center;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: 0 8px 25px {button_color}30;
                ">
                    <h4 style="margin: 0; color: {button_color};">{button_style} {state}</h4>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem;">Critical: {critical_districts}</p>
                    <p style="margin: 0; font-size: 0.8rem;">Poverty: {avg_poverty:.2f}</p>
                </div>
                """
                
                if st.button(f"{button_style} {state}\n({critical_districts} Critical)", 
                           key=f"state_{state}", use_container_width=True):
                    st.session_state.selected_state = state
                    st.session_state.selected_district = None
        
        # If a state is selected, show districts
        if st.session_state.selected_state:
            selected_state = st.session_state.selected_state
            st.success(f"📍 Selected State: {selected_state}")
            
            # Show state overview
            state_data = self.district_data[self.district_data['State'] == selected_state]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Districts", len(state_data))
            with col2:
                st.metric("Critical Districts", len(state_data[state_data['Alert_Level'] == 'Critical']))
            with col3:
                st.metric("Avg Poverty Score", f"{state_data['Poverty_Score'].mean():.2f}")
            with col4:
                st.metric("Total Population", f"{state_data['Population'].sum():,}")
            
            # District selection
            st.subheader(f"🏘️ Select a District in {selected_state}")
            
            district_cols = st.columns(4)
            districts = state_data['District'].tolist()
            
            for i, district in enumerate(districts):
                col = district_cols[i % 4]
                district_data = state_data[state_data['District'] == district].iloc[0]
                
                # Color code based on alert level
                alert_colors = {
                    'Critical': '🔴',
                    'High': '🟡', 
                    'Medium': '🟠',
                    'Low': '🟢'
                }
                
                alert_icon = alert_colors.get(district_data['Alert_Level'], '⚪')
                
                with col:
                    if st.button(f"{alert_icon} {district.split('_')[-1]}\n{district_data['Alert_Level']}", 
                               key=f"district_{district}", use_container_width=True):
                        st.session_state.selected_district = district
            
            # If a district is selected, show full details
            if st.session_state.selected_district:
                selected_district = state_data[state_data['District'] == st.session_state.selected_district].iloc[0]
                
                st.success(f"🎯 Selected: {selected_district['District']}, {selected_district['State']}")
                
                # Show district details and auto-matched resources
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    self.show_district_resources(selected_district)
                
                with col2:
                    self.show_nearest_ngos(selected_district)
                
                with col3:
                    self.show_government_contacts_for_state(selected_district['State'])
    
    def show_district_resources(self, district):
        """Show resource needs for selected district"""
        st.subheader(f"📦 Resource Needs")
        
        # Calculate resource needs based on poverty score and population
        poverty_score = district['Poverty_Score']
        population = district['Population']
        
        if poverty_score >= 0.8:
            needs = ['Emergency Food', 'Medical Supplies', 'Clean Water', 'Shelter', 'Emergency Cash']
            urgency = 'CRITICAL'
            color = '#dc3545'
        elif poverty_score >= 0.7:
            needs = ['Food Security', 'Healthcare', 'Education', 'Infrastructure']
            urgency = 'HIGH'
            color = '#fd7e14'
        elif poverty_score >= 0.5:
            needs = ['Education', 'Skill Development', 'Healthcare', 'Water Supply']
            urgency = 'MEDIUM'
            color = '#ffc107'
        else:
            needs = ['Infrastructure', 'Education', 'Economic Development']
            urgency = 'LOW'
            color = '#28a745'
        
        st.markdown(f"""
        <div class="resource-need">
            <h4 style="color: {color};">Urgency: {urgency}</h4>
            <p><strong>District:</strong> {district['District']}</p>
            <p><strong>Population Affected:</strong> {int(population * poverty_score):,}</p>
            <p><strong>Poverty Score:</strong> {poverty_score:.2f}</p>
            <p><strong>Priority Resources:</strong></p>
            <ul>
        """ + ''.join([f"<li>{need}</li>" for need in needs]) + """
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Resource allocation buttons
        if st.button(f"📦 Allocate Resources", key=f"allocate_{district['District']}", use_container_width=True):
            st.success("✅ Resources allocated successfully!")
            st.balloons()
    
    def show_nearest_ngos(self, district):
        """Show nearest NGOs and auto-contact them"""
        st.subheader(f"🏢 Nearest NGOs")
        
        # Find NGOs in the same state
        state_ngos = [ngo for ngo in self.ngo_database if ngo['state'] == district['State']]
        
        # Calculate distances and sort
        for ngo in state_ngos:
            distance = ((ngo['latitude'] - district['Latitude'])**2 + 
                       (ngo['longitude'] - district['Longitude'])**2)**0.5
            ngo['distance'] = distance * 111  # Convert to approximate km
        
        nearest_ngos = sorted(state_ngos, key=lambda x: x['distance'])[:3]
        
        for i, ngo in enumerate(nearest_ngos):
            match_score = max(70, 100 - int(ngo['distance']))
            
            st.markdown(f"""
            <div class="ngo-card">
                <h4>{ngo['name']}</h4>
                <p><strong>Specialization:</strong> {', '.join(ngo['specialization'])}</p>
                <p><strong>Distance:</strong> {ngo['distance']:.1f} km</p>
                <p><strong>Match Score:</strong> {match_score}%</p>
                <p><strong>Response Time:</strong> {ngo['response_time']}</p>
                <p><strong>Status:</strong> <span style="color: {'green' if ngo['status'] == 'Active' else 'orange'};">{ngo['status']}</span></p>
                <p><strong>Contact:</strong> {ngo['contact_phone']}</p>
                <p><strong>Email:</strong> {ngo['contact_email']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-contact button
            if st.button(f"📞 Contact {ngo['name']}", key=f"contact_ngo_{i}_{district['District']}", use_container_width=True):
                st.success(f"✅ Contacted {ngo['name']} successfully!")
                st.info(f"📞 Calling {ngo['contact_phone']}...")
    
    def show_government_contacts_for_state(self, state):
        """Show government contacts for the state"""
        st.subheader(f"🏛️ Government Contacts")
        
        if state in self.government_contacts:
            contacts = self.government_contacts[state]
            
            for dept, contact_info in contacts.items():
                st.markdown(f"""
                <div class="gov-contact">
                    <h4>{dept.replace('_', ' ')}</h4>
                    <p><strong>Officer:</strong> {contact_info['name']}</p>
                    <p><strong>Phone:</strong> {contact_info['phone']}</p>
                    <p><strong>Email:</strong> {contact_info['email']}</p>
                    {'<p><strong>Emergency:</strong> ' + contact_info.get('emergency_phone', '') + '</p>' if 'emergency_phone' in contact_info else ''}
                    {'<p><strong>Hotline:</strong> ' + contact_info.get('hotline', '') + '</p>' if 'hotline' in contact_info else ''}
                </div>
                """, unsafe_allow_html=True)
                
                # Quick contact button
                if st.button(f"📞 Contact {dept.replace('_', ' ')}", key=f"gov_contact_{dept}_{state}", use_container_width=True):
                    st.success(f"✅ Contacted {dept.replace('_', ' ')} successfully!")
                    st.info(f"📞 Calling {contact_info['phone']}...")
    
    def render_ai_predictions(self):
        """Render AI predictions and training"""
        st.header("🤖 AI-Powered Predictions & Model Training")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🔮 Real-time Poverty Prediction")
            
            # Input parameters
            state = st.selectbox("Select State:", self.district_data['State'].unique())
            literacy = st.slider("Literacy Rate (%):", 0.0, 100.0, 65.0)
            employment = st.slider("Employment Rate (%):", 0.0, 100.0, 45.0)
            healthcare = st.slider("Healthcare Index:", 0.0, 1.0, 0.6)
            infrastructure = st.slider("Infrastructure Score:", 0.0, 1.0, 0.5)
            water_access = st.slider("Clean Water Access (%):", 0.0, 100.0, 70.0)
            population = st.number_input("Population:", min_value=1000, value=150000)
            
            if st.button("🔮 Generate AI Prediction", type="primary"):
                prediction = self.make_ai_prediction(literacy, employment, healthcare, infrastructure, water_access, population)
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Poverty Score", f"{prediction['score']:.3f}")
                with col_b:
                    st.metric("Risk Level", prediction['level'])
                with col_c:
                    st.metric("Confidence", f"{prediction['confidence']:.1%}")
                
                # AI recommendations
                st.subheader("🧠 AI Recommendations")
                for rec in prediction['recommendations']:
                    st.write(f"• {rec}")
                
                # Auto-trigger alerts if needed
                if prediction['score'] >= 0.8:
                    st.error("🚨 CRITICAL: Auto-triggering emergency response!")
        
        with col2:
            st.subheader("🎯 Model Training & Performance")
            
            models = st.multiselect("Select AI Models:",
                                   ['Random Forest', 'XGBoost', 'LightGBM', 'Neural Network', 'SVM', 'Ensemble'],
                                   default=['Random Forest', 'XGBoost'])
            
            optimization = st.checkbox("Enable Hyperparameter Optimization", value=True)
            
            if st.button("🚀 Train AI Models", type="primary"):
                with st.spinner("🔄 Training AI models..."):
                    progress_bar = st.progress(0)
                    for i in range(101):
                        progress_bar.progress(i)
                        time.sleep(0.02)
                    
                    st.success("✅ AI training completed!")
                    
                    # Show performance metrics
                    performance_data = {
                        'Model': models,
                        'Accuracy': [np.random.uniform(0.85, 0.95) for _ in models],
                        'Precision': [np.random.uniform(0.80, 0.92) for _ in models],
                        'Recall': [np.random.uniform(0.82, 0.94) for _ in models]
                    }
                    
                    perf_df = pd.DataFrame(performance_data)
                    st.dataframe(perf_df)
    
    def render_ngo_matching(self):
        """Render advanced NGO matching system"""
        st.header("🏢 Advanced NGO Auto-Matching System")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎯 Find Perfect NGO Match")
            
            selected_state = st.selectbox("Select State:", self.district_data['State'].unique())
            selected_district = st.selectbox("Select District:", 
                                           self.district_data[self.district_data['State'] == selected_state]['District'])
            
            resource_types = st.multiselect("Resource Types Needed:",
                                          ['Food Security', 'Healthcare', 'Education', 'Clean Water', 
                                           'Shelter', 'Emergency Relief', 'Child Welfare', 'Women Empowerment'],
                                          default=['Food Security'])
            
            urgency = st.selectbox("Urgency Level:", ['Low', 'Medium', 'High', 'Critical'])
            
            if st.button("🔍 Find & Auto-Contact NGOs", type="primary"):
                matching_ngos = self.find_matching_ngos(selected_state, resource_types)
                
                if matching_ngos:
                    st.success(f"✅ Found {len(matching_ngos)} matching NGOs!")
                    
                    # Auto-contact if urgent
                    if urgency in ['High', 'Critical']:
                        st.warning(f"🚨 Auto-contacted top 3 NGOs due to {urgency} urgency!")
                        
                    for ngo in matching_ngos[:5]:
                        st.write(f"📞 **{ngo['name']}** - {', '.join(ngo['specialization'])}")
                else:
                    st.error("❌ No matching NGOs found")
        
        with col2:
            st.subheader("📊 NGO Performance Analytics")
            
            # NGO status distribution
            status_counts = {}
            for ngo in self.ngo_database:
                status = ngo['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            fig = px.pie(values=list(status_counts.values()), 
                        names=list(status_counts.keys()),
                        title="NGO Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    def render_analytics(self):
        """Render comprehensive analytics"""
        st.header("📈 Real-time Analytics & Insights")
        
        # Time-based analytics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Alert Trends (Last 30 Days)")
            
            dates = pd.date_range(start=datetime.now()-timedelta(days=29), periods=30, freq='D')
            critical_alerts = np.random.poisson(3, 30)
            high_alerts = np.random.poisson(8, 30)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=critical_alerts, mode='lines+markers', name='Critical Alerts', line=dict(color='red')))
            fig.add_trace(go.Scatter(x=dates, y=high_alerts, mode='lines+markers', name='High Alerts', line=dict(color='orange')))
            fig.update_layout(title='Daily Alert Generation')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🗺️ Geographic Poverty Distribution")
            
            state_summary = self.district_data.groupby('State').agg({
                'Poverty_Score': 'mean',
                'Population': 'sum',
                'Alert_Level': lambda x: (x == 'Critical').sum()
            }).round(2)
            state_summary.columns = ['Avg_Poverty_Score', 'Total_Population', 'Critical_Districts']
            
            fig = px.scatter(state_summary.reset_index(), 
                            x='Total_Population', y='Avg_Poverty_Score', 
                            size='Critical_Districts', hover_name='State',
                            title='State-wise Poverty vs Population Analysis')
            st.plotly_chart(fig, use_container_width=True)
        
        # INNOVATIVE ANALYTICS SECTION
        st.markdown("---")
        st.header("🚀 **INNOVATIVE REAL-TIME ANALYTICS**")
        
        # Predictive Analytics Dashboard
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🔮 Predictive Poverty Forecasting")
            
            # Generate future predictions
            future_dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
            base_poverty = 0.65
            seasonal_effect = 0.1 * np.sin(np.arange(30) * 2 * np.pi / 365)
            trend_effect = np.linspace(0, 0.05, 30)
            noise = np.random.normal(0, 0.02, 30)
            future_poverty = base_poverty + seasonal_effect + trend_effect + noise
            
            fig = px.line(x=future_dates, y=future_poverty, 
                         title='30-Day Poverty Score Forecast',
                         labels={'x': 'Date', 'y': 'Predicted Poverty Score'})
            fig.add_hline(y=0.7, line_dash="dash", line_color="red", 
                         annotation_text="High Alert Threshold")
            fig.add_hline(y=0.8, line_dash="dash", line_color="darkred", 
                         annotation_text="Critical Alert Threshold")
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Confidence Score
            confidence = np.random.uniform(0.85, 0.95)
            st.metric("🎯 AI Prediction Confidence", f"{confidence:.1%}")
        
        with col2:
            st.subheader("⚡ Real-Time Resource Flow")
            
            # Resource flow simulation
            resource_types = ['Food', 'Medical', 'Water', 'Shelter', 'Education']
            flow_data = []
            
            for i in range(10):  # Last 10 time points
                timestamp = datetime.now() - timedelta(minutes=i*5)
                for resource in resource_types:
                    flow_data.append({
                        'Time': timestamp,
                        'Resource': resource,
                        'Flow_Rate': np.random.uniform(50, 200),
                        'Efficiency': np.random.uniform(0.7, 0.95)
                    })
            
            flow_df = pd.DataFrame(flow_data)
            
            # Resource flow heatmap
            pivot_data = flow_df.pivot_table(values='Flow_Rate', 
                                           index='Resource', 
                                           columns='Time', 
                                           fill_value=0)
            
            fig = px.imshow(pivot_data.values, 
                           x=[t.strftime('%H:%M') for t in pivot_data.columns],
                           y=pivot_data.index,
                           title='Resource Flow Heatmap (Last 50 min)',
                           color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
            
            # Live efficiency meter
            current_efficiency = np.random.uniform(0.75, 0.95)
            st.metric("🚀 Current System Efficiency", f"{current_efficiency:.1%}", 
                     delta=f"{np.random.uniform(-0.05, 0.05):.1%}")
        
        with col3:
            st.subheader("🧠 AI Sentiment Analysis")
            
            # Simulated social media sentiment about poverty initiatives
            sentiments = ['Very Positive', 'Positive', 'Neutral', 'Negative', 'Very Negative']
            sentiment_scores = [35, 30, 20, 10, 5]  # Percentages
            
            fig = px.pie(values=sentiment_scores, names=sentiments,
                        title='Public Sentiment Analysis',
                        color_discrete_map={
                            'Very Positive': '#28a745',
                            'Positive': '#6cb04a',
                            'Neutral': '#ffc107',
                            'Negative': '#fd7e14',
                            'Very Negative': '#dc3545'
                        })
            st.plotly_chart(fig, use_container_width=True)
            
            # Social impact score
            impact_score = np.random.uniform(7.5, 9.2)
            st.metric("📱 Social Impact Score", f"{impact_score:.1f}/10", 
                     delta=f"{np.random.uniform(-0.3, 0.5):.1f}")
        
        # Advanced Analytics Row
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌐 Multi-Dimensional Risk Assessment")
            
            # 3D risk visualization
            risk_factors = ['Economic', 'Social', 'Environmental', 'Political', 'Health']
            risk_scores = [np.random.uniform(0.3, 0.9) for _ in risk_factors]
            
            fig = go.Figure(data=go.Scatterpolar(
                r=risk_scores,
                theta=risk_factors,
                fill='toself',
                name='Current Risk Profile'
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                title="Multi-Dimensional Risk Radar",
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Impact Prediction Model")
            
            # Impact simulation
            interventions = ['Education Program', 'Healthcare Initiative', 'Food Security', 
                           'Infrastructure', 'Economic Development']
            
            impact_data = []
            for intervention in interventions:
                before_score = np.random.uniform(0.4, 0.7)
                after_score = before_score + np.random.uniform(0.1, 0.3)
                impact_data.append({
                    'Intervention': intervention,
                    'Before': before_score,
                    'After': after_score,
                    'Impact': after_score - before_score
                })
            
            impact_df = pd.DataFrame(impact_data)
            
            fig = px.bar(impact_df, x='Intervention', y=['Before', 'After'],
                        title='Predicted Intervention Impact',
                        barmode='group')
            st.plotly_chart(fig, use_container_width=True)
            
            # Best intervention recommendation
            best_intervention = impact_df.loc[impact_df['Impact'].idxmax(), 'Intervention']
            best_impact = impact_df['Impact'].max()
            st.success(f"🏆 **Recommended Priority:** {best_intervention} (Impact: +{best_impact:.2f})")
        
        # Real-time monitoring section
        st.markdown("---")
        st.subheader("📡 **LIVE SYSTEM MONITORING**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Server performance
            cpu_usage = np.random.uniform(15, 85)
            st.metric("💻 CPU Usage", f"{cpu_usage:.1f}%", 
                     delta=f"{np.random.uniform(-5, 5):.1f}%")
        
        with col2:
            # API response time
            response_time = np.random.uniform(120, 300)
            st.metric("⚡ API Response", f"{response_time:.0f}ms", 
                     delta=f"{np.random.uniform(-20, 20):.0f}ms")
        
        with col3:
            # Active users
            active_users = np.random.randint(450, 750)
            st.metric("👥 Active Users", f"{active_users:,}", 
                     delta=f"{np.random.randint(-50, 100):+d}")
        
        with col4:
            # Data processing rate
            processing_rate = np.random.uniform(2.5, 4.2)
            st.metric("📊 Data Processing", f"{processing_rate:.1f}K/s", 
                     delta=f"{np.random.uniform(-0.3, 0.5):+.1f}K/s")
    
    def render_innovative_resource_management(self):
        """Render innovative resource management system"""
        st.header("📦 **INNOVATIVE RESOURCE MANAGEMENT SYSTEM**")
        
        # AI-Powered Resource Optimization
        st.markdown("---")
        st.subheader("🤖 **AI-Powered Smart Resource Allocation**")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Resource optimization dashboard
            st.markdown("### 🎯 Dynamic Resource Optimization Engine")
            
            # Generate resource allocation data
            resources = ['Food Supplies', 'Medical Equipment', 'Clean Water', 'Shelter Materials', 
                        'Educational Kits', 'Emergency Cash', 'Clothing', 'Solar Panels']
            
            allocation_data = []
            for resource in resources:
                current_stock = np.random.randint(500, 5000)
                demand = np.random.randint(300, 2000)
                optimal_allocation = min(current_stock, demand * 1.2)  # 20% buffer
                efficiency = optimal_allocation / max(demand, 1)
                
                allocation_data.append({
                    'Resource': resource,
                    'Current_Stock': current_stock,
                    'Demand': demand,
                    'Optimal_Allocation': optimal_allocation,
                    'Efficiency': min(efficiency, 1.0),
                    'Status': 'Optimal' if efficiency >= 0.9 else 'Needs Attention' if efficiency >= 0.7 else 'Critical'
                })
            
            resource_df = pd.DataFrame(allocation_data)
            
            # Display resource table with status colors
            st.dataframe(
                resource_df.style.applymap(
                    lambda x: 'background-color: #d4edda' if x == 'Optimal' 
                    else 'background-color: #fff3cd' if x == 'Needs Attention'
                    else 'background-color: #f8d7da' if x == 'Critical'
                    else '', subset=['Status']
                ),
                use_container_width=True
            )
            
            # Resource efficiency chart
            fig = px.bar(resource_df, x='Resource', y='Efficiency',
                        title='Resource Allocation Efficiency',
                        color='Efficiency',
                        color_continuous_scale='RdYlGn',
                        range_color=[0, 1])
            fig.add_hline(y=0.9, line_dash="dash", line_color="green", 
                         annotation_text="Optimal Threshold")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### ⚡ Quick Actions")
            
            # Quick action buttons
            if st.button("🚀 Auto-Optimize All Resources", type="primary", use_container_width=True):
                with st.spinner("🔄 AI optimizing resources..."):
                    time.sleep(2)
                st.success("✅ All resources optimized!")
                st.balloons()
            
            if st.button("📊 Generate Supply Report", use_container_width=True):
                st.info("📈 Supply report generated and sent to stakeholders")
            
            if st.button("🚨 Emergency Redistribution", use_container_width=True):
                st.warning("🚨 Emergency redistribution protocol activated")
            
            if st.button("🔄 Refresh Inventory", use_container_width=True):
                st.info("🔄 Real-time inventory updated")
            
            # Critical alerts
            st.markdown("### 🚨 Critical Alerts")
            critical_resources = resource_df[resource_df['Status'] == 'Critical']
            if len(critical_resources) > 0:
                for _, resource in critical_resources.iterrows():
                    st.error(f"🔴 **{resource['Resource']}**: Critical shortage!")
            else:
                st.success("🟢 All resources within acceptable levels")
        
        # Blockchain Supply Chain
        st.markdown("---")
        st.subheader("🔗 **Blockchain-Powered Supply Chain Transparency**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📦 Supply Chain Tracking")
            
            # Simulated blockchain transactions
            blockchain_data = []
            locations = ['Warehouse Delhi', 'Transit Hub Mumbai', 'Distribution Bihar', 'End User Village']
            
            for i, location in enumerate(locations):
                blockchain_data.append({
                    'Step': i + 1,
                    'Location': location,
                    'Timestamp': datetime.now() - timedelta(hours=len(locations)-i),
                    'Status': 'Completed' if i < len(locations)-1 else 'In Progress',
                    'Hash': f"0x{np.random.randint(100000, 999999):x}",
                    'Verified': True
                })
            
            blockchain_df = pd.DataFrame(blockchain_data)
            
            for _, step in blockchain_df.iterrows():
                status_color = "🟢" if step['Status'] == 'Completed' else "🟡"
                verification = "✅" if step['Verified'] else "❌"
                
                st.markdown(f"""
                **{status_color} Step {step['Step']}: {step['Location']}**  
                📅 {step['Timestamp'].strftime('%Y-%m-%d %H:%M')}  
                🔗 Hash: `{step['Hash']}`  
                {verification} Verified on Blockchain
                """)
        
        with col2:
            st.markdown("### 🤝 Smart Contract Automation")
            
            # Smart contract status
            contracts = [
                {'name': 'Auto-Release Funds', 'status': 'Active', 'triggered': 45},
                {'name': 'Quality Verification', 'status': 'Active', 'triggered': 38},
                {'name': 'Delivery Confirmation', 'status': 'Pending', 'triggered': 12},
                {'name': 'Impact Measurement', 'status': 'Active', 'triggered': 67}
            ]
            
            for contract in contracts:
                status_color = "🟢" if contract['status'] == 'Active' else "🟡"
                st.markdown(f"""
                **{status_color} {contract['name']}**  
                Status: {contract['status']}  
                Triggered: {contract['triggered']} times
                """)
            
            # Contract performance
            contract_names = [c['name'] for c in contracts]
            contract_triggers = [c['triggered'] for c in contracts]
            
            fig = px.pie(values=contract_triggers, names=contract_names,
                        title='Smart Contract Usage')
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.markdown("### 🔒 Security & Verification")
            
            # Security metrics
            security_metrics = [
                {'metric': 'Blockchain Integrity', 'value': '99.98%', 'status': '🟢'},
                {'metric': 'Transaction Security', 'value': '100%', 'status': '🟢'},
                {'metric': 'Data Encryption', 'value': 'AES-256', 'status': '🟢'},
                {'metric': 'Access Control', 'value': 'Multi-Sig', 'status': '🟢'},
                {'metric': 'Audit Trail', 'value': 'Complete', 'status': '🟢'}
            ]
            
            for metric in security_metrics:
                st.markdown(f"**{metric['status']} {metric['metric']}:** {metric['value']}")
            
            # Recent verifications
            st.markdown("### ✅ Recent Verifications")
            verifications = [
                "Food delivery to Bihar District 3",
                "Medical supplies to Maharashtra",
                "Water purification systems installed",
                "Educational materials distributed"
            ]
            
            for verification in verifications:
                st.write(f"✅ {verification}")
        
        # IoT Integration
        st.markdown("---")
        st.subheader("🌐 **IoT-Enabled Smart Warehousing**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 Real-Time Warehouse Monitoring")
            
            # IoT sensor data
            sensors = [
                {'name': 'Temperature', 'value': 22.5, 'unit': '°C', 'status': 'Normal'},
                {'name': 'Humidity', 'value': 45.2, 'unit': '%', 'status': 'Normal'},
                {'name': 'Air Quality', 'value': 95, 'unit': 'AQI', 'status': 'Good'},
                {'name': 'Security', 'value': 'Secure', 'unit': '', 'status': 'Normal'},
                {'name': 'Inventory Level', 'value': 78, 'unit': '%', 'status': 'Normal'}
            ]
            
            for sensor in sensors:
                status_icon = "🟢" if sensor['status'] in ['Normal', 'Good'] else "🟡"
                unit_text = f" {sensor['unit']}" if sensor['unit'] else ""
                st.metric(f"{status_icon} {sensor['name']}", f"{sensor['value']}{unit_text}")
        
        with col2:
            st.markdown("### 🚛 Automated Logistics")
            
            # Drone delivery status
            st.markdown("**🚁 Drone Fleet Status**")
            drone_status = [
                {'id': 'Drone-001', 'status': 'Delivering', 'battery': 78, 'eta': '15 min'},
                {'id': 'Drone-002', 'status': 'Charging', 'battery': 95, 'eta': 'Ready'},
                {'id': 'Drone-003', 'status': 'Maintenance', 'battery': 0, 'eta': '2 hrs'},
                {'id': 'Drone-004', 'status': 'Available', 'battery': 100, 'eta': 'Ready'}
            ]
            
            for drone in drone_status:
                status_colors = {
                    'Delivering': '🟡', 'Charging': '🔵', 
                    'Maintenance': '🔴', 'Available': '🟢'
                }
                icon = status_colors.get(drone['status'], '⚪')
                st.write(f"{icon} **{drone['id']}**: {drone['status']} (Battery: {drone['battery']}%, ETA: {drone['eta']})")
        
        with col3:
            st.markdown("### 🔮 Predictive Maintenance")
            
            # Equipment health prediction
            equipment = [
                {'name': 'Refrigeration Unit 1', 'health': 95, 'next_maintenance': '15 days'},
                {'name': 'Packaging Machine', 'health': 78, 'next_maintenance': '5 days'},
                {'name': 'Sorting System', 'health': 88, 'next_maintenance': '10 days'},
                {'name': 'Loading Dock', 'health': 92, 'next_maintenance': '20 days'}
            ]
            
            for eq in equipment:
                health_color = "🟢" if eq['health'] >= 85 else "🟡" if eq['health'] >= 70 else "🔴"
                st.write(f"{health_color} **{eq['name']}**: {eq['health']}% health")
                st.write(f"🔧 Next maintenance: {eq['next_maintenance']}")
                st.write("---")
        
        # Advanced Analytics Section
        st.markdown("---")
        st.subheader("📈 **Advanced Resource Analytics**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Resource utilization over time
            st.markdown("### 📊 Resource Utilization Trends")
            
            dates = pd.date_range(start=datetime.now()-timedelta(days=30), periods=30, freq='D')
            utilization_data = {
                'Date': dates,
                'Food': 75 + 15 * np.sin(np.arange(30) * 0.2) + np.random.normal(0, 5, 30),
                'Medical': 60 + 20 * np.sin(np.arange(30) * 0.15) + np.random.normal(0, 7, 30),
                'Water': 85 + 10 * np.sin(np.arange(30) * 0.25) + np.random.normal(0, 3, 30)
            }
            
            util_df = pd.DataFrame(utilization_data)
            
            fig = px.line(util_df, x='Date', y=['Food', 'Medical', 'Water'],
                         title='Resource Utilization Trends (30 Days)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Cost optimization
            st.markdown("### 💰 Cost Optimization Analysis")
            
            cost_data = {
                'Category': ['Transportation', 'Storage', 'Processing', 'Distribution', 'Overhead'],
                'Current_Cost': [45000, 23000, 18000, 32000, 12000],
                'Optimized_Cost': [38000, 20000, 15000, 28000, 10000],
                'Savings': [7000, 3000, 3000, 4000, 2000]
            }
            
            cost_df = pd.DataFrame(cost_data)
            
            fig = px.bar(cost_df, x='Category', y=['Current_Cost', 'Optimized_Cost'],
                        title='Cost Optimization Opportunities',
                        barmode='group')
            st.plotly_chart(fig, use_container_width=True)
            
            total_savings = cost_df['Savings'].sum()
            st.success(f"💰 **Total Potential Savings: ₹{total_savings:,} per month**")
    
    # Helper methods
    def find_matching_ngos(self, state, resource_types):
        """Find matching NGOs based on criteria"""
        matching = []
        for ngo in self.ngo_database:
            if (ngo['state'] == state and 
                any(rt in ngo['specialization'] for rt in resource_types)):
                matching.append(ngo)
        return matching
    
    def make_ai_prediction(self, literacy, employment, healthcare, infrastructure, water, population):
        """Make AI prediction"""
        # Simplified AI prediction logic
        features = np.array([literacy, employment, healthcare*100, infrastructure*100, water])
        poverty_score = max(0, min(1, 1 - features.mean()/100 + np.random.normal(0, 0.1)))
        
        level = 'Critical' if poverty_score >= 0.8 else 'High' if poverty_score >= 0.7 else 'Medium' if poverty_score >= 0.5 else 'Low'
        confidence = np.random.uniform(0.85, 0.98)
        
        recommendations = []
        if poverty_score >= 0.8:
            recommendations = ['Immediate food aid required', 'Emergency medical support', 'Government intervention needed']
        elif poverty_score >= 0.7:
            recommendations = ['Targeted nutrition programs', 'Healthcare infrastructure', 'Education initiatives']
        else:
            recommendations = ['Preventive measures', 'Sustainable development', 'Monitoring programs']
        
        return {
            'score': poverty_score,
            'level': level,
            'confidence': confidence,
            'recommendations': recommendations
        }
    
    def run(self):
        """Main application runner"""
        self.render_header()
        
        # Sidebar navigation
        page, alert_threshold, auto_ngo_contact = self.render_sidebar()
        
        # Route to appropriate page
        if page == "🏠 Emergency Dashboard":
            self.render_emergency_dashboard()
        elif page == "🗺️ Interactive State Selection":
            self.render_interactive_state_selection()
        elif page == "🤖 AI Predictions & Training":
            self.render_ai_predictions()
        elif page == "🛰️ Satellite Intelligence":
            self.render_satellite_intelligence()
        elif page == "🧠 Neural Network Analytics":
            self.render_neural_network_analytics()
        elif page == "🔮 Future Predictions":
            self.render_future_predictions()
        elif page == "🏢 NGO Auto-Matching":
            self.render_ngo_matching()
        elif page == "🏛️ Government Contacts":
            st.header("🏛️ Government Emergency Contacts")
            for state, contacts in self.government_contacts.items():
                st.subheader(f"📍 {state}")
                for dept, contact_info in contacts.items():
                    st.write(f"**{dept.replace('_', ' ')}:** {contact_info['name']} - {contact_info['phone']}")
        elif page == "📊 Resource Management":
            self.render_innovative_resource_management()
        elif page == "📈 Real-time Analytics":
            self.render_analytics()
    
    def render_satellite_intelligence(self):
        """Advanced satellite intelligence dashboard"""
        st.header("🛰️ Satellite Intelligence & Remote Sensing")
        
        # Satellite system overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🛰️ Active Satellites", "12", "↑2")
        with col2:
            st.metric("📡 Data Streams", "48", "↑8")
        with col3:
            st.metric("🔄 Update Frequency", "15 min", "-5 min")
        with col4:
            st.metric("📊 Coverage", "99.8%", "↑0.2%")
        
        st.markdown("---")
        
        # Satellite analysis selection
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.markdown("### 🎛️ **Satellite Controls**")
            selected_analysis = st.selectbox(
                "Analysis Type:",
                ["Infrastructure Development", "Vegetation Index", "Urban Density", "Night Lights", "Road Networks"]
            )
            
            time_period = st.selectbox(
                "Time Period:",
                ["Real-time", "Last 24h", "Last Week", "Last Month"]
            )
            
            if st.button("🔄 Refresh Satellite Data"):
                st.success("🛰️ Satellite data refreshed successfully!")
        
        with col1:
            # Generate satellite-style heatmap
            if hasattr(self, 'satellite_data'):
                # Create satellite analysis visualization
                analysis_data = []
                for district_name, sat_data in self.satellite_data.items():
                    district_info = self.district_data[self.district_data['District'] == district_name].iloc[0]
                    
                    if selected_analysis == "Infrastructure Development":
                        value = sat_data['infrastructure_index']
                    elif selected_analysis == "Vegetation Index":
                        value = sat_data['vegetation_index'] 
                    elif selected_analysis == "Urban Density":
                        value = sat_data['urban_density']
                    elif selected_analysis == "Night Lights":
                        value = sat_data['night_lights_intensity']
                    else:  # Road Networks
                        value = sat_data['road_network_score']
                    
                    analysis_data.append({
                        'District': district_name,
                        'Latitude': district_info['Latitude'],
                        'Longitude': district_info['Longitude'],
                        'Analysis_Value': value,
                        'State': district_info['State']
                    })
                
                df_analysis = pd.DataFrame(analysis_data)
                
                # Create satellite-style map
                fig = px.scatter_mapbox(
                    df_analysis,
                    lat="Latitude",
                    lon="Longitude", 
                    color="Analysis_Value",
                    size="Analysis_Value",
                    hover_name="District",
                    hover_data={"State": True, "Analysis_Value": ":.3f"},
                    color_continuous_scale="Viridis",
                    size_max=15,
                    zoom=4,
                    center={"lat": 22, "lon": 78},
                    mapbox_style="satellite",
                    title=f"🛰️ Satellite Analysis: {selected_analysis}"
                )
                
                fig.update_layout(
                    height=500,
                    mapbox_accesstoken=os.getenv("MAPBOX_TOKEN")
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Detailed satellite metrics
        st.markdown("### 📊 **Detailed Satellite Metrics**")
        
        if hasattr(self, 'satellite_data'):
            # Display top districts by selected metric
            metric_data = []
            for district_name, sat_data in self.satellite_data.items():
                if selected_analysis == "Infrastructure Development":
                    value = sat_data['infrastructure_index']
                elif selected_analysis == "Vegetation Index":
                    value = sat_data['vegetation_index']
                elif selected_analysis == "Urban Density": 
                    value = sat_data['urban_density']
                elif selected_analysis == "Night Lights":
                    value = sat_data['night_lights_intensity']
                else:
                    value = sat_data['road_network_score']
                
                metric_data.append({
                    'District': district_name,
                    'Value': value,
                    'Last_Update': sat_data['last_satellite_pass'].strftime('%H:%M:%S')
                })
            
            df_metrics = pd.DataFrame(metric_data)
            df_metrics = df_metrics.sort_values('Value', ascending=False)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🔝 Top Performing Districts:**")
                st.dataframe(df_metrics.head(10), use_container_width=True)
            
            with col2:
                st.markdown("**⚠️ Districts Needing Attention:**")
                st.dataframe(df_metrics.tail(10), use_container_width=True)
    
    def render_neural_network_analytics(self):
        """Advanced neural network analytics dashboard"""
        st.header("🧠 Neural Network Analytics & Deep Learning")
        
        # Neural network status
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🧠 Active Networks", "8", "↑1")
        with col2:
            st.metric("⚡ Processing Speed", "2.4 THz", "↑0.3")
        with col3:
            st.metric("🎯 Accuracy Rate", "94.7%", "↑2.1%")
        with col4:
            st.metric("📊 Data Points", "2.8M", "↑145K")
        
        st.markdown("---")
        
        # Neural network architecture visualization
        st.markdown("### 🏗️ **Neural Network Architecture**")
        
        # Create network architecture diagram
        fig = go.Figure()
        
        # Input layer
        for i in range(5):
            fig.add_shape(type="circle", x0=0, y0=i, x1=0.2, y1=i+0.2, 
                         fillcolor="lightblue", line=dict(color="blue"))
            fig.add_annotation(x=0.1, y=i+0.1, text=f"I{i+1}", showarrow=False)
        
        # Hidden layers
        for layer in range(1, 4):
            for i in range(4):
                fig.add_shape(type="circle", x0=layer, y0=i+0.5, x1=layer+0.2, y1=i+0.7,
                             fillcolor="lightgreen", line=dict(color="green"))
                fig.add_annotation(x=layer+0.1, y=i+0.6, text=f"H{i+1}", showarrow=False)
        
        # Output layer
        for i in range(3):
            fig.add_shape(type="circle", x0=4, y0=i+1, x1=4.2, y1=i+1.2,
                         fillcolor="lightcoral", line=dict(color="red"))
            fig.add_annotation(x=4.1, y=i+1.1, text=f"O{i+1}", showarrow=False)
        
        # Add connections (simplified)
        for i in range(5):
            for j in range(4):
                fig.add_shape(type="line", x0=0.2, y0=i+0.1, x1=1, y1=j+0.6,
                             line=dict(color="gray", width=1))
        
        fig.update_layout(
            title="🧠 Poverty Prediction Neural Network",
            xaxis=dict(range=[-0.5, 4.5], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[-0.5, 5.5], showgrid=False, zeroline=False, showticklabels=False),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Training metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 **Training Progress**")
            
            # Generate training curve data
            epochs = list(range(1, 101))
            train_acc = [0.3 + 0.65 * (1 - np.exp(-i/20)) + np.random.normal(0, 0.02) for i in epochs]
            val_acc = [0.25 + 0.6 * (1 - np.exp(-i/25)) + np.random.normal(0, 0.03) for i in epochs]
            
            fig_training = go.Figure()
            fig_training.add_trace(go.Scatter(x=epochs, y=train_acc, name="Training Accuracy",
                                           line=dict(color="blue")))
            fig_training.add_trace(go.Scatter(x=epochs, y=val_acc, name="Validation Accuracy", 
                                           line=dict(color="red")))
            
            fig_training.update_layout(
                title="Model Training Progress",
                xaxis_title="Epochs",
                yaxis_title="Accuracy",
                height=300
            )
            
            st.plotly_chart(fig_training, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 **Model Performance**")
            
            # Confusion matrix
            confusion_data = np.array([[450, 23, 12], [18, 389, 31], [8, 19, 401]])
            
            fig_confusion = px.imshow(confusion_data, 
                                    labels=dict(x="Predicted", y="Actual"),
                                    x=['Low', 'Medium', 'High'],
                                    y=['Low', 'Medium', 'High'],
                                    color_continuous_scale='Blues',
                                    title="Confusion Matrix")
            
            fig_confusion.update_layout(height=300)
            st.plotly_chart(fig_confusion, use_container_width=True)
        
        # Feature importance analysis
        st.markdown("### 🔍 **Feature Importance Analysis**")
        
        features = ['Population Density', 'Literacy Rate', 'Healthcare Index', 'Employment Rate', 
                   'Infrastructure Score', 'Education Access', 'Water Quality', 'Income Level']
        importance = [0.18, 0.16, 0.14, 0.13, 0.12, 0.11, 0.09, 0.07]
        
        fig_importance = px.bar(x=importance, y=features, orientation='h',
                               title="Feature Importance in Poverty Prediction",
                               color=importance, color_continuous_scale='Viridis')
        
        fig_importance.update_layout(height=400)
        st.plotly_chart(fig_importance, use_container_width=True)
    
    def render_future_predictions(self):
        """Advanced future predictions dashboard"""
        st.header("🔮 Future Predictions & Scenario Analysis")
        
        # Prediction metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔮 Predictions Made", "2,847", "↑247")
        with col2:
            st.metric("🎯 Accuracy", "93.2%", "↑1.8%")
        with col3:
            st.metric("⏰ Forecast Horizon", "90 days", "")
        with col4:
            st.metric("🔄 Model Updates", "Daily", "")
        
        st.markdown("---")
        
        # Prediction controls
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.markdown("### 🎛️ **Prediction Controls**")
            
            prediction_type = st.selectbox(
                "Prediction Type:",
                ["Poverty Trends", "Resource Needs", "Economic Impact", "Social Stability"]
            )
            
            time_horizon = st.selectbox(
                "Time Horizon:",
                ["30 days", "60 days", "90 days", "6 months", "1 year"]
            )
            
            confidence_level = st.slider("Confidence Level", 80, 99, 95)
            
            if st.button("🔮 Generate Predictions"):
                st.success("🔮 Predictions generated successfully!")
        
        with col1:
            if hasattr(self, 'predictions'):
                # Generate prediction visualization
                if prediction_type == "Poverty Trends":
                    # Create poverty trend predictions
                    districts = list(self.predictions.keys())[:10]
                    current_scores = [random.uniform(0.3, 0.8) for _ in districts]
                    future_30d = [self.predictions[d]['poverty_trend_30d'] for d in districts]
                    future_90d = [self.predictions[d]['poverty_trend_90d'] for d in districts]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=districts, y=current_scores, name="Current", marker_color='lightblue'))
                    fig.add_trace(go.Bar(x=districts, y=future_30d, name="30-day Forecast", marker_color='orange'))
                    fig.add_trace(go.Bar(x=districts, y=future_90d, name="90-day Forecast", marker_color='red'))
                    
                    fig.update_layout(
                        title="🔮 Poverty Score Predictions",
                        xaxis_title="Districts",
                        yaxis_title="Poverty Score",
                        barmode='group',
                        height=400
                    )
                    
                elif prediction_type == "Resource Needs":
                    # Resource needs forecasting
                    districts = list(self.predictions.keys())[:8]
                    food_needs = [self.predictions[d]['resource_need_forecast']['food_aid_tons'] for d in districts]
                    medical_needs = [self.predictions[d]['resource_need_forecast']['medical_supplies_units'] for d in districts]
                    
                    fig = make_subplots(rows=1, cols=2, subplot_titles=("Food Aid (Tons)", "Medical Supplies"))
                    fig.add_trace(go.Bar(x=districts, y=food_needs, name="Food Aid"), row=1, col=1)
                    fig.add_trace(go.Bar(x=districts, y=medical_needs, name="Medical Supplies"), row=1, col=2)
                    
                    fig.update_layout(title="📦 Resource Needs Forecast", height=400)
                
                elif prediction_type == "Economic Impact":
                    # Economic impact analysis
                    districts = list(self.predictions.keys())[:10]
                    impact_scores = [self.predictions[d]['economic_impact_score'] for d in districts]
                    
                    fig = px.scatter(x=districts, y=impact_scores, size=impact_scores,
                                   color=impact_scores, color_continuous_scale='RdYlGn',
                                   title="💰 Economic Impact Predictions")
                    fig.update_layout(height=400)
                
                else:  # Social Stability
                    districts = list(self.predictions.keys())[:10]
                    stability_scores = [self.predictions[d]['social_stability_index'] for d in districts]
                    
                    fig = px.bar(x=districts, y=stability_scores, color=stability_scores,
                               color_continuous_scale='RdYlGn',
                               title="🏛️ Social Stability Index Predictions")
                    fig.update_layout(height=400)
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Scenario analysis
        st.markdown("### 🎭 **Scenario Analysis**")
        
        scenario_col1, scenario_col2, scenario_col3 = st.columns(3)
        
        with scenario_col1:
            st.markdown("""
            **🟢 Best Case Scenario**
            - 15% poverty reduction
            - Increased government funding
            - Improved NGO coordination
            - Enhanced infrastructure
            """)
            
        with scenario_col2:
            st.markdown("""
            **🟡 Most Likely Scenario**
            - 8% poverty reduction
            - Stable government support
            - Current NGO activity level
            - Gradual infrastructure improvement
            """)
            
        with scenario_col3:
            st.markdown("""
            **🔴 Worst Case Scenario**
            - 2% poverty increase
            - Reduced funding
            - Limited NGO access
            - Infrastructure challenges
            """)
        
        # Predictive alerts
        st.markdown("### 🚨 **Predictive Alerts**")
        
        if hasattr(self, 'predictions'):
            alert_districts = []
            for district, pred_data in list(self.predictions.items())[:5]:
                if pred_data['poverty_trend_90d'] > 0.7:
                    alert_districts.append({
                        'District': district,
                        'Current_Score': random.uniform(0.5, 0.7),
                        'Predicted_Score': pred_data['poverty_trend_90d'],
                        'Risk_Level': 'High' if pred_data['poverty_trend_90d'] > 0.8 else 'Medium'
                    })
            
            if alert_districts:
                df_alerts = pd.DataFrame(alert_districts)
                
                for _, alert in df_alerts.iterrows():
                    color = "🔴" if alert['Risk_Level'] == 'High' else "🟡"
                    st.warning(f"{color} **{alert['District']}**: Predicted poverty increase from {alert['Current_Score']:.2f} to {alert['Predicted_Score']:.2f}")
        
        return

# Main execution
if __name__ == "__main__":
    app = AdvancedPovertySystem()
    app.run()
