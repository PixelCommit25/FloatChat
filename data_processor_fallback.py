"""
Fallback Data Processor for FloatChat
Works without netcdf4 by using sample data
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

def create_sample_argo_dataframe(n_profiles: int = 1000) -> pd.DataFrame:
    """
    Create sample ARGO data that mimics real oceanographic data
    """
    np.random.seed(42)
    
    data = []
    for i in range(n_profiles):
        # Random locations in Indian Ocean
        lat = np.random.uniform(-30, 30)
        lon = np.random.uniform(40, 120)
        
        # Random date in last 2 years
        days_ago = np.random.randint(0, 730)
        date = (datetime.now() - pd.Timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Depth profile (multiple measurements per float)
        for depth in [10, 50, 100, 200, 500, 1000]:
            # Realistic oceanographic relationships
            temp = 25 - (depth / 100) + np.random.normal(0, 1)  # Temperature decreases with depth
            sal = 35 + np.random.normal(0, 0.5)  # Salinity around 35 PSU
            oxy = 200 + np.random.normal(0, 20)  # Oxygen in μmol/kg
            chl = np.random.exponential(0.5)  # Chlorophyll in mg/m³
            
            data.append({
                'LATITUDE': lat,
                'LONGITUDE': lon,
                'TIME': date,
                'PRES': depth,
                'TEMP': temp,
                'PSAL': sal,
                'DOXY': oxy,
                'CHLA': chl,
                'float_id': f'FLOAT_{i//10:04d}',
                'cycle_number': i % 10
            })
    
    return pd.DataFrame(data)

def process_argo_netcdf_fallback(netcdf_file_path: str) -> Optional[pd.DataFrame]:
    """
    Fallback NetCDF processor that creates sample data
    """
    print(f"⚠️  netcdf4 not available. Using sample data instead of {netcdf_file_path}")
    
    # Create sample data
    df = create_sample_argo_dataframe(1000)
    
    print(f"✅ Created sample data: {len(df)} rows, {len(df.columns)} columns")
    return df

class ArgoDataPipelineFallback:
    """
    Fallback pipeline that works without netcdf4
    """
    
    def __init__(self, output_dir: str = "processed_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
    def process_single_file(self, netcdf_path: str, export_format: str = "both") -> Optional[Dict[str, Any]]:
        """
        Process file using fallback method
        """
        try:
            # Use fallback processor
            df = process_argo_netcdf_fallback(netcdf_path)
            if df is None:
                return None
                
            # Generate output filename
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
                
            # Export to Parquet
            if export_format in ["parquet", "both"]:
                parquet_path = self.output_dir / f"{base_filename}.parquet"
                df.to_parquet(parquet_path, index=False)
                results["output_files"].append(str(parquet_path))
                self.logger.info(f"Exported Parquet: {parquet_path}")
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error processing {netcdf_path}: {str(e)}")
            return None

# Try to import the real processor, fallback if not available
try:
    from data_processor import ArgoDataPipeline, process_argo_netcdf
    print("✅ Using real NetCDF processor")
except ImportError:
    print("⚠️  Using fallback processor (netcdf4 not available)")
    ArgoDataPipeline = ArgoDataPipelineFallback
    process_argo_netcdf = process_argo_netcdf_fallback
