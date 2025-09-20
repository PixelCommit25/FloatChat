#!/usr/bin/env python3
"""
FloatChat Startup Script
Easy way to start the FloatChat ocean data AI agent
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Core packages that are absolutely required
    core_packages = ['streamlit', 'pandas', 'numpy', 'xarray', 'plotly', 'folium', 'pyarrow']
    
    # Optional packages that enhance functionality
    optional_packages = ['netcdf4', 'faiss', 'chromadb', 'openai']
    
    missing_core = []
    missing_optional = []
    
    for package in core_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING (REQUIRED)")
            missing_core.append(package)
    
    for package in optional_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ⚠️  {package} - MISSING (OPTIONAL)")
            missing_optional.append(package)
    
    if missing_core:
        print(f"\n❌ Missing required packages: {', '.join(missing_core)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing optional packages: {', '.join(missing_optional)}")
        print("Some features may not work, but the core system will run.")
    
    print("   ✅ Core dependencies found!")
    return True

def check_data_files():
    """Check if data files exist"""
    print("\n📁 Checking data files...")
    
    # Check for ARGO NetCDF file
    if Path('R13857_001.nc').exists():
        print("   ✅ Found R13857_001.nc (ARGO data)")
    else:
        print("   ⚠️  R13857_001.nc not found (will use sample data)")
    
    # Check for processed data
    if Path('argo_data.db').exists():
        print("   ✅ Found argo_data.db (processed data)")
    else:
        print("   ℹ️  argo_data.db will be created with sample data")
    
    return True

def start_streamlit():
    """Start the Streamlit application"""
    print("\n🚀 Starting FloatChat...")
    print("=" * 50)
    print("🌊 FloatChat - AI-Powered ARGO Ocean Data Explorer")
    print("=" * 50)
    print("The app will open in your web browser.")
    print("If it doesn't open automatically, go to: http://localhost:8501")
    print("\nPress Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Start Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "floatchat_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 FloatChat stopped. Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting Streamlit: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🌊 FloatChat Startup")
    print("=" * 30)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first.")
        return False
    
    # Check data files
    check_data_files()
    
    # Start the application
    print("\n🎯 Ready to start FloatChat!")
    response = input("Start the application? (y/n): ").lower().strip()
    
    if response in ['y', 'yes', '']:
        return start_streamlit()
    else:
        print("👋 Goodbye!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
