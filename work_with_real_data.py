#!/usr/bin/env python3
"""
How to Work with Real ARGO Data
"""

import pandas as pd
import sqlite3
from floatchat_system import FloatChatQueryProcessor

def show_real_data_options():
    """Show different ways to work with real ARGO data"""
    print("🌊 Working with Real ARGO Data")
    print("=" * 50)
    
    print("\n1. 📊 Your Current Real Data:")
    print("   - File: real_argo_data.csv")
    print("   - Location: 0.267°N, 16.032°W (Atlantic Ocean)")
    print("   - Measurements: 448 temperature/pressure profiles")
    print("   - Temperature: 21-22°C (tropical waters)")
    
    print("\n2. 🔄 How to Load More Real Data:")
    print("   Option A: Download from ARGO GDAC")
    print("   Option B: Process more .nc files you have")
    print("   Option C: Use the existing real data")
    
    print("\n3. 📈 What You Can Do Right Now:")
    print("   - Query: 'Show me temperature profiles near the equator'")
    print("   - Query: 'Display all data from my real ARGO float'")
    print("   - Query: 'Find temperature data at different depths'")
    
    print("\n4. 🎯 Real Data Queries to Try:")
    
    # Load and show real data
    try:
        df = pd.read_csv('real_argo_data.csv')
        print(f"\n   📋 Your Real Data Preview:")
        print(f"   - {len(df)} measurements")
        print(f"   - Location: {df['LATITUDE'].iloc[0]:.3f}°N, {df['LONGITUDE'].iloc[0]:.3f}°W")
        print(f"   - Temperature range: {df['TEMP'].min():.2f}°C to {df['TEMP'].max():.2f}°C")
        print(f"   - Pressure range: {df['PRES'].min():.1f} to {df['PRES'].max():.1f} dbar")
        
        print(f"\n   🌡️ Sample measurements:")
        print(df[['LATITUDE', 'LONGITUDE', 'PRES', 'TEMP']].head())
        
    except Exception as e:
        print(f"   Error reading data: {e}")

def load_real_data_into_app():
    """Load real data into the app database"""
    print("\n🔄 Loading Real Data into App...")
    
    try:
        # Read real data
        df = pd.read_csv('real_argo_data.csv')
        
        # Convert to app format
        df_app = df.rename(columns={
            'LATITUDE': 'latitude',
            'LONGITUDE': 'longitude', 
            'PRES': 'pressure',
            'TEMP': 'temperature'
        })
        
        # Add missing columns
        df_app['float_id'] = 'REAL_FLOAT_001'
        df_app['cycle_number'] = 1
        df_app['date_time'] = '2024-01-01'
        df_app['salinity'] = 35.0
        df_app['oxygen'] = 200.0
        df_app['chlorophyll'] = 0.5
        df_app['source_file'] = 'real_argo_data.csv'
        
        # Load into database
        processor = FloatChatQueryProcessor()
        conn = sqlite3.connect('argo_data.db')
        
        # Clear and reload
        conn.execute('DROP TABLE IF EXISTS argo_profiles')
        conn.commit()
        processor.setup_database()
        
        df_app.to_sql('argo_profiles', conn, if_exists='append', index=False)
        conn.close()
        
        print(f"✅ Loaded {len(df_app)} real ARGO profiles!")
        print("🚀 Refresh your Streamlit app to see real data!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_real_data_queries():
    """Show example queries for real data"""
    print("\n💡 Real Data Query Examples:")
    print("=" * 40)
    
    queries = [
        "Show me temperature profiles near the equator",
        "Display all data from my real ARGO float", 
        "Find temperature data at different depths",
        "Show me data from the Atlantic Ocean",
        "Compare surface vs deep ocean temperature",
        "Find the warmest and coldest measurements"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"{i}. {query}")

def main():
    """Main function"""
    show_real_data_options()
    
    print("\n" + "="*50)
    print("🎯 What would you like to do?")
    print("1. Load real data into app")
    print("2. See query examples")
    print("3. Both")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        load_real_data_into_app()
    elif choice == "2":
        show_real_data_queries()
    elif choice == "3":
        load_real_data_into_app()
        show_real_data_queries()
    else:
        print("Invalid choice. Showing query examples:")
        show_real_data_queries()

if __name__ == "__main__":
    main()
