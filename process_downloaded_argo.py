#!/usr/bin/env python3
"""
Process Downloaded ARGO Files
Process your downloaded ARGO NetCDF file and integrate with FloatChat
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import xarray as xr
import sqlite3
from datetime import datetime
import logging

# Import our components
from data_processor import ArgoDataPipeline, process_argo_netcdf
from floatchat_system import FloatChatQueryProcessor

def analyze_argo_file(netcdf_path: str):
    """
    Analyze the structure and content of an ARGO NetCDF file
    """
    print(f"🔍 Analyzing ARGO file: {netcdf_path}")
    print("=" * 60)
    
    try:
        # Open with xarray to see the structure
        ds = xr.open_dataset(netcdf_path)
        
        print("📊 File Information:")
        print(f"   File: {Path(netcdf_path).name}")
        print(f"   Dimensions: {dict(ds.dims)}")
        print(f"   Variables: {list(ds.data_vars.keys())}")
        print(f"   Coordinates: {list(ds.coords.keys())}")
        
        # Show global attributes
        print(f"\n🏷️ Global Attributes:")
        for attr, value in ds.attrs.items():
            print(f"   {attr}: {value}")
        
        # Show data variables with their shapes
        print(f"\n📈 Data Variables:")
        for var_name, var in ds.data_vars.items():
            print(f"   {var_name}: {var.dims} - {var.shape}")
            if hasattr(var, 'long_name'):
                print(f"      Description: {var.long_name}")
            if hasattr(var, 'units'):
                print(f"      Units: {var.units}")
        
        # Show coordinate information
        print(f"\n🗺️ Coordinates:")
        for coord_name, coord in ds.coords.items():
            print(f"   {coord_name}: {coord.dims} - {coord.shape}")
            if coord.size > 0:
                if coord.size == 1:
                    print(f"      Value: {coord.values}")
                else:
                    print(f"      Range: {coord.min().values} to {coord.max().values}")
        
        # Check for oceanographic parameters
        print(f"\n🌊 Oceanographic Parameters Found:")
        ocean_params = {
            'TEMP': 'Temperature',
            'PSAL': 'Practical Salinity', 
            'PRES': 'Pressure',
            'DOXY': 'Dissolved Oxygen',
            'CHLA': 'Chlorophyll-a',
            'BBP': 'Backscattering',
            'CDOM': 'Colored Dissolved Organic Matter'
        }
        
        found_params = []
        for param, description in ocean_params.items():
            if param in ds.data_vars:
                found_params.append(param)
                var = ds.data_vars[param]
                try:
                    # Handle fill values more carefully
                    if hasattr(var, '_FillValue'):
                        fill_value = var._FillValue
                    elif hasattr(var, 'attrs') and '_FillValue' in var.attrs:
                        fill_value = var.attrs['_FillValue']
                    else:
                        fill_value = 99999.0  # Common ARGO fill value
                    
                    # Get valid data
                    valid_data = var.where(var != fill_value)
                    valid_data = valid_data.where(~np.isnan(valid_data))
                    
                    if valid_data.count() > 0:
                        print(f"   ✅ {param} ({description})")
                        print(f"      Range: {float(valid_data.min()):.3f} to {float(valid_data.max()):.3f}")
                        if hasattr(var, 'units'):
                            print(f"      Units: {var.units}")
                        print(f"      Valid measurements: {int(valid_data.count())}")
                    else:
                        print(f"   ⚠️ {param} ({description}) - No valid data")
                except Exception as e:
                    print(f"   ⚠️ {param} ({description}) - Error reading data: {str(e)}")
        
        if not found_params:
            print("   ❌ No standard oceanographic parameters found")
        
        # Geographic and temporal info
        if 'LATITUDE' in ds.coords:
            lat = ds.coords['LATITUDE'].values
            print(f"\n🌍 Geographic Location:")
            print(f"   Latitude: {lat}")
        
        if 'LONGITUDE' in ds.coords:
            lon = ds.coords['LONGITUDE'].values
            print(f"   Longitude: {lon}")
        
        if 'JULD' in ds.coords:
            # ARGO uses Julian days
            juld = ds.coords['JULD'].values
            print(f"\n⏰ Temporal Information:")
            print(f"   Julian Day: {juld}")
            
            # Convert to readable date
            try:
                # ARGO reference date is 1950-01-01
                reference_date = pd.Timestamp('1950-01-01')
                actual_date = reference_date + pd.Timedelta(days=float(juld))
                print(f"   Date: {actual_date.strftime('%Y-%m-%d %H:%M:%S')}")
            except:
                print(f"   Date: Could not convert Julian day")
        
        ds.close()
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing file: {str(e)}")
        return False

def process_argo_to_floatchat(netcdf_path: str):
    """
    Process ARGO file and set up FloatChat database
    """
    print(f"\n🔄 Processing ARGO file for FloatChat...")
    
    # Process the NetCDF file
    df = process_argo_netcdf(netcdf_path)
    
    if df is None or len(df) == 0:
        print("❌ Failed to process NetCDF file")
        return False
    
    print(f"✅ Processed {len(df)} profiles")
    print(f"   Columns: {list(df.columns)}")
    
    # Save as CSV and Parquet
    csv_path = "real_argo_data.csv"
    parquet_path = "real_argo_data.parquet"
    
    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)
    
    print(f"✅ Saved processed data:")
    print(f"   CSV: {csv_path}")
    print(f"   Parquet: {parquet_path}")
    
    # Create FloatChat database
    print(f"\n🗄️ Creating FloatChat database...")
    
    db_path = "argo_data.db"
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE argo_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            float_id TEXT,
            cycle_number INTEGER,
            latitude REAL,
            longitude REAL,
            date_time TEXT,
            pressure REAL,
            temperature REAL,
            salinity REAL,
            oxygen REAL,
            chlorophyll REAL,
            source_file TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Prepare data for insertion
    float_id = extract_float_id_from_filename(netcdf_path)
    
    insert_data = []
    for idx, row in df.iterrows():
        insert_data.append({
            'float_id': float_id,
            'cycle_number': idx % 100,
            'latitude': row.get('LATITUDE', None),
            'longitude': row.get('LONGITUDE', None),
            'date_time': str(row.get('TIME', datetime.now().strftime('%Y-%m-%d'))),
            'pressure': row.get('PRES', None),
            'temperature': row.get('TEMP', None),
            'salinity': row.get('PSAL', None),
            'oxygen': row.get('DOXY', None),
            'chlorophyll': row.get('CHLA', None),
            'source_file': Path(netcdf_path).name
        })
    
    # Insert data
    insert_df = pd.DataFrame(insert_data)
    insert_df.to_sql('argo_profiles', conn, if_exists='append', index=False)
    
    # Create indexes
    cursor.execute('CREATE INDEX idx_location ON argo_profiles (latitude, longitude)')
    cursor.execute('CREATE INDEX idx_time ON argo_profiles (date_time)')
    cursor.execute('CREATE INDEX idx_float ON argo_profiles (float_id)')
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database created: {db_path}")
    print(f"   Records: {len(insert_data)}")
    print(f"   Float ID: {float_id}")
    
    # Test the database
    print(f"\n🧪 Testing database...")
    processor = FloatChatQueryProcessor(db_path)
    test_query = "SELECT COUNT(*) as count FROM argo_profiles"
    result = processor.execute_query(test_query)
    print(f"   Database test: {result.iloc[0]['count']} records found")
    
    return True

def extract_float_id_from_filename(filepath: str) -> str:
    """
    Extract float ID from ARGO filename
    Example: R13857_001.nc -> FLOAT_13857
    """
    filename = Path(filepath).stem
    
    # Look for pattern like R13857 or 13857
    import re
    match = re.search(r'[R]?(\d+)', filename)
    if match:
        return f"FLOAT_{match.group(1)}"
    
    return "FLOAT_UNKNOWN"

def show_data_summary(csv_path: str = "real_argo_data.csv"):
    """
    Show summary of processed data
    """
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return
    
    df = pd.read_csv(csv_path)
    
    print(f"\n📊 Data Summary")
    print("=" * 30)
    print(f"Total profiles: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    
    # Geographic extent
    if 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
        lat_data = df['LATITUDE'].dropna()
        lon_data = df['LONGITUDE'].dropna()
        if len(lat_data) > 0:
            print(f"Latitude range: {lat_data.min():.3f}° to {lat_data.max():.3f}°")
            print(f"Longitude range: {lon_data.min():.3f}° to {lon_data.max():.3f}°")
    
    # Oceanographic parameters
    ocean_params = ['TEMP', 'PSAL', 'PRES', 'DOXY', 'CHLA']
    for param in ocean_params:
        if param in df.columns:
            param_data = df[param].dropna()
            if len(param_data) > 0:
                print(f"{param}: {param_data.min():.3f} to {param_data.max():.3f} (mean: {param_data.mean():.3f})")
    
    # Show first few rows
    print(f"\n👀 Sample Data:")
    print(df.head(3))

def main():
    """
    Main function to process downloaded ARGO file
    """
    print("🌊 Process Downloaded ARGO File")
    print("=" * 40)
    
    # Look for NetCDF files in current directory
    netcdf_files = list(Path('.').glob('*.nc'))
    
    if not netcdf_files:
        print("❌ No NetCDF files found in current directory")
        print("Please make sure your ARGO .nc file is in the same folder as this script")
        return
    
    print(f"📁 Found NetCDF files:")
    for i, file in enumerate(netcdf_files):
        print(f"   {i+1}. {file.name}")
    
    # If only one file, use it automatically
    if len(netcdf_files) == 1:
        selected_file = netcdf_files[0]
        print(f"\n🎯 Using: {selected_file.name}")
    else:
        # Let user choose
        try:
            choice = int(input(f"\nSelect file (1-{len(netcdf_files)}): ")) - 1
            selected_file = netcdf_files[choice]
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            return
    
    # Analyze the file
    success = analyze_argo_file(str(selected_file))
    if not success:
        return
    
    # Ask user if they want to process it
    print(f"\n" + "="*60)
    process = input("Process this file for FloatChat? (y/n): ")
    
    if process.lower() == 'y':
        success = process_argo_to_floatchat(str(selected_file))
        
        if success:
            show_data_summary()
            
            print(f"\n🎉 Setup Complete!")
            print(f"Your ARGO data is ready for FloatChat!")
            print(f"\n🚀 Next steps:")
            print(f"1. Run: streamlit run floatchat_app.py")
            print(f"2. Try queries like:")
            print(f"   - 'Show me temperature profiles from this float'")
            print(f"   - 'Display salinity data'")
            print(f"   - 'What is the depth range of measurements?'")
        else:
            print(f"❌ Processing failed")
    else:
        print("Processing cancelled")

if __name__ == "__main__":
    main()