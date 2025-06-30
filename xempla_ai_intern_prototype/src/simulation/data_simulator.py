"""
Data Simulator for AI Systems Intern Prototype

This module generates realistic operational data for testing closed-loop AI systems
in energy efficiency, predictive maintenance, and fault diagnostics applications.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)

class DataSimulator:
    """
    Simulates operational data for various industrial systems
    """
    
    def __init__(self, seed: int = 42):
        self.seed = seed
        np.random.seed(seed)
        random.seed(seed)
        
    def generate_hvac_data(self, days: int = 30, frequency_minutes: int = 15) -> pd.DataFrame:
        """
        Generate HVAC system operational data
        
        Args:
            days: Number of days to simulate
            frequency_minutes: Data collection frequency in minutes
            
        Returns:
            DataFrame with HVAC operational parameters
        """
        timestamps = pd.date_range(
            start=datetime.now() - timedelta(days=days),
            end=datetime.now(),
            freq=f'{frequency_minutes}T'
        )
        
        n_samples = len(timestamps)
        
        # Base parameters with realistic ranges
        data = {
            'timestamp': timestamps,
            'temperature_setpoint': np.random.normal(22, 2, n_samples),  # Celsius
            'actual_temperature': np.random.normal(22, 3, n_samples),   # Celsius
            'humidity': np.random.normal(45, 10, n_samples),            # %
            'energy_consumption': np.random.normal(50, 15, n_samples),  # kWh
            'compressor_runtime': np.random.normal(70, 20, n_samples),  # %
            'fan_speed': np.random.normal(60, 15, n_samples),          # %
            'filter_pressure_drop': np.random.normal(0.5, 0.2, n_samples),  # Pa
            'refrigerant_pressure': np.random.normal(300, 50, n_samples),    # kPa
            'efficiency': np.random.normal(85, 8, n_samples),           # %
        }
        
        # Add seasonal patterns
        seasonal_factor = np.sin(2 * np.pi * np.arange(n_samples) / (24 * 4))  # Daily cycle
        data['energy_consumption'] += seasonal_factor * 10
        data['actual_temperature'] += seasonal_factor * 2
        
        # Add some anomalies for fault detection
        anomaly_indices = random.sample(range(n_samples), n_samples // 20)
        for idx in anomaly_indices:
            data['energy_consumption'][idx] *= 1.5
            data['efficiency'][idx] *= 0.8
        
        return pd.DataFrame(data)
    
    def generate_manufacturing_data(self, hours: int = 168) -> pd.DataFrame:
        """
        Generate manufacturing equipment operational data
        
        Args:
            hours: Number of hours to simulate
            
        Returns:
            DataFrame with manufacturing equipment parameters
        """
        timestamps = pd.date_range(
            start=datetime.now() - timedelta(hours=hours),
            end=datetime.now(),
            freq='1H'
        )
        
        n_samples = len(timestamps)
        
        data = {
            'timestamp': timestamps,
            'motor_vibration': np.random.normal(2.5, 0.8, n_samples),      # mm/s
            'bearing_temperature': np.random.normal(65, 15, n_samples),     # Celsius
            'oil_pressure': np.random.normal(200, 30, n_samples),          # kPa
            'oil_temperature': np.random.normal(80, 10, n_samples),        # Celsius
            'motor_current': np.random.normal(45, 8, n_samples),           # A
            'motor_voltage': np.random.normal(480, 20, n_samples),         # V
            'power_factor': np.random.normal(0.85, 0.05, n_samples),       # unitless
            'efficiency': np.random.normal(92, 3, n_samples),              # %
            'operating_hours': np.arange(n_samples),                       # hours
        }
        
        # Simulate equipment degradation over time
        degradation_factor = np.arange(n_samples) / n_samples * 0.3
        data['motor_vibration'] += degradation_factor
        data['bearing_temperature'] += degradation_factor * 10
        data['efficiency'] -= degradation_factor * 5
        
        # Add random faults
        fault_indices = random.sample(range(n_samples), n_samples // 15)
        for idx in fault_indices:
            data['motor_vibration'][idx] *= 2.5
            data['bearing_temperature'][idx] += 30
            data['efficiency'][idx] *= 0.7
        
        return pd.DataFrame(data)
    
    def generate_energy_grid_data(self, days: int = 7) -> pd.DataFrame:
        """
        Generate energy grid operational data
        
        Args:
            days: Number of days to simulate
            
        Returns:
            DataFrame with energy grid parameters
        """
        timestamps = pd.date_range(
            start=datetime.now() - timedelta(days=days),
            end=datetime.now(),
            freq='1H'
        )
        
        n_samples = len(timestamps)
        
        # Base load with daily and weekly patterns
        base_load = 1000  # MW
        daily_pattern = np.sin(2 * np.pi * np.arange(n_samples) / 24) * 200
        weekly_pattern = np.sin(2 * np.pi * np.arange(n_samples) / (24 * 7)) * 100
        
        data = {
            'timestamp': timestamps,
            'total_load': base_load + daily_pattern + weekly_pattern + np.random.normal(0, 50, n_samples),
            'renewable_generation': np.random.normal(300, 100, n_samples),
            'grid_frequency': np.random.normal(50, 0.1, n_samples),        # Hz
            'voltage_level': np.random.normal(230, 5, n_samples),          # V
            'power_factor': np.random.normal(0.95, 0.03, n_samples),
            'transmission_losses': np.random.normal(5, 1, n_samples),      # %
            'system_efficiency': np.random.normal(88, 2, n_samples),       # %
            'peak_demand': np.random.normal(1200, 150, n_samples),        # MW
        }
        
        # Add renewable energy variability
        solar_pattern = np.maximum(0, np.sin(np.pi * (np.arange(n_samples) % 24) / 12)) * 200
        data['renewable_generation'] += solar_pattern
        
        return pd.DataFrame(data)
    
    def generate_predictive_maintenance_data(self, cycles: int = 1000) -> pd.DataFrame:
        """
        Generate data for predictive maintenance simulation (NASA Turbofan dataset style)
        
        Args:
            cycles: Number of operational cycles to simulate
            
        Returns:
            DataFrame with engine degradation parameters
        """
        # Simulate engine operational cycles
        cycle_numbers = np.arange(1, cycles + 1)
        
        # Engine parameters with degradation over time
        data = {
            'cycle': cycle_numbers,
            'op1': np.random.normal(0, 1, cycles),                    # Operational setting 1
            'op2': np.random.normal(0, 1, cycles),                    # Operational setting 2
            'op3': np.random.normal(100, 10, cycles),                 # Operational setting 3
            'sensor1': np.random.normal(518.67, 33.6, cycles),        # Temperature sensor
            'sensor2': np.random.normal(642.0, 106.9, cycles),        # Pressure sensor
            'sensor3': np.random.normal(1589.1, 112.8, cycles),       # Pressure sensor
            'sensor4': np.random.normal(1400.0, 20.0, cycles),        # Temperature sensor
            'sensor5': np.random.normal(14.62, 8.05, cycles),         # Pressure sensor
            'sensor6': np.random.normal(21.61, 8.45, cycles),         # Pressure sensor
            'sensor7': np.random.normal(553.9, 33.3, cycles),         # Temperature sensor
            'sensor8': np.random.normal(2388.0, 45.1, cycles),        # Pressure sensor
            'sensor9': np.random.normal(9046.0, 521.0, cycles),       # Pressure sensor
            'sensor10': np.random.normal(1.3, 0.4, cycles),           # Pressure sensor
            'sensor11': np.random.normal(47.47, 5.29, cycles),        # Pressure sensor
            'sensor12': np.random.normal(521.66, 6.06, cycles),       # Temperature sensor
            'sensor13': np.random.normal(2388.06, 45.1, cycles),      # Pressure sensor
            'sensor14': np.random.normal(8138.62, 29.1, cycles),      # Pressure sensor
            'sensor15': np.random.normal(8.4195, 0.4, cycles),        # Pressure sensor
            'sensor16': np.random.normal(0.03, 0.01, cycles),         # Pressure sensor
            'sensor17': np.random.normal(392, 7, cycles),             # Temperature sensor
            'sensor18': np.random.normal(2388, 45, cycles),           # Pressure sensor
            'sensor19': np.random.normal(100, 0, cycles),             # Pressure sensor
            'sensor20': np.random.normal(39.06, 1.94, cycles),        # Pressure sensor
            'sensor21': np.random.normal(23.419, 1.52, cycles),       # Pressure sensor
        }
        
        # Add degradation patterns
        degradation_rate = np.arange(cycles) / cycles
        
        # Degrade critical sensors over time
        critical_sensors = ['sensor1', 'sensor2', 'sensor3', 'sensor4', 'sensor5']
        for sensor in critical_sensors:
            data[sensor] += degradation_rate * np.random.normal(10, 2, cycles)
        
        # Add random noise and anomalies
        for sensor in data.keys():
            if sensor != 'cycle':
                # Add some random anomalies
                anomaly_indices = random.sample(range(cycles), cycles // 50)
                for idx in anomaly_indices:
                    data[sensor][idx] *= np.random.uniform(1.2, 1.8)
        
        return pd.DataFrame(data)
    
    def generate_fault_scenarios(self, n_scenarios: int = 10) -> List[Dict[str, Any]]:
        """
        Generate realistic fault scenarios for testing
        
        Args:
            n_scenarios: Number of fault scenarios to generate
            
        Returns:
            List of fault scenario dictionaries
        """
        fault_types = [
            'bearing_wear',
            'motor_overheating',
            'vibration_anomaly',
            'oil_contamination',
            'electrical_fault',
            'sensor_failure',
            'control_system_fault',
            'mechanical_wear',
            'thermal_stress',
            'lubrication_failure'
        ]
        
        scenarios = []
        for i in range(n_scenarios):
            fault_type = random.choice(fault_types)
            
            scenario = {
                'scenario_id': f'fault_{i+1:03d}',
                'fault_type': fault_type,
                'severity': random.choice(['low', 'medium', 'high', 'critical']),
                'detection_delay_hours': random.randint(1, 72),
                'repair_time_hours': random.randint(2, 48),
                'cost_impact': random.uniform(1000, 50000),
                'safety_risk': random.choice(['low', 'medium', 'high']),
                'operational_impact': random.choice(['minimal', 'moderate', 'significant', 'severe']),
                'preventable': random.choice([True, False]),
                'detection_method': random.choice(['vibration_analysis', 'thermal_imaging', 'oil_analysis', 'acoustic_monitoring']),
                'recommended_actions': self._generate_recommendations(fault_type)
            }
            
            scenarios.append(scenario)
        
        return scenarios
    
    def _generate_recommendations(self, fault_type: str) -> List[str]:
        """Generate recommendations based on fault type"""
        recommendations = {
            'bearing_wear': [
                'Schedule bearing replacement within 48 hours',
                'Monitor vibration levels continuously',
                'Check lubrication system',
                'Reduce operational load if possible'
            ],
            'motor_overheating': [
                'Immediate shutdown recommended',
                'Check cooling system',
                'Inspect electrical connections',
                'Verify load conditions'
            ],
            'vibration_anomaly': [
                'Perform detailed vibration analysis',
                'Check alignment and balance',
                'Inspect mounting and foundation',
                'Monitor trend for 24 hours'
            ],
            'oil_contamination': [
                'Change oil immediately',
                'Identify contamination source',
                'Clean oil system',
                'Implement oil analysis program'
            ],
            'electrical_fault': [
                'Isolate electrical system',
                'Check insulation resistance',
                'Inspect electrical connections',
                'Verify protective devices'
            ]
        }
        
        return recommendations.get(fault_type, [
            'Perform detailed inspection',
            'Monitor system parameters',
            'Consult maintenance manual',
            'Schedule maintenance review'
        ]) 