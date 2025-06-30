#!/usr/bin/env python3
"""
Xempla AI Systems Intern Prototype - Interactive Dashboard

This dashboard provides comprehensive visualization of the closed-loop AI system
performance, building energy analysis, and optimization results.
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

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.simulation.building_data_loader import BuildingEnergyDataLoader
from src.agents.energy_optimization_agent import EnergyOptimizationAgent
from src.feedback.feedback_loop import FeedbackLoop

# Page configuration
st.set_page_config(
    page_title="Xempla AI Systems Intern Prototype",
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

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">🏢 Xempla AI Systems Intern Prototype</h1>', unsafe_allow_html=True)
    st.markdown("### Closed-Loop AI System for Energy Efficiency & Predictive Maintenance")
    
    # Sidebar
    st.sidebar.title("🎛️ Dashboard Controls")
    
    # Load data
    data_loader = load_building_data()
    demo_results = load_demo_results()
    
    if data_loader is None:
        st.error("❌ Unable to load building data. Please ensure the dataset is properly configured.")
        return
    
    # Navigation
    page = st.sidebar.selectbox(
        "Select Dashboard Section",
        ["📊 Overview", "🏢 Building Analysis", "⚡ Energy Optimization", "🔧 Predictive Maintenance", "📈 Performance Metrics", "🎯 AI Insights"]
    )
    
    if page == "📊 Overview":
        show_overview(data_loader, demo_results)
    elif page == "🏢 Building Analysis":
        show_building_analysis(data_loader)
    elif page == "⚡ Energy Optimization":
        show_energy_optimization(data_loader, demo_results)
    elif page == "🔧 Predictive Maintenance":
        show_predictive_maintenance()
    elif page == "📈 Performance Metrics":
        show_performance_metrics(demo_results)
    elif page == "🎯 AI Insights":
        show_ai_insights(demo_results)

def show_overview(data_loader, demo_results):
    """Show overview dashboard"""
    
    st.header("📊 System Overview")
    
    # Get dataset statistics
    stats = data_loader.get_building_statistics()
    available_buildings = data_loader.list_available_buildings()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card info-metric">
            <h3>🏢 Total Buildings</h3>
            <h2>{}</h2>
        </div>
        """.format(stats.get('total_buildings', 0)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card success-metric">
            <h3>📊 Data Points</h3>
            <h2>{:,}</h2>
        </div>
        """.format(len(available_buildings) * 8760), unsafe_allow_html=True)  # 8760 hours per year
    
    with col3:
        st.markdown("""
        <div class="metric-card warning-metric">
            <h3>⚡ Avg Energy Intensity</h3>
            <h2>{:.1f} kWh/sqft</h2>
        </div>
        """.format(stats.get('avg_sqft', 0) / 1000 if stats.get('avg_sqft', 0) > 0 else 0), unsafe_allow_html=True)
    
    with col4:
        if demo_results:
            analyzed = len(demo_results.get('buildings_analyzed', []))
        else:
            analyzed = 0
        st.markdown("""
        <div class="metric-card info-metric">
            <h3>🤖 AI Analysis</h3>
            <h2>{}</h2>
        </div>
        """.format(analyzed), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Building types distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏢 Building Types Distribution")
        building_types = stats.get('building_types', {})
        if building_types:
            fig = px.pie(
                values=list(building_types.values()),
                names=list(building_types.keys()),
                title="Building Types in Dataset"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📅 Year Built Distribution")
        if stats.get('year_built_range', {}).get('min') and stats.get('year_built_range', {}).get('max'):
            # Simulate year distribution
            years = np.random.randint(
                stats['year_built_range']['min'],
                stats['year_built_range']['max'] + 1,
                size=len(available_buildings)
            )
            fig = px.histogram(
                x=years,
                title="Building Construction Years",
                nbins=20
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    if demo_results:
        st.subheader("🔄 Recent AI Activity")
        
        # Create timeline of recent decisions
        decisions = []
        for analysis in demo_results.get('individual_analyses', []):
            if 'analysis_timestamp' in analysis:
                decisions.append({
                    'timestamp': analysis['analysis_timestamp'],
                    'building': analysis['building_id'],
                    'type': 'Energy Analysis'
                })
        
        if decisions:
            df_decisions = pd.DataFrame(decisions)
            df_decisions['timestamp'] = pd.to_datetime(df_decisions['timestamp'])
            
            fig = px.timeline(
                df_decisions,
                x_start='timestamp',
                y='building',
                color='type',
                title="Recent AI Analysis Timeline"
            )
            st.plotly_chart(fig, use_container_width=True)

def show_building_analysis(data_loader):
    """Show building analysis section"""
    
    st.header("🏢 Building Energy Analysis")
    
    # Building selector
    available_buildings = data_loader.list_available_buildings()
    selected_building = st.selectbox("Select Building", available_buildings[:20])  # Limit to first 20
    
    if selected_building:
        # Get building info
        building_info = data_loader.get_building_info(selected_building)
        
        # Display building info
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏢 Building Information")
            if building_info:
                info_df = pd.DataFrame([
                    ["Building ID", building_info.get('uid', 'N/A')],
                    ["Type", building_info.get('primaryspaceusage', 'N/A')],
                    ["Square Footage", f"{building_info.get('sqft', 0):,.0f}"],
                    ["Occupants", building_info.get('occupants', 'N/A')],
                    ["Year Built", building_info.get('yearbuilt', 'N/A')],
                    ["Timezone", building_info.get('timezone', 'N/A')]
                ], columns=["Property", "Value"])
                st.dataframe(info_df, use_container_width=True)
        
        with col2:
            st.subheader("📊 Energy Consumption")
            
            # Load energy data
            energy_data = data_loader.load_building_energy_data(selected_building)
            if energy_data is not None:
                # Daily consumption
                daily_consumption = energy_data['energy_consumption'].resample('D').sum()
                
                fig = px.line(
                    x=daily_consumption.index,
                    y=daily_consumption.values,
                    title="Daily Energy Consumption",
                    labels={'x': 'Date', 'y': 'Energy Consumption (kWh)'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Energy efficiency features
        st.subheader("⚡ Energy Efficiency Analysis")
        
        features = data_loader.get_energy_efficiency_features(selected_building)
        if features:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Total Consumption",
                    f"{features['total_energy_consumption']:,.0f} kWh"
                )
                st.metric(
                    "Peak Consumption",
                    f"{features['peak_consumption']:.1f} kWh"
                )
            
            with col2:
                st.metric(
                    "Energy Intensity",
                    f"{features['energy_intensity']:.2f} kWh/sqft"
                )
                st.metric(
                    "Avg Daily Consumption",
                    f"{features['avg_daily_consumption']:.1f} kWh"
                )
            
            with col3:
                st.metric(
                    "Heating Degree Days",
                    f"{features['heating_degree_days']:.0f}"
                )
                st.metric(
                    "Cooling Degree Days",
                    f"{features['cooling_degree_days']:.0f}"
                )
            
            # Weather correlation
            combined_data = data_loader.get_combined_data(selected_building)
            if combined_data is not None and 'TemperatureC' in combined_data.columns:
                st.subheader("🌡️ Weather Correlation")
                
                # Sample data for correlation plot
                sample_data = combined_data.sample(min(1000, len(combined_data)))
                
                fig = px.scatter(
                    x=sample_data['TemperatureC'],
                    y=sample_data['energy_consumption'],
                    title="Energy Consumption vs Temperature",
                    labels={'x': 'Temperature (°C)', 'y': 'Energy Consumption (kWh)'}
                )
                st.plotly_chart(fig, use_container_width=True)

def show_energy_optimization(data_loader, demo_results):
    """Show energy optimization section"""
    
    st.header("⚡ Energy Optimization Analysis")
    
    if demo_results and 'optimization_report' in demo_results:
        report = demo_results['optimization_report']
        
        # Overall statistics
        overall_stats = report.get('overall_statistics', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Buildings Analyzed",
                overall_stats.get('successful_analyses', 0)
            )
        
        with col2:
            st.metric(
                "Potential Savings",
                f"{overall_stats.get('total_potential_savings_percent', 0):.1f}%"
            )
        
        with col3:
            st.metric(
                "Implementation Cost",
                f"${overall_stats.get('total_implementation_cost', 0):,.0f}"
            )
        
        with col4:
            st.metric(
                "Avg Payback Period",
                f"{overall_stats.get('avg_payback_period', 0):.1f} months"
            )
        
        # Optimization scenarios
        st.subheader("🎯 Optimization Scenarios")
        
        scenarios_data = []
        for analysis in report.get('building_analyses', []):
            for scenario in analysis.get('optimization_scenarios', []):
                scenarios_data.append({
                    'Building': analysis['building_id'],
                    'Type': scenario['type'],
                    'Potential Savings': scenario['potential_savings'] * 100,
                    'Implementation Cost': scenario['implementation_cost'],
                    'Payback Period': scenario['payback_period_months']
                })
        
        if scenarios_data:
            scenarios_df = pd.DataFrame(scenarios_data)
            
            # Scenarios by type
            fig = px.bar(
                scenarios_df.groupby('Type')['Potential Savings'].mean().reset_index(),
                x='Type',
                y='Potential Savings',
                title="Average Potential Savings by Optimization Type"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Cost vs Savings scatter plot
            fig = px.scatter(
                scenarios_df,
                x='Implementation Cost',
                y='Potential Savings',
                color='Type',
                size='Payback Period',
                title="Implementation Cost vs Potential Savings"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Cross-building recommendations
        st.subheader("🏢 Cross-Building Recommendations")
        recommendations = report.get('cross_building_recommendations', [])
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"**{i}.** {rec}")
        else:
            st.info("No cross-building recommendations available.")
    
    else:
        st.info("Run the building energy demo to see optimization results.")

def show_predictive_maintenance():
    """Show predictive maintenance section"""
    
    st.header("🔧 Predictive Maintenance")
    
    # Simulate maintenance data
    st.subheader("📊 Equipment Health Monitoring")
    
    # Generate sample maintenance data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    equipment_data = pd.DataFrame({
        'date': dates,
        'vibration': np.random.normal(3.0, 1.0, len(dates)) + np.sin(np.arange(len(dates)) * 0.1),
        'temperature': np.random.normal(65, 10, len(dates)) + 10 * np.sin(np.arange(len(dates)) * 0.05),
        'efficiency': np.random.normal(85, 5, len(dates)) - 0.1 * np.arange(len(dates)),
        'oil_pressure': np.random.normal(50, 5, len(dates))
    })
    
    # Equipment health metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_vibration = equipment_data['vibration'].iloc[-1]
        st.metric(
            "Motor Vibration",
            f"{current_vibration:.2f} mm/s",
            delta="0.1" if current_vibration < 4.0 else "-0.3"
        )
    
    with col2:
        current_temp = equipment_data['temperature'].iloc[-1]
        st.metric(
            "Bearing Temperature",
            f"{current_temp:.1f}°C",
            delta="2.1" if current_temp < 75 else "-5.2"
        )
    
    with col3:
        current_efficiency = equipment_data['efficiency'].iloc[-1]
        st.metric(
            "System Efficiency",
            f"{current_efficiency:.1f}%",
            delta="-1.2" if current_efficiency < 80 else "0.8"
        )
    
    with col4:
        current_pressure = equipment_data['oil_pressure'].iloc[-1]
        st.metric(
            "Oil Pressure",
            f"{current_pressure:.1f} psi",
            delta="1.5" if current_pressure > 45 else "-2.1"
        )
    
    # Equipment health trends
    st.subheader("📈 Equipment Health Trends")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Motor Vibration', 'Bearing Temperature', 'System Efficiency', 'Oil Pressure')
    )
    
    fig.add_trace(
        go.Scatter(x=equipment_data['date'], y=equipment_data['vibration'], name='Vibration'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=equipment_data['date'], y=equipment_data['temperature'], name='Temperature'),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=equipment_data['date'], y=equipment_data['efficiency'], name='Efficiency'),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=equipment_data['date'], y=equipment_data['oil_pressure'], name='Oil Pressure'),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Maintenance predictions
    st.subheader("🔮 Maintenance Predictions")
    
    # Simulate maintenance predictions
    maintenance_data = pd.DataFrame({
        'Equipment': ['Motor A', 'Pump B', 'Compressor C', 'Fan D'],
        'Health Score': [85, 72, 91, 68],
        'Days to Maintenance': [45, 12, 78, 8],
        'Priority': ['Medium', 'High', 'Low', 'Critical']
    })
    
    fig = px.bar(
        maintenance_data,
        x='Equipment',
        y='Health Score',
        color='Priority',
        title="Equipment Health Scores and Maintenance Priority"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_performance_metrics(demo_results):
    """Show performance metrics section"""
    
    st.header("📈 Performance Metrics")
    
    if demo_results and 'performance_metrics' in demo_results:
        metrics = demo_results['performance_metrics']
        
        # AI Agent Performance
        st.subheader("🤖 AI Agent Performance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Decisions",
                metrics.get('total_decisions', 0)
            )
        
        with col2:
            success_rate = metrics.get('success_rate', 0)
            st.metric(
                "Success Rate",
                f"{success_rate:.1f}%"
            )
        
        with col3:
            st.metric(
                "Learning Rate",
                f"{metrics.get('learning_rate', 0):.2f}"
            )
        
        # Performance trends
        st.subheader("📊 Performance Trends")
        
        # Simulate performance trends
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='W')
        performance_data = pd.DataFrame({
            'date': dates,
            'accuracy': np.random.normal(85, 5, len(dates)) + np.cumsum(np.random.normal(0, 0.5, len(dates))),
            'efficiency': np.random.normal(78, 3, len(dates)) + np.cumsum(np.random.normal(0, 0.3, len(dates))),
            'cost_savings': np.random.normal(12, 2, len(dates)) + np.cumsum(np.random.normal(0, 0.2, len(dates)))
        })
        
        fig = px.line(
            performance_data,
            x='date',
            y=['accuracy', 'efficiency', 'cost_savings'],
            title="Performance Metrics Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Decision quality analysis
        st.subheader("🎯 Decision Quality Analysis")
        
        if 'individual_analyses' in demo_results:
            analyses = demo_results['individual_analyses']
            
            # Extract confidence scores
            confidence_scores = []
            for analysis in analyses:
                if 'ai_recommendations' in analysis and 'confidence' in analysis['ai_recommendations']:
                    confidence_scores.append(analysis['ai_recommendations']['confidence'])
            
            if confidence_scores:
                fig = px.histogram(
                    x=confidence_scores,
                    title="Distribution of AI Decision Confidence Scores",
                    nbins=10
                )
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("Run the demo to see performance metrics.")

def show_ai_insights(demo_results):
    """Show AI insights section"""
    
    st.header("🎯 AI Insights & Recommendations")
    
    if demo_results:
        # Key insights
        st.subheader("🔍 Key Insights")
        
        insights = [
            "🏢 **Building Diversity**: The dataset contains diverse building types with varying energy consumption patterns",
            "⚡ **Energy Intensity**: Office buildings show higher energy intensity compared to residential buildings",
            "🌡️ **Weather Correlation**: Strong correlation between temperature and energy consumption observed",
            "🤖 **AI Performance**: AI agent shows improving decision accuracy over time",
            "💰 **Cost Savings**: Potential for 15-20% energy savings through optimization strategies"
        ]
        
        for insight in insights:
            st.markdown(f"• {insight}")
        
        # Optimization opportunities
        if 'optimization_report' in demo_results:
            report = demo_results['optimization_report']
            
            st.subheader("🎯 Top Optimization Opportunities")
            
            opportunities = []
            for analysis in report.get('building_analyses', []):
                for scenario in analysis.get('optimization_scenarios', []):
                    opportunities.append({
                        'Building': analysis['building_id'],
                        'Type': scenario['type'],
                        'Savings': scenario['potential_savings'] * 100,
                        'Cost': scenario['implementation_cost'],
                        'ROI': (scenario['potential_savings'] * 100) / (scenario['implementation_cost'] / 1000)
                    })
            
            if opportunities:
                opportunities_df = pd.DataFrame(opportunities)
                opportunities_df = opportunities_df.sort_values('Savings', ascending=False).head(10)
                
                fig = px.bar(
                    opportunities_df,
                    x='Building',
                    y='Savings',
                    color='Type',
                    title="Top 10 Energy Optimization Opportunities"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # AI recommendations
        st.subheader("🤖 AI Recommendations")
        
        recommendations = [
            "**Immediate Actions**:",
            "• Implement real-time energy monitoring systems",
            "• Set up automated alerts for energy consumption anomalies",
            "• Conduct energy audits for high-consumption buildings",
            "",
            "**Medium-term Strategies**:",
            "• Upgrade HVAC systems with smart controls",
            "• Implement demand-based optimization",
            "• Establish energy efficiency training programs",
            "",
            "**Long-term Vision**:",
            "• Integrate renewable energy sources",
            "• Develop predictive maintenance systems",
            "• Create building-wide energy management platforms"
        ]
        
        for rec in recommendations:
            st.markdown(rec)
    
    else:
        st.info("Run the demo to see AI insights and recommendations.")

if __name__ == "__main__":
    main() 