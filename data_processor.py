import xarray as xr
import pandas as pd
import os
import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

def process_argo_netcdf(netcdf_file_path):
    """
    Takes a path to an ARGO NetCDF file, loads it, converts it to a DataFrame,
    and cleans the data.

    Args:
        netcdf_file_path (str): The path to the .nc file.

    Returns:
        pandas.DataFrame: A cleaned DataFrame ready for analysis.
    """

    # 1. CONVERT: Open the NetCDF file and convert to DataFrame
    try:
        # Use xarray to open the complex NetCDF file
        ds = xr.open_dataset(netcdf_file_path)
        # Convert the dataset to a Pandas DataFrame. This flattens the structure.
        df = ds.to_dataframe()
        
        # 2. CLEAN: Handle common data issues
        
        # Reset the index. The dimensions (time, depth) become columns instead of indexes.
        df = df.reset_index()
        
        # Drop rows where essential measurements are missing (NaN)
        # Focus on key columns that actually exist in the file
        potential_essential_cols = ['TEMP', 'PSAL', 'LONGITUDE', 'LATITUDE', 'PRES']
        essential_cols = [col for col in potential_essential_cols if col in df.columns]
        
        # Require at least temperature and pressure for a valid profile
        required_cols = ['TEMP', 'PRES']
        missing_required = [col for col in required_cols if col not in df.columns]
        if missing_required:
            print(f"Warning: Missing required columns {missing_required}")
            return None
            
        df_clean = df.dropna(subset=essential_cols)
        
        # Filter out any "fill values" or bad data. Argo data often uses a specific value like 99999.0 to indicate bad data.
        # Apply sanity checks only to columns that exist
        if 'TEMP' in df_clean.columns:
            df_clean = df_clean[df_clean['TEMP'] < 50]  # Temperature sanity check
        if 'PSAL' in df_clean.columns:
            df_clean = df_clean[df_clean['PSAL'] > 0]   # Salinity sanity check

        # Select only the most useful columns to keep the file size small
        potential_columns = ['LATITUDE', 'LONGITUDE', 'TIME', 'PRES', 'TEMP', 'PSAL', 'DOXY', 'CHLA']
        # Check which of these columns actually exist in the DataFrame to avoid errors
        columns_to_keep = [col for col in potential_columns if col in df_clean.columns]
        df_clean = df_clean[columns_to_keep]
        
        # Close the original dataset
        ds.close()
        
        print(f"Successfully processed {netcdf_file_path}. Original rows: {len(df)}, Cleaned rows: {len(df_clean)}")
        return df_clean

    except Exception as e:
        print(f"Error processing file {netcdf_file_path}: {str(e)}")
        return None


class ArgoDataPipeline:
    """
    Complete end-to-end pipeline for ARGO NetCDF data processing.
    Converts NetCDF → Clean DataFrame → CSV/Parquet files
    """
    
    def __init__(self, output_dir: str = "processed_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def process_single_file(self, netcdf_path: str, export_format: str = "both") -> Optional[Dict[str, Any]]:
        """
        Process a single NetCDF file and export to CSV/Parquet.
        
        Args:
            netcdf_path: Path to NetCDF file
            export_format: "csv", "parquet", or "both"
            
        Returns:
            Dict with processing results and file paths
        """
        try:
            # Use existing function to process the file
            df = process_argo_netcdf(netcdf_path)
            if df is None:
                return None
                
            # Generate output filename based on input
            input_name = Path(netcdf_path).stem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"argo_{input_name}_{timestamp}"
            
            results = {
                "input_file": netcdf_path,
                "rows_processed": len(df),
                "columns": list(df.columns),
                "output_files": []
            }
            
            # Export to CSV
            if export_format in ["csv", "both"]:
                csv_path = self.output_dir / f"{base_filename}.csv"
                df.to_csv(csv_path, index=False)
                results["output_files"].append(str(csv_path))
                self.logger.info(f"Exported CSV: {csv_path}")
                
            # Export to Parquet (more efficient for large datasets)
            if export_format in ["parquet", "both"]:
                parquet_path = self.output_dir / f"{base_filename}.parquet"
                df.to_parquet(parquet_path, index=False)
                results["output_files"].append(str(parquet_path))
                self.logger.info(f"Exported Parquet: {parquet_path}")
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error processing {netcdf_path}: {str(e)}")
            return None
    
    def process_directory(self, input_dir: str, pattern: str = "*.nc", export_format: str = "both") -> List[Dict[str, Any]]:
        """
        Process all NetCDF files in a directory.
        
        Args:
            input_dir: Directory containing NetCDF files
            pattern: File pattern to match (default: *.nc)
            export_format: "csv", "parquet", or "both"
            
        Returns:
            List of processing results for each file
        """
        input_path = Path(input_dir)
        netcdf_files = list(input_path.glob(pattern))
        
        if not netcdf_files:
            self.logger.warning(f"No files matching '{pattern}' found in {input_dir}")
            return []
            
        self.logger.info(f"Found {len(netcdf_files)} NetCDF files to process")
        
        results = []
        for netcdf_file in netcdf_files:
            self.logger.info(f"Processing: {netcdf_file}")
            result = self.process_single_file(str(netcdf_file), export_format)
            if result:
                results.append(result)
                
        return results
    
    def create_summary_report(self, results: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Create a summary report of all processed files.
        """
        if not results:
            return pd.DataFrame()
            
        summary_data = []
        for result in results:
            summary_data.append({
                "input_file": Path(result["input_file"]).name,
                "rows_processed": result["rows_processed"],
                "columns_count": len(result["columns"]),
                "output_files_count": len(result["output_files"]),
                "columns": ", ".join(result["columns"])
            })
            
        summary_df = pd.DataFrame(summary_data)
        
        # Save summary report
        summary_path = self.output_dir / f"processing_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        summary_df.to_csv(summary_path, index=False)
        self.logger.info(f"Summary report saved: {summary_path}")
        
        return summary_df