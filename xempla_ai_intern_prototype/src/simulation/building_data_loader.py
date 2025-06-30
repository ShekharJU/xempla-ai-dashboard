"""
Building Energy Dataset Loader for Xempla AI Systems Intern Prototype

This module provides specialized data loading and preprocessing for the building
energy dataset, enabling real-world energy efficiency analysis and optimization.
"""

import pandas as pd
import numpy as np
import os
import glob
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class BuildingEnergyDataLoader:
    """
    Loader for building energy consumption and weather data
    """
    
    def __init__(self, data_path: str = "data/building_energy_dataset"):
        self.data_path = data_path
        self.meta_data = None
        self.building_data = {}
        self.weather_data = {}
        
        # Load metadata
        self._load_metadata()
        
    def _load_metadata(self):
        """Load building metadata"""
        meta_file = os.path.join(self.data_path, "meta_open.csv")
        if os.path.exists(meta_file):
            self.meta_data = pd.read_csv(meta_file)
            logger.info(f"Loaded metadata for {len(self.meta_data)} buildings")
        else:
            logger.warning("Metadata file not found")
    
    def get_building_info(self, building_id: str) -> Optional[Dict]:
        """Get information about a specific building"""
        if self.meta_data is None:
            return None
        
        building_info = self.meta_data[self.meta_data['uid'] == building_id]
        if len(building_info) > 0:
            return building_info.iloc[0].to_dict()
        return None
    
    def load_building_energy_data(self, building_id: str) -> Optional[pd.DataFrame]:
        """
        Load energy consumption data for a specific building
        
        Args:
            building_id: Building identifier (e.g., 'Office_Abigail')
            
        Returns:
            DataFrame with timestamp and energy consumption
        """
        if building_id in self.building_data:
            return self.building_data[building_id]
        
        file_path = os.path.join(self.data_path, f"{building_id}.csv")
        if not os.path.exists(file_path):
            logger.warning(f"Building data file not found: {file_path}")
            return None
        
        try:
            data = pd.read_csv(file_path)
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            data.set_index('timestamp', inplace=True)
            
            # Rename column to standard format
            energy_col = [col for col in data.columns if col != 'timestamp'][0]
            data.rename(columns={energy_col: 'energy_consumption'}, inplace=True)
            
            self.building_data[building_id] = data
            logger.info(f"Loaded energy data for {building_id}: {len(data)} records")
            return data
            
        except Exception as e:
            logger.error(f"Error loading building data for {building_id}: {e}")
            return None
    
    def load_weather_data(self, weather_file: str) -> Optional[pd.DataFrame]:
        """
        Load weather data for a specific location
        
        Args:
            weather_file: Weather file name (e.g., 'weather0.csv')
            
        Returns:
            DataFrame with weather parameters
        """
        if weather_file in self.weather_data:
            return self.weather_data[weather_file]
        
        file_path = os.path.join(self.data_path, weather_file)
        if not os.path.exists(file_path):
            logger.warning(f"Weather data file not found: {file_path}")
            return None
        
        try:
            data = pd.read_csv(file_path)
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            data.set_index('timestamp', inplace=True)
            
            # Clean up column names and remove HTML tags
            data.columns = [col.replace('<br />', '').strip() for col in data.columns]
            
            # Convert numeric columns
            numeric_columns = ['TemperatureC', 'Dew PointC', 'Humidity', 'Sea Level PressurehPa', 
                             'VisibilityKm', 'Wind SpeedKm/h', 'Gust SpeedKm/h', 'Precipitationmm']
            
            for col in numeric_columns:
                if col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors='coerce')
            
            self.weather_data[weather_file] = data
            logger.info(f"Loaded weather data from {weather_file}: {len(data)} records")
            return data
            
        except Exception as e:
            logger.error(f"Error loading weather data from {weather_file}: {e}")
            return None
    
    def get_combined_data(self, building_id: str, start_date: Optional[str] = None, 
                         end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        Get combined building energy and weather data
        
        Args:
            building_id: Building identifier
            start_date: Start date for data filtering (YYYY-MM-DD)
            end_date: End date for data filtering (YYYY-MM-DD)
            
        Returns:
            DataFrame with combined energy and weather data
        """
        # Load building data
        building_data = self.load_building_energy_data(building_id)
        if building_data is None:
            return None
        
        # Get building info to find weather file
        building_info = self.get_building_info(building_id)
        if building_info is None:
            logger.warning(f"No metadata found for building {building_id}")
            return building_data
        
        weather_file = building_info.get('newweatherfile', 'weather0.csv')
        weather_data = self.load_weather_data(weather_file)
        
        if weather_data is None:
            logger.warning(f"No weather data available for {building_id}")
            return building_data
        
        # Merge building and weather data
        combined_data = building_data.merge(weather_data, left_index=True, right_index=True, how='left')
        
        # Filter by date range if specified
        if start_date:
            combined_data = combined_data[combined_data.index >= start_date]
        if end_date:
            combined_data = combined_data[combined_data.index <= end_date]
        
        # Add building metadata
        combined_data['building_id'] = building_id
        combined_data['building_type'] = building_info.get('primaryspaceusage', 'Unknown')
        combined_data['sqft'] = building_info.get('sqft', 0)
        combined_data['occupants'] = building_info.get('occupants', 0)
        
        logger.info(f"Combined data for {building_id}: {len(combined_data)} records")
        return combined_data
    
    def get_energy_efficiency_features(self, building_id: str) -> Optional[Dict]:
        """
        Extract energy efficiency features for AI analysis
        
        Args:
            building_id: Building identifier
            
        Returns:
            Dictionary with energy efficiency features
        """
        data = self.get_combined_data(building_id)
        if data is None or len(data) == 0:
            return None
        
        # Calculate energy efficiency metrics
        features = {
            'building_id': building_id,
            'total_energy_consumption': data['energy_consumption'].sum(),
            'avg_daily_consumption': data['energy_consumption'].resample('D').sum().mean(),
            'peak_consumption': data['energy_consumption'].max(),
            'energy_variability': data['energy_consumption'].std(),
            'avg_temperature': data.get('TemperatureC', pd.Series()).mean(),
            'temperature_range': data.get('TemperatureC', pd.Series()).max() - data.get('TemperatureC', pd.Series()).min(),
            'avg_humidity': data.get('Humidity', pd.Series()).mean(),
            'heating_degree_days': self._calculate_heating_degree_days(data),
            'cooling_degree_days': self._calculate_cooling_degree_days(data),
            'energy_intensity': data['energy_consumption'].sum() / data.get('sqft', 1).iloc[0] if data.get('sqft', 1).iloc[0] > 0 else 0,
            'occupancy_efficiency': data['energy_consumption'].sum() / data.get('occupants', 1).iloc[0] if data.get('occupants', 1).iloc[0] > 0 else 0
        }
        
        return features
    
    def _calculate_heating_degree_days(self, data: pd.DataFrame, base_temp: float = 18.0) -> float:
        """Calculate heating degree days"""
        if 'TemperatureC' not in data.columns:
            return 0.0
        
        daily_temp = data['TemperatureC'].resample('D').mean()
        hdd = daily_temp[daily_temp < base_temp].apply(lambda x: base_temp - x).sum()
        return hdd
    
    def _calculate_cooling_degree_days(self, data: pd.DataFrame, base_temp: float = 18.0) -> float:
        """Calculate cooling degree days"""
        if 'TemperatureC' not in data.columns:
            return 0.0
        
        daily_temp = data['TemperatureC'].resample('D').mean()
        cdd = daily_temp[daily_temp > base_temp].apply(lambda x: x - base_temp).sum()
        return cdd
    
    def get_anomaly_detection_data(self, building_id: str) -> Optional[pd.DataFrame]:
        """
        Prepare data for anomaly detection in energy consumption
        
        Args:
            building_id: Building identifier
            
        Returns:
            DataFrame with features for anomaly detection
        """
        data = self.get_combined_data(building_id)
        if data is None:
            return None
        
        # Create features for anomaly detection
        anomaly_data = data.copy()
        
        # Add time-based features
        anomaly_data['hour'] = anomaly_data.index.hour
        anomaly_data['day_of_week'] = anomaly_data.index.dayofweek
        anomaly_data['month'] = anomaly_data.index.month
        
        # Add rolling statistics
        anomaly_data['energy_ma_24h'] = anomaly_data['energy_consumption'].rolling(window=24).mean()
        anomaly_data['energy_std_24h'] = anomaly_data['energy_consumption'].rolling(window=24).std()
        
        # Add weather-based features
        if 'TemperatureC' in anomaly_data.columns:
            anomaly_data['temp_ma_24h'] = anomaly_data['TemperatureC'].rolling(window=24).mean()
            anomaly_data['temp_deviation'] = anomaly_data['TemperatureC'] - anomaly_data['temp_ma_24h']
        
        # Remove rows with NaN values
        anomaly_data = anomaly_data.dropna()
        
        return anomaly_data
    
    def get_optimization_scenarios(self, building_id: str) -> List[Dict]:
        """
        Generate optimization scenarios for energy efficiency
        
        Args:
            building_id: Building identifier
            
        Returns:
            List of optimization scenarios
        """
        data = self.get_combined_data(building_id)
        if data is None:
            return []
        
        scenarios = []
        
        # Scenario 1: Temperature optimization
        if 'TemperatureC' in data.columns:
            scenarios.append({
                'scenario_id': f'{building_id}_temp_optimization',
                'type': 'temperature_optimization',
                'current_avg_temp': data['TemperatureC'].mean(),
                'target_temp_range': (20, 24),  # Celsius
                'potential_savings': 0.15,  # 15% potential savings
                'implementation_cost': 5000,
                'payback_period_months': 12
            })
        
        # Scenario 2: Occupancy-based optimization
        if 'occupants' in data.columns and data['occupants'].iloc[0] > 0:
            scenarios.append({
                'scenario_id': f'{building_id}_occupancy_optimization',
                'type': 'occupancy_optimization',
                'current_occupancy': data['occupants'].iloc[0],
                'target_occupancy_efficiency': 0.8,
                'potential_savings': 0.10,  # 10% potential savings
                'implementation_cost': 3000,
                'payback_period_months': 8
            })
        
        # Scenario 3: HVAC optimization
        scenarios.append({
            'scenario_id': f'{building_id}_hvac_optimization',
            'type': 'hvac_optimization',
            'current_efficiency': 0.75,  # Estimated
            'target_efficiency': 0.85,
            'potential_savings': 0.20,  # 20% potential savings
            'implementation_cost': 15000,
            'payback_period_months': 24
        })
        
        return scenarios
    
    def list_available_buildings(self) -> List[str]:
        """Get list of available building IDs"""
        if self.meta_data is None:
            return []
        
        return self.meta_data['uid'].tolist()
    
    def get_building_statistics(self) -> Dict:
        """Get overall statistics for the dataset"""
        if self.meta_data is None:
            return {}
        
        stats = {
            'total_buildings': len(self.meta_data),
            'building_types': self.meta_data['primaryspaceusage'].value_counts().to_dict(),
            'avg_sqft': self.meta_data['sqft'].mean(),
            'avg_occupants': self.meta_data['occupants'].mean(),
            'year_built_range': {
                'min': self.meta_data['yearbuilt'].min(),
                'max': self.meta_data['yearbuilt'].max()
            },
            'timezones': self.meta_data['timezone'].value_counts().to_dict()
        }
        
        return stats 