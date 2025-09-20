# FloatChat Testing Guide 🧪

This guide shows you exactly how to verify that your FloatChat system is working correctly.

## 🚀 Quick Start Testing (2 minutes)

### Step 1: Quick System Check
```bash
python quick_test.py
```

**Expected Output:**
```
🌊 FloatChat Quick System Check
========================================
1. Testing basic imports...
   ✅ Core modules OK
2. Testing data processor...
   ✅ Data processor OK
3. Testing FloatChat system...
   ✅ FloatChat system OK
4. Testing Streamlit app...
   ✅ Streamlit app OK

🎉 Quick check PASSED!

🚀 Ready to run:
   streamlit run floatchat_app.py
```

### Step 2: Run the Web Application
```bash
streamlit run floatchat_app.py
```

**Expected Result:**
- Browser opens to `http://localhost:8501`
- You see the FloatChat interface with ocean wave emoji 🌊
- Sample data loads automatically

### Step 3: Test a Simple Query
In the web interface, try:
```
Show me temperature profiles in the Indian Ocean
```

**Expected Result:**
- Query processes successfully
- You see data table with temperature, latitude, longitude columns
- Map shows float locations
- Profile plots display temperature vs depth

---

## 🔬 Comprehensive Testing (10 minutes)

### Full System Test
```bash
python test_floatchat.py
```

This runs 6 comprehensive tests:

1. **Module Imports** - Checks all dependencies
2. **Data Processor** - Tests NetCDF processing
3. **Database Integration** - Tests SQLite and vector databases
4. **LLM Integration** - Tests natural language processing
5. **FloatChat System** - Tests query processing
6. **Streamlit App** - Tests web interface

**Expected Final Output:**
```
📊 TEST SUMMARY
==================================================
✅ PASS Module Imports
✅ PASS Data Processor
✅ PASS Database Integration
✅ PASS LLM Integration
✅ PASS FloatChat System
✅ PASS Streamlit App

🎯 Overall Result: 6/6 tests passed

🎉 ALL TESTS PASSED! FloatChat system is ready to use!
```

---

## 🌊 Testing Individual Components

### Test 1: Data Processing Pipeline
```bash
python pipeline_demo.py
```

**What it does:**
- Creates sample ARGO NetCDF files
- Processes them through the pipeline
- Exports to CSV and Parquet
- Shows data exploration examples

**Expected Output:**
```
🌊 ARGO Data Processing Pipeline Demo
=====================================
Creating sample ARGO data: demo_argo_single.nc
✅ Sample data created: demo_argo_single.nc

============================================================
DEMO 1: Single File Processing
============================================================
✅ Processing successful!
   Input file: demo_argo_single.nc
   Rows processed: 250
   Columns: ['LATITUDE', 'LONGITUDE', 'TIME', 'PRES', 'TEMP', 'PSAL']
```

### Test 2: Natural Language Processing
```bash
python llm_integration.py
```

**What it does:**
- Tests query parsing
- Shows SQL generation
- Demonstrates AI processing

**Expected Output:**
```
🧠 Testing LLM Integration for FloatChat

📝 Query: Show me temperature profiles near the equator
   Intent: visualize
   Parameters: ['temperature']
   Location: equator
   Visualization: profile
   SQL: SELECT float_id, latitude, longitude, date_time, pressure, temperature FROM argo_profiles WHERE...
```

### Test 3: Database Operations
```bash
python database_integration.py
```

**What it does:**
- Tests PostgreSQL integration setup
- Demonstrates vector database features
- Shows similarity search capabilities

---

## 🐛 Troubleshooting Common Issues

### Issue 1: Import Errors
**Error:** `ModuleNotFoundError: No module named 'streamlit'`

**Fix:**
```bash
pip install -r requirements.txt
```

### Issue 2: Streamlit Won't Start
**Error:** `streamlit: command not found`

**Fix:**
```bash
# Make sure streamlit is installed
pip install streamlit

# Or run with python -m
python -m streamlit run floatchat_app.py
```

### Issue 3: No Data in Interface
**Error:** Empty results or "No data found"

**Fix:**
- The system automatically creates sample data
- If still empty, restart the app:
```bash
# Stop the app (Ctrl+C) and restart
streamlit run floatchat_app.py
```

### Issue 4: Database Errors
**Error:** `sqlite3.OperationalError: no such table`

**Fix:**
- Delete any existing database files:
```bash
rm argo_data.db test_*.db
```
- Restart the application (it will recreate the database)

### Issue 5: LLM Features Not Working
**Error:** Rule-based processing instead of AI

**This is normal!** The system works in two modes:
- **With API Key**: Advanced AI features (GPT, Claude)
- **Without API Key**: Rule-based processing (still works great!)

To enable AI features:
```bash
# Set environment variable
export OPENAI_API_KEY=your_api_key_here

# Or add to .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

---

## ✅ Success Indicators

### Your system is working if you see:

1. **Quick test passes** ✅
2. **Streamlit app loads** ✅
3. **Sample data appears** ✅
4. **Queries return results** ✅
5. **Maps and plots display** ✅

### Example successful query results:

**Query:** "Show me temperature profiles near the equator"

**Expected Results:**
- **Data Table**: 100-1000 rows with temperature, latitude, longitude
- **Map View**: Blue markers near equator (±5° latitude)
- **Profile Plot**: Temperature vs depth curves
- **Success Message**: "Found X profiles from Y ARGO floats"

---

## 🎯 Performance Benchmarks

### Expected Response Times:
- **Simple Query**: 1-3 seconds
- **Complex Query**: 3-10 seconds
- **Large Dataset**: 10-30 seconds
- **Map Rendering**: 2-5 seconds

### Expected Data Volumes:
- **Sample Dataset**: ~1000 profiles
- **Query Results**: 100-5000 profiles typically
- **Memory Usage**: 100-500 MB
- **Database Size**: 10-100 MB

---

## 🚀 Next Steps After Testing

### If All Tests Pass:
1. **Explore the Interface**: Try different queries
2. **Load Real Data**: Replace sample data with actual ARGO files
3. **Customize Queries**: Modify for your specific region/parameters
4. **Deploy**: Set up for production use

### If Tests Fail:
1. **Check Dependencies**: Run `pip install -r requirements.txt`
2. **Check Python Version**: Ensure Python 3.8+
3. **Check File Permissions**: Ensure write access to directory
4. **Check Network**: Some features need internet access
5. **Contact Support**: Share error messages for help

---

## 📞 Getting Help

### Common Commands for Debugging:
```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(streamlit|pandas|plotly)"

# Check system resources
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"

# Verbose error output
python test_floatchat.py 2>&1 | tee test_output.log
```

### Log Files to Check:
- Terminal output from `streamlit run`
- Browser console (F12 → Console tab)
- Test output from `test_floatchat.py`

Remember: The system is designed to work even without advanced AI features. The rule-based processing provides excellent functionality for ocean data queries!