# FloatChat Troubleshooting Guide

## 🚨 Common Issues and Solutions

### 1. **"ModuleNotFoundError" or Import Errors**

**Problem**: Missing Python packages
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution**:
```bash
# Install all required packages
pip install -r requirements.txt

# Or install individually
pip install streamlit pandas numpy xarray netcdf4 plotly folium pyarrow
```

### 2. **"No data found" in the app**

**Problem**: Database is empty or queries return no results

**Solutions**:
- The app automatically loads sample data on first run
- If you have real ARGO data, process it first:
  ```python
  from data_processor import ArgoDataPipeline
  pipeline = ArgoDataPipeline()
  result = pipeline.process_single_file('your_file.nc')
  ```

### 3. **Streamlit app won't start**

**Problem**: Port already in use or other startup issues

**Solutions**:
```bash
# Try different port
streamlit run floatchat_app.py --server.port 8502

# Or kill existing processes
# On Windows:
taskkill /f /im python.exe
# On Mac/Linux:
pkill -f streamlit
```

### 4. **NetCDF file processing fails**

**Problem**: Error processing your .nc files

**Solutions**:
- Check file format: Must be valid NetCDF4 format
- Check file path: Use absolute path if relative doesn't work
- Check file permissions: Make sure file is readable
- Test with sample data first:
  ```python
  python pipeline_demo.py
  ```

### 5. **"LLM not available" warning**

**Problem**: AI features using rule-based processing instead of LLM

**Solutions**:
- This is normal! The system works without API keys
- To enable AI features, add API key to `.streamlit/secrets.toml`:
  ```toml
  OPENAI_API_KEY = "your-api-key-here"
  ```

### 6. **Memory issues with large files**

**Problem**: System runs out of memory processing large NetCDF files

**Solutions**:
- Process files individually instead of batch processing
- Increase system memory
- Use cloud processing for very large files
- Filter data early in the pipeline

### 7. **Database connection errors**

**Problem**: SQLite database issues

**Solutions**:
- Delete `argo_data.db` and restart (will recreate with sample data)
- Check file permissions
- Ensure sufficient disk space

## 🔧 Quick Fixes

### Reset Everything
```bash
# Delete database and restart
rm argo_data.db
python start_floatchat.py
```

### Test Individual Components
```bash
# Test data processing
python test_my_code.py

# Test complete system
python test_complete_system.py

# Test pipeline demo
python pipeline_demo.py
```

### Check System Status
```bash
# Quick system check
python quick_test.py
```

## 📊 Expected Behavior

### ✅ Working System Should:
1. Convert NetCDF files to CSV/Parquet successfully
2. Load sample data into database automatically
3. Start Streamlit app on http://localhost:8501
4. Respond to natural language queries
5. Display maps, charts, and data tables

### 🎯 Sample Queries That Should Work:
- "Show me temperature profiles near the equator"
- "Find salinity data in the Arabian Sea"
- "Display oxygen levels in the Indian Ocean"
- "Compare temperature profiles from last 6 months"

## 🆘 Still Having Issues?

1. **Check Python version**: Should be 3.8 or higher
   ```bash
   python --version
   ```

2. **Check all dependencies**:
   ```bash
   pip list | grep -E "(streamlit|pandas|numpy|xarray|netcdf4|plotly|folium)"
   ```

3. **Run the complete test**:
   ```bash
   python test_complete_system.py
   ```

4. **Check the logs**: Look for error messages in the terminal output

5. **Try the simple test**:
   ```bash
   python quick_test.py
   ```

## 📞 Getting Help

If you're still having issues:

1. Run `python test_complete_system.py` and share the output
2. Check the error messages in the terminal
3. Verify your NetCDF file format
4. Make sure all dependencies are installed correctly

The system is designed to work out-of-the-box with sample data, so most issues are related to missing dependencies or file format problems.
