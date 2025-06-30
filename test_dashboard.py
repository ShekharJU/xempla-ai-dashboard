import streamlit as st

st.set_page_config(page_title="Test Dashboard", layout="wide")

st.title("🎯 Xempla AI Intern Prototype - Test Dashboard")
st.write("This is a test to verify Streamlit is working properly.")

st.header("System Status")
st.success("✅ Streamlit is running successfully!")
st.info("✅ All dependencies are installed")
st.warning("⚠️ This is a test dashboard")

st.header("Next Steps")
st.write("1. If you can see this page, Streamlit is working")
st.write("2. Close this and run the main dashboard")
st.write("3. Access the full AI system at localhost:8502")

if st.button("Test Button"):
    st.balloons()
    st.write("🎉 Everything is working!") 