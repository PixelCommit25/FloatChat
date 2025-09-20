#!/usr/bin/env python3
"""
Auto NetCDF to CSV Converter
Put your .nc file names in this code and it will convert them automatically
"""

from data_processor import process_argo_netcdf
import pandas as pd
from pathlib import Path

def auto_convert_netcdf_files():
    """
    Automatically finds and converts ALL .nc files in your folder
    No need to manually add file names!
    """
    
    # 🔍 AUTOMATICALLY FIND ALL .NC FILES:
    netcdf_files = list(Path(".").glob("*.nc"))
    
    if not netcdf_files:
        print("❌ No .nc files found in current folder")
        print("💡 Just put your .nc files in this folder and run the script!")
        return []
    
    print(f"📁 Found {len(netcdf_files)} NetCDF files automatically:")
    for i, file in enumerate(netcdf_files, 1):
        print(f"   {i}. {file.name}")
    
    print("🔄 Auto Converting NetCDF Files to CSV...")
    print("=" * 50)
    
    converted_files = []
    
    for netcdf_file in netcdf_files:
        print(f"\n📁 Processing: {netcdf_file}")
        
        # Check if file exists
        if not Path(netcdf_file).exists():
            print(f"❌ File not found: {netcdf_file}")
            continue
        
        # Convert to CSV
        try:
            df = process_argo_netcdf(netcdf_file)
            
            if df is not None:
                # Create output filename
                csv_filename = f"{Path(netcdf_file).stem}_converted.csv"
                
                # Save as CSV
                df.to_csv(csv_filename, index=False)
                
                print(f"✅ Converted: {netcdf_file} → {csv_filename}")
                print(f"   📊 Rows: {len(df)}, Columns: {list(df.columns)}")
                
                converted_files.append({
                    'input': netcdf_file,
                    'output': csv_filename,
                    'rows': len(df)
                })
            else:
                print(f"❌ Failed to process: {netcdf_file}")
                
        except Exception as e:
            print(f"❌ Error processing {netcdf_file}: {e}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"✅ CONVERSION SUMMARY:")
    print(f"   Total files processed: {len(converted_files)}")
    print(f"   Total ocean measurements: {sum(f['rows'] for f in converted_files)}")
    
    print(f"\n📋 Converted Files:")
    for file_info in converted_files:
        print(f"   ✅ {file_info['input']} → {file_info['output']} ({file_info['rows']} rows)")
    
    return converted_files

def convert_specific_files():
    """
    Convert only specific files you want
    """
    
    # 📝 PUT ONLY THE FILES YOU WANT TO CONVERT:
    files_to_convert = [
        "R13857_001.nc",
        "R13857_002.nc"
        # Add more files here as needed
    ]
    
    print("🎯 Converting Specific Files...")
    
    for file in files_to_convert:
        if Path(file).exists():
            df = process_argo_netcdf(file)
            if df is not None:
                output_file = f"{Path(file).stem}_converted.csv"
                df.to_csv(output_file, index=False)
                print(f"✅ {file} → {output_file} ({len(df)} rows)")
        else:
            print(f"❌ File not found: {file}")

def convert_new_files_only():
    """
    Convert only new .nc files (ones that don't have corresponding .csv files yet)
    """
    
    print("🆕 Converting Only New NetCDF Files...")
    
    # Find all .nc files
    netcdf_files = list(Path(".").glob("*.nc"))
    
    new_files = []
    for nc_file in netcdf_files:
        csv_file = f"{nc_file.stem}_converted.csv"
        if not Path(csv_file).exists():
            new_files.append(nc_file)
    
    if not new_files:
        print("✅ All NetCDF files already converted!")
        return
    
    print(f"📁 Found {len(new_files)} new files to convert:")
    for file in new_files:
        print(f"   - {file}")
    
    for nc_file in new_files:
        print(f"\n🔄 Converting: {nc_file}")
        df = process_argo_netcdf(str(nc_file))
        if df is not None:
            csv_file = f"{nc_file.stem}_converted.csv"
            df.to_csv(csv_file, index=False)
            print(f"✅ Created: {csv_file} ({len(df)} rows)")

def super_simple_convert():
    """
    SUPER SIMPLE: Just put .nc files in folder and run this!
    """
    print("🚀 SUPER SIMPLE NetCDF to CSV Converter")
    print("=" * 50)
    print("Just put your .nc files in this folder and run!")
    
    # Find all .nc files
    netcdf_files = list(Path(".").glob("*.nc"))
    
    if not netcdf_files:
        print("\n❌ No .nc files found!")
        print("📁 Put your .nc files in this folder and run again.")
        return
    
    print(f"\n📁 Found {len(netcdf_files)} NetCDF files:")
    for file in netcdf_files:
        print(f"   ✅ {file.name}")
    
    print(f"\n🔄 Converting all files to CSV...")
    
    success_count = 0
    for netcdf_file in netcdf_files:
        print(f"\n📁 Processing: {netcdf_file}")
        
        try:
            df = process_argo_netcdf(str(netcdf_file))
            if df is not None:
                csv_filename = f"{netcdf_file.stem}_converted.csv"
                df.to_csv(csv_filename, index=False)
                print(f"✅ {netcdf_file} → {csv_filename} ({len(df)} rows)")
                success_count += 1
            else:
                print(f"❌ Failed to process: {netcdf_file}")
        except Exception as e:
            print(f"❌ Error: {netcdf_file} - {e}")
    
    print(f"\n{'='*50}")
    print(f"🎉 DONE! Converted {success_count}/{len(netcdf_files)} files successfully!")
    print("📊 Your CSV files are ready for your team!")

def main():
    """
    Choose how you want to convert files
    """
    print("🌊 Auto NetCDF to CSV Converter")
    print("=" * 40)
    
    print("Choose conversion method:")
    print("1. 🚀 SUPER SIMPLE - Convert all .nc files automatically")
    print("2. Convert only new files (not converted yet)")
    print("3. Convert specific files only")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        super_simple_convert()
    elif choice == "2":
        convert_new_files_only()
    elif choice == "3":
        convert_specific_files()
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
