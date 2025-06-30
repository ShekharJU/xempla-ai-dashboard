"""
Test configuration and fixtures for Xempla AI Systems Intern Prototype
"""
import sys
import os
import pytest
from unittest.mock import Mock

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

@pytest.fixture
def mock_llm_client():
    """Mock LLM client for testing"""
    mock_client = Mock()
    mock_client.generate_response.return_value = "Mock response"
    mock_client.get_embedding.return_value = [0.1] * 768
    return mock_client

@pytest.fixture
def sample_sensor_data():
    """Sample sensor data for testing"""
    return {
        'timestamp': '2024-01-01T00:00:00Z',
        'temperature': 22.5,
        'humidity': 45.0,
        'pressure': 1013.25,
        'asset_id': 'HVAC_001'
    }

@pytest.fixture
def mock_feedback_data():
    """Mock feedback data for testing"""
    return {
        'decision_id': 'dec_123',
        'outcome': 'success',
        'confidence': 0.85,
        'execution_time': 1.2,
        'context': {'asset_type': 'HVAC', 'action': 'temperature_adjust'}
    }

@pytest.fixture
def sample_building_data():
    """Sample building data for testing"""
    return {
        'building_id': 'B001',
        'floor': 1,
        'room': '101',
        'asset_type': 'HVAC',
        'temperature': 22.0,
        'humidity': 50.0,
        'energy_consumption': 1500.0,
        'timestamp': '2024-01-01T12:00:00Z'
    }

@pytest.fixture
def mock_gemini_response():
    """Mock Gemini API response for testing"""
    return {
        'candidates': [{
            'content': {
                'parts': [{
                    'text': 'Mock Gemini response for testing'
                }]
            }
        }]
    }

@pytest.fixture
def temp_feedback_file(tmp_path):
    """Temporary feedback file for testing"""
    feedback_file = tmp_path / "test_feedback.jsonl"
    return str(feedback_file) 