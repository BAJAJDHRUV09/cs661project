#!/usr/bin/env python3
"""
Test script to verify the earthquake data visualization app.
"""

from src.data_processor import DataProcessor
from src.visualizations import create_global_earthquake_map, create_time_series_plot

def test_data_loading():
    """Test if data loads correctly."""
    print("Testing data loading...")
    
    # Initialize data processor
    data_processor = DataProcessor()
    
    # Check if data was loaded
    if data_processor.processed_data is not None and not data_processor.processed_data.empty:
        print(f"✅ Successfully loaded {len(data_processor.processed_data)} earthquake records")
        print(f"Date range: {data_processor.processed_data['time'].min()} to {data_processor.processed_data['time'].max()}")
        print(f"Magnitude range: {data_processor.processed_data['mag'].min():.1f} to {data_processor.processed_data['mag'].max():.1f}")
        print(f"Countries found: {len(data_processor.get_countries())}")
        return True
    else:
        print("❌ Failed to load earthquake data")
        return False

def test_visualizations():
    """Test if visualizations can be created."""
    print("\nTesting visualizations...")
    
    data_processor = DataProcessor()
    
    try:
        # Test global map
        fig = create_global_earthquake_map(data_processor)
        print("✅ Global earthquake map created successfully")
        
        # Test time series
        fig = create_time_series_plot(data_processor)
        print("✅ Time series plot created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Visualization test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🌍 Earthquake Data Visualization - Test Suite")
    print("=" * 50)
    
    # Test data loading
    data_ok = test_data_loading()
    
    # Test visualizations
    viz_ok = test_visualizations()
    
    print("\n" + "=" * 50)
    if data_ok and viz_ok:
        print("🎉 All tests passed! The app should work correctly.")
        print("\nTo run the app:")
        print("python app.py")
        print("\nThen open http://localhost:8050 in your browser")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 