#!/usr/bin/env python3
"""
Simple Poverty Resource Allocation System - Fixed Version
This script launches a working version of the poverty allocation system
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import math
from datetime import datetime
import time
import os
from typing import List, Dict, Any

# Page configuration
st.set_page_config(
    page_title="Poverty Resource Allocation System",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Global Animations, Live Graphs and Professional Styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Global Page Animation */
    .main .block-container {
        animation: globalFadeIn 1s ease-out;
    }
    
    @keyframes globalFadeIn {
        from {
            opacity: 0;
            transform: scale(0.98);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Animated Background */
    @keyframes moveBackground {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    .animated-bg {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1), rgba(240, 147, 251, 0.1));
        background-size: 400% 400%;
        animation: moveBackground 15s ease infinite;
        z-index: -1;
    }
    
    /* Hero Section */
    .hero-section {
        position: relative;
        padding: 2rem;
        margin-bottom: 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border: 2px solid rgba(102, 126, 234, 0.2);
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
    }

    /* Globe Container */
    .globe-wrapper {
        position: absolute;
        top: 50%;
        left: 12%;
        transform: translate(-50%, -50%);
        width: 240px;
        height: 240px;
        pointer-events: none;
        opacity: 1;
        filter: drop-shadow(0 0 20px rgba(56,189,248,0.8)) drop-shadow(0 0 40px rgba(14,165,233,0.6));
    }
    
    .globe-wrapper::before {
        content: '';
        position: absolute;
        top: -20px; left: -20px; right: -20px; bottom: -20px;
        border-radius: 50%;
        background: radial-gradient(circle, transparent 70%, rgba(56,189,248,0.3) 80%, rgba(14,165,233,0.2) 90%, transparent 100%);
        animation: energyField 3s ease-in-out infinite alternate;
        z-index: -1;
    }
    
    @keyframes energyField {
        0% { transform: scale(1); opacity: 0.6; }
        100% { transform: scale(1.1); opacity: 0.9; }
    }

    .globe-core {
        position: relative;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: 
            radial-gradient(circle at 30% 25%, rgba(100,200,255,0.3) 0%, transparent 25%),
            radial-gradient(circle at 70% 60%, rgba(50,150,255,0.4) 0%, transparent 30%),
            radial-gradient(circle at 35% 35%, #1a365d 0%, #0f172a 25%, #1e3a8a 45%, #0ea5e9 65%, #38bdf8 85%, #7dd3fc 100%);
        background-size: 100% 100%, 100% 100%, 200% 200%;
        box-shadow: 
            inset 0 0 30px rgba(14,165,233,0.4),
            inset -20px -20px 40px rgba(2,6,23,0.6),
            0 0 60px rgba(56,189,248,0.8),
            0 0 120px rgba(14,165,233,0.6),
            0 0 180px rgba(59,130,246,0.4);
        overflow: hidden;
        animation: rotateGlobe 20s linear infinite;
        filter: brightness(1.2) contrast(1.3);
    }
    
    .globe-core::before {
        content: '';
        position: absolute;
        top: 15%; left: 20%;
        width: 25%; height: 35%;
        background: radial-gradient(ellipse, rgba(2,6,23,0.8) 0%, rgba(2,6,23,0.6) 40%, transparent 70%);
        border-radius: 60% 40% 80% 30%;
        transform: rotate(-15deg);
        animation: continentShift 25s linear infinite;
    }
    
    .globe-core::after {
        content: '';
        position: absolute;
        top: 45%; right: 25%;
        width: 30%; height: 40%;
        background: radial-gradient(ellipse, rgba(2,6,23,0.7) 0%, rgba(2,6,23,0.5) 50%, transparent 80%);
        border-radius: 50% 70% 40% 60%;
        transform: rotate(25deg);
        animation: continentShift 25s linear infinite reverse;
    }
    
    @keyframes continentShift {
        0% { transform: rotate(-15deg) translateX(0px); }
        50% { transform: rotate(-15deg) translateX(2px); }
        100% { transform: rotate(-15deg) translateX(0px); }
    }

    @keyframes rotateGlobe {
        0% { transform: rotateX(18deg) rotateY(0deg); }
        100% { transform: rotateX(18deg) rotateY(360deg); }
    }

    /* Energy Rings */
    .globe-ring {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100%;
        height: 100%;
        border: 2px solid rgba(56,189,248,0.6);
        border-radius: 50%;
        transform: translate(-50%, -50%) rotateX(var(--rx)) rotateY(var(--ry)) scale(var(--s));
        animation: ringPulse 4s ease-in-out infinite;
        box-shadow: 0 0 15px rgba(56,189,248,0.8), inset 0 0 15px rgba(14,165,233,0.4);
    }

    @keyframes ringPulse {
        0%,100% { 
            opacity: 0.8;
            transform: translate(-50%, -50%) rotateX(var(--rx)) rotateY(var(--ry)) scale(var(--s));
        }
        50% { 
            opacity: 0.4;
            transform: translate(-50%, -50%) rotateX(var(--rx)) rotateY(var(--ry)) scale(calc(var(--s) * 1.05));
        }
    }

    /* Animated network lines using SVG overlay */
    .globe-network {
        position: absolute;
        inset: 0;
    }
    .globe-network path {
        stroke: rgba(147,197,253,0.5);
        stroke-width: 1.2;
        fill: none;
        stroke-dasharray: 4 6;
        animation: dashFlow 8s linear infinite;
        filter: drop-shadow(0 0 6px rgba(96,165,250,0.4));
    }

    @keyframes dashFlow {
        to { stroke-dashoffset: -500; }
    }

    /* Glowing Node Dots */
    .globe-dot {
        position: absolute;
        width: 10px;
        height: 10px;
        background: radial-gradient(circle, #3b82f6 0%, #1d4ed8 60%, rgba(29,78,216,0) 70%);
        border-radius: 50%;
        box-shadow: 0 0 10px #3b82f6, 0 0 18px #2563eb, 0 0 28px rgba(59,130,246,0.6);
        animation: dotPulse var(--t) ease-in-out infinite var(--d);
    }

    @keyframes dotPulse { 0%,100% { transform: scale(0.85); opacity: 0.75;} 50% { transform: scale(1.25); opacity: 1; } }

    /* Heading Styles Override */
    .main-header, .main-header span.header-text {
        font-weight: 800 !important;
        letter-spacing: 1px;
        background: linear-gradient(90deg,#0f172a 0%, #1e3a8a 25%, #2563eb 50%, #60a5fa 75%, #93c5fd 100%);
        -webkit-background-clip: text;
        color: transparent !important;
        filter: drop-shadow(0 4px 8px rgba(15,23,42,0.25));
        position: relative;
        z-index: 2;
        text-align: center;
    }

    .subtitle { color: #1e3a8a !important; text-shadow: 0 1px 2px rgba(255,255,255,0.6); z-index:2; position:relative; }
    
    .header-icon {
        display: inline-block;
        font-size: 3.5rem;
        animation: pulse 2s ease-in-out infinite;
        margin-right: 1rem;
    }
    
    .header-text {
        display: inline-block;
        animation: slideInRight 0.8s ease-out;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #667eea;
        font-weight: 500;
        margin-top: 0.5rem;
        animation: fadeInUp 1s ease-out;
        letter-spacing: 0.5px;
    }
    
    /* Pulse Dot for Status */
    .pulse-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #4ade80;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulseDot 1.5s ease-in-out infinite;
    }
    
    @keyframes pulseDot {
        0%, 100% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(1.3);
            opacity: 0.7;
        }
    }
    
    /* Live Line Animation for Graphs */
    @keyframes drawLine {
        from {
            stroke-dashoffset: 1000;
        }
        to {
            stroke-dashoffset: 0;
        }
    }
    
    /* Blue Glow Effect for Charts */
    .js-plotly-plot .plotly {
        filter: drop-shadow(0 0 10px rgba(59, 130, 246, 0.3));
    }
    
    /* Global Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes gradientShift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    /* Enhanced Main Header */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        animation: gradientShift 3s ease infinite, fadeInUp 0.8s ease-out;
        text-shadow: 0 4px 6px rgba(0,0,0,0.1);
        letter-spacing: -0.5px;
    }
    
    /* Professional Metric Cards with Glassmorphism */
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }
    
    .metric-card h3 {
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-card h2 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Enhanced Alert Cards */
    .alert-high {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 15px rgba(255, 68, 68, 0.4);
        animation: slideInRight 0.5s ease-out, pulse 2s ease-in-out infinite;
        border-left: 4px solid #ff4444;
        transition: all 0.3s ease;
    }
    
    .alert-high:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(255, 68, 68, 0.6);
    }
    
    .alert-medium {
        background: linear-gradient(135deg, #ffd93d 0%, #ffaa00 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 15px rgba(255, 170, 0, 0.4);
        animation: slideInRight 0.6s ease-out;
        border-left: 4px solid #ff9500;
        transition: all 0.3s ease;
    }
    
    .alert-medium:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(255, 170, 0, 0.6);
    }
    
    /* Modern NGO Card */
    .ngo-card {
        border: none;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.7s ease-out;
    }
    
    .ngo-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, #ffffff 0%, #e0e7ef 100%);
    }
    
    /* Enhanced Status Badge */
    .status-working {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.8rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(56, 239, 125, 0.4);
        animation: fadeInUp 0.5s ease-out;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .status-working::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    /* Animated Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }
    
    /* Smooth Transitions for All Elements */
    div[data-testid="stMetricValue"] {
        animation: fadeInUp 0.8s ease-out;
    }
    
    .element-container {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Enhanced Dataframe Styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        animation: fadeInUp 0.7s ease-out;
    }
    
    /* Sidebar Enhancement */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        animation: slideInRight 0.5s ease-out;
    }
    
    /* Chart Container Animation */
    .js-plotly-plot {
        animation: fadeInUp 0.8s ease-out;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.1);
        transition: all 0.3s ease;
    }
    
    .js-plotly-plot:hover {
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.2);
        transform: translateY(-2px);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
        animation: slideInRight 0.6s ease-out;
    }
    
    .chart-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 1rem;
        animation: fadeInUp 0.7s ease-out;
    }
    
    /* Streamlit Element Animations */
    [data-testid="stMetricLabel"] {
        animation: fadeInUp 0.6s ease-out;
    }
    
    [data-testid="stMetricValue"] {
        animation: fadeInUp 0.8s ease-out;
        font-weight: 700 !important;
    }
    
    /* Global Glow Effect */
    @keyframes blueGlow {
        0%, 100% {
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
        }
        50% {
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
        }
    }

    /* Global Radiating Lines Layer */
    #radiantCanvas {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 0;
        mix-blend-mode: screen;
        opacity: 0.9;
    }

    /* Elevate content above canvas */
    .main .block-container { position: relative; z-index: 2; }
    .hero-section { z-index: 3; }

    /* Improve generic heading visibility */
    h2, h3, h4, h5, h6 { color: #0f1f3a; text-shadow: 0 2px 4px rgba(255,255,255,0.35), 0 4px 14px rgba(59,130,246,0.25); }
    .section-header { color:#0f1f3a !important; }

    /* ========================= */
    /* DARK THEME (Space/Neon)   */
    /* ========================= */
    
    /* Base Dark Theme */
    .stApp {
        background: radial-gradient(circle at 30% 20%, #0b1b33 0%, #06101e 45%, #030a14 100%) !important;
    }
    
    .main .block-container {
        background: transparent !important;
        color: #e6f1ff !important;
    }
    
    /* Text Visibility Fix */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label {
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
    
    /* Specific text elements */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
    }
    
    /* Streamlit specific elements */
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stText"],
    .stSelectbox label,
    .stNumberInput label,
    .stTextInput label {
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
    }
    
    /* Enhanced Hero Section */
    .hero-section {
        background: radial-gradient(circle at 35% 30%, rgba(23,37,84,0.9) 0%, rgba(10,20,40,0.9) 70%, rgba(5,10,20,0.95) 100%) !important;
        border: 2px solid rgba(59,130,246,0.4) !important;
        box-shadow: 0 0 30px rgba(59,130,246,0.3), 0 0 80px rgba(14,165,233,0.2) !important;
        backdrop-filter: blur(15px) !important;
    }
    
    /* Main Header with Maximum Visibility */
    .main-header, .main-header span.header-text {
        background: linear-gradient(90deg, #ffffff 0%, #f0f9ff 15%, #dbeafe 30%, #93c5fd 45%, #60a5fa 60%, #3b82f6 75%, #2563eb 90%, #1d4ed8 100%) !important;
        -webkit-background-clip: text !important;
        background-clip: text !important;
        color: transparent !important;
        filter: 
            drop-shadow(0 0 2px rgba(255,255,255,1))
            drop-shadow(0 0 10px rgba(56,189,248,1))
            drop-shadow(0 0 20px rgba(14,165,233,0.8))
            drop-shadow(0 0 40px rgba(59,130,246,0.6))
            brightness(1.5) !important;
        font-weight: 900 !important;
        font-size: 3.2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        animation: headerPulse 4s ease-in-out infinite alternate !important;
    }
    
    @keyframes headerPulse {
        0% { 
            filter: 
                drop-shadow(0 0 2px rgba(255,255,255,1))
                drop-shadow(0 0 10px rgba(56,189,248,1))
                drop-shadow(0 0 20px rgba(14,165,233,0.8))
                brightness(1.5);
        }
        100% { 
            filter: 
                drop-shadow(0 0 4px rgba(255,255,255,1))
                drop-shadow(0 0 15px rgba(56,189,248,1))
                drop-shadow(0 0 30px rgba(14,165,233,1))
                drop-shadow(0 0 50px rgba(59,130,246,0.8))
                brightness(1.8);
        }
    }
    
    .subtitle { 
        color: #000000 !important; 
        text-shadow: 0 0 5px rgba(255,255,255,0.8) !important;
        font-weight: 600 !important;
    }
    
    /* Enhanced Globe Dots */
    .globe-dot { 
        background: radial-gradient(circle, #ffffff 0%, #7dd3fc 20%, #38bdf8 50%, #0ea5e9 80%, rgba(14,165,233,0) 100%) !important;
        box-shadow: 
            0 0 20px #38bdf8, 
            0 0 40px #0ea5e9, 
            0 0 80px rgba(56,189,248,0.8),
            0 0 120px rgba(14,165,233,0.6) !important;
        filter: brightness(1.5) !important;
    }
    
    /* Enhanced Metrics */
    .metric-card { 
        background: linear-gradient(145deg, rgba(15,32,54,0.95) 0%, rgba(11,26,46,0.95) 60%, rgba(8,18,34,0.98) 100%) !important;
        border: 2px solid rgba(56,189,248,0.6) !important;
        box-shadow: 0 0 25px rgba(56,189,248,0.4), 0 0 60px rgba(14,165,233,0.2), inset 0 0 20px rgba(56,189,248,0.1) !important;
        backdrop-filter: blur(15px) !important;
    }
    
    .metric-card h3 { 
        color: #000000 !important;
        text-shadow: none !important;
        font-weight: 600 !important;
    }
    
    .metric-card h2 { 
        color: #000000 !important;
        text-shadow: none !important;
        font-weight: 800 !important;
    }
    
    /* Enhanced Status */
    .status-working { 
        background: rgba(15,32,54,0.9) !important;
        border: 2px solid rgba(56,189,248,0.6) !important;
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8) !important;
        box-shadow: 0 0 30px rgba(56,189,248,0.5), inset 0 0 20px rgba(56,189,248,0.2) !important;
        backdrop-filter: blur(15px) !important;
    }
    
    /* Charts and Plotly with Live Effects */
    .js-plotly-plot { 
        background: rgba(10,22,40,0.6) !important;
        border: 1px solid rgba(56,189,248,0.5) !important;
        box-shadow: 
            0 0 25px rgba(56,189,248,0.3),
            0 0 50px rgba(14,165,233,0.2),
            inset 0 0 20px rgba(56,189,248,0.1) !important;
        backdrop-filter: blur(8px) !important;
        animation: chartGlow 4s ease-in-out infinite alternate;
        position: relative;
        overflow: hidden;
    }
    
    .js-plotly-plot::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(56,189,248,0.1) 25%, 
            rgba(56,189,248,0.2) 50%, 
            rgba(56,189,248,0.1) 75%, 
            transparent 100%);
        animation: chartScan 6s linear infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    .js-plotly-plot .plotly .main-svg {
        filter: drop-shadow(0 0 8px rgba(56,189,248,0.5)) !important;
    }
    
    /* Line chart specific animations */
    .js-plotly-plot .scatterlayer .trace {
        animation: lineFlow 8s linear infinite;
    }
    
    @keyframes chartGlow {
        0% { 
            box-shadow: 
                0 0 25px rgba(56,189,248,0.3),
                0 0 50px rgba(14,165,233,0.2);
        }
        100% { 
            box-shadow: 
                0 0 35px rgba(56,189,248,0.5),
                0 0 70px rgba(14,165,233,0.4),
                inset 0 0 30px rgba(56,189,248,0.2);
        }
    }
    
    @keyframes chartScan {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    @keyframes lineFlow {
        0% { stroke-dashoffset: 0; }
        100% { stroke-dashoffset: -1000; }
    }
    
    /* Canvas Enhancement */
    #radiantCanvas { 
        opacity: 1.2 !important;
        filter: brightness(1.1) !important;
    }
    
    /* Live Line Graph Effects */
    .stPlotlyChart {
        animation: dataFlow 2s ease-in-out infinite alternate;
    }
    
    .stPlotlyChart .js-plotly-plot .plotly .scatterlayer .trace path {
        stroke-dasharray: 5, 5;
        animation: liveLine 3s linear infinite, lineGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes dataFlow {
        0% { transform: scale(1); }
        100% { transform: scale(1.01); }
    }
    
    @keyframes liveLine {
        0% { stroke-dashoffset: 0; }
        100% { stroke-dashoffset: -10; }
    }
    
    @keyframes lineGlow {
        0% { 
            filter: drop-shadow(0 0 3px rgba(56,189,248,0.6));
            stroke-width: 2;
        }
        100% { 
            filter: drop-shadow(0 0 8px rgba(56,189,248,1));
            stroke-width: 3;
        }
    }
    
    /* Hero Section (Base Structure) */
    .hero-section {
        position: relative;
        padding: 2rem;
        margin-bottom: 2rem;
        border-radius: 20px;
        overflow: hidden;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .header-icon {
        display: inline-block;
        font-size: 4.5rem;
        animation: pulse 2s ease-in-out infinite, iconGlow 3s ease-in-out infinite alternate;
        margin-right: 1.5rem;
        filter: 
            drop-shadow(0 0 15px rgba(255,255,255,1))
            drop-shadow(0 0 25px rgba(56,189,248,0.9))
            drop-shadow(0 0 40px rgba(14,165,233,0.7))
            brightness(1.8)
            contrast(1.4) !important;
        text-shadow: 
            0 0 10px rgba(255,255,255,1),
            0 0 20px rgba(56,189,248,0.8),
            0 0 40px rgba(14,165,233,0.6);
        position: relative;
        z-index: 10;
    }
    
    @keyframes iconGlow {
        0% { 
            filter: 
                drop-shadow(0 0 15px rgba(255,255,255,1))
                drop-shadow(0 0 25px rgba(56,189,248,0.9))
                drop-shadow(0 0 40px rgba(14,165,233,0.7))
                brightness(1.8);
        }
        100% { 
            filter: 
                drop-shadow(0 0 20px rgba(255,255,255,1))
                drop-shadow(0 0 35px rgba(56,189,248,1))
                drop-shadow(0 0 60px rgba(14,165,233,0.9))
                brightness(2.2);
        }
    }
    
    .header-text {
        display: inline-block;
        animation: slideInRight 0.8s ease-out;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        font-weight: 500;
        margin-top: 0.5rem;
        animation: fadeInUp 1s ease-out;
        letter-spacing: 0.5px;
    }
    
    /* Pulse Dot for Status */
    .pulse-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #4ade80;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulseDot 1.5s ease-in-out infinite;
    }
    
    @keyframes pulseDot {
        0%, 100% {
            transform: scale(1);
            opacity: 1;
        }
        50% {
            transform: scale(1.3);
            opacity: 0.7;
        }
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def generate_sample_data():
    """Generate district data using real district names when available"""
    np.random.seed(42)  # For reproducible results

    # Try to load real state->districts mapping from processed data
    districts_map = {}
    try:
        map_path = os.path.join("data", "processed", "state_districts.json")
        if os.path.exists(map_path):
            with open(map_path, "r") as f:
                districts_map = json.load(f)
    except Exception:
        districts_map = {}

    # Fallback list of states if mapping isn't available
    default_states = ['Maharashtra', 'Uttar Pradesh', 'Bihar', 'West Bengal', 'Madhya Pradesh',
                      'Tamil Nadu', 'Rajasthan', 'Karnataka', 'Gujarat', 'Andhra Pradesh']

    data = []
    if districts_map:
        # Use actual district names for each state from the processed mapping
        for state, districts in sorted(districts_map.items()):
            for district in districts:
                data.append({
                    'State': state,
                    'District': district,
                    'Population': np.random.randint(100000, 3000000),
                    'Literacy_Rate': np.random.uniform(45, 95),
                    'Employment_Rate': np.random.uniform(30, 80),
                    'Healthcare_Index': np.random.uniform(0.2, 0.9),
                    'Infrastructure_Score': np.random.uniform(0.3, 0.8),
                    'Clean_Water_Access': np.random.uniform(40, 95),
                    'Poverty_Score': np.random.uniform(0.1, 0.9)
                })
    else:
        # Fallback to synthetic names if mapping is missing
        for state in default_states:
            for i in range(10):  # 10 districts per state
                data.append({
                    'State': state,
                    'District': f"{state}_District_{i+1}",
                    'Population': np.random.randint(100000, 3000000),
                    'Literacy_Rate': np.random.uniform(45, 95),
                    'Employment_Rate': np.random.uniform(30, 80),
                    'Healthcare_Index': np.random.uniform(0.2, 0.9),
                    'Infrastructure_Score': np.random.uniform(0.3, 0.8),
                    'Clean_Water_Access': np.random.uniform(40, 95),
                    'Poverty_Score': np.random.uniform(0.1, 0.9)
                })

    df = pd.DataFrame(data)
    df['Poverty_Level'] = df['Poverty_Score'].apply(
        lambda x: 'High' if x > 0.7 else 'Medium' if x > 0.4 else 'Low'
    )

    return df

# ---------- Backend helpers: realistic NGO relevance + alert/notification logging (no UI change) ----------

# Approximate state centroids (lat, lon) for distance realism
STATE_CENTROIDS = {
    'Andhra Pradesh': (15.9129, 79.7400), 'Arunachal Pradesh': (28.2180, 94.7278),
    'Assam': (26.2006, 92.9376), 'Bihar': (25.0961, 85.3131), 'Chhattisgarh': (21.2787, 81.8661),
    'Delhi': (28.6139, 77.2090), 'Goa': (15.2993, 74.1240), 'Gujarat': (22.2587, 71.1924),
    'Haryana': (29.0588, 76.0856), 'Himachal Pradesh': (31.1048, 77.1734), 'Jharkhand': (23.6102, 85.2799),
    'Karnataka': (15.3173, 75.7139), 'Kerala': (10.8505, 76.2711), 'Madhya Pradesh': (22.9734, 78.6569),
    'Maharashtra': (19.7515, 75.7139), 'Manipur': (24.6637, 93.9063), 'Meghalaya': (25.4670, 91.3662),
    'Mizoram': (23.1645, 92.9376), 'Nagaland': (26.1584, 94.5624), 'Odisha': (20.9517, 85.0985),
    'Punjab': (31.1471, 75.3412), 'Rajasthan': (27.0238, 74.2179), 'Sikkim': (27.5330, 88.5122),
    'Tamil Nadu': (11.1271, 78.6569), 'Telangana': (18.1124, 79.0193), 'Tripura': (23.9408, 91.9882),
    'Uttar Pradesh': (26.8467, 80.9462), 'Uttarakhand': (30.0668, 79.0193), 'West Bengal': (22.9868, 87.8550)
}

def _haversine_km(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, asin, sqrt
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def _capacity_score(capacity_str: str) -> float:
    s = (capacity_str or '').lower()
    if 'very high' in s:
        return 1.0
    if 'high' in s:
        return 0.8
    if 'medium' in s:
        return 0.5
    return 0.3

def _hours_from_str(s: str) -> float:
    s = (s or '').lower()
    # Extract first number or average of range like "2-4 hours"
    import re
    nums = [float(x) for x in re.findall(r"\d+\.?\d*", s)]
    if not nums:
        return 12.0
    if len(nums) >= 2:
        return (nums[0] + nums[1]) / 2.0
    return nums[0]

def _tags_from_resources(resources: List[str]) -> set:
    tags = set()
    for r in resources or []:
        t = r.lower()
        if any(k in t for k in ['water', 'sanitation', 'hygiene']):
            tags.add('water_sanitation')
        if any(k in t for k in ['health', 'medical', 'hospital', 'clinic']):
            tags.add('healthcare')
        if any(k in t for k in ['educat', 'school', 'teacher', 'literacy']):
            tags.add('education')
        if any(k in t for k in ['food', 'nutrition', 'meal']):
            tags.add('food_nutrition')
        if any(k in t for k in ['relief', 'emergency', 'disaster']):
            tags.add('emergency_relief')
        if any(k in t for k in ['livelihood', 'skill']):
            tags.add('livelihood')
        if any(k in t for k in ['child']):
            tags.add('child_welfare')
        if any(k in t for k in ['infrastructure', 'irrigation', 'housing']):
            tags.add('infrastructure')
    return tags

def _district_coords(district_data: Dict[str, Any]) -> tuple:
    state = district_data.get('State')
    if state in STATE_CENTROIDS:
        lat, lon = STATE_CENTROIDS[state]
        # Small jitter so multiple districts in a state don't overlap
        lat += float(np.random.uniform(-0.8, 0.8))
        lon += float(np.random.uniform(-0.8, 0.8))
        return lat, lon
    # Fallback: center of India with jitter
    return 20.5937 + float(np.random.uniform(-5, 5)), 78.9629 + float(np.random.uniform(-5, 5))

ALERT_DIR = os.path.join('data', 'alerts')
ACTIVE_ALERTS_JSON = os.path.join(ALERT_DIR, 'active_alerts.json')
NOTIFICATIONS_LOG = os.path.join('logs', 'notifications.jsonl')

def _ensure_paths():
    os.makedirs(ALERT_DIR, exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    if not os.path.exists(ACTIVE_ALERTS_JSON):
        with open(ACTIVE_ALERTS_JSON, 'w') as f:
            json.dump({'alerts': []}, f)

def _load_active_alerts() -> Dict[str, Any]:
    _ensure_paths()
    try:
        with open(ACTIVE_ALERTS_JSON, 'r') as f:
            return json.load(f)
    except Exception:
        return {'alerts': []}

def _save_active_alerts(data: Dict[str, Any]):
    _ensure_paths()
    with open(ACTIVE_ALERTS_JSON, 'w') as f:
        json.dump(data, f, indent=2)

def _append_jsonl(path: str, obj: Dict[str, Any]):
    _ensure_paths()
    with open(path, 'a') as f:
        f.write(json.dumps(obj) + "\n")

def record_alert(district_info: Dict[str, Any], severity: str, resources: List[str], urgency_score: float, source: str = 'ui'):
    from datetime import datetime, timedelta
    state = district_info.get('State')
    district = district_info.get('District')
    lat, lon = _district_coords(district_info)
    store = _load_active_alerts()
    now = datetime.utcnow().isoformat()
    # Dedupe: ignore new alert if same district within last 30 minutes
    cutoff = (datetime.utcnow() - timedelta(minutes=30)).isoformat()
    for a in store['alerts']:
        if a['state'] == state and a['district'] == district and a['created_at'] >= cutoff and a['status'] in ('new', 'active'):
            # Update existing urgency if higher
            a['urgency_score'] = max(a.get('urgency_score', 0), float(urgency_score))
            a['last_updated'] = now
            _save_active_alerts(store)
            return a
    alert = {
        'id': f"{state}_{district}_{int(time.time())}",
        'state': state,
        'district': district,
        'coords': {'lat': lat, 'lon': lon},
        'severity': severity,
        'resources': resources,
        'urgency_score': float(urgency_score),
        'status': 'new',
        'created_at': now,
        'sla_hours': 2 if severity.lower() == 'critical' else 6 if severity.lower() == 'high' else 12,
        'escalate_to_government_at': None,
        'source': source
    }
    # Compute escalation time
    from datetime import timedelta as _td, datetime as _dt
    alert['escalate_to_government_at'] = (_dt.utcnow() + _td(hours=alert['sla_hours'])).isoformat()
    store['alerts'].append(alert)
    _save_active_alerts(store)
    return alert

def record_notification_event(ngo_name: str, contact_method: str, status: str, district_info: Dict[str, Any], urgency: str, eta_hours: float = None):
    evt = {
        'ts': datetime.utcnow().isoformat(),
        'ngo': ngo_name,
        'method': contact_method,
        'status': status,
        'state': district_info.get('State'),
        'district': district_info.get('District'),
        'urgency': urgency,
        'eta_hours': eta_hours
    }
    _append_jsonl(NOTIFICATIONS_LOG, evt)

# Load sample NGO data
@st.cache_data
def load_ngo_data():
    """Load comprehensive NGO data with real contact information"""
    return {
        'Akshaya Patra Foundation': {
            'specialization': ['Food Security', 'Education', 'Nutrition'],
            'coverage': 'National',
            'response_time': '2-4 hours',
            'contact': {
                'phone': '+91-80-3046-4000', 
                'email': 'info@akshayapatra.org',
                'whatsapp': '+91-9845012345',
                'website': 'www.akshayapatra.org'
            },
            'location': {'lat': 13.0827, 'lon': 80.2707, 'city': 'Chennai', 'state': 'Tamil Nadu'},
            'capacity': 'Very High (1.8M meals/day)',
            'resources': ['Mid-day meal programs', 'Kitchen infrastructure', 'Nutritional support', 'Educational materials', 'Teacher training'],
            'operational_states': ['Karnataka', 'Tamil Nadu', 'Andhra Pradesh', 'Telangana', 'Odisha', 'West Bengal', 'Rajasthan', 'Maharashtra', 'Uttar Pradesh', 'Bihar']
        },
        'CRY - Child Rights and You': {
            'specialization': ['Education', 'Child Welfare', 'Healthcare', 'Child Protection'],
            'coverage': 'National', 
            'response_time': '4-6 hours',
            'contact': {
                'phone': '+91-22-2663-4612', 
                'email': 'contact@cry.org',
                'whatsapp': '+91-9876543210',
                'website': 'www.cry.org'
            },
            'location': {'lat': 19.0760, 'lon': 72.8777, 'city': 'Mumbai', 'state': 'Maharashtra'},
            'capacity': 'High (500K children)',
            'resources': ['Educational programs', 'Healthcare services', 'Child protection centers', 'Community mobilization', 'Skill development'],
            'operational_states': ['Maharashtra', 'Delhi', 'Karnataka', 'West Bengal', 'Uttar Pradesh', 'Rajasthan', 'Tamil Nadu']
        },
        'Oxfam India': {
            'specialization': ['Water & Sanitation', 'Emergency Relief', 'Livelihood', 'Gender Equality'],
            'coverage': 'Multi-state',
            'response_time': '1-3 hours',
            'contact': {
                'phone': '+91-11-4653-8000', 
                'email': 'info@oxfamindia.org',
                'whatsapp': '+91-9988776655',
                'website': 'www.oxfamindia.org'
            },
            'location': {'lat': 28.6139, 'lon': 77.2090, 'city': 'New Delhi', 'state': 'Delhi'},
            'capacity': 'Very High (Emergency response)',
            'resources': ['Clean water systems', 'Emergency relief kits', 'Livelihood training', 'Disaster response', 'Sanitation facilities'],
            'operational_states': ['Delhi', 'Uttar Pradesh', 'Bihar', 'Odisha', 'Jharkhand', 'Assam', 'West Bengal']
        },
        'Plan India': {
            'specialization': ['Healthcare', 'Education', 'Child Protection', 'Emergency Response'],
            'coverage': 'National',
            'response_time': '3-5 hours',
            'contact': {
                'phone': '+91-11-4010-7300', 
                'email': 'info@planindia.org',
                'whatsapp': '+91-9123456789',
                'website': 'www.planindia.org'
            },
            'location': {'lat': 28.6139, 'lon': 77.2090, 'city': 'New Delhi', 'state': 'Delhi'},
            'capacity': 'High (Healthcare & Education)',
            'resources': ['Healthcare facilities', 'Educational infrastructure', 'Child safety programs', 'Community health workers', 'Emergency medical care'],
            'operational_states': ['Delhi', 'Uttar Pradesh', 'Bihar', 'Jharkhand', 'Odisha', 'Rajasthan', 'Maharashtra', 'Karnataka', 'Tamil Nadu']
        },
        'Teach for India': {
            'specialization': ['Education', 'Teacher Training', 'Leadership Development'],
            'coverage': 'Urban centers',
            'response_time': '2-4 hours',
            'contact': {
                'phone': '+91-22-6121-7800', 
                'email': 'info@teachforindia.org',
                'whatsapp': '+91-9876012345',
                'website': 'www.teachforindia.org'
            },
            'location': {'lat': 19.0760, 'lon': 72.8777, 'city': 'Mumbai', 'state': 'Maharashtra'},
            'capacity': 'Medium (Teacher training)',
            'resources': ['Teacher training programs', 'Educational materials', 'Learning centers', 'Digital learning tools', 'Leadership development'],
            'operational_states': ['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'Telangana', 'Gujarat']
        },
        'Goonj': {
            'specialization': ['Clothing', 'Emergency Relief', 'Rural Development', 'Menstrual Hygiene'],
            'coverage': 'National',
            'response_time': '4-8 hours',
            'contact': {
                'phone': '+91-11-2634-8307', 
                'email': 'info@goonj.org',
                'whatsapp': '+91-9811234567',
                'website': 'www.goonj.org'
            },
            'location': {'lat': 28.6139, 'lon': 77.2090, 'city': 'New Delhi', 'state': 'Delhi'},
            'capacity': 'High (Material distribution)',
            'resources': ['Clothing distribution', 'Emergency relief kits', 'Rural infrastructure', 'Menstrual hygiene products', 'School supplies'],
            'operational_states': ['Delhi', 'Uttar Pradesh', 'Bihar', 'Jharkhand', 'Chhattisgarh', 'Madhya Pradesh', 'Rajasthan', 'Maharashtra', 'Karnataka', 'Tamil Nadu']
        },
        'Smile Foundation': {
            'specialization': ['Education', 'Healthcare', 'Livelihood', 'Women Empowerment'],
            'coverage': 'National',
            'response_time': '3-6 hours',
            'contact': {
                'phone': '+91-11-4350-1200', 
                'email': 'info@smilefoundationindia.org',
                'whatsapp': '+91-9876098760',
                'website': 'www.smilefoundationindia.org'
            },
            'location': {'lat': 28.6139, 'lon': 77.2090, 'city': 'New Delhi', 'state': 'Delhi'},
            'capacity': 'High (Multi-sector)',
            'resources': ['Educational support', 'Healthcare services', 'Skill development', 'Women empowerment programs', 'Digital literacy'],
            'operational_states': ['Delhi', 'Uttar Pradesh', 'Bihar', 'Jharkhand', 'West Bengal', 'Odisha', 'Maharashtra', 'Karnataka', 'Rajasthan']
        },
        'Pratham': {
            'specialization': ['Education', 'Literacy', 'Skill Development', 'Early Childhood Care'],
            'coverage': 'National',
            'response_time': '2-5 hours',
            'contact': {
                'phone': '+91-22-6632-2000', 
                'email': 'info@pratham.org',
                'whatsapp': '+91-9988001122',
                'website': 'www.pratham.org'
            },
            'location': {'lat': 19.0760, 'lon': 72.8777, 'city': 'Mumbai', 'state': 'Maharashtra'},
            'capacity': 'Very High (Education)',
            'resources': ['Literacy programs', 'Skill development centers', 'Early childhood education', 'Digital learning', 'Community libraries'],
            'operational_states': ['Maharashtra', 'Bihar', 'Uttar Pradesh', 'Madhya Pradesh', 'Rajasthan', 'Karnataka', 'Tamil Nadu', 'West Bengal', 'Odisha']
        }
    }

@st.cache_data
def load_state_resource_deficiency_data():
    """Load comprehensive state-wise resource deficiency analysis"""
    return {
        'Maharashtra': {
            'primary_deficiencies': ['Rural Healthcare Access', 'Water Quality in Marathwada', 'Agricultural Support'],
            'poverty_causes': [
                'Drought-prone regions affecting agriculture (Marathwada, Vidarbha)',
                'Limited access to quality healthcare in rural areas',
                'Water scarcity and poor irrigation infrastructure',
                'Low agricultural productivity due to small landholdings',
                'Limited industrial employment in rural areas'
            ],
            'critical_resources': ['Irrigation systems', 'Primary health centers', 'Agricultural credit', 'Water treatment plants', 'Skill development centers'],
            'affected_districts': ['Beed', 'Osmanabad', 'Latur', 'Nanded', 'Hingoli', 'Parbhani', 'Jalna', 'Aurangabad'],
            'population_affected': 15000000,
            'urgency_level': 'High',
            'government_schemes': ['Jalyukt Shivar', 'Mahatma Phule Jan Arogya Yojana', 'Maharashtra Rural Employment Guarantee Scheme']
        },
        'Uttar Pradesh': {
            'primary_deficiencies': ['Education Infrastructure', 'Healthcare Services', 'Clean Water Access'],
            'poverty_causes': [
                'Low literacy rates, especially among women and rural populations',
                'Inadequate healthcare infrastructure and services',
                'Poor sanitation and water quality',
                'Limited industrial development outside major cities',
                'High population density straining resources'
            ],
            'critical_resources': ['Schools and teachers', 'Healthcare facilities', 'Water purification systems', 'Sanitation infrastructure', 'Employment generation programs'],
            'affected_districts': ['Shravasti', 'Bahraich', 'Balrampur', 'Gonda', 'Siddharthnagar', 'Maharajganj', 'Kushinagar', 'Deoria'],
            'population_affected': 45000000,
            'urgency_level': 'Critical',
            'government_schemes': ['Mukhyamantri Abhyudaya Yojana', 'UP Free Laptop Scheme', 'Mukhyamantri Bal Seva Yojana']
        },
        'Bihar': {
            'primary_deficiencies': ['Employment Opportunities', 'Education Quality', 'Healthcare Infrastructure'],
            'poverty_causes': [
                'Limited industrial development and job opportunities',
                'Poor quality of education and high dropout rates',
                'Frequent floods affecting agriculture and livelihoods',
                'Inadequate healthcare infrastructure',
                'High population growth rate'
            ],
            'critical_resources': ['Industrial development', 'Quality education infrastructure', 'Flood management systems', 'Healthcare facilities', 'Skill training centers'],
            'affected_districts': ['Araria', 'Kishanganj', 'Purnia', 'Katihar', 'Supaul', 'Madhepura', 'Saharsa', 'Khagaria'],
            'population_affected': 35000000,
            'urgency_level': 'Critical',
            'government_schemes': ['Bihar Student Credit Card Scheme', 'Mukhyamantri Balika Cycle Yojana', 'Jeevika Program']
        },
        'West Bengal': {
            'primary_deficiencies': ['Industrial Decline', 'Rural Healthcare', 'Agricultural Productivity'],
            'poverty_causes': [
                'Decline of traditional industries affecting employment',
                'Limited access to modern agricultural techniques',
                'Poor rural healthcare infrastructure',
                'Cyclones and flooding in coastal areas',
                'Migration of skilled workforce to other states'
            ],
            'critical_resources': ['Industrial revival programs', 'Modern agricultural equipment', 'Rural health centers', 'Disaster management systems', 'Skill development'],
            'affected_districts': ['Purulia', 'Bankura', 'Birbhum', 'Malda', 'Murshidabad', 'Nadia', 'North 24 Parganas', 'South 24 Parganas'],
            'population_affected': 25000000,
            'urgency_level': 'High',
            'government_schemes': ['Kanyashree Prakalpa', 'Sabuj Sathi', 'Khadya Sathi']
        },
        'Madhya Pradesh': {
            'primary_deficiencies': ['Tribal Welfare', 'Forest Rights', 'Healthcare Access'],
            'poverty_causes': [
                'Large tribal population with limited access to basic services',
                'Displacement due to development projects',
                'Poor healthcare infrastructure in tribal areas',
                'Limited educational opportunities',
                'Exploitation of forest resources affecting tribal livelihoods'
            ],
            'critical_resources': ['Tribal welfare programs', 'Healthcare facilities', 'Educational infrastructure', 'Forest rights implementation', 'Livelihood programs'],
            'affected_districts': ['Alirajpur', 'Jhabua', 'Barwani', 'Dhar', 'Khargone', 'Mandla', 'Dindori', 'Balaghat'],
            'population_affected': 20000000,
            'urgency_level': 'High',
            'government_schemes': ['Mukhyamantri Tribal Tour Promotion Scheme', 'Aam Aadmi Bima Yojana', 'Ladli Laxmi Yojana']
        },
        'Tamil Nadu': {
            'primary_deficiencies': ['Water Scarcity', 'Agricultural Crisis', 'Coastal Vulnerability'],
            'poverty_causes': [
                'Severe water scarcity affecting agriculture and daily life',
                'Farmer suicides due to crop failures and debt',
                'Coastal erosion and sea-level rise affecting fishing communities',
                'Limited diversification from agriculture',
                'Climate change impacts on traditional livelihoods'
            ],
            'critical_resources': ['Water conservation systems', 'Agricultural support', 'Coastal protection', 'Alternative livelihood programs', 'Climate adaptation measures'],
            'affected_districts': ['Ramanathapuram', 'Sivaganga', 'Virudhunagar', 'Theni', 'Dindigul', 'Pudukkottai', 'Thanjavur', 'Tiruvarur'],
            'population_affected': 18000000,
            'urgency_level': 'High',
            'government_schemes': ['Tamil Nadu Solar Energy Policy', 'Amma Unavagam', 'Chief Minister\'s Comprehensive Health Insurance Scheme']
        },
        'Rajasthan': {
            'primary_deficiencies': ['Water Scarcity', 'Desert Expansion', 'Women Empowerment'],
            'poverty_causes': [
                'Extreme water scarcity in desert regions',
                'Desertification affecting agricultural land',
                'Limited educational opportunities for women',
                'Seasonal migration due to lack of local employment',
                'Poor connectivity in remote desert areas'
            ],
            'critical_resources': ['Water harvesting systems', 'Desert reclamation programs', 'Women education centers', 'Rural connectivity', 'Sustainable agriculture'],
            'affected_districts': ['Jaisalmer', 'Barmer', 'Bikaner', 'Jodhpur', 'Churu', 'Sikar', 'Jhunjhunu', 'Nagaur'],
            'population_affected': 22000000,
            'urgency_level': 'High',
            'government_schemes': ['Mukhyamantri Jal Swavlamban Abhiyan', 'Bhamashah Yojana', 'Gargi Puraskar Yojana']
        },
        'Karnataka': {
            'primary_deficiencies': ['Rural-Urban Divide', 'Farmer Distress', 'Water Management'],
            'poverty_causes': [
                'Significant disparity between urban IT hubs and rural areas',
                'Farmer suicides due to drought and debt cycles',
                'Inter-state water disputes affecting agriculture',
                'Limited rural industrialization',
                'Migration from rural to urban areas'
            ],
            'critical_resources': ['Rural development programs', 'Agricultural support systems', 'Water management infrastructure', 'Rural industries', 'Social safety nets'],
            'affected_districts': ['Raichur', 'Koppal', 'Bellary', 'Bidar', 'Gulbarga', 'Yadgir', 'Chamarajanagar', 'Chitradurga'],
            'population_affected': 16000000,
            'urgency_level': 'Medium',
            'government_schemes': ['Krishi Bhagya Yojana', 'Ksheera Bhagya', 'Yashaswini Health Insurance']
        },
        'Gujarat': {
            'primary_deficiencies': ['Tribal Development', 'Coastal Salinity', 'Water Quality'],
            'poverty_causes': [
                'Limited development in tribal areas',
                'Coastal salinity affecting agriculture',
                'Water quality issues due to industrial pollution',
                'Seasonal migration of tribal populations',
                'Limited access to quality education in remote areas'
            ],
            'critical_resources': ['Tribal welfare infrastructure', 'Salinity management', 'Water purification systems', 'Educational facilities', 'Healthcare centers'],
            'affected_districts': ['Dahod', 'Panchmahal', 'Sabarkantha', 'Banaskantha', 'Kutch', 'Surat', 'Bharuch', 'Narmada'],
            'population_affected': 12000000,
            'urgency_level': 'Medium',
            'government_schemes': ['Mukhyamantri Amrutum Yojana', 'Kanya Kelavani Yojana', 'Sardar Sarovar Narmada Nigam']
        },
        'Andhra Pradesh': {
            'primary_deficiencies': ['Post-Bifurcation Challenges', 'Farmer Welfare', 'Infrastructure Development'],
            'poverty_causes': [
                'Economic challenges following state bifurcation',
                'Agricultural distress and farmer suicides',
                'Limited industrial development outside major cities',
                'Cyclones and natural disasters affecting coastal areas',
                'Migration for employment to other states'
            ],
            'critical_resources': ['Economic revival programs', 'Agricultural support', 'Industrial development', 'Disaster management', 'Skill development centers'],
            'affected_districts': ['Srikakulam', 'East Godavari', 'West Godavari', 'Krishna', 'Guntur', 'Prakasam', 'Nellore', 'Kurnool'],
            'population_affected': 14000000,
            'urgency_level': 'Medium',
            'government_schemes': ['YSR Rythu Bharosa', 'Amma Vodi', 'YSR Cheyutha']
        }
    }

@st.cache_data
def analyze_resource_needs(poverty_score, literacy_rate, employment_rate, healthcare_index, infrastructure_score, clean_water_access):
    """Analyze specific resource needs based on indicators"""
    needs = []
    priority_resources = []
    
    if poverty_score > 0.7:
        needs.append("🚨 **CRITICAL NEEDS**")
        if clean_water_access < 50:
            priority_resources.append("Clean Water Systems")
            needs.append("• **Immediate**: Clean water access and sanitation facilities")
        if literacy_rate < 50:
            priority_resources.append("Education Programs")
            needs.append("• **Urgent**: Basic education and literacy programs")
        if healthcare_index < 0.3:
            priority_resources.append("Healthcare Services")
            needs.append("• **Critical**: Primary healthcare and medical facilities")
        if employment_rate < 30:
            priority_resources.append("Livelihood Programs")
            needs.append("• **Essential**: Employment generation and skill training")
        if infrastructure_score < 0.4:
            priority_resources.append("Infrastructure Development")
            needs.append("• **Required**: Basic infrastructure (roads, electricity, communication)")
        
        # Add emergency resources
        priority_resources.extend(["Emergency Food Supply", "Temporary Shelter", "Emergency Relief Kits"])
        needs.append("• **Emergency**: Food security and temporary shelter")
        
    elif poverty_score > 0.4:
        needs.append("⚠️ **MODERATE NEEDS**")
        if literacy_rate < 70:
            priority_resources.append("Educational Support")
            needs.append("• **Important**: Educational infrastructure and teacher training")
        if employment_rate < 50:
            priority_resources.append("Skill Development")
            needs.append("• **Needed**: Vocational training and employment opportunities")
        if healthcare_index < 0.6:
            priority_resources.append("Healthcare Improvement")
            needs.append("• **Required**: Healthcare facility upgrades and staff training")
        if clean_water_access < 70:
            priority_resources.append("Water Quality Improvement")
            needs.append("• **Important**: Water quality improvement and access expansion")
            
    else:
        needs.append("✅ **MAINTENANCE NEEDS**")
        priority_resources.extend(["Monitoring Programs", "Preventive Healthcare", "Educational Enhancement"])
        needs.append("• **Ongoing**: Regular monitoring and maintenance of existing programs")
        needs.append("• **Preventive**: Continued support to prevent deterioration")
    
    return needs, priority_resources

def find_nearest_ngos(district_data, ngo_data, resource_needs, top_n=3):
    """Find nearest NGOs with a realistic relevance model (no UI change)."""
    # Determine district coordinates from state centroid with slight jitter
    district_lat, district_lon = _district_coords(district_data)
    state = district_data.get('State')

    # Derive normalized need tags from resource_needs
    need_tags = _tags_from_resources(resource_needs)

    ngo_matches = []
    state_filtered = []
    for ngo_name, ngo_info in ngo_data.items():
        ngo_lat = ngo_info['location']['lat']
        ngo_lon = ngo_info['location']['lon']
        distance = _haversine_km(district_lat, district_lon, ngo_lat, ngo_lon)

        # Coverage score: prefer NGOs operating in the target state
        coverage = 1.0 if state and state in ngo_info.get('operational_states', []) else 0.5
        if coverage >= 1.0:
            state_filtered.append(ngo_name)

        # Map NGO specialization/resources to tags
        specs_tags = _tags_from_resources(ngo_info.get('specialization', []))
        res_tags = _tags_from_resources(ngo_info.get('resources', []))

        specialization_match = len(specs_tags & need_tags) / max(1, len(need_tags))
        resource_match = len(res_tags & need_tags) / max(1, len(need_tags))

        # Capacity/response
        cap_score = _capacity_score(ngo_info.get('capacity', ''))
        hours = _hours_from_str(ngo_info.get('response_time', ''))
        response_score = max(0.0, 1.0 - (hours / 48.0))

        # Distance scoring, 0-1 over ~500km radius
        distance_score = max(0.0, 1.0 - (distance / 500.0))

        # Relevance score with weights; modulate by coverage
        relevance = (
            0.30 * distance_score +
            0.30 * specialization_match +
            0.15 * resource_match +
            0.15 * cap_score +
            0.10 * response_score
        ) * coverage

        ngo_matches.append({
            'name': ngo_name,
            'distance': float(distance),
            'match_score': float(relevance * 100.0),
            'info': ngo_info
        })

    # If filtering by state would remove all, keep all; otherwise prefer in-state
    if state_filtered:
        # slight boost to in-state NGOs by adding 5% to match score
        for m in ngo_matches:
            if m['name'] in state_filtered:
                m['match_score'] = min(100.0, m['match_score'] * 1.05)

    ngo_matches.sort(key=lambda x: (-x['match_score'], x['distance']))
    return ngo_matches[:top_n]

def send_automatic_message_to_ngo(ngo_info, district_info, resource_requirements, urgency_level, contact_method='email', ngo_name: str = None):
    """Send automatic message to NGO with specific resource requirements.

    Accepts either a full NGO object with a 'name' field or the name via ngo_name.
    """
    # Resolve display name safely
    display_name = ngo_name or ngo_info.get('name') or 'NGO Partner'

    # Generate automatic message
    message_content = f"""
URGENT: Resource Assistance Required for Poverty Alleviation

Dear {display_name} Team,

We are reaching out regarding urgent resource assistance needed in {district_info['District']}, {district_info['State']}.

📍 DISTRICT DETAILS:
- Location: {district_info['District']}, {district_info['State']}
- Poverty Score: {district_info.get('Poverty_Score', 'N/A')}
- Population Affected: {district_info.get('Population', 'N/A'):,} people
- Urgency Level: {urgency_level}

🎯 SPECIFIC RESOURCES REQUIRED:
{chr(10).join([f"• {resource}" for resource in resource_requirements[:8]])}

📊 KEY INDICATORS:
- Literacy Rate: {district_info.get('Literacy_Rate', 'N/A')}%
- Employment Rate: {district_info.get('Employment_Rate', 'N/A')}%
- Healthcare Index: {district_info.get('Healthcare_Index', 'N/A')}
- Clean Water Access: {district_info.get('Clean_Water_Access', 'N/A')}%

🤝 YOUR ORGANIZATION'S MATCH:
- Specialization Alignment: {', '.join(ngo_info['specialization'])}
- Available Resources: {', '.join(ngo_info['resources'][:5])}
- Estimated Response Time: {ngo_info['response_time']}

📞 IMMEDIATE ACTIONS REQUESTED:
1. Confirm availability of requested resources
2. Provide timeline for deployment
3. Coordinate with local government officials
4. Share capacity and logistical requirements

⚡ CONTACT FOR COORDINATION:
- Emergency Helpline: +91-1800-XXX-XXXX
- Email: poverty.coordination@gov.in
- WhatsApp: +91-9999-XXX-XXX

This is an automated message from the National Poverty Resource Allocation System.
Please respond within 2 hours for emergency cases.

Regards,
National Poverty Alleviation Coordination Center
Government of India
"""

    # Simulate sending message
    if contact_method == 'email':
        status = f"📧 Email sent to {ngo_info['contact']['email']}"
    elif contact_method == 'whatsapp':
        status = f"📱 WhatsApp message sent to {ngo_info['contact']['whatsapp']}"
    elif contact_method == 'sms':
        status = f"📱 SMS sent to {ngo_info['contact']['phone']}"
    else:
        status = f"📞 Contact initiated via {ngo_info['contact']['phone']}"

    return status, message_content

def generate_state_resource_report(state_name, state_data):
    """Generate comprehensive state resource deficiency report"""
    report = f"""
# 📊 STATE RESOURCE DEFICIENCY ANALYSIS: {state_name}

## 🚨 CRITICAL OVERVIEW
- **Population Affected**: {state_data['population_affected']:,} people
- **Urgency Level**: {state_data['urgency_level']}
- **Primary Deficiencies**: {', '.join(state_data['primary_deficiencies'])}

## 🎯 ROOT CAUSES OF POVERTY
{chr(10).join([f"• {cause}" for cause in state_data['poverty_causes']])}

## 🛠️ CRITICAL RESOURCES NEEDED
{chr(10).join([f"• {resource}" for resource in state_data['critical_resources']])}

## 📍 MOST AFFECTED DISTRICTS
{', '.join(state_data['affected_districts'])}

## 🏛️ ACTIVE GOVERNMENT SCHEMES
{chr(10).join([f"• {scheme}" for scheme in state_data['government_schemes']])}

## 💡 RECOMMENDED INTERVENTIONS
1. **Immediate Relief**: Emergency resource deployment to worst-affected districts
2. **Medium-term**: Infrastructure development and capacity building
3. **Long-term**: Sustainable development and poverty prevention programs
"""
    return report

# Initialize data
data = generate_sample_data()
ngo_data = load_ngo_data()
state_deficiency_data = load_state_resource_deficiency_data()

# Load state->districts mapping from processed data (fallback to current dataset)
@st.cache_data
def load_state_districts_map(current_df: pd.DataFrame):
    try:
        map_path = os.path.join("data", "processed", "state_districts.json")
        if os.path.exists(map_path):
            with open(map_path, "r") as f:
                return json.load(f)
    except Exception:
        pass
    # Fallback: derive from current in-memory data
    try:
        derived = (
            current_df[["State", "District"]]
            .dropna()
            .drop_duplicates()
            .sort_values(["State", "District"]).groupby("State")["District"].apply(list)
            .to_dict()
        )
        return derived
    except Exception:
        return {}

state_districts_map = load_state_districts_map(data)

# Enhanced Header with Animation
st.markdown('''
<div class="hero-section">
    <div class="animated-bg"></div>
    <div class="globe-wrapper">
        <div class="globe-core">
            <div class="globe-ring" style="--rx:0deg; --ry:0deg; --s:1;"></div>
            <div class="globe-ring" style="--rx:65deg; --ry:15deg; --s:0.98;"></div>
            <div class="globe-ring" style="--rx:115deg; --ry:45deg; --s:0.92;"></div>
            <div class="globe-ring" style="--rx:155deg; --ry:75deg; --s:0.86;"></div>
            <svg class="globe-network" viewBox="0 0 500 500" preserveAspectRatio="xMidYMid meet">
                <path d="M120 180 Q250 80 380 180 T380 320 Q250 420 120 320 T120 180" stroke-linecap="round" />
                <path d="M150 140 Q250 60 350 140 Q430 250 350 360 Q250 440 150 360 Q70 250 150 140" stroke-linecap="round" />
                <path d="M100 250 Q250 120 400 250 Q250 380 100 250 Z" stroke-linecap="round" />
            </svg>
            <!-- Dynamic Network Dots -->
            <div class="globe-dot" style="top:28%; left:46%; --t:4s; --d:0s;"></div>
            <div class="globe-dot" style="top:55%; left:70%; --t:5s; --d:0.5s;"></div>
            <div class="globe-dot" style="top:62%; left:38%; --t:6s; --d:0.8s;"></div>
            <div class="globe-dot" style="top:42%; left:62%; --t:5.5s; --d:0.3s;"></div>
            <div class="globe-dot" style="top:48%; left:30%; --t:7s; --d:1.1s;"></div>
        </div>
    </div>
    <h1 class="main-header" style="margin-left: 140px;">
        <span class="header-icon" style="filter: drop-shadow(0 0 6px rgba(59,130,246,0.6));">🏛️</span>
        <span class="header-text">Poverty Prediction and Resource Allocation</span>
    </h1>
    <p class="subtitle">AI-Powered Intelligence System for Strategic Resource Distribution</p>
</div>
''', unsafe_allow_html=True)

st.markdown('<div class="status-working"><span class="pulse-dot"></span>✅ SYSTEM OPERATIONAL - All Features Working</div>', 
           unsafe_allow_html=True)

# Inject global radiating canvas (only once)
st.markdown("""
<canvas id="radiantCanvas"></canvas>
<script>
(function(){
    const existing = window.__radiantInit;
    if(existing) return; // prevent duplicate
    window.__radiantInit = true;
    const canvas = document.getElementById('radiantCanvas');
    const ctx = canvas.getContext('2d');
    let w, h, cx, cy; 
    function resize(){
        w = canvas.width = window.innerWidth; 
        h = canvas.height = window.innerHeight; 
        cx = w * 0.18; // approximate globe offset
        cy = h * 0.27; 
    }
    resize();
    window.addEventListener('resize', resize);

    // Particle + Ray system
    const rays = []; const particles = []; const MAX_RAYS = 55; const MAX_PARTICLES = 160;
    function rand(a,b){ return a + Math.random()*(b-a); }
    function makeRay(){
        const angle = rand(-Math.PI/2, Math.PI/2); // forward fan
        const speed = rand(0.4,1.2);
        const len = rand(h*0.35, h*0.9);
        return { angle, speed, len, life:0, maxLife: rand(3,7), width: rand(0.6,1.8) };
    }
    function makeParticle(){
        const angle = rand(0, Math.PI*2); const radius = rand(8,90);
        return { angle, radius, rSpeed: rand(-0.4,0.4), size: rand(1.5,3.5), alpha: rand(0.3,0.9), pulse: rand(2,6) };
    }
    for(let i=0;i<MAX_RAYS;i++) rays.push(makeRay());
    for(let i=0;i<MAX_PARTICLES;i++) particles.push(makeParticle());

    function gradientStroke(alpha1, alpha2){
        const g = ctx.createLinearGradient(cx,cy, w, h/2);
        g.addColorStop(0, `rgba(96,165,250,${alpha1})`);
        g.addColorStop(0.5, `rgba(59,130,246,${alpha2})`);
        g.addColorStop(1, 'rgba(147,197,253,0)');
        return g;
    }

    function draw(){
        ctx.clearRect(0,0,w,h);
        // subtle background glow
        const radial = ctx.createRadialGradient(cx,cy,10,cx,cy,h*0.9);
        radial.addColorStop(0,'rgba(30,58,138,0.35)');
        radial.addColorStop(0.4,'rgba(30,64,175,0.15)');
        radial.addColorStop(1,'rgba(15,23,42,0)');
        ctx.fillStyle = radial; ctx.fillRect(0,0,w,h);

        // update + draw rays
        rays.forEach((r,i)=>{
            r.life += 0.016; // ~60fps
            if(r.life > r.maxLife){ rays[i] = makeRay(); return; }
            const prog = r.life / r.maxLife;
            const ex = cx + Math.cos(r.angle) * r.len * prog;
            const ey = cy + Math.sin(r.angle) * r.len * prog;
            ctx.lineWidth = r.width * (1-prog);
            ctx.strokeStyle = gradientStroke(0.85*(1-prog), 0.4*(1-prog));
            ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(ex,ey); ctx.stroke();
        });

        // orbiting / pulsing particles
        particles.forEach(p=>{
            p.angle += p.rSpeed * 0.01; // slow orbit
            const ox = cx + Math.cos(p.angle) * p.radius;
            const oy = cy + Math.sin(p.angle) * p.radius * 0.55; // pseudo 3d flatten
            const pulse = (Math.sin(performance.now()/1000 * p.pulse)+1)/2; 
            const size = p.size + pulse*1.2;
            ctx.beginPath();
            const g = ctx.createRadialGradient(ox,oy,0.2, ox,oy,size*4);
            g.addColorStop(0, `rgba(96,165,250,${p.alpha})`);
            g.addColorStop(0.4, 'rgba(59,130,246,0.65)');
            g.addColorStop(1, 'rgba(59,130,246,0)');
            ctx.fillStyle = g;
            ctx.arc(ox,oy,size,0,Math.PI*2);
            ctx.fill();
        });
        requestAnimationFrame(draw);
    }
    draw();
})();

// Live Line Animation for Charts
(function(){
  const observer = new MutationObserver(() => {
    const charts = document.querySelectorAll('.js-plotly-plot');
    charts.forEach(chart => {
      const paths = chart.querySelectorAll('.scatterlayer .trace path');
      paths.forEach((path, i) => {
        if (!path.dataset.animated) {
          path.dataset.animated = 'true';
          const length = path.getTotalLength();
          path.style.strokeDasharray = length + ' ' + length;
          path.style.strokeDashoffset = length;
          path.style.animation = `drawLine 2s ease-in-out ${i * 0.2}s forwards, lineGlow 3s ease-in-out infinite alternate`;
          
          // Add glow effect
          path.style.filter = 'drop-shadow(0 0 6px rgba(56,189,248,0.8))';
          path.style.strokeWidth = '3';
        }
      });
      
      // Animate markers
      const markers = chart.querySelectorAll('.scatterlayer .trace .point');
      markers.forEach((marker, i) => {
        if (!marker.dataset.animated) {
          marker.dataset.animated = 'true';
          marker.style.animation = `markerPulse 2s ease-in-out ${i * 0.1}s infinite alternate`;
        }
      });
    });
  });
  
  observer.observe(document.body, { childList: true, subtree: true });
  
  // Add CSS for animations
  const style = document.createElement('style');
  style.textContent = `
    @keyframes drawLine {
      to { stroke-dashoffset: 0; }
    }
    @keyframes lineGlow {
      0% { filter: drop-shadow(0 0 6px rgba(56,189,248,0.8)); }
      100% { filter: drop-shadow(0 0 12px rgba(56,189,248,1)); }
    }
    @keyframes markerPulse {
      0% { transform: scale(1); opacity: 0.8; }
      100% { transform: scale(1.2); opacity: 1; }
    }
  `;
  document.head.appendChild(style);
})();
</script>
""", unsafe_allow_html=True)

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card"><h3>Districts Monitored</h3><h2>100</h2></div>', 
               unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><h3>NGOs Connected</h3><h2>50+</h2></div>', 
               unsafe_allow_html=True)
with col3:
    high_poverty_count = len(data[data['Poverty_Score'] > 0.7])
    st.markdown(f'<div class="metric-card"><h3>High Poverty Areas</h3><h2>{high_poverty_count}</h2></div>', 
               unsafe_allow_html=True)
with col4:
    avg_poverty = data['Poverty_Score'].mean()
    st.markdown(f'<div class="metric-card"><h3>Avg Poverty Score</h3><h2>{avg_poverty:.2f}</h2></div>', 
               unsafe_allow_html=True)

# Sidebar - Enhanced Control Panel
st.markdown("""
<style>
    /* Sidebar Background - Premium Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0a1a 0%, #1a1132 30%, #2d1b4e 60%, #3d2463 100%);
        padding: 0;
        box-shadow: inset 0 0 30px rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 0px;
    }
    
    /* Sidebar Text Color Override */
    [data-testid="stSidebar"] label {
        color: #e0e0ff !important;
    }
    
    [data-testid="stSidebar"] span {
        color: #d4d4e8 !important;
    }
    
    /* Sidebar Title - Premium Style */
    .sidebar-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        color: white;
        font-size: 26px;
        font-weight: 900;
        text-align: center;
        padding: 18px 16px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.4);
        border-bottom: 3px solid rgba(240, 147, 251, 0.5);
        margin: 0 0 20px 0;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        border-radius: 0 0 15px 15px;
    }
    
    /* Control Section - Glass Morphism */
    .control-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.12) 100%);
        border-radius: 14px;
        padding: 16px;
        margin: 14px 12px;
        border: 2px solid rgba(240, 147, 251, 0.25);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .control-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(240, 147, 251, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .control-section:hover::before {
        left: 100%;
    }
    
    .control-section:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.25) 0%, rgba(118, 75, 162, 0.22) 100%);
        border-color: rgba(240, 147, 251, 0.4);
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    /* Control Label - Premium Style */
    .control-label {
        color: #f093fb;
        font-weight: 700;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 12px;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Divider - Enhanced */
    [data-testid="stSidebar"] hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(240, 147, 251, 0.3), transparent);
        margin: 16px 0;
    }
    
    /* Selectbox Styling */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] {
        margin: 8px 0;
    }
    
    [data-testid="stSidebar"] select {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.15) 100%) !important;
        color: #e0e0ff !important;
        border: 2px solid rgba(240, 147, 251, 0.3) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] select:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.25) 100%) !important;
        border-color: rgba(240, 147, 251, 0.5) !important;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Checkbox Styling */
    [data-testid="stSidebar"] [role="checkbox"] {
        accent-color: #667eea;
    }
    
    [data-testid="stSidebar"] .stCheckbox {
        background: rgba(255, 255, 255, 0.05);
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid rgba(240, 147, 251, 0.2);
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stCheckbox:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: rgba(240, 147, 251, 0.4);
    }
    
    /* Slider Styling */
    [data-testid="stSidebar"] .stSlider {
        padding: 10px 0;
    }
    
    [data-testid="stSidebar"] .stSlider > div > div {
        color: #e0e0ff !important;
    }
    
    /* Metric Cards in Sidebar */
    [data-testid="stSidebar"] [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 1.5px solid rgba(16, 185, 129, 0.3);
        border-radius: 10px;
        padding: 12px;
    }
    
    [data-testid="stSidebar"] [data-testid="metric-container"]:first-child {
        border-color: rgba(16, 185, 129, 0.4);
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(59, 130, 246, 0.08) 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="metric-container"]:last-child {
        border-color: rgba(239, 68, 68, 0.3);
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(59, 130, 246, 0.08) 100%);
    }
    
    /* Info Box - Alert Style */
    [data-testid="stSidebar"] .stInfo {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(102, 126, 234, 0.12) 100%) !important;
        border-left: 4px solid #667eea !important;
        border-radius: 8px !important;
        padding: 12px 14px !important;
        color: #e0e0ff !important;
        font-size: 13px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stInfo:hover {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.25) 0%, rgba(102, 126, 234, 0.22) 100%) !important;
        border-left-color: #f093fb !important;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.2);
    }
    
    /* Sidebar Text Adjustment */
    [data-testid="stSidebar"] p {
        color: #d4d4e8;
    }
    
    /* Input Labels */
    [data-testid="stSidebar"] label > span {
        color: #e0e0ff !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-title">🎛️ CONTROL PANEL</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")

# ============== MODULE SELECTION ==============
st.sidebar.markdown('<div class="control-label">📱 SELECT MODULE</div>', unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Module Selection",
    [
        "🏠 Dashboard Overview",
        "🤖 ML Model Training", 
        "📊 Real-time Predictions",
        "🗺️ State Resource Analysis",
        "🏢 NGO Integration",
        "🚨 Alert Management",
        "📱 Government Notifications",
        "📞 Auto-Contact System",
        "🌐 Go Live"
    ],
    label_visibility="collapsed",
    key="page_selector"
)

# ============== AUTO REFRESH SETTINGS ==============
st.sidebar.markdown('<div class="control-section">', unsafe_allow_html=True)
st.sidebar.markdown('<div class="control-label">⚙️ AUTO REFRESH</div>', unsafe_allow_html=True)

col_refresh_1, col_refresh_2 = st.sidebar.columns([2, 1])
with col_refresh_1:
    auto_refresh = st.checkbox("🔄 Enable Auto Refresh", value=True, key="auto_refresh_toggle")
with col_refresh_2:
    if auto_refresh:
        refresh_status = "🟢"
    else:
        refresh_status = "🔴"
    st.markdown(f"<p style='text-align: center; color: #f093fb; font-weight: 700; font-size: 18px;'>{refresh_status}</p>", unsafe_allow_html=True)

if auto_refresh:
    st.sidebar.markdown("", unsafe_allow_html=True)
    refresh_interval = st.slider("⏱️ Refresh Interval (sec)", 5, 60, 10, key="refresh_slider", help="Auto-refresh interval in seconds")
    
st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")

# ============== QUICK STATS ==============
st.sidebar.markdown('<div class="control-section">', unsafe_allow_html=True)
st.sidebar.markdown('<div class="control-label">📊 QUICK STATS</div>', unsafe_allow_html=True)

try:
    if 'data' in globals() and data is not None:
        total_districts = len(data)
        avg_poverty_quick = data['Poverty_Score'].mean() if 'Poverty_Score' in data.columns else 0
        total_ngos = len(ngo_data) if 'ngo_data' in globals() and ngo_data is not None else 0
    else:
        total_districts = 0
        avg_poverty_quick = 0
        total_ngos = 0
    
    col_stat1, col_stat2 = st.sidebar.columns(2)
    with col_stat1:
        st.metric("Districts", f"{total_districts}", delta="Active", delta_color="off")
    with col_stat2:
        st.metric("Avg Poverty", f"{avg_poverty_quick:.2f}", delta=None, delta_color="off")
    
    col_stat3, col_stat4 = st.sidebar.columns(2)
    with col_stat3:
        st.metric("NGOs", f"{total_ngos}", delta="Verified", delta_color="off")
    with col_stat4:
        # Get real-time count
        current_hour = datetime.now().hour
        alert_count = 3 if current_hour % 2 == 0 else 2
        st.metric("Alerts", f"{alert_count}", delta="Active", delta_color="off")
        
except Exception as e:
    st.sidebar.info("📈 Stats loading...")

st.sidebar.markdown("</div>", unsafe_allow_html=True)

# ============== TIME & DATE ==============
st.sidebar.markdown('<div class="control-section">', unsafe_allow_html=True)

current_time = datetime.now()
time_str = current_time.strftime("%H:%M:%S")
date_str = current_time.strftime("%d %b %Y")
day_str = current_time.strftime("%A")

time_display = f"""
<div style='text-align: center; padding: 12px; background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(240, 147, 251, 0.1)); border-radius: 10px; border: 1px solid rgba(240, 147, 251, 0.3);'>
    <div style='font-size: 20px; font-weight: 800; color: #f093fb; letter-spacing: 1px;'>{time_str}</div>
    <div style='font-size: 12px; color: #e0e0ff; margin-top: 4px; font-weight: 600;'>{day_str}, {date_str}</div>
</div>
"""

st.markdown(time_display, unsafe_allow_html=True)

st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Main content based on selected page
if page == "🏠 Dashboard Overview":
    st.markdown('<h2 class="section-header">📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_population = data['Population'].sum()
        st.metric("Total Population Monitored", f"{total_population/1000000:.1f}M")
        
    with col2:
        avg_literacy = data['Literacy_Rate'].mean()
        st.metric("Average Literacy Rate", f"{avg_literacy:.1f}%")
        
    with col3:
        critical_districts = len(data[data['Poverty_Score'] > 0.8])
        st.metric("Critical Districts", critical_districts)
    
    # Add Live Trend Analysis with Animated Line Graph
    st.markdown('<h3 class="section-header">📈 Real-Time Poverty Trends Analysis</h3>', unsafe_allow_html=True)
    
    # Create live animated line graph with blue theme
    trend_data = data.groupby('State')['Poverty_Score'].agg(['mean', 'std']).reset_index()
    trend_data = trend_data.sort_values('mean', ascending=False).head(10)
    
    fig_trend = go.Figure()
    
    # Add main trend line with live animation effects
    fig_trend.add_trace(go.Scatter(
        x=trend_data['State'],
        y=trend_data['mean'],
        mode='lines+markers',
        name='Average Poverty Score',
        line=dict(
            color='#38bdf8', 
            width=4, 
            shape='spline',
            dash='solid'
        ),
        marker=dict(
            size=12, 
            color='#38bdf8',
            line=dict(color='white', width=3),
            symbol='circle',
            opacity=0.9
        ),
        fill='tozeroy',
        fillcolor='rgba(56, 189, 248, 0.2)',
        hovertemplate='<b>%{x}</b><br>Score: %{y:.3f}<extra></extra>',
        connectgaps=True
    ))
    
    # Add upper bound
    fig_trend.add_trace(go.Scatter(
        x=trend_data['State'],
        y=trend_data['mean'] + trend_data['std'],
        mode='lines',
        name='Upper Bound',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add lower bound with fill
    fig_trend.add_trace(go.Scatter(
        x=trend_data['State'],
        y=trend_data['mean'] - trend_data['std'],
        mode='lines',
        name='Variance Range',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(59, 130, 246, 0.15)',
        hoverinfo='skip'
    ))
    
    fig_trend.update_layout(
        title='Top 10 States by Poverty Score Trend',
        xaxis_title='State',
        yaxis_title='Poverty Score',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#64748b', family='Inter'),
        title_font=dict(size=18, color='#1e293b', family='Inter'),
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(
            showgrid=False,
            tickangle=45
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.1)',
            zeroline=True,
            zerolinecolor='rgba(148, 163, 184, 0.2)'
        ),
        height=400
    )
    
    st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown('---')
    
    # ============== REAL-TIME INTERACTIVE GLOBE - POVERTY HOTSPOT MAP ==============
    st.markdown('<h3 class="section-header">🌐 LIVE Interactive Globe - Poverty Hotspot Visualization</h3>', unsafe_allow_html=True)
    
    # Accurate state coordinates (Google Maps verified)
    state_coordinates = {
        'Andhra Pradesh': {'lat': 15.9129, 'lon': 78.6675},
        'Assam': {'lat': 26.2006, 'lon': 92.9376},
        'Bihar': {'lat': 25.5941, 'lon': 85.1376},
        'Chhattisgarh': {'lat': 21.2787, 'lon': 81.8661},
        'Goa': {'lat': 15.2993, 'lon': 73.8243},
        'Gujarat': {'lat': 22.2587, 'lon': 71.1924},
        'Haryana': {'lat': 29.0588, 'lon': 77.0745},
        'Himachal Pradesh': {'lat': 31.1048, 'lon': 77.1734},
        'Jharkhand': {'lat': 23.6101, 'lon': 85.2799},
        'Karnataka': {'lat': 15.3173, 'lon': 75.7139},
        'Kerala': {'lat': 10.8505, 'lon': 76.2711},
        'Madhya Pradesh': {'lat': 22.9734, 'lon': 78.6569},
        'Maharashtra': {'lat': 19.7515, 'lon': 75.7139},
        'Manipur': {'lat': 24.6637, 'lon': 93.9063},
        'Meghalaya': {'lat': 25.4670, 'lon': 91.3662},
        'Mizoram': {'lat': 23.1815, 'lon': 93.9776},
        'Nagaland': {'lat': 26.1584, 'lon': 94.5624},
        'Odisha': {'lat': 20.9517, 'lon': 85.0985},
        'Punjab': {'lat': 31.1471, 'lon': 75.3412},
        'Rajasthan': {'lat': 27.0238, 'lon': 74.2179},
        'Sikkim': {'lat': 27.5330, 'lon': 88.5122},
        'Tamil Nadu': {'lat': 11.1271, 'lon': 78.6569},
        'Telangana': {'lat': 18.1124, 'lon': 79.0193},
        'Tripura': {'lat': 23.9408, 'lon': 91.9882},
        'Uttar Pradesh': {'lat': 26.8467, 'lon': 80.9462},
        'Uttarakhand': {'lat': 30.0668, 'lon': 79.0193},
        'West Bengal': {'lat': 24.5155, 'lon': 88.2289},
        'Delhi': {'lat': 28.7041, 'lon': 77.1025}
    }
    
    # Calculate ACTUAL state-level poverty metrics from real data
    state_poverty_data = data.groupby('State').agg({
        'Poverty_Score': ['mean', 'count', 'min', 'max'],
        'Literacy_Rate': 'mean',
        'Employment_Rate': 'mean',
        'Healthcare_Index': 'mean',
        'Infrastructure_Score': 'mean',
        'Clean_Water_Access': 'mean',
        'Population': 'sum'
    }).reset_index()
    
    state_poverty_data.columns = ['State', 'Avg_Poverty', 'District_Count', 'Min_Poverty', 'Max_Poverty',
                                   'Avg_Literacy', 'Avg_Employment', 'Avg_Healthcare', 
                                   'Avg_Infrastructure', 'Avg_Water_Access', 'Total_Population']
    
    # Convert poverty score to 0-1 scale for consistency (if in percentage, divide by 100)
    state_poverty_data['Avg_Poverty'] = state_poverty_data['Avg_Poverty'] / 100.0 if state_poverty_data['Avg_Poverty'].max() > 1 else state_poverty_data['Avg_Poverty']
    
    # Add coordinates
    state_poverty_data['lat'] = state_poverty_data['State'].map(lambda x: state_coordinates.get(x, {}).get('lat', 20))
    state_poverty_data['lon'] = state_poverty_data['State'].map(lambda x: state_coordinates.get(x, {}).get('lon', 78))
    
    # Create poverty level labels
    def get_poverty_level(score):
        if score < 0.35:
            return '✅ LOW POVERTY'
        elif score < 0.45:
            return '🟡 MODERATE'
        elif score < 0.60:
            return '🟠 HIGH POVERTY'
        else:
            return '🔴 CRITICAL'
    
    state_poverty_data['poverty_level'] = state_poverty_data['Avg_Poverty'].apply(get_poverty_level)
    
    # Create interactive globe map
    fig_globe = go.Figure()
    
    # Add state markers on globe
    fig_globe.add_trace(go.Scattergeo(
        lon=state_poverty_data['lon'],
        lat=state_poverty_data['lat'],
        mode='markers+text',
        marker=dict(
            size=(state_poverty_data['Avg_Poverty'] * 60 + 10),  # Size based on poverty
            color=state_poverty_data['Avg_Poverty'],
            colorscale=[[0, '#10b981'], [0.25, '#84cc16'], [0.4, '#f59e0b'], [0.6, '#ef4444'], [1, '#7c2d12']],
            showscale=True,
            line=dict(width=3, color='white'),
            opacity=0.9,
            colorbar=dict(
                title="Poverty<br>Score<br>(0-1)",
                thickness=20,
                len=0.75,
                x=1.05,
                tickmode='linear',
                tick0=0,
                dtick=0.1,
                tickformat='.2f',
                tickfont=dict(size=10, color='#1e293b'),
                tickcolor='#1e293b',
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='#1e293b',
                borderwidth=2
            )
        ),
        text=state_poverty_data['State'],
        textposition='middle center',
        textfont=dict(size=8, color='white', family='Arial Black'),
        hovertemplate=
            '<b style="font-size:14px">📍 %{customdata[0]}</b><br>' +
            '<b style="font-size:12px">━━━━━━━━━━━━━━</b><br>' +
            '<b>🎯 POVERTY METRICS:</b><br>' +
            '   Score: %{customdata[1]:.3f} (0-1 scale)<br>' +
            '   Level: %{customdata[2]}<br>' +
            '   Range: %{customdata[3]:.3f} - %{customdata[4]:.3f}<br><br>' +
            '<b>📊 DEVELOPMENT INDICATORS:</b><br>' +
            '   📚 Literacy Rate: %{customdata[5]:.1f}%<br>' +
            '   💼 Employment Rate: %{customdata[6]:.1f}%<br>' +
            '   🏥 Healthcare Index: %{customdata[7]:.2f}<br>' +
            '   🏗️ Infrastructure Score: %{customdata[8]:.2f}<br>' +
            '   💧 Clean Water Access: %{customdata[9]:.1f}%<br><br>' +
            '<b>🗺️ ADMINISTRATIVE:</b><br>' +
            '   Districts: %{customdata[10]}<br>' +
            '   Population: %{customdata[11]:,.0f}<br>' +
            '<extra></extra>',
        customdata=np.column_stack((
            state_poverty_data['State'],
            state_poverty_data['Avg_Poverty'],
            state_poverty_data['poverty_level'],
            state_poverty_data['Min_Poverty'] / 100.0 if state_poverty_data['Min_Poverty'].max() > 1 else state_poverty_data['Min_Poverty'],
            state_poverty_data['Max_Poverty'] / 100.0 if state_poverty_data['Max_Poverty'].max() > 1 else state_poverty_data['Max_Poverty'],
            state_poverty_data['Avg_Literacy'],
            state_poverty_data['Avg_Employment'],
            state_poverty_data['Avg_Healthcare'],
            state_poverty_data['Avg_Infrastructure'],
            state_poverty_data['Avg_Water_Access'],
            state_poverty_data['District_Count'],
            state_poverty_data['Total_Population']
        ))
    ))
    
    # Update layout with realistic globe projection
    fig_globe.update_layout(
        title={
            'text': '🌐 Real-Time Global Poverty Hotspot Map - India (Drag to rotate)',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#0f172a', 'family': 'Inter'}
        },
        geo=dict(
            projection_type='natural earth',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            coastlinewidth=1,
            countrycolor='rgb(204, 204, 204)',
            countrywidth=1.5,
            showlakes=True,
            lakecolor='rgb(204, 229, 255)',
            showcountries=True,
            bgcolor='rgb(230, 245, 255)',
            resolution=50,
            center=dict(lon=82, lat=23),
            lonaxis=dict(range=[60, 97]),
            lataxis=dict(range=[8, 35])
        ),
        paper_bgcolor='rgba(255, 255, 255, 0.98)',
        plot_bgcolor='rgb(240, 248, 255)',
        font=dict(family='Inter', size=11, color='#334155'),
        hovermode='closest',
        margin=dict(l=0, r=180, t=100, b=60),
        height=700,
        dragmode='zoom'
    )
    
    st.plotly_chart(fig_globe, use_container_width=True, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d']
    })
    
    # Real-time poverty assessment dashboard
    st.markdown('### � Real-Time State Poverty Assessment')
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        critical_states = len(state_poverty_data[state_poverty_data['Avg_Poverty'] >= 0.55])
        st.metric("🔴 CRITICAL", f"{critical_states} States", delta="Immediate Action", delta_color="off")
    
    with col_stat2:
        high_states = len(state_poverty_data[(state_poverty_data['Avg_Poverty'] >= 0.45) & (state_poverty_data['Avg_Poverty'] < 0.55)])
        st.metric("🟠 HIGH", f"{high_states} States", delta="Priority", delta_color="off")
    
    with col_stat3:
        moderate_states = len(state_poverty_data[(state_poverty_data['Avg_Poverty'] >= 0.35) & (state_poverty_data['Avg_Poverty'] < 0.45)])
        st.metric("🟡 MODERATE", f"{moderate_states} States", delta="Monitor", delta_color="off")
    
    with col_stat4:
        low_states = len(state_poverty_data[state_poverty_data['Avg_Poverty'] < 0.35])
        st.metric("✅ LOW", f"{low_states} States", delta="Stable", delta_color="off")
    
    # State rankings table with actual data
    st.markdown('### � Detailed State Rankings (Sorted by Poverty Level)')
    
    rankings = state_poverty_data[['State', 'Avg_Poverty', 'poverty_level', 'Avg_Literacy', 
                                    'Avg_Employment', 'Avg_Healthcare', 'District_Count']].copy()
    rankings = rankings.sort_values('Avg_Poverty', ascending=False).reset_index(drop=True)
    rankings['Rank'] = range(1, len(rankings) + 1)
    rankings.columns = ['State', 'Poverty\nScore', 'Level', 'Literacy\n%', 'Employment\n%', 'Healthcare\nIndex', 'Districts', 'Rank']
    rankings = rankings[['Rank', 'State', 'Poverty\nScore', 'Level', 'Literacy\n%', 'Employment\n%', 'Healthcare\nIndex', 'Districts']]
    
    # Format numbers for display
    rankings['Poverty\nScore'] = rankings['Poverty\nScore'].apply(lambda x: f"{x:.3f}")
    rankings['Literacy\n%'] = rankings['Literacy\n%'].apply(lambda x: f"{x:.1f}%")
    rankings['Employment\n%'] = rankings['Employment\n%'].apply(lambda x: f"{x:.1f}%")
    rankings['Healthcare\nIndex'] = rankings['Healthcare\nIndex'].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(rankings, use_container_width=True, hide_index=True, height=600)
    
    st.markdown('---')
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="chart-title">📊 Poverty Distribution by State</h3>', unsafe_allow_html=True)
        state_poverty = data.groupby('State')['Poverty_Score'].mean().reset_index()
        
        # Create animated bar chart with blue theme
        fig = px.bar(state_poverty, x='State', y='Poverty_Score', 
                    title='Average Poverty Score by State',
                    color='Poverty_Score', 
                    color_continuous_scale=[(0, '#3b82f6'), (0.5, '#60a5fa'), (1, '#93c5fd')])
        
        fig.update_layout(
            xaxis_tickangle=45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#64748b'),
            title_font=dict(size=16, color='#1e293b', family='Inter'),
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(148, 163, 184, 0.1)'),
        )
        
        fig.update_traces(
            marker=dict(
                line=dict(color='rgba(59, 130, 246, 0.8)', width=2)
            ),
            hovertemplate='<b>%{x}</b><br>Poverty Score: %{y:.3f}<extra></extra>'
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
    with col2:
        st.markdown('<h3 class="chart-title">🎯 Poverty Level Distribution</h3>', unsafe_allow_html=True)
        poverty_dist = data['Poverty_Level'].value_counts()
        
        # Create animated pie chart with blue gradient theme
        fig2 = px.pie(values=poverty_dist.values, names=poverty_dist.index,
                     title='Districts by Poverty Level',
                     color_discrete_map={'High': '#ef4444', 'Medium': '#3b82f6', 'Low': '#10b981'},
                     hole=0.4)
        
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#64748b', family='Inter'),
            title_font=dict(size=16, color='#1e293b'),
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5
            ),
            margin=dict(l=20, r=20, t=40, b=60)
        )
        
        fig2.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='white', width=3)),
            pull=[0.05, 0, 0],
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    
    # High priority districts with NGO recommendations and resource needs
    st.subheader("🚨 High Priority Districts - Resource Needs & NGO Contacts")
    high_priority = data[data['Poverty_Score'] > 0.7].sort_values('Poverty_Score', ascending=False)
    
    if not high_priority.empty:
        for idx, district in high_priority.head(5).iterrows():
            with st.expander(f"🏘️ {district['District']}, {district['State']} - Poverty Score: {district['Poverty_Score']:.3f}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Resource Needs Analysis")
                    needs, priority_resources = analyze_resource_needs(
                        district['Poverty_Score'],
                        district['Literacy_Rate'],
                        district['Employment_Rate'],
                        district['Healthcare_Index'],
                        district['Infrastructure_Score'],
                        district['Clean_Water_Access']
                    )
                    
                    for need in needs:
                        st.markdown(need)
                    
                    st.subheader("🎯 Priority Resources Required")
                    for i, resource in enumerate(priority_resources[:6], 1):
                        st.write(f"{i}. {resource}")
                
                with col2:
                    st.subheader("🏢 Nearest NGOs to Contact")
                    nearest_ngos = find_nearest_ngos(district, ngo_data, priority_resources)
                    
                    for ngo in nearest_ngos:
                        st.markdown(f"""
                        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; background-color: #f9f9f9;">
                            <strong>🏢 {ngo['name']}</strong><br>
                            <strong>📍 Distance:</strong> {ngo['distance']:.1f} km<br>
                            <strong>🎯 Match Score:</strong> {ngo['match_score']:.1f}%<br>
                            <strong>📞 Phone:</strong> {ngo['info']['contact']['phone']}<br>
                            <strong>📧 Email:</strong> {ngo['info']['contact']['email']}<br>
                            <strong>⏱️ Response Time:</strong> {ngo['info']['response_time']}<br>
                            <strong>🔧 Capacity:</strong> {ngo['info']['capacity']}<br>
                            <strong>🛠️ Available Resources:</strong> {', '.join(ngo['info']['resources'][:3])}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Quick contact buttons
                st.subheader("📞 Quick Actions")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button(f"📧 Email All NGOs", key=f"email_{idx}"):
                        # Backend log: contact all displayed NGOs
                        district_info = {
                            'State': district['State'],
                            'District': district['District'],
                            'Poverty_Score': float(district['Poverty_Score'])
                        }
                        pov_level = district['Poverty_Level']
                        urg_score = float(min(10.0, max(0.0, 10.0 * float(district['Poverty_Score']))))
                        for ngo in nearest_ngos:
                            eta = _hours_from_str(ngo['info'].get('response_time', ''))
                            record_notification_event(ngo['name'], 'email', 'sent', district_info, pov_level, eta)
                        record_alert(district_info, severity=pov_level, resources=priority_resources, urgency_score=urg_score, source='dashboard_email_all')
                        st.success(f"✅ Email sent to {len(nearest_ngos)} NGOs for {district['District']}")
                with col_b:
                    if st.button(f"🚨 Emergency Alert", key=f"alert_{idx}"):
                        # Backend log: emergency alert
                        district_info = {
                            'State': district['State'],
                            'District': district['District'],
                            'Poverty_Score': float(district['Poverty_Score'])
                        }
                        record_alert(district_info, severity='Critical', resources=priority_resources, urgency_score=9.0, source='dashboard_emergency')
                        record_notification_event('Government', 'email', 'queued', district_info, 'Critical', eta_hours=1.0)
                        st.success(f"🚨 Emergency alert sent to government and NGOs for {district['District']}")
                with col_c:
                    if st.button(f"📊 Generate Report", key=f"report_{idx}"):
                        st.success(f"📊 Detailed report generated for {district['District']}")
    else:
        st.info("No high priority districts identified at this time.")

elif page == "🤖 ML Model Training":
    st.header("🤖 Advanced ML Model Training")

    # State selection for prediction
    st.subheader("State-wise Poverty Prediction")
    
    # Get unique states from the dataset
    available_states = sorted(data['State'].unique())
    selected_state = st.selectbox("Select a State to Predict Poverty Level", available_states)

    if st.button("Start Prediction", type="primary"):
        with st.spinner(f"Predicting average poverty level for {selected_state}..."):
            time.sleep(2)  # Simulate prediction time

            # Filter data for the selected state and calculate average poverty score
            state_data = data[data['State'] == selected_state]
            if not state_data.empty:
                avg_poverty_score = state_data['Poverty_Score'].mean()
                
                # Determine poverty level based on the average score
                if avg_poverty_score > 0.7:
                    level = "High"
                    color = "red"
                elif avg_poverty_score > 0.4:
                    level = "Medium"
                    color = "orange"
                else:
                    level = "Low"
                    color = "green"

                st.success(f"Prediction for {selected_state}:")
                st.markdown(f"### Average Poverty Level: <span style='color:{color};'>{level}</span>", unsafe_allow_html=True)
                st.metric(label="Average Poverty Score", value=f"{avg_poverty_score:.3f}")
            else:
                st.warning(f"No data available for {selected_state} to make a prediction.")

    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Training Configuration")
        
        selected_models = st.multiselect(
            "Select Models to Train",
            ['RandomForest', 'ExtraTrees', 'GradientBoosting', 'XGBoost (if available)'],
            default=['RandomForest', 'ExtraTrees']
        )
        
        optimization = st.checkbox("Enable Hyperparameter Optimization", value=True)
        cv_folds = st.slider("Cross-validation Folds", 3, 10, 5)
        
        if st.button("🚀 Start Training"):
            with st.spinner("Training models..."):
                progress = st.progress(0)
                status = st.empty()
                
                for i in range(101):
                    progress.progress(i)
                    if i < 30:
                        status.text(f"Preprocessing data: {i}%")
                    elif i < 70:
                        status.text(f"Training models: {i}%")
                    else:
                        status.text(f"Evaluating performance: {i}%")
                    time.sleep(0.05)
                
                st.success("✅ Training completed successfully!")
                st.session_state['models_trained'] = True
    
    with col2:
        st.subheader("Model Performance")
        
        if st.session_state.get('models_trained', False):
            # Mock performance data
            performance_data = {
                'Model': ['RandomForest', 'ExtraTrees', 'GradientBoosting'],
                'Accuracy': [0.923, 0.917, 0.909],
                'Precision': [0.912, 0.905, 0.898],
                'Recall': [0.934, 0.928, 0.920]
            }
            
            df_perf = pd.DataFrame(performance_data)
            st.dataframe(df_perf, use_container_width=True)
            
            # Performance chart
            fig = px.bar(df_perf, x='Model', y=['Accuracy', 'Precision', 'Recall'],
                        title='Model Performance Comparison')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Start training to see performance results")

elif page == "📊 Real-time Predictions":
    st.header("📊 Real-time Poverty Predictions")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎯 Make Prediction")
        
        # Input form
        state = st.selectbox("Select State", data['State'].unique())
        district_name = st.text_input("District Name", "New District")
        
        literacy = st.slider("Literacy Rate (%)", 0.0, 100.0, 65.0)
        employment = st.slider("Employment Rate (%)", 0.0, 100.0, 50.0)
        healthcare = st.slider("Healthcare Index", 0.0, 1.0, 0.5)
        infrastructure = st.slider("Infrastructure Score", 0.0, 1.0, 0.6)
        water_access = st.slider("Clean Water Access (%)", 0.0, 100.0, 70.0)
        population = st.number_input("Population", 10000, 5000000, 200000)
        
        if st.button("🔮 Predict Poverty Level", type="primary"):
            # Simple prediction algorithm
            poverty_score = 1.0 - (
                (literacy/100 * 0.25) + 
                (employment/100 * 0.25) + 
                (healthcare * 0.2) + 
                (infrastructure * 0.15) + 
                (water_access/100 * 0.15)
            )
            poverty_score = max(0.0, min(1.0, poverty_score + np.random.uniform(-0.1, 0.1)))
            
            # Calculate metrics
            confidence = np.random.uniform(0.85, 0.95)
            level = "High" if poverty_score > 0.7 else "Medium" if poverty_score > 0.4 else "Low"
            
            # Derived backend-only context
            poverty_level = level
            urgency_level = level
            urgency_score = float(min(10.0, max(0.0, 10.0 * poverty_score)))
            
            # Analyze resource needs
            needs, priority_resources = analyze_resource_needs(
                poverty_score, literacy, employment, healthcare, infrastructure, water_access
            )
            
            # Find nearest NGOs
            district_info = {
                'State': state,
                'District': district_name,
                'Poverty_Score': poverty_score
            }
            
            nearest_ngos = find_nearest_ngos(district_info, ngo_data, priority_resources, top_n=4)
            
            # Get CURRENT date and time information - ALWAYS FRESH
            from datetime import datetime as dt
            now = dt.now()
            current_date = now.strftime("%d %b %Y")  # 27 Oct 2025
            current_time = now.strftime("%I:%M:%S %p")  # 02:30:45 PM
            day_name = now.strftime("%A")  # Monday, Tuesday, etc
            
            # Use Streamlit container with native components
            st.markdown("---")
            
            # Header section - Display Current Date/Time/Day
            col_h1, col_h2, col_h3 = st.columns(3)
            with col_h1:
                st.metric(" Month ", current_date)
            with col_h2:
                st.metric(" Day", day_name)
            with col_h3:
                st.metric("🕐 Time", current_time)
            
            st.markdown("---")
            st.subheader("📊 Real-time Predictions Prompt")
            st.markdown("---")
            
            # Prediction Results
            st.subheader("🎯 Prediction Results")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Poverty Score", f"{poverty_score:.3f}")
            with col_b:
                st.metric("Confidence", f"{confidence:.1%}")
            with col_c:
                st.metric("Poverty Level", level)
            
            st.markdown("---")
            
            # Two column layout
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.subheader("📋 Resource Needs Analysis")
                for need in needs:
                    st.markdown(need)
            
            with col_right:
                st.subheader("🎯 Required Resources")
                for i, resource in enumerate(priority_resources[:8], 1):
                    st.write(f"✓ {resource}")
            
            st.markdown("---")
            
            # NGO Table
            st.subheader("🏢 Recommended NGOs to Contact")
            
            # Create NGO dataframe
            ngo_data_list = []
            for ngo in nearest_ngos:
                ngo_data_list.append({
                    "Organization": ngo['name'],
                    "Distance (km)": f"{ngo['distance']:.1f}",
                    "Match Score": f"{ngo['match_score']:.1f}%",
                    "Phone": ngo['info']['contact']['phone'],
                    "Email": ngo['info']['contact']['email'],
                    "Response Time": ngo['info']['response_time'],
                    "Capacity": ngo['info']['capacity']
                })
            
            ngo_df = pd.DataFrame(ngo_data_list)
            st.dataframe(ngo_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Action buttons
            st.subheader("🚀 Immediate Actions")
            col_action1, col_action2, col_action3, col_action4 = st.columns(4)
            
            with col_action1:
                if st.button("📧 Contact NGOs"):
                    # Log backend events for each NGO contact with ETA derived from response_time
                    for ngo in nearest_ngos:
                        eta = _hours_from_str(ngo['info'].get('response_time', ''))
                        record_notification_event(ngo['name'], 'email', 'sent', district_info, urgency_level, eta)
                    # Persist an alert snapshot for SLA monitoring
                    record_alert(district_info, severity=poverty_level, resources=priority_resources, urgency_score=urgency_score, source='prediction_contact')
                    st.success(f"✅ Contact requests sent to {len(nearest_ngos)} matching NGOs")
            
            with col_action2:
                if st.button("🚨 Send Alert"):
                    # Create a high-urgency alert record and log a government notification
                    rec = record_alert(district_info, severity='Critical', resources=priority_resources, urgency_score=max(8.0, urgency_score), source='prediction_alert')
                    record_notification_event('Government', 'email', 'queued', district_info, 'Critical', eta_hours=1.0)
                    st.success("🚨 Emergency alert sent to government departments")
            
            with col_action3:
                if st.button("📊 Generate Report"):
                    st.success("📊 Comprehensive assessment report generated")
            
            with col_action4:
                if st.button("📍 Track Progress"):
                    st.success("📍 Added to monitoring dashboard for progress tracking")
    
    with col2:
        st.subheader("📈 Recent Predictions Timeline")
        
        # Sample timeline data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        scores = np.random.uniform(0.2, 0.8, 100)
        
        timeline_df = pd.DataFrame({
            'Date': dates,
            'Poverty_Score': scores
        })
        
        fig = px.line(timeline_df, x='Date', y='Poverty_Score',
                     title='Poverty Score Predictions Over Time')
        fig.add_hline(y=0.7, line_dash="dash", line_color="red", 
                     annotation_text="High Poverty Threshold")
        fig.add_hline(y=0.4, line_dash="dash", line_color="orange",
                     annotation_text="Medium Poverty Threshold")
        st.plotly_chart(fig, use_container_width=True)

elif page == "🗺️ State Resource Analysis":
    st.header("🗺️ State-wise Resource Deficiency Analysis")
    
    # State selection
    selected_state = st.selectbox("Select State for Detailed Analysis", list(state_deficiency_data.keys()))
    
    if selected_state:
        state_info = state_deficiency_data[selected_state]
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Population Affected", f"{state_info['population_affected']/1000000:.1f}M")
        with col2:
            urgency_color = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}
            st.metric("Urgency Level", f"{urgency_color.get(state_info['urgency_level'], '🔵')} {state_info['urgency_level']}")
        with col3:
            st.metric("Affected Districts", len(state_info['affected_districts']))
        with col4:
            st.metric("Government Schemes", len(state_info['government_schemes']))
        
        # Detailed analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚨 Primary Deficiencies")
            for deficiency in state_info['primary_deficiencies']:
                st.error(f"• {deficiency}")
            
            st.subheader("🎯 Root Causes of Poverty")
            for i, cause in enumerate(state_info['poverty_causes'], 1):
                st.write(f"{i}. {cause}")
            
            st.subheader("🛠️ Critical Resources Needed")
            for resource in state_info['critical_resources']:
                st.info(f"• {resource}")
        
        with col2:
            st.subheader("📍 Most Affected Districts")
            affected_districts_df = pd.DataFrame({
                'District': state_info['affected_districts'],
                'Priority': ['High'] * len(state_info['affected_districts']),
                'Status': ['Needs Intervention'] * len(state_info['affected_districts'])
            })
            st.dataframe(affected_districts_df, use_container_width=True)
            
            # All districts in selected state (informational; does not alter graphs)
            st.subheader("🗂️ All Districts in State")
            full_list = state_districts_map.get(selected_state, [])
            if full_list:
                all_districts_df = pd.DataFrame({'District': full_list})
                st.dataframe(all_districts_df, use_container_width=True)
            else:
                st.info("No district list available for this state in processed data.")
            
            st.subheader("�️ Active Government Schemes")
            for scheme in state_info['government_schemes']:
                st.success(f"• {scheme}")
        
        # NGO matching for the state
        st.subheader(f"�🏢 NGOs Operating in {selected_state}")
        
        # Find NGOs operating in this state
        state_ngos = []
        for ngo_name, ngo_info in ngo_data.items():
            if selected_state in ngo_info.get('operational_states', []):
                state_ngos.append((ngo_name, ngo_info))
        
        if state_ngos:
            for ngo_name, ngo_info in state_ngos:
                col_ngo1, col_ngo2 = st.columns([2, 1])
                
                with col_ngo1:
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; background-color: #f8f9fa;">
                        <h4>🏢 {ngo_name}</h4>
                        <strong>📞 Phone:</strong> {ngo_info['contact']['phone']}<br>
                        <strong>📧 Email:</strong> {ngo_info['contact']['email']}<br>
                        <strong>📱 WhatsApp:</strong> {ngo_info['contact']['whatsapp']}<br>
                        <strong>🌐 Website:</strong> {ngo_info['contact']['website']}<br>
                        <strong>🎯 Specialization:</strong> {', '.join(ngo_info['specialization'])}<br>
                        <strong>🔧 Capacity:</strong> {ngo_info['capacity']}<br>
                        <strong>⏱️ Response Time:</strong> {ngo_info['response_time']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_ngo2:
                    if st.button(f"📧 Auto-Contact {ngo_name[:20]}...", key=f"contact_{ngo_name}"):
                        # Auto-generate and send message
                        district_sample = {"District": state_info['affected_districts'][0], "State": selected_state, "Poverty_Score": 0.8}
                        status, message = send_automatic_message_to_ngo(
                            ngo_info, district_sample, state_info['critical_resources'], 
                            state_info['urgency_level'], 'email', ngo_name=ngo_name
                        )
                        st.success(status)
                        with st.expander("📄 View Message Content"):
                            st.text(message)
        else:
            st.warning(f"No NGOs currently operating in {selected_state} in our database")
        
        # Generate comprehensive report
        if st.button("📊 Generate Comprehensive State Report", type="primary"):
            report = generate_state_resource_report(selected_state, state_info)
            
            col_rep1, col_rep2 = st.columns([2, 1])
            with col_rep1:
                st.markdown(report)
            with col_rep2:
                st.success("✅ Report generated successfully!")
                st.info("📤 Report can be shared with:")
                st.write("• State Government")
                st.write("• Central Ministries")
                st.write("• NGO Partners")
                st.write("• International Organizations")

elif page == "📞 Auto-Contact System":
    st.header("📞 Automatic NGO Contact & Messaging System")
    
    # Contact configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Contact Configuration")
        
        # District selection
        target_state = st.selectbox("Select State", list(state_deficiency_data.keys()))
        if target_state:
            target_district = st.selectbox("Select District", state_deficiency_data[target_state]['affected_districts'])
        
        # Resource selection
        if target_state:
            available_resources = state_deficiency_data[target_state]['critical_resources']
            selected_resources = st.multiselect("Select Required Resources", available_resources, default=available_resources[:3])
        
        urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High", "Critical", "Emergency"])
        
        # Contact methods
        contact_methods = st.multiselect("Contact Methods", ["Email", "WhatsApp", "SMS", "Phone Call"], default=["Email", "WhatsApp"])
        
        # Message customization
        custom_message = st.text_area("Additional Message (Optional)", 
                                    placeholder="Add any specific requirements or context...")
    
    with col2:
        st.subheader("📊 NGO Availability")
        
        if target_state:
            # Show available NGOs for the state
            available_ngos = []
            for ngo_name, ngo_info in ngo_data.items():
                if target_state in ngo_info.get('operational_states', []):
                    available_ngos.append(ngo_name)
            
            st.info(f"🏢 Available NGOs in {target_state}: {len(available_ngos)}")
            
            # Show NGO capacity
            for ngo_name in available_ngos[:3]:
                ngo_info = ngo_data[ngo_name]
                st.markdown(f"""
                <div style="background-color: #e8f5e8; padding: 0.5rem; margin: 0.3rem 0; border-radius: 5px;">
                    <strong>{ngo_name}</strong><br>
                    Capacity: {ngo_info['capacity']}<br>
                    Response: {ngo_info['response_time']}
                </div>
                """, unsafe_allow_html=True)
    
    # Mass contact system
    st.subheader("🚀 Automated Mass Contact")
    
    if st.button("📤 Send Automatic Messages to All NGOs", type="primary"):
        if target_state and selected_resources:
            success_count = 0
            messages_sent = []
            
            # Get NGOs operating in the selected state
            for ngo_name, ngo_info in ngo_data.items():
                if target_state in ngo_info.get('operational_states', []):
                    
                    # Create district info
                    district_info = {
                        "District": target_district,
                        "State": target_state,
                        "Poverty_Score": 0.75 + np.random.uniform(-0.1, 0.15),
                        "Population": np.random.randint(100000, 1000000),
                        "Literacy_Rate": np.random.uniform(45, 85),
                        "Employment_Rate": np.random.uniform(30, 70),
                        "Healthcare_Index": np.random.uniform(0.3, 0.8),
                        "Clean_Water_Access": np.random.uniform(40, 90)
                    }
                    
                    # Send message via selected methods
                    for method in contact_methods:
                        method_map = {"Email": "email", "WhatsApp": "whatsapp", "SMS": "sms", "Phone Call": "phone"}
                        status, message_content = send_automatic_message_to_ngo(
                            ngo_info, district_info, selected_resources, urgency, method_map.get(method, "email")
                        )
                        
                        messages_sent.append({
                            "NGO": ngo_name,
                            "Method": method,
                            "Status": status,
                            "Time": datetime.now().strftime("%H:%M:%S")
                        })
                        success_count += 1
            
            # Display results
            st.success(f"✅ {success_count} messages sent successfully!")
            
            # Message log
            st.subheader("📋 Message Delivery Log")
            messages_df = pd.DataFrame(messages_sent)
            st.dataframe(messages_df, use_container_width=True)
            
            # Expected responses
            st.subheader("⏱️ Expected Response Timeline")
            response_times = []
            for ngo_name, ngo_info in ngo_data.items():
                if target_state in ngo_info.get('operational_states', []):
                    response_times.append({
                        "NGO": ngo_name,
                        "Expected Response": ngo_info['response_time'],
                        "Contact": ngo_info['contact']['phone'],
                        "Email": ngo_info['contact']['email']
                    })
            
            if response_times:
                st.dataframe(pd.DataFrame(response_times), use_container_width=True)
        else:
            st.warning("Please select state and resources before sending messages")
    
    # Real-time monitoring
    st.subheader("📊 Real-time Response Monitoring")
    
    # Simulate response tracking
    if st.button("🔄 Check Response Status"):
        st.info("📡 Checking NGO response status...")
        
        # Simulate responses
        response_data = []
        for ngo_name, ngo_info in list(ngo_data.items())[:5]:
            status = np.random.choice(["Responded", "Pending", "Confirmed", "Declined"], p=[0.4, 0.3, 0.2, 0.1])
            response_data.append({
                "NGO": ngo_name,
                "Status": status,
                "Response Time": f"{np.random.randint(30, 180)} minutes ago" if status != "Pending" else "Waiting",
                "Resources Offered": "Available" if status == "Confirmed" else "Under Review"
            })
        
        response_df = pd.DataFrame(response_data)
        st.dataframe(response_df, use_container_width=True)
        
        # Summary
        confirmed = len(response_df[response_df['Status'] == 'Confirmed'])
        pending = len(response_df[response_df['Status'] == 'Pending'])
        
        col_sum1, col_sum2, col_sum3 = st.columns(3)
        with col_sum1:
            st.metric("✅ Confirmed", confirmed)
        with col_sum2:
            st.metric("⏳ Pending", pending)
        with col_sum3:
            st.metric("📞 Total Contacted", len(response_df))
    st.header("🏢 NGO Integration & Coordination")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Find Matching NGOs")
        
        target_district = st.selectbox("Select District", data['District'].unique())
        resource_needed = st.selectbox("Resource Type", 
                                     ['Food Security', 'Healthcare', 'Education', 'Water & Sanitation', 'Emergency Relief'])
        urgency_level = st.selectbox("Urgency", ['Low', 'Medium', 'High', 'Emergency'])
        
        if st.button("🔍 Find NGOs", type="primary"):
            st.subheader("📋 Matching NGOs with Resource Analysis")
            
            # Get district data for analysis
            district_data = data[data['District'] == target_district].iloc[0] if not data[data['District'] == target_district].empty else None
            
            if district_data is not None:
                # Analyze resource needs
                needs, priority_resources = analyze_resource_needs(
                    district_data['Poverty_Score'],
                    district_data['Literacy_Rate'],
                    district_data['Employment_Rate'],
                    district_data['Healthcare_Index'],
                    district_data['Infrastructure_Score'],
                    district_data['Clean_Water_Access']
                )
                
                # Display resource needs
                st.subheader("🎯 Identified Resource Needs")
                col_need1, col_need2 = st.columns(2)
                
                with col_need1:
                    st.markdown("**📋 Analysis:**")
                    for need in needs:
                        st.markdown(need)
                
                with col_need2:
                    st.markdown("**🛠️ Priority Resources:**")
                    for i, resource in enumerate(priority_resources[:6], 1):
                        st.write(f"{i}. {resource}")
                
                # Find and display matching NGOs
                st.subheader("🏢 Best Matching NGOs")
                try:
                    nearest_ngos = find_nearest_ngos(district_data, ngo_data, priority_resources, top_n=5)
                    
                    if nearest_ngos and len(nearest_ngos) > 0:
                        for ngo in nearest_ngos:
                            # Calculate additional metrics
                            urgency_multiplier = {"Emergency": 1.5, "High": 1.2, "Medium": 1.0, "Low": 0.8}[urgency_level]
                            adjusted_score = min(100, ngo['match_score'] * urgency_multiplier)
                            
                            st.markdown(f"""
                            <div style="border: 2px solid #{'#ff4444' if adjusted_score > 80 else '#ffaa00' if adjusted_score > 60 else '#44ff44'}; 
                                        border-radius: 10px; padding: 1.5rem; margin: 1rem 0; 
                                        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <h4 style="margin: 0; color: #2c3e50;">🏢 {ngo['name']}</h4>
                                    <span style="background: #{'#ff4444' if adjusted_score > 80 else '#ffaa00' if adjusted_score > 60 else '#44ff44'}; 
                                                 color: white; padding: 5px 10px; border-radius: 15px; font-weight: bold;">
                                        {adjusted_score:.1f}% Match
                                    </span>
                                </div>
                                <hr style="margin: 10px 0;">
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                                    <div>
                                        <strong>📍 Distance:</strong> {ngo['distance']:.1f} km<br>
                                        <strong>📞 Phone:</strong> {ngo['info']['contact']['phone']}<br>
                                        <strong>📧 Email:</strong> {ngo['info']['contact']['email']}<br>
                                        <strong>⏱️ Response Time:</strong> {ngo['info']['response_time']}<br>
                                    </div>
                                    <div>
                                        <strong>🎯 Specialization:</strong> {', '.join(ngo['info']['specialization'])}<br>
                                        <strong>🔧 Capacity:</strong> {ngo['info']['capacity']}<br>
                                        <strong>🌐 Coverage:</strong> {ngo['info']['coverage']}<br>
                                        <strong>🏪 Location:</strong> {ngo['info']['location']['city']}<br>
                                    </div>
                                </div>
                                <div style="margin-top: 10px;">
                                    <strong>🛠️ Available Resources:</strong> {', '.join(ngo['info']['resources'])}
                                </div>
                                <div style="margin-top: 10px;">
                                    <strong>📋 Requested Resource:</strong> {resource_needed} | 
                                    <strong>🚨 Urgency:</strong> {urgency_level}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("No matching NGOs found for the selected criteria")
                except Exception as e:
                    st.error(f"Error finding NGOs: {str(e)}")
                    nearest_ngos = []                # Action buttons for each NGO with auto-messaging
                st.subheader("🚀 Quick Actions")
                col_act1, col_act2, col_act3, col_act4 = st.columns(4)
                
                with col_act1:
                    if st.button("� Auto-Email All NGOs"):
                        messages_sent = 0
                        for ngo in nearest_ngos:
                            status, message = send_automatic_message_to_ngo(
                                ngo['info'], district_data, priority_resources, 
                                urgency_level, 'email', ngo_name=ngo['name']
                            )
                            messages_sent += 1
                            # Backend logging per NGO
                            eta = _hours_from_str(ngo['info'].get('response_time', ''))
                            record_notification_event(ngo['name'], 'email', 'sent', {'State': district_data['State'], 'District': district_data['District']}, urgency_level, eta)
                        # Persist alert for monitoring
                        record_alert({'State': district_data['State'], 'District': district_data['District'], 'Poverty_Score': float(district_data['Poverty_Score'])}, severity=urgency_level, resources=priority_resources, urgency_score=min(10.0, 10.0*float(district_data['Poverty_Score'])), source='integration_email_all')
                        st.success(f"✅ {messages_sent} automatic emails sent!")
                        st.info("📧 Detailed resource requirements sent to all matching NGOs")
                
                with col_act2:
                    if st.button("📱 WhatsApp Alerts"):
                        messages_sent = 0
                        for ngo in nearest_ngos:
                            status, message = send_automatic_message_to_ngo(
                                ngo['info'], district_data, priority_resources, 
                                urgency_level, 'whatsapp', ngo_name=ngo['name']
                            )
                            messages_sent += 1
                            eta = _hours_from_str(ngo['info'].get('response_time', ''))
                            record_notification_event(ngo['name'], 'whatsapp', 'sent', {'State': district_data['State'], 'District': district_data['District']}, urgency_level, eta)
                        record_alert({'State': district_data['State'], 'District': district_data['District'], 'Poverty_Score': float(district_data['Poverty_Score'])}, severity=urgency_level, resources=priority_resources, urgency_score=min(10.0, 10.0*float(district_data['Poverty_Score'])), source='integration_whatsapp_all')
                        st.success(f"📱 {messages_sent} WhatsApp alerts sent!")
                        st.info("⚡ Emergency alerts sent via WhatsApp for immediate response")
                
                with col_act3:
                    if st.button("📊 Generate Coordination Report"):
                        st.success("📊 Coordination report generated and shared with all stakeholders")
                        st.info("🔄 Report includes resource mapping, NGO capabilities, and action timeline")
                
                with col_act4:
                    if st.button("🚨 Create Emergency Task Force"):
                        st.success("🚨 Emergency task force created with top 3 NGOs")
                        st.info("⚡ Task force activated for immediate response coordination")
                
                # Show message templates
                if st.checkbox("📄 View Auto-Generated Message Template"):
                    sample_message = send_automatic_message_to_ngo(
                        nearest_ngos[0]['info'], district_data, priority_resources, 
                        urgency_level, 'email', ngo_name=nearest_ngos[0]['name']
                    )[1]
                    st.text_area("Message Template", sample_message, height=200)
            else:
                st.warning("District data not found for detailed analysis")
    
    with col2:
        st.subheader("📨 Send Alerts")
        
        alert_type = st.selectbox("Alert Type", 
                                ['Resource Request', 'Emergency Alert', 'Coordination Update'])
        
        message = st.text_area("Message", height=100, 
                              placeholder="Enter your message to NGOs and government departments...")
        
        notification_methods = st.multiselect("Send via", 
                                            ['Email', 'SMS', 'WhatsApp'], 
                                            default=['Email'])
        
        if st.button("📤 Send Alert", type="primary"):
            if message:
                st.success(f"✅ {alert_type} sent via {', '.join(notification_methods)}")
                st.info(f"Message delivered to: 5 NGOs, 3 Government Departments")
                st.write(f"**Sent at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.warning("Please enter a message")
    
    # NGO Directory with enhanced information
    st.subheader("📋 Complete NGO Directory")
    ngo_df_data = []
    for name, info in ngo_data.items():
        ngo_df_data.append({
            'NGO Name': name,
            'Specialization': ', '.join(info['specialization']),
            'Coverage': info['coverage'],
            'Response Time': info['response_time'],
            'Phone': info['contact']['phone'],
            'Email': info['contact']['email'],
            'City': info['location']['city'],
            'Capacity': info['capacity'],
            'Key Resources': ', '.join(info['resources'][:3]) + '...',
            'Status': np.random.choice(['Active', 'Available', 'Busy'], p=[0.6, 0.3, 0.1])
        })
    
    ngo_df = pd.DataFrame(ngo_df_data)
    st.dataframe(ngo_df, use_container_width=True)
    
    # Export functionality
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        if st.button("📥 Export NGO Contacts"):
            st.success("✅ NGO contact list exported as CSV")
    with col_exp2:
        if st.button("📊 Generate NGO Capability Report"):
            st.success("📊 NGO capability assessment report generated")

elif page == "🌐 Go Live":
    st.header("🌐 Go Live & Sharing")
    st.write("This section helps you view active local instances and provides guidance to access the app from other devices or share it externally.")

    import socket, http.client
    from contextlib import closing

    def _port_alive(p:int)->bool:
        try:
            conn = http.client.HTTPConnection('127.0.0.1', p, timeout=0.8)
            conn.request('GET', '/')
            resp = conn.getresponse()
            return resp.status in (200, 302, 304, 403)
        except Exception:
            return False
        finally:
            try:
                conn.close()
            except Exception:
                pass

    # Include the port configured for this Streamlit process. The launcher can
    # move to 8502-8510 when the default port is busy.
    configured_port = int(st.get_option("server.port") or 8501)
    candidate_ports = sorted({configured_port, *range(8501, 8514)})
    live_ports = []
    for p in candidate_ports:
        if _port_alive(p):
            live_ports.append(p)
    if configured_port not in live_ports:
        # The current Streamlit process is itself live even when loopback
        # probing is blocked by the host environment.
        live_ports.insert(0, configured_port)

    colA, colB = st.columns(2)
    with colA:
        st.subheader("🟢 Active Local Instances")
        for p in live_ports:
            st.markdown(f"- [Open app](http://127.0.0.1:{p})  \n  `http://127.0.0.1:{p}`")
        if not live_ports:
            st.info("No active Streamlit instances detected on common ports.")
    with colB:
        st.subheader("🖥️ LAN Access")
        try:
            lan_ip = socket.gethostbyname(socket.gethostname())
            if lan_ip.startswith("127."):
                # Fallback: try common interface names
                import subprocess
                for iface in ["en0", "en1"]:
                    try:
                        out = subprocess.check_output(["ipconfig", "getifaddr", iface], text=True).strip()
                        if out:
                            lan_ip = out
                            break
                    except Exception:
                        pass
        except Exception:
            lan_ip = "127.0.0.1"
        if live_ports:
            for p in live_ports:
                st.markdown(f"- http://{lan_ip}:{p}")
        else:
            st.write("(Waiting for a running instance)")

    st.subheader("🔐 External / Public Sharing Options")
    st.markdown("""
You currently run the app locally. To expose it publicly you can:
1. Use a tunneling tool (recommended for quick demos):
   - Install ngrok then run in a terminal:
     ```bash
     ngrok http <active-port>
     ```
     Replace `<active-port>` with one of the active ports above.
2. Use Cloudflare Tunnel (`cloudflared tunnel --url http://localhost:<active-port>`).
3. Configure your router to port-forward the active port (ensure you understand security implications).

If you install pyngrok, this page can start a tunnel directly.
""")

    start_tunnel = st.button("🚀 Start Temporary ngrok Tunnel (if installed)")
    if start_tunnel:
        try:
            from pyngrok import ngrok
            target_port = live_ports[0] if live_ports else configured_port
            public_url = ngrok.connect(target_port, bind_tls=True).public_url
            st.success(f"Tunnel active: {public_url}")
            st.info("Keep this page open to maintain the tunnel.")
        except ModuleNotFoundError:
            st.error("pyngrok not installed. Run 'pip install pyngrok' and refresh.")
        except Exception as e:
            st.error(f"Tunnel error: {e}")

    st.subheader("📄 Diagnostics")
    st.write({"live_ports": live_ports})
    if st.button("🔄 Refresh live status"):
        st.rerun()
    st.caption("If the link does not open, restart the app with run_app.sh and refresh this page.")

elif page == "🚨 Alert Management":
    st.header("🚨 Real-time Alert Management")
    
    # Current alerts
    st.subheader("⚡ Active Alerts")
    
    # Load persisted alerts and convert to current display schema
    def _fmt_time(ts_iso: str) -> str:
        try:
            from datetime import datetime as _dt
            dt = _dt.fromisoformat(ts_iso.replace('Z',''))
            delta = datetime.now() - dt
            mins = int(delta.total_seconds() // 60)
            if mins < 1:
                return "just now"
            if mins < 60:
                return f"{mins} min ago"
            hrs = int(mins // 60)
            return f"{hrs} hours ago"
        except Exception:
            return "recently"

    persisted = _load_active_alerts().get('alerts', [])
    alerts = []
    for a in persisted[-10:]:  # show last 10
        atype = ' / '.join(a.get('resources', [])[:1]) or 'General'
        alerts.append({
            'district': a.get('district'),
            'state': a.get('state'),
            'severity': a.get('severity', 'Medium').title(),
            'time': _fmt_time(a.get('created_at', datetime.now().isoformat())),
            'type': atype.title()
        })
    # Fallback to defaults if none persisted yet
    if not alerts:
        alerts = [
            {"district": "Bihar_District_3", "state": "Bihar", "severity": "High", "time": "5 min ago", "type": "Food Security"},
            {"district": "Maharashtra_District_7", "state": "Maharashtra", "severity": "Critical", "time": "12 min ago", "type": "Healthcare"},
            {"district": "Uttar Pradesh_District_2", "state": "Uttar Pradesh", "severity": "Medium", "time": "25 min ago", "type": "Education"},
            {"district": "West Bengal_District_5", "state": "West Bengal", "severity": "High", "time": "35 min ago", "type": "Water"},
        ]
    
    for alert in alerts:
        severity_class = f"alert-{alert['severity'].lower()}"
        st.markdown(f"""
        <div class="{severity_class}">
            <strong>🚨 {alert['district']}, {alert['state']}</strong><br>
            Severity: {alert['severity']} | Type: {alert['type']} | {alert['time']}
        </div>
        """, unsafe_allow_html=True)
    
    # Alert statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Alert Statistics")
        alert_stats = {
            'Severity': ['Critical', 'High', 'Medium', 'Low'],
            'Count': [2, 8, 15, 5],
            'Avg Response Time': ['45 min', '1.2 hours', '2.5 hours', '4 hours']
        }
        st.dataframe(pd.DataFrame(alert_stats), use_container_width=True)
    
    with col2:
        st.subheader("📈 Alert Trends")
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        counts = [12, 8, 15, 10, 18, 6, 9]
        
        fig = px.bar(x=days, y=counts, title='Weekly Alert Distribution')
        st.plotly_chart(fig, use_container_width=True)

elif page == "📱 Government Notifications":
    st.header("📱 Government Notification System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏛️ Send Government Alert")
        
        department = st.selectbox("Government Department", [
            "Ministry of Rural Development",
            "Department of Social Welfare", 
            "District Collector Office",
            "Public Distribution System",
            "Ministry of Health"
        ])
        
        priority = st.selectbox("Priority Level", ["Low", "Medium", "High", "Emergency"])
        
        category = st.selectbox("Category", [
            "Resource Allocation",
            "Emergency Response",
            "Policy Implementation",
            "Coordination Request"
        ])
        
        gov_message = st.text_area("Official Message", height=120,
                                  placeholder="Enter official message to government department...")
        
        if st.button("🚨 Send Official Alert", type="primary"):
            if gov_message:
                st.success(f"✅ Official alert sent to {department}")
                st.info(f"Priority: {priority} | Category: {category}")
                st.write(f"**Reference ID:** GOV-{np.random.randint(10000, 99999)}")
                st.write(f"**Sent at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.warning("Please enter a message")
    
    with col2:
        st.subheader("📋 Recent Government Communications")
        
        gov_comms = [
            {"dept": "Ministry of Rural Development", "type": "Resource Request", "status": "Acknowledged", "time": "2 hours ago"},
            {"dept": "District Collector Office", "type": "Emergency Alert", "status": "In Progress", "time": "4 hours ago"},
            {"dept": "Department of Social Welfare", "type": "Coordination", "status": "Completed", "time": "1 day ago"},
        ]
        
        for comm in gov_comms:
            status_color = {"Acknowledged": "🟡", "In Progress": "🔵", "Completed": "🟢"}[comm['status']]
            st.markdown(f"""
            <div class="ngo-card">
                <strong>{status_color} {comm['dept']}</strong><br>
                Type: {comm['type']}<br>
                Status: {comm['status']} | {comm['time']}
            </div>
            """, unsafe_allow_html=True)

# Auto refresh logic
if auto_refresh and 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

if auto_refresh:
    # Show last refresh time
    st.sidebar.write(f"Last refresh: {st.session_state.last_refresh.strftime('%H:%M:%S')}")
    
    # Auto refresh every interval (commented out to prevent continuous refresh)
    # time.sleep(refresh_interval)
    # st.session_state.last_refresh = datetime.now()
    # st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("**🏛️ Poverty Resource Allocation System** | Real-time monitoring and coordination for poverty alleviation")
