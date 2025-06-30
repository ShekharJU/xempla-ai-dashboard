# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from xempla_ai_intern_prototype.src.feedback import FeedbackCollector, FeedbackAnalyzer
from xempla_ai_intern_prototype.src.llm.router import LLMRouter

st.set_page_config(page_title="Universal AI Analytics Dashboard", layout="wide")

st.title("🔄 Closed-Loop AI System")

# --- Data Loading ---
  DATA_FOLDER = os.path.join(os.path.dirname(__file__), "xempla_ai_intern_prototype", "sample_data")"
st.write("Looking for CSVs in:", DATA_FOLDER)
try:
    csv_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
except Exception as e:
    csv_files = []

st.markdown("### 📂 Select Dataset")
if csv_files:
    selected_csv = st.selectbox("Choose a dataset:", csv_files, index=0)
    selected_path = os.path.join(DATA_FOLDER, selected_csv)
    try:
        data = pd.read_csv(selected_path)
        st.success(f"Loaded dataset: {selected_csv} (shape: {data.shape})")
    except Exception as e:
        st.error(f"Failed to load {selected_csv}: {e}")
        st.stop()
else:
    st.warning("No CSV files found.")
    st.stop()

# --- Model Training (if possible) ---
numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
target_col = st.selectbox("Select target for prediction (optional):", ["None"] + numeric_cols)
model_trained = False
if target_col != "None":
    features = [col for col in numeric_cols if col != target_col]
    if features:
        X = data[features]
        y = data[target_col]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        st.success(f"Model trained! MAE: {mae:.2f}, R²: {r2:.3f}")
        model_trained = True

# --- Analytics UI ---
st.header("📊 Data Overview")
st.dataframe(data.head(), use_container_width=True)

st.header("📈 Column Distributions")
for col in numeric_cols:
    st.subheader(f"Distribution: {col}")
    st.line_chart(data[col])

# --- Time Series/Trend Analysis ---
st.header("⏳ Trend Analysis")
potential_time_cols = [col for col in data.columns if "date" in col.lower() or "time" in col.lower()]
x_axis = st.selectbox("Select x-axis for trend plots (optional):", ["Index"] + potential_time_cols)
for col in numeric_cols:
    st.subheader(f"Trend: {col}")
    if x_axis != "Index" and x_axis in data.columns:
        fig = px.line(data, x=x_axis, y=col, title=f"{col} over {x_axis}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(data[col])

# --- Correlation Matrix ---
if len(numeric_cols) > 1:
    st.header("🔗 Correlation Matrix")
    corr = data[numeric_cols].corr()
    st.dataframe(corr)
    fig = px.imshow(corr, title="Correlation Matrix", color_continuous_scale='RdBu')
    st.plotly_chart(fig, use_container_width=True)

# --- AI Insights ---
st.header("\U0001F4A1 AI Insights")
if model_trained:
    st.info(f"Top feature importances for predicting {target_col}:")
    importances = model.feature_importances_
    imp_df = pd.DataFrame({"feature": features, "importance": importances}).sort_values("importance", ascending=False)
    st.dataframe(imp_df)
else:
    st.info("Train a model to see feature importances and predictions.")

# --- Feedback Loop Integration ---
st.header("\U0001F4AC Feedback Loop")
feedback_collector = FeedbackCollector()
feedback_analyzer = FeedbackAnalyzer()

with st.form("feedback_form"):
    st.write("Submit feedback on the model's decision or insights:")
    decision = st.text_input("Decision/Action taken", value="")
    context = st.text_area("Context (JSON)", value="{}")
    outcome = st.selectbox("Outcome", ["success", "failure", "needs review", "other"])
    metrics = st.text_area("Metrics (JSON)", value="{}")
    submitted = st.form_submit_button("Submit Feedback")
    if submitted:
        import json
        try:
            context_dict = json.loads(context)
        except Exception:
            context_dict = {"raw": context}
        try:
            metrics_dict = json.loads(metrics)
        except Exception:
            metrics_dict = {"raw": metrics}
        feedback_collector.collect(
            decision=decision,
            context=context_dict,
            outcome=outcome,
            metrics=metrics_dict
        )
        st.success("Feedback submitted!")

# Show recent feedback and outcome stats
st.subheader("Recent Feedback")
recent = feedback_analyzer.recent_feedback(100)
feedback_df = pd.DataFrame(recent)
if not feedback_df.empty:
    st.dataframe(feedback_df)
else:
    st.info("No feedback submitted yet.")

st.subheader("Feedback Outcome Stats")
st.write(dict(feedback_analyzer.get_outcome_stats()))

# --- Advanced Feedback Analytics ---
import plotly.express as px
if not feedback_df.empty:
    # Time-series plot
    st.subheader("Feedback Outcomes Over Time")
    if 'timestamp' in feedback_df.columns:
        feedback_df['timestamp'] = pd.to_datetime(feedback_df['timestamp'])
        fig = px.histogram(feedback_df, x='timestamp', color='outcome', barmode='group', nbins=20, title='Feedback Outcomes Over Time')
        st.plotly_chart(fig, use_container_width=True)

    # Outcome distribution
    st.subheader("Feedback Outcome Distribution")
    fig2 = px.pie(feedback_df, names='outcome', title='Outcome Distribution')
    st.plotly_chart(fig2, use_container_width=True)

    # Top decisions
    st.subheader("Most Common Decisions")
    st.write(feedback_df['decision'].value_counts().head(5))

    # Filter by outcome
    selected_outcome = st.selectbox("Filter feedback by outcome", ["All"] + feedback_df['outcome'].unique().tolist())
    if selected_outcome != "All":
        st.dataframe(feedback_df[feedback_df['outcome'] == selected_outcome])
    else:
        st.dataframe(feedback_df)
else:
    st.info("Not enough feedback for analytics.")

# --- LLM Recommendations ---
import asyncio

st.header("\U0001F916 LLM Recommendation Engine")
if st.button("Get LLM Recommendation"):
    try:
        # Summarize data and feedback for prompt
        summary = f"Data shape: {data.shape}, Columns: {list(data.columns)}. Recent feedback: {feedback_df['outcome'].value_counts().to_dict() if not feedback_df.empty else 'No feedback yet.'}"
        prompt = f"""You are an AI assistant for building operations. Given the following data summary and recent feedback, recommend the next best action for energy efficiency or maintenance. Be concise.\n\n{summary}"""
        router = LLMRouter()
        llm_response = asyncio.run(router.generate(prompt))
        st.success(f"LLM Recommendation: {llm_response}")
    except Exception as e:
        st.warning(f"LLM recommendation not available: {str(e)}")
        st.info("To enable LLM recommendations, please set your GEMINI_API_KEY environment variable.")

# --- Domain-Specific Analytics ---
st.header("\U0001F3ED Domain-Specific Analytics")
tab1, tab2, tab3 = st.tabs(["Energy Efficiency", "Fault Diagnostics", "Predictive Maintenance"])

time_col = next((col for col in data.columns if "time" in col.lower() or "date" in col.lower()), None)

with tab1:
    st.subheader("Energy Consumption Trend")
    energy_cols = [col for col in data.columns if "energy" in col.lower() or "power" in col.lower()]
    if energy_cols and time_col:
        for col in energy_cols:
            st.line_chart(data[[time_col, col]].set_index(time_col))
    else:
        st.info("No energy/power or time columns found.")

    st.subheader("Temperature vs. Power")
    temp_col = next((col for col in data.columns if "temp" in col.lower()), None)
    power_col = next((col for col in data.columns if "power" in col.lower()), None)
    if temp_col and power_col:
        st.scatter_chart(data[[temp_col, power_col]])
    else:
        st.info("No temperature or power columns found.")

with tab2:
    st.subheader("Anomaly Timeline")
    if 'anomaly' in data.columns and time_col:
        st.line_chart(data[[time_col, 'anomaly']].set_index(time_col))
    else:
        st.info("No anomaly or time columns found.")

    st.subheader("Root Cause Candidates")
    cat_cols = data.select_dtypes(include=['object', 'category']).columns
    if 'anomaly' in data.columns and not data[data['anomaly'] == -1][cat_cols].empty:
        st.write(data[data['anomaly'] == -1][cat_cols].apply(pd.Series.value_counts))
    else:
        st.info("No categorical columns or anomalies found.")

with tab3:
    st.subheader("Asset Health Timeline")
    health_cols = [col for col in data.columns if any(x in col.lower() for x in ['health', 'vibration', 'runtime', 'temperature'])]
    if health_cols and time_col:
        for col in health_cols:
            st.line_chart(data[[time_col, col]].set_index(time_col))
    else:
        st.info("No health metric or time columns found.")

    st.subheader("Maintenance Cost/Benefit")
    cost_cols = [col for col in data.columns if "cost" in col.lower()]
    if cost_cols and time_col:
        for col in cost_cols:
            st.line_chart(data[[time_col, col]].set_index(time_col))
    else:
        st.info("No cost or time columns found.")

# --- Anomaly Detection ---
if len(numeric_cols) > 1:
    st.header("🚨 Anomaly Detection")
    iso = IsolationForest(contamination=0.1, random_state=42)
    preds = iso.fit_predict(data[numeric_cols])
    data['anomaly'] = preds
    st.write(f"Detected {sum(preds==-1)} anomalies.")
    st.dataframe(data[data['anomaly']==-1])
