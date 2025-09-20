#!/usr/bin/env python3
"""
Complete Workflow: Download NetCDF Files → Convert to CSV
This is your complete data processing pipeline
"""

import requests
import os
from pathlib import Path
from data_processor import ArgoDataPipeline, process_argo_netcdf
import pandas as pd

def download_argo_netcdf(url, filename):
    """
    Download a NetCDF file from ARGO GDAC
    """
    print(f"📥 Downloading {filename}...")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Downloaded: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def convert_netcdf_to_csv(netcdf_file, output_name=None):
    """
    Convert NetCDF file to CSV - YOUR MAIN JOB!
    """
    print(f"🔄 Converting {netcdf_file} to CSV...")
    
    # Process the NetCDF file
    df = process_argo_netcdf(netcdf_file)
    
    if df is not None:
        # Generate output filename
        if output_name is None:
            output_name = f"{Path(netcdf_file).stem}_converted.csv"
        
        # Save as CSV
        df.to_csv(output_name, index=False)
        
        print(f"✅ CSV created: {output_name}")
        print(f"📊 Data: {len(df)} rows, {len(df.columns)} columns")
        print(f"📋 Columns: {list(df.columns)}")
        
        # Show sample data
        print(f"\n📋 Sample data:")
        print(df.head())
        
        return output_name
    else:
        print("❌ Conversion failed")
        return None

def batch_convert_netcdf_files(netcdf_files, output_dir="converted_csv"):
    """
    Convert multiple NetCDF files to CSV
    """
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"🔄 Converting {len(netcdf_files)} files to CSV...")
    
    results = []
    for netcdf_file in netcdf_files:
        print(f"\n{'='*50}")
        output_name = Path(output_dir) / f"{Path(netcdf_file).stem}_converted.csv"
        result = convert_netcdf_to_csv(netcdf_file, str(output_name))
        
        if result:
            results.append({
                'input': netcdf_file,
                'output': result,
                'status': 'success'
            })
        else:
            results.append({
                'input': netcdf_file,
                'output': None,
                'status': 'failed'
            })
    
    # Summary
    successful = sum(1 for r in results if r['status'] == 'success')
    print(f"\n{'='*50}")
    print(f"✅ Conversion Summary: {successful}/{len(netcdf_files)} files converted successfully")
    
    return results

def show_argo_download_sources():
    """
    Show where to download ARGO NetCDF files
    """
    print("🌊 ARGO NetCDF Download Sources:")
    print("=" * 50)
    
    print("\n1. 📥 ARGO GDAC (Global Data Assembly Center):")
    print("   URL: https://data-argo.ifremer.fr/")
    print("   - Real-time and delayed mode data")
    print("   - Search by float ID, date, location")
    
    print("\n2. 📥 ARGO FTP Servers:")
    print("   - ftp://ftp.ifremer.fr/ifremer/argo/dac/")
    print("   - ftp://ftp.usgodae.org/pub/outgoing/argo/dac/")
    
    print("\n3. 📥 Example Download URLs:")
    print("   - https://data-argo.ifremer.fr/argo/dac/aoml/13857/profiles/R13857_001.nc")
    print("   - https://data-argo.ifremer.fr/argo/dac/coriolis/6902743/profiles/R6902743_001.nc")
    
    print("\n4. 🔍 How to Find Files:")
    print("   - Go to https://data-argo.ifremer.fr/")
    print("   - Search for floats by ID, date, or location")
    print("   - Download the .nc profile files")
    print("   - Place them in your project folder")

def main():
    """Main workflow for your NetCDF conversion job"""
    print("🌊 NetCDF to CSV Conversion Workflow")
    print("=" * 50)
    
    # Check current NetCDF files
    netcdf_files = list(Path(".").glob("*.nc"))
    
    print(f"📁 Current NetCDF files: {len(netcdf_files)}")
    for i, file in enumerate(netcdf_files, 1):
        print(f"   {i}. {file.name}")
    
    print("\n🎯 Your Options:")
    print("1. Convert existing NetCDF files to CSV")
    print("2. Show download sources for more NetCDF files")
    print("3. Convert specific file")
    print("4. Batch convert all files")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        if netcdf_files:
            batch_convert_netcdf_files(netcdf_files)
        else:
            print("❌ No NetCDF files found. Download some first!")
    
    elif choice == "2":
        show_argo_download_sources()
    
    elif choice == "3":
        if netcdf_files:
            print("\nSelect file to convert:")
            for i, file in enumerate(netcdf_files, 1):
                print(f"   {i}. {file.name}")
            
            try:
                file_idx = int(input("Enter file number: ")) - 1
                if 0 <= file_idx < len(netcdf_files):
                    convert_netcdf_to_csv(netcdf_files[file_idx])
                else:
                    print("❌ Invalid file number")
            except ValueError:
                print("❌ Please enter a valid number")
        else:
            print("❌ No NetCDF files found")
    
    elif choice == "4":
        if netcdf_files:
            batch_convert_netcdf_files(netcdf_files)
        else:
            print("❌ No NetCDF files found")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
