#!/usr/bin/env python3
"""
Load your real ARGO data into the database
"""

import pandas as pd
import sqlite3
from floatchat_system import FloatChatQueryProcessor

def load_real_argo_data():
    """Load your real ARGO data from CSV into the database"""
    print("🌊 Loading Real ARGO Data")
    print("=" * 40)
    
    try:
        # Read your real data
        print("1. Reading real_argo_data.csv...")
        df = pd.read_csv('real_argo_data.csv')
        print(f"   ✅ Loaded {len(df)} rows with columns: {list(df.columns)}")
        
        # Check the data
        print("\n2. Data preview:")
        print(df.head())
        
        # Convert column names to lowercase to match database schema
        print("\n3. Converting column names and adding missing columns...")
        
        # Rename columns to match database schema
        df = df.rename(columns={
            'LATITUDE': 'latitude',
            'LONGITUDE': 'longitude', 
            'PRES': 'pressure',
            'TEMP': 'temperature'
        })
        
        # Add missing columns for compatibility
        if 'float_id' not in df.columns:
            df['float_id'] = 'REAL_FLOAT_001'  # Single float for your data
        
        if 'cycle_number' not in df.columns:
            df['cycle_number'] = 1
        
        if 'date_time' not in df.columns:
            df['date_time'] = '2024-01-01'  # Default date
        
        # Add missing oceanographic parameters with default values
        if 'salinity' not in df.columns:
            df['salinity'] = 35.0  # Default salinity
        if 'oxygen' not in df.columns:
            df['oxygen'] = 200.0  # Default oxygen
        if 'chlorophyll' not in df.columns:
            df['chlorophyll'] = 0.5  # Default chlorophyll
        if 'source_file' not in df.columns:
            df['source_file'] = 'real_argo_data.csv'
        
        print(f"   ✅ Added missing columns. Final columns: {list(df.columns)}")
        
        # Connect to database
        print("\n4. Loading into database...")
        processor = FloatChatQueryProcessor()
        
        # Clear existing data and load real data
        conn = sqlite3.connect('argo_data.db')
        
        # Drop existing table and recreate
        conn.execute('DROP TABLE IF EXISTS argo_profiles')
        conn.commit()
        
        # Recreate table structure
        processor.setup_database()
        
        # Insert real data
        df.to_sql('argo_profiles', conn, if_exists='append', index=False)
        conn.close()
        
        print(f"   ✅ Successfully loaded {len(df)} real ARGO profiles!")
        
        # Verify the data
        print("\n5. Verifying loaded data...")
        test_result = processor.execute_query("SELECT COUNT(*) as count FROM argo_profiles")
        count = test_result.iloc[0]['count']
        print(f"   ✅ Database now contains {count} profiles")
        
        print("\n🎉 Real ARGO data loaded successfully!")
        print("🚀 Refresh your Streamlit app to see the real data!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading real data: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    load_real_argo_data()
