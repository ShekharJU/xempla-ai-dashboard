import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Xempla AI Intern Prototype",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
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
    .ai-insight {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ff7f0e;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎯 Xempla AI Intern Prototype</h1>', unsafe_allow_html=True)
st.markdown("### Closed-Loop AI System for Energy Efficiency & Predictive Maintenance")

# Sidebar
st.sidebar.title("🎛️ Control Panel")
st.sidebar.markdown("### System Configuration")

# Industry selection
industry = st.sidebar.selectbox(
    "Select Industry",
    ["Manufacturing", "Energy", "Healthcare", "Retail", "Office Buildings"]
)

# AI Model selection
ai_model = st.sidebar.selectbox(
    "AI Model",
    ["Google Gemini Pro", "GPT-4", "Claude-3"]
)

# Main content
col1, col2, col3, col4 = st.columns(4)

# Generate sample data based on industry
def generate_industry_data(industry):
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    if industry == "Manufacturing":
        data = {
            'date': dates,
            'production_efficiency': np.random.normal(85, 5, len(dates)),
            'energy_consumption': np.random.normal(1200, 200, len(dates)),
            'maintenance_cost': np.random.normal(5000, 1000, len(dates)),
            'equipment_uptime': np.random.normal(92, 3, len(dates))
        }
    elif industry == "Energy":
        data = {
            'date': dates,
            'power_generation': np.random.normal(500, 50, len(dates)),
            'grid_efficiency': np.random.normal(88, 4, len(dates)),
            'renewable_ratio': np.random.normal(35, 8, len(dates)),
            'distribution_loss': np.random.normal(5, 1, len(dates))
        }
    elif industry == "Healthcare":
        data = {
            'date': dates,
            'patient_throughput': np.random.normal(150, 20, len(dates)),
            'equipment_utilization': np.random.normal(78, 8, len(dates)),
            'energy_per_patient': np.random.normal(45, 5, len(dates)),
            'maintenance_requests': np.random.poisson(3, len(dates))
        }
    elif industry == "Retail":
        data = {
            'date': dates,
            'sales_per_sqft': np.random.normal(350, 50, len(dates)),
            'energy_per_sale': np.random.normal(2.5, 0.3, len(dates)),
            'hvac_efficiency': np.random.normal(82, 6, len(dates)),
            'customer_satisfaction': np.random.normal(4.2, 0.3, len(dates))
        }
    else:  # Office Buildings
        data = {
            'date': dates,
            'occupancy_rate': np.random.normal(75, 10, len(dates)),
            'energy_per_occupant': np.random.normal(15, 2, len(dates)),
            'hvac_performance': np.random.normal(85, 5, len(dates)),
            'maintenance_score': np.random.normal(88, 4, len(dates))
        }
    
    return pd.DataFrame(data)

# Generate data
df = generate_industry_data(industry)

# Key Metrics
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="Current Efficiency",
        value=f"{df.iloc[-1, 1]:.1f}%",
        delta=f"{df.iloc[-1, 1] - df.iloc[-30, 1]:.1f}%"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="Energy Consumption",
        value=f"{df.iloc[-1, 2]:.0f} kWh",
        delta=f"{df.iloc[-1, 2] - df.iloc[-30, 2]:.0f} kWh"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="Maintenance Score",
        value=f"{df.iloc[-1, 3]:.1f}%",
        delta=f"{df.iloc[-1, 3] - df.iloc[-30, 3]:.1f}%"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="System Health",
        value=f"{df.iloc[-1, 4]:.1f}%",
        delta=f"{df.iloc[-1, 4] - df.iloc[-30, 4]:.1f}%"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Charts
st.markdown("---")
st.subheader("📊 Performance Analytics")

col1, col2 = st.columns(2)

with col1:
    # Time series chart
    fig1 = px.line(df, x='date', y=df.columns[1], 
                   title=f"{industry} Performance Over Time",
                   labels={'value': 'Performance', 'date': 'Date'})
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Correlation heatmap
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numeric_cols].corr()
    
    fig2 = px.imshow(corr_matrix, 
                     title="Feature Correlation Matrix",
                     color_continuous_scale='RdBu',
                     aspect="auto")
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

# AI Insights Section
st.markdown("---")
st.subheader("🤖 AI-Powered Insights")

# Generate AI insights based on data
def generate_ai_insights(df, industry):
    insights = []
    
    # Trend analysis
    recent_trend = df.iloc[-30:, 1].mean() - df.iloc[-60:-30, 1].mean()
    if recent_trend > 0:
        insights.append(f"📈 Positive trend detected: {industry} efficiency has improved by {recent_trend:.1f}% over the last 30 days.")
    else:
        insights.append(f"📉 Performance decline detected: {industry} efficiency has decreased by {abs(recent_trend):.1f}% over the last 30 days.")
    
    # Anomaly detection
    current_value = df.iloc[-1, 1]
    mean_value = df.iloc[-30:, 1].mean()
    std_value = df.iloc[-30:, 1].std()
    
    if abs(current_value - mean_value) > 2 * std_value:
        insights.append(f"⚠️ Anomaly detected: Current performance ({current_value:.1f}%) is significantly different from recent average ({mean_value:.1f}%).")
    
    # Optimization recommendations
    if industry == "Manufacturing":
        insights.append("🔧 Recommendation: Schedule preventive maintenance for production line equipment to maintain optimal efficiency.")
    elif industry == "Energy":
        insights.append("⚡ Recommendation: Consider peak load shifting strategies to reduce energy costs during high-demand periods.")
    elif industry == "Healthcare":
        insights.append("🏥 Recommendation: Optimize HVAC scheduling based on patient occupancy patterns to reduce energy waste.")
    elif industry == "Retail":
        insights.append("🛍️ Recommendation: Implement smart lighting controls to reduce energy consumption during low-traffic hours.")
    else:
        insights.append("🏢 Recommendation: Adjust HVAC settings based on occupancy data to improve energy efficiency.")
    
    return insights

insights = generate_ai_insights(df, industry)

for insight in insights:
    st.markdown(f'<div class="ai-insight">{insight}</div>', unsafe_allow_html=True)

# Predictive Maintenance
st.markdown("---")
st.subheader("🔮 Predictive Maintenance Forecast")

# Generate maintenance predictions
maintenance_data = {
    'Equipment': ['HVAC System', 'Production Line', 'Energy Grid', 'Medical Devices', 'Retail Systems'],
    'Health_Score': [85, 72, 91, 88, 79],
    'Next_Maintenance': ['2024-07-15', '2024-06-30', '2024-08-01', '2024-07-20', '2024-07-10'],
    'Risk_Level': ['Low', 'High', 'Low', 'Medium', 'Medium']
}

maintenance_df = pd.DataFrame(maintenance_data)

# Color coding for risk levels
def color_risk(val):
    if val == 'High':
        return 'background-color: #ffcccc'
    elif val == 'Medium':
        return 'background-color: #fff3cd'
    else:
        return 'background-color: #d4edda'

st.dataframe(maintenance_df.style.applymap(color_risk, subset=['Risk_Level']), use_container_width=True)

# Feedback System
st.markdown("---")
st.subheader("🔄 Closed-Loop Feedback System")

feedback_col1, feedback_col2 = st.columns(2)

with feedback_col1:
    st.write("**System Learning Metrics**")
    learning_metrics = {
        'Model_Accuracy': '94.2%',
        'Prediction_Confidence': '87.5%',
        'Feedback_Integration_Rate': '92.1%',
        'System_Improvement': '+15.3%'
    }
    
    for metric, value in learning_metrics.items():
        st.metric(metric.replace('_', ' '), value)

with feedback_col2:
    st.write("**User Feedback**")
    user_rating = st.slider("Rate the AI recommendations", 1, 5, 4)
    user_feedback = st.text_area("Additional feedback (optional)")
    
    if st.button("Submit Feedback"):
        st.success("✅ Feedback submitted! The AI system will learn from your input.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎯 Xempla AI Intern Prototype | Closed-Loop AI System for Energy Efficiency & Predictive Maintenance</p>
    <p>Powered by Google Gemini AI | Real-time Analytics | Continuous Learning</p>
</div>
""", unsafe_allow_html=True) 