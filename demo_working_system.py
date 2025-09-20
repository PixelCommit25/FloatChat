#!/usr/bin/env python3
"""
Demo script showing the working FloatChat system
"""

import pandas as pd
from floatchat_system import FloatChatQueryProcessor, FloatChatVisualizer, load_sample_data_to_db

def demo_working_system():
    """Demonstrate the working FloatChat system"""
    print("🌊 FloatChat Working System Demo")
    print("=" * 50)
    
    # Initialize components
    print("1. Initializing system components...")
    processor = FloatChatQueryProcessor()
    visualizer = FloatChatVisualizer()
    
    # Load sample data
    print("2. Loading sample data...")
    load_sample_data_to_db()
    
    # Test queries
    print("3. Testing natural language queries...")
    
    queries = [
        "Show me temperature profiles near the equator",
        "Find salinity data in the Arabian Sea", 
        "Display oxygen levels in the Indian Ocean",
        "Show me all data from the last 6 months"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n📝 Query {i}: {query}")
        print("-" * 50)
        
        # Process query
        result = processor.process_natural_language_query(query)
        
        if result['success']:
            df = result['results']
            print(f"✅ Success: Found {len(df)} profiles")
            print(f"📊 Data shape: {df.shape}")
            print(f"🗺️  Geographic range: {df['latitude'].min():.2f}° to {df['latitude'].max():.2f}°N")
            print(f"🌊 Depth range: {df['pressure'].min():.0f} to {df['pressure'].max():.0f} dbar")
            
            # Show sample data
            print("\n📋 Sample data:")
            print(df[['float_id', 'latitude', 'longitude', 'temperature', 'salinity']].head(3))
            
        else:
            print(f"❌ Failed: {result['message']}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed successfully!")
    print("\n🚀 To run the full Streamlit app:")
    print("   streamlit run floatchat_app.py")
    print("\n💡 Try these queries in the app:")
    for query in queries:
        print(f"   • {query}")

if __name__ == "__main__":
    demo_working_system()
