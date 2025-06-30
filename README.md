# Xempla AI Systems Internship Dashboard

A universal Streamlit dashboard for closed-loop autonomous decision systems in asset maintenance (e.g., HVAC, energy, predictive maintenance). Integrates multi-LLM (Gemini API), advanced analytics, and feedback loops for context-aware recommendations.

## Features
- 📊 Data analytics and visualization
- 🔄 Closed-loop feedback collection and analysis
- 🤖 LLM-powered recommendations (Google Gemini, extensible)
- 🏭 Domain-specific analytics (energy, fault, maintenance)
- 🚨 Anomaly detection

## Getting Started
![WhatsApp Image 2025-06-30 at 13 03 01_f34c2281](https://github.com/user-attachments/assets/8d3f535b-6149-4d73-9c8c-81928017f551)
![WhatsApp Image 2025-06-30 at 13 04 09_82cd7a2c](https://github.com/user-attachments/assets/0656c280-ebd9-4308-9976-da416a0955e5)
![WhatsApp Image 2025-06-30 at 13 05 09_a622f0f5](https://github.com/user-attachments/assets/9e719614-d09a-4af8-9265-64cc38244beb)
![WhatsApp Image 2025-06-30 at 13 07 20_dbc03656](https://github.com/user-attachments/assets/c41bbf4b-2e7b-4318-9e82-e6bcda7b8103)
![WhatsApp Image 2025-06-30 at 13 06 44_694fbcbb](https://github.com/user-attachments/assets/5cd30850-a2ab-4260-baaf-80223d331535)


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

## Deployment (Streamlit Cloud)
- Push your code to GitHub
- Ensure `requirements.txt` and `README.md` are in the root
- Deploy via https://streamlit.io/cloud using your repo and set the main file to `xempla_final_dashboard.py`
-[view the dashboard](https://xempla-ai-dashboard-aqv4see6dlejqjmapyrmjp.streamlit.app/)

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE) 
