#!/usr/bin/env python3
"""
ARGO Data Processing Pipeline Demo

This script demonstrates the complete end-to-end pipeline for processing ARGO NetCDF data.
It shows how to:
1. Process single files
2. Batch process directories
3. Export to CSV and Parquet formats
4. Generate summary reports

Usage:
    python pipeline_demo.py
"""

from data_processor import ArgoDataPipeline, process_argo_netcdf
import pandas as pd
import numpy as np
import xarray as xr
from pathlib import Path

def create_sample_argo_data(output_path: str = "sample_argo.nc"):
    """
    Create a sample ARGO-like NetCDF file for testing purposes.
    This simulates real ARGO data structure.
    """
    print(f"Creating sample ARGO data: {output_path}")
    
    # Create sample data that mimics ARGO structure
    n_profiles = 5
    n_levels = 50
    
    # Create coordinates
    time = pd.date_range('2024-01-01', periods=n_profiles, freq='D')
    pressure = np.linspace(0, 2000, n_levels)  # Pressure levels in dbar
    
    # Create sample oceanographic data
    np.random.seed(42)  # For reproducible results
    
    # Temperature decreases with depth
    temp_base = np.linspace(25, 2, n_levels)  # Surface to deep temperature
    temperature = np.array([temp_base + np.random.normal(0, 0.5, n_levels) for _ in range(n_profiles)])
    
    # Salinity varies realistically
    sal_base = np.linspace(35, 34.5, n_levels)
    salinity = np.array([sal_base + np.random.normal(0, 0.1, n_levels) for _ in range(n_profiles)])
    
    # Geographic coordinates (sample locations in Atlantic)
    latitudes = np.random.uniform(30, 60, n_profiles)
    longitudes = np.random.uniform(-50, -10, n_profiles)
    
    # Create xarray Dataset
    ds = xr.Dataset({
        'TEMP': (['TIME', 'PRES'], temperature),
        'PSAL': (['TIME', 'PRES'], salinity),
        'LATITUDE': (['TIME'], latitudes),
        'LONGITUDE': (['TIME'], longitudes),
    }, coords={
        'TIME': time,
        'PRES': pressure,
    })
    
    # Add attributes (metadata)
    ds.attrs['title'] = 'Sample ARGO Profile Data'
    ds.attrs['institution'] = 'Test Institution'
    ds.attrs['source'] = 'Simulated ARGO float data'
    
    # Save to NetCDF
    ds.to_netcdf(output_path)
    ds.close()
    print(f"✅ Sample data created: {output_path}")
    return output_path

def demo_single_file_processing():
    """Demonstrate processing a single NetCDF file."""
    print("\n" + "="*60)
    print("DEMO 1: Single File Processing")
    print("="*60)
    
    # Create sample data
    sample_file = create_sample_argo_data("demo_argo_single.nc")
    
    # Initialize pipeline
    pipeline = ArgoDataPipeline(output_dir="demo_output")
    
    # Process the file
    result = pipeline.process_single_file(sample_file, export_format="both")
    
    if result:
        print(f"\n✅ Processing successful!")
        print(f"   Input file: {result['input_file']}")
        print(f"   Rows processed: {result['rows_processed']}")
        print(f"   Columns: {result['columns']}")
        print(f"   Output files: {result['output_files']}")
        
        # Load and preview the CSV output
        if result['output_files']:
            csv_file = [f for f in result['output_files'] if f.endswith('.csv')][0]
            df = pd.read_csv(csv_file)
            print(f"\n📊 Preview of {Path(csv_file).name}:")
            print(df.head())
            print(f"\nDataFrame shape: {df.shape}")
            print(f"Data types:\n{df.dtypes}")
    else:
        print("❌ Processing failed!")

def demo_batch_processing():
    """Demonstrate batch processing of multiple files."""
    print("\n" + "="*60)
    print("DEMO 2: Batch Processing")
    print("="*60)
    
    # Create a directory with multiple sample files
    batch_dir = Path("demo_batch_input")
    batch_dir.mkdir(exist_ok=True)
    
    # Create multiple sample files
    sample_files = []
    for i in range(3):
        filename = batch_dir / f"argo_profile_{i+1}.nc"
        create_sample_argo_data(str(filename))
        sample_files.append(filename)
    
    # Initialize pipeline
    pipeline = ArgoDataPipeline(output_dir="demo_batch_output")
    
    # Process all files in the directory
    results = pipeline.process_directory(str(batch_dir), export_format="both")
    
    print(f"\n✅ Batch processing complete!")
    print(f"   Files processed: {len(results)}")
    
    # Create and display summary report
    summary_df = pipeline.create_summary_report(results)
    print(f"\n📋 Processing Summary:")
    print(summary_df)
    
    # Show total statistics
    total_rows = sum(r['rows_processed'] for r in results)
    total_files = len([f for r in results for f in r['output_files']])
    print(f"\n📈 Total Statistics:")
    print(f"   Total rows processed: {total_rows}")
    print(f"   Total output files created: {total_files}")

def demo_data_exploration():
    """Demonstrate how to work with the processed data."""
    print("\n" + "="*60)
    print("DEMO 3: Data Exploration")
    print("="*60)
    
    # Create and process a sample file
    sample_file = create_sample_argo_data("demo_exploration.nc")
    pipeline = ArgoDataPipeline(output_dir="demo_exploration_output")
    result = pipeline.process_single_file(sample_file, export_format="both")
    
    if result and result['output_files']:
        # Load the CSV file
        csv_file = [f for f in result['output_files'] if f.endswith('.csv')][0]
        df = pd.read_csv(csv_file)
        
        print(f"📊 Data Exploration for {Path(csv_file).name}")
        print(f"   Shape: {df.shape}")
        print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        # Basic statistics
        print(f"\n🌡️  Temperature Statistics:")
        if 'TEMP' in df.columns:
            print(f"   Range: {df['TEMP'].min():.2f}°C to {df['TEMP'].max():.2f}°C")
            print(f"   Mean: {df['TEMP'].mean():.2f}°C")
        
        print(f"\n🧂 Salinity Statistics:")
        if 'PSAL' in df.columns:
            print(f"   Range: {df['PSAL'].min():.2f} to {df['PSAL'].max():.2f} PSU")
            print(f"   Mean: {df['PSAL'].mean():.2f} PSU")
        
        print(f"\n🌊 Pressure/Depth Statistics:")
        if 'PRES' in df.columns:
            print(f"   Range: {df['PRES'].min():.1f} to {df['PRES'].max():.1f} dbar")
            print(f"   Levels: {df['PRES'].nunique()} unique pressure levels")
        
        # Geographic coverage
        if 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
            print(f"\n🗺️  Geographic Coverage:")
            print(f"   Latitude: {df['LATITUDE'].min():.2f}°N to {df['LATITUDE'].max():.2f}°N")
            print(f"   Longitude: {df['LONGITUDE'].min():.2f}°E to {df['LONGITUDE'].max():.2f}°E")

def main():
    """Run all demonstrations."""
    print("🌊 ARGO Data Processing Pipeline Demo")
    print("=====================================")
    print("This demo shows how to convert ARGO NetCDF data to CSV/Parquet files")
    
    try:
        # Run demonstrations
        demo_single_file_processing()
        demo_batch_processing()
        demo_data_exploration()
        
        print("\n" + "="*60)
        print("✅ ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\n📁 Check the following directories for output files:")
        print("   - demo_output/")
        print("   - demo_batch_output/")
        print("   - demo_exploration_output/")
        
        print("\n🚀 Next Steps:")
        print("   1. Replace sample data with your real ARGO NetCDF files")
        print("   2. Adjust column filtering in data_processor.py as needed")
        print("   3. Use the CSV/Parquet files in Pandas, Streamlit, or databases")
        print("   4. Consider adding database integration (PostgreSQL, FAISS, Chroma)")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        print("Please check your environment and dependencies.")

if __name__ == "__main__":
    main()