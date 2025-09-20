#!/usr/bin/env python3
"""
Simple ARGO Data Downloader
A simplified approach to download ARGO data from the official repository
Works with the actual data structure shown in your browser
"""

import ftplib
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import time
import random

# Import our processing components
from data_processor import ArgoDataPipeline, process_argo_netcdf

class SimpleArgoDownloader:
    """
    Simplified ARGO data downloader that works with the real data structure
    """
    
    def __init__(self, base_dir: str = "argo_data"):
        self.ftp_host = "ftp.ifremer.fr"
        self.ftp_base_path = "/ifremer/argo"
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Known good ARGO data paths (from your browser screenshot)
        self.sample_paths = [
            "/dac/aoml/13857/profiles/R13857_001.nc",
            "/dac/aoml/13858/profiles/R13858_001.nc", 
            "/dac/aoml/13859/profiles/R13859_001.nc",
            "/dac/aoml/15819/profiles/R15819_001.nc",
            "/dac/aoml/15820/profiles/R15820_001.nc",
            "/dac/aoml/15851/profiles/R15851_001.nc",
            "/dac/aoml/15852/profiles/R15852_001.nc",
            "/dac/aoml/15853/profiles/R15853_001.nc",
            "/dac/aoml/15854/profiles/R15854_001.nc",
            "/dac/aoml/15855/profiles/R15855_001.nc",
            "/dac/aoml/1900022/profiles/R1900022_001.nc",
            "/dac/aoml/1900033/profiles/R1900033_001.nc",
            "/dac/aoml/1900034/profiles/R1900034_001.nc",
            "/dac/aoml/1900035/profiles/R1900035_001.nc",
            "/dac/aoml/1900036/profiles/R1900036_001.nc",
            "/dac/aoml/1900037/profiles/R1900037_001.nc",
            "/dac/aoml/1900038/profiles/R1900038_001.nc",
            "/dac/aoml/1900039/profiles/R1900039_001.nc",
            "/dac/aoml/1900040/profiles/R1900040_001.nc",
            "/dac/aoml/1900041/profiles/R1900041_001.nc",
            "/dac/aoml/1900042/profiles/R1900042_001.nc",
            "/dac/aoml/1900043/profiles/R1900043_001.nc",
            "/dac/aoml/1900044/profiles/R1900044_001.nc",
            "/dac/aoml/1900045/profiles/R1900045_001.nc",
            "/dac/aoml/1900046/profiles/R1900046_001.nc",
            "/dac/aoml/1900047/profiles/R1900047_001.nc",
            "/dac/aoml/1900048/profiles/R1900048_001.nc",
            "/dac/aoml/1900049/profiles/R1900049_001.nc",
            "/dac/aoml/1900050/profiles/R1900050_001.nc",
            "/dac/aoml/1900051/profiles/R1900051_001.nc"
        ]
    
    def connect_ftp(self) -> ftplib.FTP:
        """Connect to ARGO FTP server"""
        try:
            ftp = ftplib.FTP(self.ftp_host)
            ftp.login()  # Anonymous login
            self.logger.info(f"Connected to {self.ftp_host}")
            return ftp
        except Exception as e:
            self.logger.error(f"Failed to connect to FTP: {str(e)}")
            raise
    
    def download_sample_files(self, num_files: int = 10) -> List[str]:
        """
        Download a sample of ARGO files for testing
        """
        self.logger.info(f"Downloading {num_files} sample ARGO files...")
        
        # Create profiles directory
        profiles_dir = self.base_dir / "profiles"
        profiles_dir.mkdir(exist_ok=True)
        
        downloaded_files = []
        
        try:
            ftp = self.connect_ftp()
            
            # Randomly select files to download
            selected_paths = random.sample(self.sample_paths, min(num_files, len(self.sample_paths)))
            
            for file_path in selected_paths:
                try:
                    # Extract filename
                    filename = Path(file_path).name
                    local_path = profiles_dir / filename
                    
                    # Skip if already exists
                    if local_path.exists():
                        self.logger.info(f"File already exists: {filename}")
                        downloaded_files.append(str(local_path))
                        continue
                    
                    # Download the file
                    self.logger.info(f"Downloading {filename}...")
                    
                    # Change to the correct directory
                    ftp.cwd(self.ftp_base_path)
                    
                    with open(local_path, 'wb') as f:
                        ftp.retrbinary(f'RETR {file_path}', f.write)
                    
                    downloaded_files.append(str(local_path))
                    self.logger.info(f"✅ Downloaded: {filename}")
                    
                    # Be respectful to the server
                    time.sleep(1)
                    
                except Exception as e:
                    self.logger.error(f"❌ Failed to download {filename}: {str(e)}")
                    continue
            
            ftp.quit()
            
        except Exception as e:
            self.logger.error(f"FTP connection error: {str(e)}")
        
        self.logger.info(f"Downloaded {len(downloaded_files)} files successfully")
        return downloaded_files
    
    def explore_argo_structure(self, max_dirs: int = 5):
        """
        Explore the ARGO FTP structure to find available data
        """
        self.logger.info("Exploring ARGO FTP structure...")
        
        try:
            ftp = self.connect_ftp()
            ftp.cwd(self.ftp_base_path + "/dac")
            
            # List data assembly centers
            dacs = ftp.nlst()
            self.logger.info(f"Found {len(dacs)} Data Assembly Centers")
            
            for dac in dacs[:max_dirs]:
                self.logger.info(f"\nExploring DAC: {dac}")
                try:
                    ftp.cwd(f"{self.ftp_base_path}/dac/{dac}")
                    floats = ftp.nlst()
                    self.logger.info(f"  Found {len(floats)} floats in {dac}")
                    
                    # Look at first few floats
                    for float_id in floats[:3]:
                        try:
                            ftp.cwd(f"{self.ftp_base_path}/dac/{dac}/{float_id}")
                            contents = ftp.nlst()
                            self.logger.info(f"    Float {float_id}: {contents}")
                            
                            # Check for profiles directory
                            if 'profiles' in contents:
                                ftp.cwd(f"{self.ftp_base_path}/dac/{dac}/{float_id}/profiles")
                                profiles = ftp.nlst()
                                self.logger.info(f"      Profiles: {len(profiles)} files")
                                if profiles:
                                    self.logger.info(f"      Example: {profiles[0]}")
                        except:
                            continue
                            
                except Exception as e:
                    self.logger.error(f"  Error exploring {dac}: {str(e)}")
                    continue
            
            ftp.quit()
            
        except Exception as e:
            self.logger.error(f"Error exploring structure: {str(e)}")
    
    def download_from_dac(self, dac: str = "aoml", max_floats: int = 5, max_profiles_per_float: int = 2) -> List[str]:
        """
        Download files from a specific Data Assembly Center
        
        Args:
            dac: Data Assembly Center (e.g., 'aoml', 'coriolis', 'csiro')
            max_floats: Maximum number of floats to download from
            max_profiles_per_float: Maximum profiles per float
        """
        self.logger.info(f"Downloading from DAC: {dac}")
        
        profiles_dir = self.base_dir / "profiles"
        profiles_dir.mkdir(exist_ok=True)
        
        downloaded_files = []
        
        try:
            ftp = self.connect_ftp()
            ftp.cwd(f"{self.ftp_base_path}/dac/{dac}")
            
            # Get list of floats
            floats = ftp.nlst()
            self.logger.info(f"Found {len(floats)} floats in {dac}")
            
            # Randomly select floats
            selected_floats = random.sample(floats, min(max_floats, len(floats)))
            
            for float_id in selected_floats:
                try:
                    # Check if float has profiles directory
                    ftp.cwd(f"{self.ftp_base_path}/dac/{dac}/{float_id}")
                    contents = ftp.nlst()
                    
                    if 'profiles' not in contents:
                        continue
                    
                    # Get profile files
                    ftp.cwd(f"{self.ftp_base_path}/dac/{dac}/{float_id}/profiles")
                    profiles = ftp.nlst()
                    
                    # Filter for NetCDF files
                    nc_files = [f for f in profiles if f.endswith('.nc') and not f.endswith('_tech.nc')]
                    
                    if not nc_files:
                        continue
                    
                    # Download a few profiles from this float
                    selected_profiles = nc_files[:max_profiles_per_float]
                    
                    for profile_file in selected_profiles:
                        local_path = profiles_dir / f"{dac}_{float_id}_{profile_file}"
                        
                        # Skip if already exists
                        if local_path.exists():
                            downloaded_files.append(str(local_path))
                            continue
                        
                        try:
                            self.logger.info(f"Downloading {profile_file} from float {float_id}...")
                            
                            with open(local_path, 'wb') as f:
                                ftp.retrbinary(f'RETR {profile_file}', f.write)
                            
                            downloaded_files.append(str(local_path))
                            self.logger.info(f"✅ Downloaded: {local_path.name}")
                            
                            # Be respectful to the server
                            time.sleep(0.5)
                            
                        except Exception as e:
                            self.logger.error(f"❌ Failed to download {profile_file}: {str(e)}")
                            continue
                
                except Exception as e:
                    self.logger.error(f"Error processing float {float_id}: {str(e)}")
                    continue
            
            ftp.quit()
            
        except Exception as e:
            self.logger.error(f"Error downloading from {dac}: {str(e)}")
        
        self.logger.info(f"Downloaded {len(downloaded_files)} files from {dac}")
        return downloaded_files


def quick_download_and_setup():
    """
    Quick download and setup for FloatChat
    """
    print("🌊 Quick ARGO Data Download and Setup")
    print("=" * 50)
    
    # Download sample files
    downloader = SimpleArgoDownloader()
    
    print("📥 Downloading sample ARGO files...")
    downloaded_files = downloader.download_sample_files(num_files=15)
    
    if not downloaded_files:
        print("❌ No files downloaded. Check internet connection.")
        return False
    
    print(f"✅ Downloaded {len(downloaded_files)} files")
    
    # Process files
    print("\n🔄 Processing NetCDF files...")
    pipeline = ArgoDataPipeline(output_dir="argo_processed")
    
    processed_data = []
    for netcdf_file in downloaded_files:
        try:
            print(f"Processing: {Path(netcdf_file).name}")
            df = process_argo_netcdf(netcdf_file)
            
            if df is not None and len(df) > 0:
                df['source_file'] = Path(netcdf_file).name
                processed_data.append(df)
            else:
                print(f"   ⚠️ No valid data in {Path(netcdf_file).name}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            continue
    
    if not processed_data:
        print("❌ No files processed successfully")
        return False
    
    # Combine and save data
    combined_df = pd.concat(processed_data, ignore_index=True)
    print(f"✅ Processed {len(processed_data)} files, {len(combined_df)} profiles")
    
    # Save processed data
    combined_df.to_csv("real_argo_data.csv", index=False)
    combined_df.to_parquet("real_argo_data.parquet", index=False)
    
    print(f"\n📊 Data Summary:")
    print(f"   Total profiles: {len(combined_df)}")
    if 'LATITUDE' in combined_df.columns:
        print(f"   Latitude range: {combined_df['LATITUDE'].min():.2f}° to {combined_df['LATITUDE'].max():.2f}°")
        print(f"   Longitude range: {combined_df['LONGITUDE'].min():.2f}° to {combined_df['LONGITUDE'].max():.2f}°")
    
    print(f"\n✅ Setup complete! Files saved:")
    print(f"   - real_argo_data.csv")
    print(f"   - real_argo_data.parquet")
    
    print(f"\n🚀 Ready to run FloatChat:")
    print(f"   streamlit run floatchat_app.py")
    
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "quick":
            quick_download_and_setup()
        elif sys.argv[1] == "explore":
            downloader = SimpleArgoDownloader()
            downloader.explore_argo_structure()
        elif sys.argv[1] == "aoml":
            downloader = SimpleArgoDownloader()
            files = downloader.download_from_dac("aoml", max_floats=3)
            print(f"Downloaded {len(files)} files from AOML")
        else:
            print("Usage: python simple_argo_downloader.py [quick|explore|aoml]")
    else:
        print("🌊 Simple ARGO Data Downloader")
        print("=" * 40)
        print("Commands:")
        print("  python simple_argo_downloader.py quick    - Quick download and setup")
        print("  python simple_argo_downloader.py explore  - Explore FTP structure") 
        print("  python simple_argo_downloader.py aoml     - Download from AOML DAC")
        print("\nRecommended: python simple_argo_downloader.py quick")