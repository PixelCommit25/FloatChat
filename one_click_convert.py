#!/usr/bin/env python3
"""
ONE-CLICK NetCDF to CSV Converter
Just put .nc files in folder and run this script!
No manual editing needed!
"""

from data_processor import process_argo_netcdf
import pandas as pd
from pathlib import Path

def main():
    """
    ONE-CLICK CONVERTER: Just run this and it converts all .nc files!
    """
    print("🚀 ONE-CLICK NetCDF to CSV Converter")
    print("=" * 50)
    print("Just put your .nc files in this folder and run!")
    
    # Find all .nc files automatically
    netcdf_files = list(Path(".").glob("*.nc"))
    
    if not netcdf_files:
        print("\n❌ No .nc files found!")
        print("📁 Put your .nc files in this folder and run again.")
        input("\nPress Enter to exit...")
        return
    
    print(f"\n📁 Found {len(netcdf_files)} NetCDF files:")
    for file in netcdf_files:
        print(f"   ✅ {file.name}")
    
    print(f"\n🔄 Converting all files to CSV...")
    print("=" * 50)
    
    success_count = 0
    total_rows = 0
    
    for netcdf_file in netcdf_files:
        print(f"\n📁 Processing: {netcdf_file}")
        
        try:
            df = process_argo_netcdf(str(netcdf_file))
            if df is not None:
                csv_filename = f"{netcdf_file.stem}_converted.csv"
                df.to_csv(csv_filename, index=False)
                print(f"✅ {netcdf_file} → {csv_filename}")
                print(f"   📊 {len(df)} ocean measurements")
                success_count += 1
                total_rows += len(df)
            else:
                print(f"❌ Failed to process: {netcdf_file}")
        except Exception as e:
            print(f"❌ Error processing {netcdf_file}: {e}")
    
    # Final summary
    print(f"\n{'='*50}")
    print(f"🎉 CONVERSION COMPLETE!")
    print(f"✅ Successfully converted: {success_count}/{len(netcdf_files)} files")
    print(f"📊 Total ocean measurements: {total_rows:,}")
    print(f"📁 CSV files ready for your team!")
    
    # Show converted files
    csv_files = list(Path(".").glob("*_converted.csv"))
    if csv_files:
        print(f"\n📋 Your CSV files:")
        for csv_file in csv_files:
            print(f"   ✅ {csv_file.name}")
    
    print(f"\n💡 To convert more files:")
    print(f"   1. Put new .nc files in this folder")
    print(f"   2. Run this script again")
    
    input(f"\nPress Enter to exit...")

if __name__ == "__main__":
    main()
