# Xempla AI Systems Intern Prototype

A comprehensive closed-loop AI system prototype demonstrating LLM integration, feedback mechanisms, and real-world applications in energy efficiency, predictive maintenance, and fault diagnostics.

## 🚀 Features

- **Google Gemini Integration**: Powered by Google's latest Gemini 1.5 Flash model
- **Real Building Energy Data**: Integration with comprehensive building energy consumption datasets
- **Closed-Loop Learning**: Continuous improvement through feedback mechanisms
- **Multi-Domain Applications**: Energy optimization, predictive maintenance, fault diagnosis
- **Real-Time Decision Making**: AI agents that make operational decisions
- **Performance Analytics**: Comprehensive metrics and insights

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Real Data     │    │   AI Agents     │    │   Feedback      │
│   Sources       │───▶│   (Gemini)      │───▶│   Loop          │
│                 │    │                 │    │                 │
│ • Building      │    │ • Energy Opt    │    │ • Decision      │
│   Energy Data   │    │ • Maintenance   │    │   Recording     │
│ • Weather Data  │    │ • Fault Diag    │    │ • Performance   │
│ • Sensor Data   │    │                 │    │   Tracking      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API key (free tier available)
- Basic understanding of AI/ML concepts

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd xempla_ai_intern_prototype
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   python setup_env.py
   ```
   This will guide you through creating your `.env` file with your Gemini API key.

4. **Get your Gemini API key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated key

## 🎯 Quick Start

### Option 1: Building Energy Demo (Recommended)
```bash
python building_energy_demo.py
```
This demo uses real building energy consumption data to demonstrate:
- Energy efficiency analysis
- Anomaly detection
- Optimization recommendations
- Cross-building insights

### Option 2: Quick Start Demo
```bash
python quick_start.py
```
This demo uses simulated data to show:
- Predictive maintenance
- Energy optimization
- Fault diagnosis
- Feedback loop mechanisms

## 📊 Dataset Integration

The prototype includes a comprehensive building energy dataset with:
- **500+ buildings** across different types (Office, University, Dormitory, Laboratory)
- **Hourly energy consumption** data for 2015
- **Weather data** for correlation analysis
- **Building metadata** (size, occupancy, year built, etc.)

## 🔧 Configuration

Key configuration options in `.env`:

```env
GEMINI_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-1.5-flash
MAX_TOKENS=2000
TEMPERATURE=0.7
```

## 📈 Use Cases

### 1. Energy Efficiency Optimization
- Analyze building energy consumption patterns
- Identify optimization opportunities
- Generate actionable recommendations
- Calculate potential savings and ROI

### 2. Predictive Maintenance
- Monitor equipment health indicators
- Predict maintenance needs
- Optimize maintenance schedules
- Reduce downtime and costs

### 3. Fault Diagnosis
- Detect anomalies in operational data
- Diagnose potential faults
- Provide corrective action recommendations
- Assess safety implications

## 🧠 AI Agent Capabilities

### Energy Optimization Agent
- Building efficiency analysis
- Weather correlation analysis
- Optimization scenario generation
- Cross-building pattern recognition

### Maintenance Agent
- Equipment health assessment
- Failure prediction
- Maintenance scheduling
- Cost-benefit analysis

### Fault Diagnosis Agent
- Anomaly detection
- Root cause analysis
- Safety risk assessment
- Corrective action planning

## 📊 Performance Metrics

The system tracks comprehensive metrics:
- Decision accuracy and success rates
- Energy savings achieved
- Maintenance cost reductions
- Fault detection accuracy
- Learning rate improvements

## 🔄 Feedback Loop Mechanism

1. **Decision Making**: AI agents analyze operational data
2. **Action Implementation**: Recommendations are executed
3. **Outcome Monitoring**: Results are tracked and measured
4. **Feedback Integration**: Performance data feeds back to improve future decisions
5. **Continuous Learning**: Agents adapt and improve over time

## 🚀 Future Enhancements

- Real-time data streaming integration
- Advanced anomaly detection algorithms
- Multi-agent coordination
- Integration with building management systems
- Renewable energy optimization
- Demand response capabilities

## 📝 Learning Objectives

This prototype demonstrates key concepts for AI Systems Interns:
- **LLM Integration**: Working with modern language models
- **Feedback Loops**: Implementing continuous learning systems
- **Real Data Integration**: Processing and analyzing operational data
- **Multi-Domain Applications**: Applying AI across different use cases
- **Performance Optimization**: Measuring and improving system performance

## 🤝 Contributing

This is a prototype for the Xempla AI Systems Intern role. Contributions should focus on:
- Improving AI agent performance
- Adding new use cases
- Enhancing data processing capabilities
- Optimizing feedback mechanisms

## 📄 License

This project is part of the Xempla AI Systems Intern application process.

---

**Ready to explore the future of AI-powered energy management?** 🚀 