# FloatChat Setup Guide

## 🚀 Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/floatchat.git
cd floatchat
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run fixed_floatchat_app.py
```

## 📊 Working with Real ARGO Data

### Option 1: Use Sample Data
The app will automatically create sample data if no real data is found.

### Option 2: Download Real ARGO Data
```bash
# Download sample ARGO files
python simple_argo_downloader.py quick

# Process your own NetCDF file
python process_downloaded_argo.py
```

### Option 3: Use Your Own NetCDF Files
1. Place your ARGO NetCDF files in the project directory
2. Run: `python process_downloaded_argo.py`
3. Follow the prompts to process your data

## 🧪 Testing

```bash
# Quick system test
python quick_test.py

# Test data processing
python pipeline_demo.py
```

## 🌊 Example Queries

Once the app is running, try these queries:
- "Show me temperature profiles"
- "Where are the ARGO floats located?"
- "Display deep temperature data"
- "Show me the data table"

## 📁 Project Structure

```
floatchat/
├── fixed_floatchat_app.py         # Main Streamlit app
├── data_processor.py              # NetCDF processing
├── process_downloaded_argo.py     # Process ARGO files
├── simple_argo_downloader.py      # Download ARGO data
├── pipeline_demo.py               # Demo script
├── quick_test.py                  # System test
├── requirements.txt               # Dependencies
├── README.md                      # Main documentation
├── SETUP.md                       # This setup guide
└── TESTING_GUIDE.md               # Testing instructions
```

## 🔧 Troubleshooting

### Common Issues:

1. **Import Errors**: Run `pip install -r requirements.txt`
2. **No Data Found**: Run `python process_downloaded_argo.py` to process data
3. **Streamlit Issues**: Try `python -m streamlit run fixed_floatchat_app.py`

### Getting Help:

1. Check the TESTING_GUIDE.md for detailed testing
2. Run `python quick_test.py` to verify installation
3. Check the GitHub Issues page for common problems

## 🌊 Data Sources

- **ARGO Global Data Repository**: ftp.ifremer.fr/ifremer/argo
- **Indian ARGO Project**: https://incois.gov.in/OON/index.jsp

## 🏛️ Acknowledgments

Developed for:
- **Ministry of Earth Sciences (MoES)**
- **Indian National Centre for Ocean Information Services (INCOIS)**