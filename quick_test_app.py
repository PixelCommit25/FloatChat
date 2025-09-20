#!/usr/bin/env python3
"""
Quick test to verify the app components work
"""

def test_app_components():
    """Test all app components"""
    print("🧪 Testing App Components")
    print("=" * 40)
    
    try:
        # Test imports
        print("1. Testing imports...")
        import streamlit as st
        import pandas as pd
        import plotly.express as px
        import folium
        print("   ✅ All imports successful")
        
        # Test query processor
        print("2. Testing query processor...")
        from floatchat_system import FloatChatQueryProcessor, load_sample_data_to_db
        processor = FloatChatQueryProcessor()
        load_sample_data_to_db()
        print("   ✅ Query processor working")
        
        # Test a simple query
        print("3. Testing query execution...")
        result = processor.process_natural_language_query("Show me temperature profiles")
        if result['success']:
            print(f"   ✅ Query successful: {len(result['results'])} profiles found")
        else:
            print(f"   ❌ Query failed: {result['message']}")
            return False
        
        # Test visualizer
        print("4. Testing visualizer...")
        from floatchat_system import FloatChatVisualizer
        visualizer = FloatChatVisualizer()
        
        # Create sample data
        sample_data = pd.DataFrame({
            'float_id': ['F001', 'F002'],
            'latitude': [45.0, 46.0],
            'longitude': [-30.0, -31.0],
            'pressure': [100, 150],
            'temperature': [15.0, 14.5],
            'salinity': [35.0, 35.1],
            'date_time': ['2024-01-01', '2024-01-02']
        })
        
        # Test profile plot
        fig = visualizer.create_profile_plot(sample_data, 'temperature')
        print("   ✅ Profile plot created")
        
        # Test map
        map_viz = visualizer.create_map_visualization(sample_data)
        print("   ✅ Map visualization created")
        
        print("\n🎉 All components working correctly!")
        print("🚀 The simplified app should work now!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    test_app_components()
