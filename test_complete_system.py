#!/usr/bin/env python3
"""
Complete System Test for FloatChat
Tests the entire pipeline from NetCDF to Streamlit app
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

def test_netcdf_processing():
    """Test NetCDF to CSV conversion"""
    print("🌊 Testing NetCDF Processing...")
    
    try:
        from data_processor import process_argo_netcdf, ArgoDataPipeline
        
        # Test with your real ARGO file
        if Path('R13857_001.nc').exists():
            print("   ✅ Found R13857_001.nc")
            
            # Process the file
            df = process_argo_netcdf('R13857_001.nc')
            if df is not None:
                print(f"   ✅ Successfully processed: {df.shape[0]} rows, {df.shape[1]} columns")
                print(f"   📊 Columns: {list(df.columns)}")
                return True
            else:
                print("   ❌ Processing failed")
                return False
        else:
            print("   ⚠️  R13857_001.nc not found, testing with sample data")
            # Create sample data and test
            pipeline = ArgoDataPipeline()
            result = pipeline.process_single_file("demo_argo_single.nc", export_format="csv")
            return result is not None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_database_integration():
    """Test database functionality"""
    print("\n🗄️ Testing Database Integration...")
    
    try:
        from floatchat_system import FloatChatQueryProcessor, load_sample_data_to_db
        
        # Test database setup
        processor = FloatChatQueryProcessor()
        print("   ✅ Database connection established")
        
        # Test sample data loading
        load_sample_data_to_db()
        print("   ✅ Sample data loaded")
        
        # Test query execution
        test_query = "SELECT COUNT(*) as count FROM argo_profiles"
        result = processor.execute_query(test_query)
        count = result.iloc[0]['count']
        print(f"   ✅ Query executed: {count} profiles in database")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_llm_integration():
    """Test LLM processing"""
    print("\n🧠 Testing LLM Integration...")
    
    try:
        from llm_integration import ArgoLLMProcessor
        
        processor = ArgoLLMProcessor()
        print("   ✅ LLM processor initialized")
        
        # Test query processing
        test_queries = [
            "Show me temperature profiles near the equator",
            "Find salinity data in the Arabian Sea",
            "Display oxygen levels in the Indian Ocean"
        ]
        
        for query in test_queries:
            result = processor.process_with_llm(query)
            if result and 'sql_query' in result:
                print(f"   ✅ Processed: '{query[:30]}...'")
            else:
                print(f"   ❌ Failed: '{query[:30]}...'")
                return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_streamlit_app():
    """Test Streamlit app components"""
    print("\n🖥️ Testing Streamlit App...")
    
    try:
        import streamlit as st
        from floatchat_system import FloatChatQueryProcessor, FloatChatVisualizer
        
        # Test query processor
        processor = FloatChatQueryProcessor()
        print("   ✅ Query processor working")
        
        # Test visualizer
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
        fig = FloatChatVisualizer.create_profile_plot(sample_data, 'temperature')
        print("   ✅ Profile visualization working")
        
        # Test map visualization
        map_viz = FloatChatVisualizer.create_map_visualization(sample_data)
        print("   ✅ Map visualization working")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run complete system test"""
    print("🌊 FloatChat Complete System Test")
    print("=" * 50)
    
    tests = [
        ("NetCDF Processing", test_netcdf_processing),
        ("Database Integration", test_database_integration),
        ("LLM Integration", test_llm_integration),
        ("Streamlit App", test_streamlit_app)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"   ❌ Unexpected error in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED! Your system is working correctly.")
        print("\n🚀 To run the Streamlit app:")
        print("   streamlit run floatchat_app.py")
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed. Check the errors above.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
