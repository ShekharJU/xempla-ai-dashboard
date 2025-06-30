# -*- coding: utf-8 -*-
import os
import pandas as pd
import streamlit as st
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="ML Enhanced Dashboard", layout="wide")
st.title("🎯 Xempla AI Intern Prototype - ML Enhanced Dashboard")

# Robust path to your data folder
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "archive(1)")

# List all CSV files in the folder
csv_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.csv')]

# Let user select a CSV file if available
if csv_files:
    selected_csv = st.selectbox("📂 Select Dataset", csv_files)
    df = pd.read_csv(os.path.join(DATA_FOLDER, selected_csv))
    st.success(f"Loaded {selected_csv} from {DATA_FOLDER}")
else:
    st.warning("No CSV files found in the data folder. Using synthetic data.")
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', periods=90)
    data = {
        'timestamp': dates,
        'power_usage_kwh': np.random.normal(120, 15, 90),
        'ideal_usage_kwh': np.random.normal(100, 10, 90),
        'units_produced': np.random.normal(300, 30, 90),
        'errors_detected': np.random.poisson(1, 90),
        'cost': np.random.normal(500, 50, 90),
        'production_hours': np.random.normal(8, 0.5, 90),
        'safety_incident': np.random.binomial(1, 0.05, 90)
    }
    df = pd.DataFrame(data)

# Derived metrics
df["energy_saving_%"] = ((df["ideal_usage_kwh"] - df["power_usage_kwh"]) / df["ideal_usage_kwh"]) * 100
df["production_efficiency_%"] = df["units_produced"] / df["production_hours"]
df["cost_per_unit"] = df["cost"] / df["units_produced"]
df["safe"] = df["safety_incident"].apply(lambda x: 1 if x == 0 else 0)

# Model 1: Energy Efficiency Forecast
X = df[["power_usage_kwh", "units_produced", "production_hours"]]
y = df["energy_saving_%"]
energy_model = RandomForestRegressor().fit(X, y)
df["predicted_energy_saving_%"] = energy_model.predict(X)

# Model 2: Safety Score
clf = RandomForestClassifier().fit(df[["power_usage_kwh", "production_efficiency_%", "cost_per_unit"]], df["safe"])
df["safety_probability_%"] = clf.predict_proba(df[["power_usage_kwh", "production_efficiency_%", "cost_per_unit"]])[:, 1] * 100

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Energy Savings Potential", f"{df['predicted_energy_saving_%'].mean():.2f}%")
col2.metric("Efficiency Improvement", f"{df['production_efficiency_%'].pct_change().mean() * 100:.2f}%")
col3.metric("Cost Reduction Potential", f"${df['cost'].diff().mean():.2f}")
roi = (df["units_produced"].sum() * df["cost_per_unit"].mean()) / df["cost"].sum()
col4.metric("Estimated ROI", f"{roi:.2f}x")

st.markdown("---")

# Charts
st.subheader("📈 Energy Savings: Actual vs Predicted")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['energy_saving_%'], mode='lines', name='Actual'))
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['predicted_energy_saving_%'], mode='lines', name='Predicted'))
st.plotly_chart(fig, use_container_width=True)

st.subheader("🛡️ Safety Probability Over Time")
st.line_chart(df.set_index('timestamp')["safety_probability_%"])

st.markdown("---")

# AI Insights
st.subheader("🧠 AI-Generated Insights")
energy_savings = df['predicted_energy_saving_%'].mean()
safety_score = df['safety_probability_%'].iloc[-1]
efficiency = df['production_efficiency_%'].mean()
insights = []
if energy_savings > 10:
    insights.append(f"⚡ High Energy Savings Potential: {energy_savings:.1f}% average savings predicted.")
if safety_score < 90:
    insights.append(f"⚠️ Safety Alert: Current safety score is {safety_score:.1f}%.")
else:
    insights.append(f"✅ Excellent Safety: Safety score of {safety_score:.1f}%.")
if efficiency > 35:
    insights.append(f"🚀 High Efficiency: Production efficiency at {efficiency:.1f} units/hour.")
for insight in insights:
    st.info(insight)

st.markdown("---")
st.write("**Model Performance:**")

# Calculate RMSE manually for compatibility
mse = mean_squared_error(df['energy_saving_%'], df['predicted_energy_saving_%'])
rmse = np.sqrt(mse)
st.write(f"Energy Model RMSE: {rmse:.2f}%")
st.write(f"Safety Model Accuracy: {accuracy_score(df['safe'], (df['safety_probability_%'] > 50).astype(int)):.2%}")

st.markdown("---")
st.write("**Data Preview:**")
st.dataframe(df.head()) 