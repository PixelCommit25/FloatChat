#!/usr/bin/env python3
"""
Your NetCDF to CSV Converter
This is your main tool for converting .nc files to simple CSV files
"""

from data_processor import ArgoDataPipeline, process_argo_netcdf
import pandas as pd
from pathlib import Path

def convert_single_netcdf(netcdf_file, output_format="csv"):
    """
    Convert one NetCDF file to CSV - YOUR MAIN JOB!
    
    Args:
        netcdf_file: Path to your .nc file
        output_format: "csv" or "both" (csv + parquet)
    """
    print(f"🔄 Converting {netcdf_file} to CSV...")
    
    # Method 1: Simple conversion
    df = process_argo_netcdf(netcdf_file)
    if df is not None:
        # Save as CSV
        output_file = f"{Path(netcdf_file).stem}_converted.csv"
        df.to_csv(output_file, index=False)
        print(f"✅ Saved: {output_file}")
        print(f"📊 Rows: {len(df)}, Columns: {list(df.columns)}")
        return output_file
    else:
        print("❌ Conversion failed")
        return None

def convert_multiple_netcdf(netcdf_files, output_format="csv"):
    """
    Convert multiple NetCDF files to CSV - BATCH PROCESSING
    """
    print(f"🔄 Converting {len(netcdf_files)} files...")
    
    pipeline = ArgoDataPipeline()
    results = []
    
    for netcdf_file in netcdf_files:
        result = pipeline.process_single_file(netcdf_file, output_format)
        if result:
            results.append(result)
            print(f"✅ {netcdf_file} → {result['output_files']}")
    
    return results

def show_netcdf_info(netcdf_file):
    """
    Show what's inside a NetCDF file before converting
    """
    print(f"📋 Analyzing {netcdf_file}...")
    
    try:
        import xarray as xr
        ds = xr.open_dataset(netcdf_file)
        
        print(f"📊 Dataset Info:")
        print(f"   Dimensions: {dict(ds.dims)}")
        print(f"   Variables: {list(ds.data_vars.keys())}")
        print(f"   Coordinates: {list(ds.coords.keys())}")
        
        # Show sample data
        if 'TEMP' in ds.data_vars:
            print(f"   Temperature range: {ds['TEMP'].min().values:.2f} to {ds['TEMP'].max().values:.2f} °C")
        if 'PRES' in ds.data_vars:
            print(f"   Pressure range: {ds['PRES'].min().values:.1f} to {ds['PRES'].max().values:.1f} dbar")
        
        ds.close()
        
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")

def main():
    """Main function for your NetCDF conversion work"""
    print("🌊 NetCDF to CSV Converter - Your Data Processing Tool")
    print("=" * 60)
    
    # Check what NetCDF files you have
    netcdf_files = list(Path(".").glob("*.nc"))
    
    if not netcdf_files:
        print("❌ No .nc files found in current directory")
        print("💡 Place your NetCDF files here and run again")
        return
    
    print(f"📁 Found {len(netcdf_files)} NetCDF files:")
    for i, file in enumerate(netcdf_files, 1):
        print(f"   {i}. {file.name}")
    
    print("\n🎯 What would you like to do?")
    print("1. Convert single file")
    print("2. Convert all files")
    print("3. Show file info")
    print("4. Convert specific file")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        if netcdf_files:
            file = netcdf_files[0]
            show_netcdf_info(file)
            convert_single_netcdf(file)
    
    elif choice == "2":
        results = convert_multiple_netcdf(netcdf_files)
        print(f"\n✅ Converted {len(results)} files successfully!")
    
    elif choice == "3":
        if netcdf_files:
            show_netcdf_info(netcdf_files[0])
    
    elif choice == "4":
        print("\nSelect file to convert:")
        for i, file in enumerate(netcdf_files, 1):
            print(f"   {i}. {file.name}")
        
        try:
            file_idx = int(input("Enter file number: ")) - 1
            if 0 <= file_idx < len(netcdf_files):
                file = netcdf_files[file_idx]
                show_netcdf_info(file)
                convert_single_netcdf(file)
            else:
                print("❌ Invalid file number")
        except ValueError:
            print("❌ Please enter a valid number")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
