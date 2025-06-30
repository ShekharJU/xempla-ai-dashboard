#!/usr/bin/env python3
"""
Sample Data Generator for Xempla AI Systems Intern Prototype

This script generates realistic sample data for different industries
to test the enhanced dashboard capabilities.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_manufacturing_data(days=30):
    """Generate sample manufacturing data"""
    
    # Generate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Generate realistic manufacturing data
    np.random.seed(42)  # For reproducible results
    
    data = {
        'timestamp': dates,
        'energy_consumption': np.random.normal(1000, 200, len(dates)) + 200 * np.sin(np.arange(len(dates)) * 0.1),
        'efficiency': np.random.normal(85, 5, len(dates)) + 5 * np.sin(np.arange(len(dates)) * 0.05),
        'cost': np.random.normal(5000, 1000, len(dates)) + 1000 * np.sin(np.arange(len(dates)) * 0.08),
        'safety_score': np.random.normal(92, 3, len(dates)) + 3 * np.sin(np.arange(len(dates)) * 0.03),
        'production': np.random.normal(100, 15, len(dates)) + 15 * np.sin(np.arange(len(dates)) * 0.06),
        'temperature': np.random.normal(22, 2, len(dates)) + 2 * np.sin(np.arange(len(dates)) * 0.04),
        'humidity': np.random.normal(45, 5, len(dates)) + 5 * np.sin(np.arange(len(dates)) * 0.02)
    }
    
    # Ensure realistic ranges
    data['energy_consumption'] = np.maximum(data['energy_consumption'], 500)
    data['efficiency'] = np.clip(data['efficiency'], 70, 95)
    data['cost'] = np.maximum(data['cost'], 2000)
    data['safety_score'] = np.clip(data['safety_score'], 85, 100)
    data['production'] = np.maximum(data['production'], 50)
    
    return pd.DataFrame(data)

def generate_energy_data(days=30):
    """Generate sample energy grid data"""
    
    # Generate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Generate realistic energy data
    np.random.seed(42)
    
    data = {
        'timestamp': dates,
        'energy_consumption': np.random.normal(5000, 800, len(dates)) + 800 * np.sin(np.arange(len(dates)) * 0.15),
        'efficiency': np.random.normal(88, 3, len(dates)) + 3 * np.sin(np.arange(len(dates)) * 0.04),
        'cost': np.random.normal(15000, 3000, len(dates)) + 3000 * np.sin(np.arange(len(dates)) * 0.12),
        'safety_score': np.random.normal(95, 2, len(dates)) + 2 * np.sin(np.arange(len(dates)) * 0.02),
        'grid_stability': np.random.normal(98, 1, len(dates)) + 1 * np.sin(np.arange(len(dates)) * 0.01),
        'renewable_percentage': np.random.normal(25, 5, len(dates)) + 5 * np.sin(np.arange(len(dates)) * 0.03),
        'demand_response': np.random.normal(85, 8, len(dates)) + 8 * np.sin(np.arange(len(dates)) * 0.05)
    }
    
    # Ensure realistic ranges
    data['energy_consumption'] = np.maximum(data['energy_consumption'], 3000)
    data['efficiency'] = np.clip(data['efficiency'], 80, 95)
    data['cost'] = np.maximum(data['cost'], 8000)
    data['safety_score'] = np.clip(data['safety_score'], 90, 100)
    data['grid_stability'] = np.clip(data['grid_stability'], 95, 100)
    data['renewable_percentage'] = np.clip(data['renewable_percentage'], 10, 40)
    data['demand_response'] = np.clip(data['demand_response'], 70, 95)
    
    return pd.DataFrame(data)

def generate_healthcare_data(days=30):
    """Generate sample healthcare facility data"""
    
    # Generate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Generate realistic healthcare data
    np.random.seed(42)
    
    data = {
        'timestamp': dates,
        'energy_consumption': np.random.normal(800, 150, len(dates)) + 150 * np.sin(np.arange(len(dates)) * 0.12),
        'efficiency': np.random.normal(82, 4, len(dates)) + 4 * np.sin(np.arange(len(dates)) * 0.06),
        'cost': np.random.normal(8000, 1500, len(dates)) + 1500 * np.sin(np.arange(len(dates)) * 0.10),
        'safety_score': np.random.normal(96, 2, len(dates)) + 2 * np.sin(np.arange(len(dates)) * 0.02),
        'patient_comfort': np.random.normal(88, 3, len(dates)) + 3 * np.sin(np.arange(len(dates)) * 0.04),
        'air_quality': np.random.normal(92, 2, len(dates)) + 2 * np.sin(np.arange(len(dates)) * 0.03),
        'medical_equipment_uptime': np.random.normal(95, 2, len(dates)) + 2 * np.sin(np.arange(len(dates)) * 0.02)
    }
    
    # Ensure realistic ranges
    data['energy_consumption'] = np.maximum(data['energy_consumption'], 400)
    data['efficiency'] = np.clip(data['efficiency'], 75, 90)
    data['cost'] = np.maximum(data['cost'], 5000)
    data['safety_score'] = np.clip(data['safety_score'], 90, 100)
    data['patient_comfort'] = np.clip(data['patient_comfort'], 80, 95)
    data['air_quality'] = np.clip(data['air_quality'], 85, 98)
    data['medical_equipment_uptime'] = np.clip(data['medical_equipment_uptime'], 90, 99)
    
    return pd.DataFrame(data)

def generate_retail_data(days=30):
    """Generate sample retail store data"""
    
    # Generate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Generate realistic retail data
    np.random.seed(42)
    
    data = {
        'timestamp': dates,
        'energy_consumption': np.random.normal(600, 120, len(dates)) + 120 * np.sin(np.arange(len(dates)) * 0.14),
        'efficiency': np.random.normal(78, 6, len(dates)) + 6 * np.sin(np.arange(len(dates)) * 0.07),
        'cost': np.random.normal(4000, 800, len(dates)) + 800 * np.sin(np.arange(len(dates)) * 0.11),
        'safety_score': np.random.normal(89, 4, len(dates)) + 4 * np.sin(np.arange(len(dates)) * 0.04),
        'customer_satisfaction': np.random.normal(85, 5, len(dates)) + 5 * np.sin(np.arange(len(dates)) * 0.05),
        'inventory_accuracy': np.random.normal(92, 3, len(dates)) + 3 * np.sin(np.arange(len(dates)) * 0.03),
        'sales_performance': np.random.normal(100, 20, len(dates)) + 20 * np.sin(np.arange(len(dates)) * 0.08)
    }
    
    # Ensure realistic ranges
    data['energy_consumption'] = np.maximum(data['energy_consumption'], 300)
    data['efficiency'] = np.clip(data['efficiency'], 70, 85)
    data['cost'] = np.maximum(data['cost'], 2500)
    data['safety_score'] = np.clip(data['safety_score'], 80, 95)
    data['customer_satisfaction'] = np.clip(data['customer_satisfaction'], 75, 95)
    data['inventory_accuracy'] = np.clip(data['inventory_accuracy'], 85, 98)
    data['sales_performance'] = np.maximum(data['sales_performance'], 50)
    
    return pd.DataFrame(data)

def generate_office_data(days=30):
    """Generate sample office building data"""
    
    # Generate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Generate realistic office data
    np.random.seed(42)
    
    data = {
        'timestamp': dates,
        'energy_consumption': np.random.normal(400, 80, len(dates)) + 80 * np.sin(np.arange(len(dates)) * 0.13),
        'efficiency': np.random.normal(80, 5, len(dates)) + 5 * np.sin(np.arange(len(dates)) * 0.06),
        'cost': np.random.normal(3000, 600, len(dates)) + 600 * np.sin(np.arange(len(dates)) * 0.09),
        'safety_score': np.random.normal(91, 3, len(dates)) + 3 * np.sin(np.arange(len(dates)) * 0.03),
        'occupant_comfort': np.random.normal(87, 4, len(dates)) + 4 * np.sin(np.arange(len(dates)) * 0.05),
        'workspace_utilization': np.random.normal(75, 8, len(dates)) + 8 * np.sin(np.arange(len(dates)) * 0.07),
        'productivity_score': np.random.normal(82, 6, len(dates)) + 6 * np.sin(np.arange(len(dates)) * 0.04)
    }
    
    # Ensure realistic ranges
    data['energy_consumption'] = np.maximum(data['energy_consumption'], 200)
    data['efficiency'] = np.clip(data['efficiency'], 70, 88)
    data['cost'] = np.maximum(data['cost'], 1500)
    data['safety_score'] = np.clip(data['safety_score'], 85, 98)
    data['occupant_comfort'] = np.clip(data['occupant_comfort'], 80, 95)
    data['workspace_utilization'] = np.clip(data['workspace_utilization'], 60, 90)
    data['productivity_score'] = np.clip(data['productivity_score'], 70, 90)
    
    return pd.DataFrame(data)

def main():
    """Main function to generate sample data"""
    
    print("🏢 Xempla AI Systems - Sample Data Generator")
    print("=" * 50)
    
    # Create sample data directory
    os.makedirs("sample_data", exist_ok=True)
    
    # Generate data for each industry
    industries = {
        'manufacturing': generate_manufacturing_data,
        'energy': generate_energy_data,
        'healthcare': generate_healthcare_data,
        'retail': generate_retail_data,
        'office': generate_office_data
    }
    
    for industry, generator_func in industries.items():
        print(f"Generating {industry.title()} data...")
        df = generator_func()
        
        # Save to CSV
        filename = f"sample_data/{industry}_sample_data.csv"
        df.to_csv(filename, index=False)
        
        print(f"✅ Saved {filename} ({len(df)} records)")
        print(f"   Columns: {', '.join(df.columns)}")
        print(f"   Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        print()
    
    print("🎉 Sample data generation complete!")
    print("\n📁 Generated files:")
    for industry in industries.keys():
        print(f"   • sample_data/{industry}_sample_data.csv")
    
    print("\n💡 Use these files to test the enhanced dashboard:")
    print("   1. Run: streamlit run enhanced_dashboard.py")
    print("   2. Go to 'File Upload & Analysis' section")
    print("   3. Upload any of the generated CSV files")
    print("   4. Select the appropriate industry type")
    print("   5. Click 'Analyze Data with AI'")

if __name__ == "__main__":
    main() 