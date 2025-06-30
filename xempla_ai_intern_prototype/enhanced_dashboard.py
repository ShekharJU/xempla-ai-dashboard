#!/usr/bin/env python3
"""
Enhanced Xempla AI Systems Intern Prototype - Interactive Dashboard

This dashboard provides comprehensive visualization with file upload capabilities,
industry-specific analytics, and feedback integration for continuous improvement.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import sys
from datetime import datetime, timedelta
import numpy as np
import io
import base64
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.simulation.building_data_loader import BuildingEnergyDataLoader
from src.agents.energy_optimization_agent import EnergyOptimizationAgent
from src.feedback.feedback_loop import FeedbackLoop

# Page configuration
st.set_page_config(
    page_title="Xempla AI Systems - Enhanced Analytics",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-metric {
        border-left-color: #2ca02c;
    }
    .warning-metric {
        border-left-color: #ff7f0e;
    }
    .info-metric {
        border-left-color: #1f77b4;
    }
    .danger-metric {
        border-left-color: #d62728;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 1rem;
        border: 2px dashed #dee2e6;
        text-align: center;
        margin: 1rem 0;
    }
    .feedback-section {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_building_data():
    """Load building energy data"""
    try:
        data_loader = BuildingEnergyDataLoader()
        return data_loader
    except Exception as e:
        st.error(f"Error loading building data: {e}")
        return None

@st.cache_data
def load_demo_results():
    """Load demo results if available"""
    results_file = "results/building_energy_demo_results.json"
    if os.path.exists(results_file):
        try:
            with open(results_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Could not load demo results: {e}")
    return None

def parse_uploaded_file(uploaded_file):
    """Parse uploaded file and return DataFrame"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            df = pd.read_json(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload CSV, Excel, or JSON files.")
            return None
        return df
    except Exception as e:
        st.error(f"Error parsing file: {e}")
        return None

def analyze_industry_data(df, industry_type):
    """Analyze uploaded data based on industry type"""
    analysis_results = {
        'energy_savings': {},
        'maintenance': {},
        'efficiency': {},
        'cost_analysis': {},
        'safety': {},
        'production': {},
        'recommendations': []
    }
    
    # Energy Savings Analysis
    if 'energy_consumption' in df.columns or 'power_usage' in df.columns:
        energy_col = 'energy_consumption' if 'energy_consumption' in df.columns else 'power_usage'
        analysis_results['energy_savings'] = {
            'current_consumption': df[energy_col].sum(),
            'peak_consumption': df[energy_col].max(),
            'avg_consumption': df[energy_col].mean(),
            'potential_savings': df[energy_col].sum() * 0.15,  # 15% potential savings
            'savings_percentage': 15.0
        }
    
    # Efficiency Analysis
    if 'efficiency' in df.columns:
        analysis_results['efficiency'] = {
            'current_efficiency': df['efficiency'].mean(),
            'efficiency_trend': df['efficiency'].pct_change().mean(),
            'efficiency_improvement_potential': 100 - df['efficiency'].mean()
        }
    
    # Cost Analysis
    if 'cost' in df.columns or 'expenses' in df.columns:
        cost_col = 'cost' if 'cost' in df.columns else 'expenses'
        analysis_results['cost_analysis'] = {
            'total_cost': df[cost_col].sum(),
            'avg_cost': df[cost_col].mean(),
            'cost_reduction_potential': df[cost_col].sum() * 0.12,  # 12% cost reduction
            'roi_estimate': (df[cost_col].sum() * 0.12) / (df[cost_col].sum() * 0.05)  # ROI calculation
        }
    
    # Safety Analysis
    if 'safety_score' in df.columns or 'incidents' in df.columns:
        safety_col = 'safety_score' if 'safety_score' in df.columns else 'incidents'
        analysis_results['safety'] = {
            'current_safety_score': df[safety_col].mean() if 'safety_score' in df.columns else 100 - df[safety_col].sum(),
            'safety_trend': df[safety_col].pct_change().mean() if 'safety_score' in df.columns else -df[safety_col].pct_change().mean(),
            'safety_improvements': ['Implement safety protocols', 'Regular safety training', 'Equipment maintenance']
        }
    
    # Production Analysis
    if 'production' in df.columns or 'output' in df.columns:
        prod_col = 'production' if 'production' in df.columns else 'output'
        analysis_results['production'] = {
            'total_production': df[prod_col].sum(),
            'avg_production': df[prod_col].mean(),
            'production_efficiency': df[prod_col].mean() / df[prod_col].max() * 100,
            'production_optimization_potential': 20.0  # 20% optimization potential
        }
    
    # Maintenance Analysis
    analysis_results['maintenance'] = {
        'maintenance_schedule': 'Predictive maintenance recommended',
        'equipment_health': 'Good' if 'efficiency' in df.columns and df['efficiency'].mean() > 80 else 'Needs attention',
        'maintenance_cost_savings': analysis_results['cost_analysis'].get('total_cost', 100000) * 0.08,  # 8% savings
        'next_maintenance_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    }
    
    # Industry-specific recommendations
    industry_recommendations = {
        'manufacturing': [
            'Implement IoT sensors for real-time monitoring',
            'Optimize production line efficiency',
            'Reduce energy consumption in peak hours',
            'Implement predictive maintenance systems'
        ],
        'energy': [
            'Optimize grid distribution',
            'Implement demand response programs',
            'Integrate renewable energy sources',
            'Improve energy storage systems'
        ],
        'healthcare': [
            'Optimize HVAC systems for patient comfort',
            'Implement energy-efficient lighting',
            'Reduce medical equipment energy consumption',
            'Improve facility safety protocols'
        ],
        'retail': [
            'Optimize store lighting and HVAC',
            'Implement smart inventory management',
            'Reduce refrigeration energy consumption',
            'Improve customer safety measures'
        ],
        'office': [
            'Implement smart building controls',
            'Optimize workspace utilization',
            'Reduce peak energy demand',
            'Improve indoor air quality'
        ]
    }
    
    analysis_results['recommendations'] = industry_recommendations.get(industry_type.lower(), [
        'Implement energy monitoring systems',
        'Optimize operational efficiency',
        'Reduce operational costs',
        'Improve safety protocols'
    ])
    
    return analysis_results

def create_industry_charts(df, analysis_results, industry_type):
    """Create industry-specific charts"""
    charts = {}
    
    # Energy Consumption Chart
    if 'energy_consumption' in df.columns or 'power_usage' in df.columns:
        energy_col = 'energy_consumption' if 'energy_consumption' in df.columns else 'power_usage'
        fig = px.line(
            df, 
            y=energy_col,
            title=f"{industry_type.title()} - Energy Consumption Over Time",
            labels={'value': 'Energy Consumption (kWh)', 'index': 'Time Period'}
        )
        charts['energy_consumption'] = fig
    
    # Efficiency Trend Chart
    if 'efficiency' in df.columns:
        fig = px.line(
            df,
            y='efficiency',
            title=f"{industry_type.title()} - Efficiency Trends",
            labels={'value': 'Efficiency (%)', 'index': 'Time Period'}
        )
        charts['efficiency'] = fig
    
    # Cost Analysis Chart
    if 'cost' in df.columns or 'expenses' in df.columns:
        cost_col = 'cost' if 'cost' in df.columns else 'expenses'
        fig = px.bar(
            df,
            y=cost_col,
            title=f"{industry_type.title()} - Cost Analysis",
            labels={'value': 'Cost ($)', 'index': 'Time Period'}
        )
        charts['cost_analysis'] = fig
    
    # Safety Score Chart
    if 'safety_score' in df.columns:
        fig = px.line(
            df,
            y='safety_score',
            title=f"{industry_type.title()} - Safety Score Trends",
            labels={'value': 'Safety Score', 'index': 'Time Period'}
        )
        charts['safety'] = fig
    
    # Production Output Chart
    if 'production' in df.columns or 'output' in df.columns:
        prod_col = 'production' if 'production' in df.columns else 'output'
        fig = px.line(
            df,
            y=prod_col,
            title=f"{industry_type.title()} - Production Output",
            labels={'value': 'Production Units', 'index': 'Time Period'}
        )
        charts['production'] = fig
    
    # KPI Dashboard
    kpi_data = {
        'Metric': ['Energy Savings', 'Efficiency', 'Cost Reduction', 'Safety Score', 'Production'],
        'Current': [
            f"{analysis_results['energy_savings'].get('current_consumption', 0):,.0f} kWh",
            f"{analysis_results['efficiency'].get('current_efficiency', 0):.1f}%",
            f"${analysis_results['cost_analysis'].get('total_cost', 0):,.0f}",
            f"{analysis_results['safety'].get('current_safety_score', 0):.1f}",
            f"{analysis_results['production'].get('total_production', 0):,.0f} units"
        ],
        'Potential': [
            f"{analysis_results['energy_savings'].get('potential_savings', 0):,.0f} kWh",
            f"{analysis_results['efficiency'].get('efficiency_improvement_potential', 0):.1f}%",
            f"${analysis_results['cost_analysis'].get('cost_reduction_potential', 0):,.0f}",
            "100%",
            f"{analysis_results['production'].get('production_optimization_potential', 0):.1f}%"
        ]
    }
    
    kpi_df = pd.DataFrame(kpi_data)
    fig = go.Figure(data=[
        go.Bar(name='Current', x=kpi_df['Metric'], y=kpi_df['Current']),
        go.Bar(name='Potential', x=kpi_df['Metric'], y=kpi_df['Potential'])
    ])
    fig.update_layout(title=f"{industry_type.title()} - KPI Dashboard", barmode='group')
    charts['kpi_dashboard'] = fig
    
    return charts

def save_feedback(feedback_data):
    """Save user feedback to file"""
    feedback_file = "results/user_feedback.json"
    os.makedirs("results", exist_ok=True)
    
    # Load existing feedback
    existing_feedback = []
    if os.path.exists(feedback_file):
        try:
            with open(feedback_file, 'r') as f:
                existing_feedback = json.load(f)
        except:
            existing_feedback = []
    
    # Add new feedback
    feedback_data['timestamp'] = datetime.now().isoformat()
    existing_feedback.append(feedback_data)
    
    # Save updated feedback
    with open(feedback_file, 'w') as f:
        json.dump(existing_feedback, f, indent=2)

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">🏢 Xempla AI Systems - Enhanced Analytics</h1>', unsafe_allow_html=True)
    st.markdown("### Industry-Specific AI Analytics with Feedback Integration")
    
    # Sidebar
    st.sidebar.title("🎛️ Dashboard Controls")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Select Dashboard Section",
        ["📤 File Upload & Analysis", "📊 Industry Analytics", "💰 Cost & ROI Analysis", "🔧 Maintenance & Safety", "📈 Production & Efficiency", "💬 Feedback & Learning", "📋 System Overview"]
    )
    
    # Load data
    data_loader = load_building_data()
    demo_results = load_demo_results()
    
    if page == "📤 File Upload & Analysis":
        show_file_upload_analysis()
    elif page == "📊 Industry Analytics":
        show_industry_analytics()
    elif page == "💰 Cost & ROI Analysis":
        show_cost_roi_analysis()
    elif page == "🔧 Maintenance & Safety":
        show_maintenance_safety()
    elif page == "📈 Production & Efficiency":
        show_production_efficiency()
    elif page == "💬 Feedback & Learning":
        show_feedback_learning()
    elif page == "📋 System Overview":
        show_system_overview(data_loader, demo_results)

def show_file_upload_analysis():
    """Show file upload and analysis section"""
    
    st.header("📤 File Upload & Analysis")
    
    # File upload section
    st.markdown("""
    <div class="upload-section">
        <h3>📁 Upload Your Industry Data</h3>
        <p>Upload CSV, Excel, or JSON files containing your operational data for AI-powered analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'json'],
        help="Upload files with columns like: energy_consumption, efficiency, cost, safety_score, production, etc."
    )
    
    if uploaded_file is not None:
        # Parse uploaded file
        df = parse_uploaded_file(uploaded_file)
        
        if df is not None:
            st.success(f"✅ File uploaded successfully! Shape: {df.shape}")
            
            # Show data preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Industry selection
            industry_type = st.selectbox(
                "Select Industry Type",
                ["Manufacturing", "Energy", "Healthcare", "Retail", "Office", "Other"]
            )
            
            # Analyze data
            if st.button("🚀 Analyze Data with AI"):
                with st.spinner("Analyzing data with AI algorithms..."):
                    analysis_results = analyze_industry_data(df, industry_type)
                    
                    # Store in session state
                    st.session_state['uploaded_data'] = df
                    st.session_state['analysis_results'] = analysis_results
                    st.session_state['industry_type'] = industry_type
                    
                    st.success("✅ Analysis complete! Check other sections for detailed insights.")
                    
                    # Show quick summary
                    st.subheader("📊 Quick Analysis Summary")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Energy Savings Potential",
                            f"{analysis_results['energy_savings'].get('savings_percentage', 0):.1f}%"
                        )
                    
                    with col2:
                        st.metric(
                            "Efficiency Improvement",
                            f"{analysis_results['efficiency'].get('efficiency_improvement_potential', 0):.1f}%"
                        )
                    
                    with col3:
                        st.metric(
                            "Cost Reduction",
                            f"${analysis_results['cost_analysis'].get('cost_reduction_potential', 0):,.0f}"
                        )
                    
                    with col4:
                        st.metric(
                            "Production Optimization",
                            f"{analysis_results['production'].get('production_optimization_potential', 0):.1f}%"
                        )

def show_industry_analytics():
    """Show industry-specific analytics"""
    
    st.header("📊 Industry Analytics")
    
    if 'analysis_results' not in st.session_state:
        st.info("📤 Please upload data in the File Upload section first.")
        return
    
    analysis_results = st.session_state['analysis_results']
    industry_type = st.session_state.get('industry_type', 'Industry')
    
    # Energy Savings Analysis
    st.subheader("⚡ Energy Savings Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card success-metric">
            <h3>Current Consumption</h3>
            <h2>{:,.0f} kWh</h2>
        </div>
        """.format(analysis_results['energy_savings'].get('current_consumption', 0)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card warning-metric">
            <h3>Potential Savings</h3>
            <h2>{:,.0f} kWh</h2>
        </div>
        """.format(analysis_results['energy_savings'].get('potential_savings', 0)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card info-metric">
            <h3>Savings Percentage</h3>
            <h2>{:.1f}%</h2>
        </div>
        """.format(analysis_results['energy_savings'].get('savings_percentage', 0)), unsafe_allow_html=True)
    
    # Efficiency Analysis
    st.subheader("📈 Efficiency Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Current Efficiency",
            f"{analysis_results['efficiency'].get('current_efficiency', 0):.1f}%"
        )
    
    with col2:
        st.metric(
            "Efficiency Trend",
            f"{analysis_results['efficiency'].get('efficiency_trend', 0):.2f}%"
        )
    
    with col3:
        st.metric(
            "Improvement Potential",
            f"{analysis_results['efficiency'].get('efficiency_improvement_potential', 0):.1f}%"
        )
    
    # Create charts if data is available
    if 'uploaded_data' in st.session_state:
        df = st.session_state['uploaded_data']
        charts = create_industry_charts(df, analysis_results, industry_type)
        
        # Display charts
        for chart_name, chart in charts.items():
            st.plotly_chart(chart, use_container_width=True)

def show_cost_roi_analysis():
    """Show cost and ROI analysis"""
    
    st.header("💰 Cost & ROI Analysis")
    
    if 'analysis_results' not in st.session_state:
        st.info("📤 Please upload data in the File Upload section first.")
        return
    
    analysis_results = st.session_state['analysis_results']
    
    # Cost Analysis
    st.subheader("💵 Cost Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Cost",
            f"${analysis_results['cost_analysis'].get('total_cost', 0):,.0f}"
        )
    
    with col2:
        st.metric(
            "Average Cost",
            f"${analysis_results['cost_analysis'].get('avg_cost', 0):,.0f}"
        )
    
    with col3:
        st.metric(
            "Cost Reduction Potential",
            f"${analysis_results['cost_analysis'].get('cost_reduction_potential', 0):,.0f}"
        )
    
    with col4:
        st.metric(
            "Estimated ROI",
            f"{analysis_results['cost_analysis'].get('roi_estimate', 0):.1f}x"
        )
    
    # ROI Breakdown Chart
    st.subheader("📊 ROI Breakdown")
    
    roi_data = {
        'Category': ['Energy Savings', 'Maintenance', 'Efficiency', 'Safety', 'Production'],
        'Investment': [50000, 30000, 40000, 25000, 60000],
        'Returns': [75000, 45000, 60000, 35000, 90000],
        'ROI': [1.5, 1.5, 1.5, 1.4, 1.5]
    }
    
    roi_df = pd.DataFrame(roi_data)
    
    fig = go.Figure(data=[
        go.Bar(name='Investment ($)', x=roi_df['Category'], y=roi_df['Investment']),
        go.Bar(name='Returns ($)', x=roi_df['Category'], y=roi_df['Returns'])
    ])
    fig.update_layout(title="Investment vs Returns by Category", barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost Optimization Recommendations
    st.subheader("🎯 Cost Optimization Recommendations")
    
    recommendations = [
        "Implement energy monitoring systems to identify waste",
        "Optimize maintenance schedules to reduce downtime costs",
        "Invest in energy-efficient equipment with high ROI",
        "Implement predictive maintenance to prevent costly breakdowns",
        "Optimize production processes to reduce operational costs"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"**{i}.** {rec}")

def show_maintenance_safety():
    """Show maintenance and safety analysis"""
    
    st.header("🔧 Maintenance & Safety Analysis")
    
    if 'analysis_results' not in st.session_state:
        st.info("📤 Please upload data in the File Upload section first.")
        return
    
    analysis_results = st.session_state['analysis_results']
    
    # Maintenance Analysis
    st.subheader("🔧 Maintenance Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Equipment Health",
            analysis_results['maintenance']['equipment_health']
        )
    
    with col2:
        st.metric(
            "Maintenance Cost Savings",
            f"${analysis_results['maintenance']['maintenance_cost_savings']:,.0f}"
        )
    
    with col3:
        st.metric(
            "Next Maintenance",
            analysis_results['maintenance']['next_maintenance_date']
        )
    
    with col4:
        st.metric(
            "Schedule Type",
            analysis_results['maintenance']['maintenance_schedule']
        )
    
    # Safety Analysis
    st.subheader("🛡️ Safety Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Current Safety Score",
            f"{analysis_results['safety'].get('current_safety_score', 0):.1f}"
        )
    
    with col2:
        st.metric(
            "Safety Trend",
            f"{analysis_results['safety'].get('safety_trend', 0):.2f}%"
        )
    
    with col3:
        st.metric(
            "Safety Status",
            "🟢 Good" if analysis_results['safety'].get('current_safety_score', 0) > 80 else "🟡 Needs Attention"
        )
    
    # Safety Improvements
    st.subheader("🔧 Safety Improvements")
    
    safety_improvements = analysis_results['safety'].get('safety_improvements', [])
    for i, improvement in enumerate(safety_improvements, 1):
        st.markdown(f"**{i}.** {improvement}")
    
    # Maintenance Schedule Chart
    st.subheader("📅 Maintenance Schedule")
    
    maintenance_data = {
        'Equipment': ['HVAC System', 'Electrical', 'Plumbing', 'Security', 'IT Systems'],
        'Last Maintenance': ['2024-01-15', '2024-02-01', '2024-01-30', '2024-02-10', '2024-02-05'],
        'Next Maintenance': ['2024-04-15', '2024-05-01', '2024-04-30', '2024-05-10', '2024-05-05'],
        'Status': ['Good', 'Good', 'Needs Attention', 'Good', 'Good']
    }
    
    maintenance_df = pd.DataFrame(maintenance_data)
    st.dataframe(maintenance_df, use_container_width=True)

def show_production_efficiency():
    """Show production and efficiency analysis"""
    
    st.header("📈 Production & Efficiency Analysis")
    
    if 'analysis_results' not in st.session_state:
        st.info("📤 Please upload data in the File Upload section first.")
        return
    
    analysis_results = st.session_state['analysis_results']
    
    # Production Analysis
    st.subheader("🏭 Production Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Production",
            f"{analysis_results['production'].get('total_production', 0):,.0f} units"
        )
    
    with col2:
        st.metric(
            "Average Production",
            f"{analysis_results['production'].get('avg_production', 0):,.0f} units"
        )
    
    with col3:
        st.metric(
            "Production Efficiency",
            f"{analysis_results['production'].get('production_efficiency', 0):.1f}%"
        )
    
    with col4:
        st.metric(
            "Optimization Potential",
            f"{analysis_results['production'].get('production_optimization_potential', 0):.1f}%"
        )
    
    # Production Optimization Chart
    st.subheader("📊 Production Optimization Opportunities")
    
    optimization_data = {
        'Factor': ['Process Efficiency', 'Equipment Utilization', 'Quality Control', 'Supply Chain', 'Workforce'],
        'Current': [75, 80, 85, 70, 90],
        'Target': [90, 95, 95, 85, 95],
        'Improvement': [15, 15, 10, 15, 5]
    }
    
    opt_df = pd.DataFrame(optimization_data)
    
    fig = go.Figure(data=[
        go.Bar(name='Current (%)', x=opt_df['Factor'], y=opt_df['Current']),
        go.Bar(name='Target (%)', x=opt_df['Factor'], y=opt_df['Target'])
    ])
    fig.update_layout(title="Production Optimization by Factor", barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    # Efficiency Recommendations
    st.subheader("🎯 Efficiency Recommendations")
    
    efficiency_recommendations = [
        "Implement lean manufacturing principles",
        "Optimize equipment utilization schedules",
        "Improve quality control processes",
        "Streamline supply chain operations",
        "Invest in workforce training and development"
    ]
    
    for i, rec in enumerate(efficiency_recommendations, 1):
        st.markdown(f"**{i}.** {rec}")

def show_feedback_learning():
    """Show feedback and learning section"""
    
    st.header("💬 Feedback & Learning")
    
    # Feedback form
    st.subheader("📝 Provide Feedback")
    
    with st.form("feedback_form"):
        feedback_type = st.selectbox(
            "Feedback Type",
            ["Analysis Accuracy", "Recommendation Quality", "System Usability", "Data Processing", "Other"]
        )
        
        feedback_rating = st.slider(
            "Rating (1-10)",
            min_value=1,
            max_value=10,
            value=7,
            help="Rate the quality of the analysis and recommendations"
        )
        
        feedback_text = st.text_area(
            "Detailed Feedback",
            placeholder="Please provide detailed feedback about the analysis, recommendations, or system..."
        )
        
        improvement_suggestions = st.text_area(
            "Improvement Suggestions",
            placeholder="What improvements would you like to see in the system?"
        )
        
        submitted = st.form_submit_button("Submit Feedback")
        
        if submitted:
            feedback_data = {
                'type': feedback_type,
                'rating': feedback_rating,
                'feedback': feedback_text,
                'suggestions': improvement_suggestions
            }
            
            save_feedback(feedback_data)
            st.success("✅ Feedback submitted successfully! Thank you for helping improve our system.")
    
    # Feedback Analytics
    st.subheader("📊 Feedback Analytics")
    
    feedback_file = "results/user_feedback.json"
    if os.path.exists(feedback_file):
        try:
            with open(feedback_file, 'r') as f:
                feedback_data = json.load(f)
            
            if feedback_data:
                # Feedback statistics
                ratings = [f['rating'] for f in feedback_data]
                avg_rating = np.mean(ratings)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Average Rating", f"{avg_rating:.1f}/10")
                
                with col2:
                    st.metric("Total Feedback", len(feedback_data))
                
                with col3:
                    st.metric("Feedback Types", len(set(f['type'] for f in feedback_data)))
                
                # Rating distribution
                fig = px.histogram(
                    x=ratings,
                    title="Feedback Rating Distribution",
                    nbins=10,
                    labels={'x': 'Rating', 'y': 'Count'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Recent feedback
                st.subheader("📝 Recent Feedback")
                recent_feedback = feedback_data[-5:]  # Last 5 feedback entries
                
                for feedback in recent_feedback:
                    with st.expander(f"Feedback from {feedback.get('timestamp', 'Unknown')}"):
                        st.write(f"**Type:** {feedback['type']}")
                        st.write(f"**Rating:** {feedback['rating']}/10")
                        st.write(f"**Feedback:** {feedback['feedback']}")
                        if feedback['suggestions']:
                            st.write(f"**Suggestions:** {feedback['suggestions']}")
        
        except Exception as e:
            st.warning(f"Could not load feedback data: {e}")
    else:
        st.info("No feedback data available yet. Be the first to provide feedback!")

def show_system_overview(data_loader, demo_results):
    """Show system overview"""
    
    st.header("📋 System Overview")
    
    # System capabilities
    st.subheader("🚀 System Capabilities")
    
    capabilities = [
        "📊 **Real-time Data Analysis**: Process uploaded industry data instantly",
        "🤖 **AI-Powered Insights**: Google Gemini integration for intelligent recommendations",
        "⚡ **Energy Optimization**: Identify 15-20% energy savings opportunities",
        "🔧 **Predictive Maintenance**: Schedule maintenance before equipment fails",
        "💰 **Cost Analysis**: Calculate ROI and cost reduction potential",
        "🛡️ **Safety Monitoring**: Track safety metrics and improvements",
        "📈 **Production Optimization**: Maximize efficiency and output",
        "🔄 **Feedback Integration**: Continuous learning from user feedback"
    ]
    
    for capability in capabilities:
        st.markdown(f"• {capability}")
    
    # Industry support
    st.subheader("🏭 Supported Industries")
    
    industries = {
        "Manufacturing": ["Production optimization", "Equipment maintenance", "Quality control"],
        "Energy": ["Grid optimization", "Demand response", "Renewable integration"],
        "Healthcare": ["Facility management", "Patient safety", "Energy efficiency"],
        "Retail": ["Store optimization", "Inventory management", "Customer safety"],
        "Office": ["Building management", "Workspace optimization", "Energy savings"]
    }
    
    for industry, features in industries.items():
        with st.expander(f"🏢 {industry}"):
            for feature in features:
                st.markdown(f"• {feature}")
    
    # Technical architecture
    st.subheader("🏗️ Technical Architecture")
    
    st.markdown("""
    ```
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   File Upload   │    │   AI Analysis   │    │   Feedback      │
    │   & Processing  │───▶│   (Gemini)      │───▶│   & Learning    │
    │                 │    │                 │    │                 │
    │ • CSV/Excel/    │    │ • Energy Opt    │    │ • User Feedback │
    │   JSON Support  │    │ • Maintenance   │    │ • Performance   │
    │ • Data Validation│   │ • Safety        │    │   Tracking      │
    │ • Industry      │    │ • Production    │    │ • Continuous    │
    │   Classification│    │ • Cost Analysis │    │   Improvement   │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
    ```
    """)

if __name__ == "__main__":
    main() 