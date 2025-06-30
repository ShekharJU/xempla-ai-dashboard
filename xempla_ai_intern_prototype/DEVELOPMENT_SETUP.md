# Xempla AI Prototype - Development Setup

## Quick Start

### Windows:
1. Run `setup_environment.bat`
2. Run `run_dashboard.bat` to start the dashboard
3. Run `run_tests.bat` to execute tests

### Linux/Mac:
1. Run `chmod +x *.sh && ./setup_environment.sh`
2. Run `./run_dashboard.sh` to start the dashboard  
3. Run `./run_tests.sh` to execute tests

## Manual Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

### Step-by-Step Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd xempla_ai_intern_prototype
   ```

2. **Create virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   
   # Linux/Mac
   python3 -m venv venv
   ```

3. **Activate virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run tests**:
   ```bash
   python -m pytest tests/ -v
   ```

6. **Start dashboard**:
   ```bash
   streamlit run xempla_final_dashboard.py
   ```

## Project Structure

```
xempla_ai_intern_prototype/
├── __init__.py                 # Main package init
├── src/                        # Source code
│   ├── __init__.py
│   ├── llm/                    # LLM integration
│   │   ├── __init__.py
│   │   ├── gemini_client.py
│   │   └── router.py
│   └── feedback/               # Feedback loop system
│       ├── __init__.py
│       ├── feedback_collector.py
│       ├── feedback_store.py
│       └── feedback_analyzer.py
├── simulation/                 # Data simulation
│   ├── __init__.py
│   ├── data_simulator.py
│   └── building_data_loader.py
├── utils/                      # Utilities
│   ├── __init__.py
│   └── retry.py
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_basic_functionality.py
│   ├── test_feedback_loop.py
│   ├── test_gemini_client.py
│   └── test_dashboard_functionality.py
├── sample_data/                # Sample datasets
├── deployment/                 # Deployment configs
├── requirements.txt            # Dependencies
├── pytest.ini                 # Test configuration
├── setup_environment.bat/.sh  # Environment setup scripts
├── run_tests.bat/.sh          # Test runner scripts
├── run_dashboard.bat/.sh      # Dashboard runner scripts
└── xempla_final_dashboard.py  # Main dashboard
```

## Testing

### Running Tests

**Using scripts:**
```bash
# Windows
run_tests.bat

# Linux/Mac
./run_tests.sh
```

**Manual execution:**
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_basic_functionality.py -v

# Run with coverage
python -m pytest tests/ -v --cov=src --cov=simulation --cov=utils

# Run specific test markers
python -m pytest tests/ -m "unit" -v
python -m pytest tests/ -m "integration" -v
```

### Test Coverage

Coverage reports are generated automatically when running tests:
- HTML report: `htmlcov/index.html`
- Terminal report: Shows missing lines
- Minimum coverage: 80%

### Test Categories

- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test component interactions
- **LLM tests**: Tests requiring LLM API access (marked with `@pytest.mark.llm`)
- **Dashboard tests**: Tests for dashboard functionality (marked with `@pytest.mark.dashboard`)

## Dashboard Usage

### Starting the Dashboard

**Using scripts:**
```bash
# Windows
run_dashboard.bat

# Linux/Mac
./run_dashboard.sh
```

**Manual execution:**
```bash
streamlit run xempla_final_dashboard.py --server.port 8501
```

### Dashboard Features

1. **Data Loading**: Upload CSV files or use sample data
2. **Analytics**: View data distributions, correlations, and trends
3. **Model Training**: Train ML models on your data
4. **Feedback Loop**: Submit and analyze feedback on decisions
5. **LLM Integration**: Get AI-powered recommendations
6. **Domain Analytics**: Energy efficiency, fault diagnostics, predictive maintenance

## Environment Variables

Create a `.env` file in the project root:

```env
# LLM API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: `ModuleNotFoundError` for project modules
**Solution**: 
- Ensure all directories have `__init__.py` files
- Check that virtual environment is activated
- Verify Python path includes project root

#### 2. Virtual Environment Issues
**Problem**: Virtual environment not found or not working
**Solution**:
```bash
# Remove and recreate virtual environment
rm -rf venv/  # Linux/Mac
rmdir /s venv  # Windows
python -m venv venv
```

#### 3. Dependency Installation Issues
**Problem**: Package installation fails
**Solution**:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Install packages individually if needed
pip install streamlit pandas numpy plotly
```

#### 4. Test Failures
**Problem**: Tests fail with import or path issues
**Solution**:
- Check that `conftest.py` is properly configured
- Verify `sys.path` includes project root
- Ensure all required packages are installed

#### 5. Dashboard Not Starting
**Problem**: Streamlit dashboard fails to start
**Solution**:
- Check if port 8501 is available
- Verify all dependencies are installed
- Check for syntax errors in dashboard code

#### 6. LLM API Issues
**Problem**: LLM integration not working
**Solution**:
- Verify API keys are set in environment variables
- Check API key permissions and quotas
- Test API connectivity separately

### Debug Mode

Enable debug mode for more detailed error messages:

```bash
# Set environment variable
export DEBUG=True  # Linux/Mac
set DEBUG=True     # Windows

# Or modify .env file
echo "DEBUG=True" >> .env
```

### Logging

Configure logging level in `.env`:
```env
LOG_LEVEL=DEBUG  # Options: DEBUG, INFO, WARNING, ERROR
```

## Development Workflow

### 1. Feature Development
1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes
3. Add tests for new functionality
4. Run tests: `python -m pytest tests/ -v`
5. Update documentation if needed
6. Commit changes: `git commit -m "Add new feature"`

### 2. Testing Workflow
1. Run unit tests: `python -m pytest tests/ -m "unit" -v`
2. Run integration tests: `python -m pytest tests/ -m "integration" -v`
3. Check coverage: `python -m pytest tests/ --cov=src --cov-report=html`
4. Fix any failing tests
5. Ensure coverage is above 80%

### 3. Code Quality
1. Format code: `black .`
2. Check linting: `flake8 .`
3. Type checking: `mypy .`
4. Run all quality checks before committing

## Deployment

### Local Development
```bash
# Start dashboard
./run_dashboard.sh

# Run tests
./run_tests.sh

# Check code quality
black .
flake8 .
mypy .
```

### Production Deployment
See `deployment/` directory for:
- Docker configuration
- Kubernetes manifests
- Deployment scripts
- Monitoring setup

## Support

For issues and questions:
1. Check this documentation
2. Review troubleshooting section
3. Check test output for specific error messages
4. Verify environment setup
5. Contact development team

## Contributing

1. Follow the development workflow
2. Write tests for new features
3. Maintain code quality standards
4. Update documentation as needed
5. Submit pull requests for review 