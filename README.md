# Xempla AI Systems Internship Dashboard

A universal Streamlit dashboard for closed-loop autonomous decision systems in asset maintenance (e.g., HVAC, energy, predictive maintenance). Integrates multi-LLM (Gemini API), advanced analytics, and feedback loops for context-aware recommendations.

## Features
- 📊 Data analytics and visualization
- 🔄 Closed-loop feedback collection and analysis
- 🤖 LLM-powered recommendations (Google Gemini, extensible)
- 🏭 Domain-specific analytics (energy, fault, maintenance)
- 🚨 Anomaly detection

## Getting Started

### Prerequisites
- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/), [Plotly](https://plotly.com/python/), [scikit-learn](https://scikit-learn.org/), [httpx](https://www.python-httpx.org/)

Install dependencies:
```bash
pip install -r requirements.txt
```

### Environment Setup
- Set your Google Gemini API key as an environment variable:
  - On Windows (PowerShell):
    ```powershell
    $env:GEMINI_API_KEY="your-gemini-api-key"
    ```
  - Or add to a `.env` file or Streamlit secrets.

### Running the Dashboard
```bash
streamlit run xempla_final_dashboard.py
```

## Project Structure
- `xempla_final_dashboard.py` — Main Streamlit app
- `xempla_ai_intern_prototype/` — Core logic, LLM integration, feedback modules
- `sample_data/` — Example datasets

## Usage
- Upload or select a CSV dataset
- Explore analytics, trends, and anomaly detection
- Submit feedback on model decisions
- Get LLM-powered recommendations for next actions

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE) 