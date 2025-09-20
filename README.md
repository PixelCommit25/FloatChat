# FloatChat - ARGO Ocean Data Explorer 🌊

**Simple and effective tool for exploring ARGO oceanographic data with natural language queries**

*Developed for INCOIS/MoES - Indian National Centre for Ocean Information Services*

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run FloatChat
```bash
streamlit run fixed_floatchat_app.py
```

### 3. Try Example Queries
- "Show me temperature profiles"
- "Where are the ARGO floats located?"
- "Display deep temperature data"
- "Show me the data table"

## 📁 Essential Files

```
FloatChat/
├── fixed_floatchat_app.py         # Main Streamlit application
├── data_processor.py              # NetCDF processing
├── process_downloaded_argo.py     # Process your ARGO files
├── simple_argo_downloader.py      # Download ARGO data
├── pipeline_demo.py               # Data processing demo
├── quick_test.py                  # System test
├── requirements.txt               # Dependencies
├── argo_data.db                   # Your processed data
└── README.md                      # This file
```

## 🔧 Core Components

### ArgoDataPipeline Class

The main pipeline class that handles:
- Single file processing
- Batch directory processing  
- Export to multiple formats
- Summary report generation

```python
pipeline = ArgoDataPipeline(output_dir="processed_data")

# Process single file
result = pipeline.process_single_file("argo_data.nc", export_format="both")

# Process directory
results = pipeline.process_directory("data/", pattern="*.nc")
```

### Data Cleaning Features

- Removes rows with missing essential measurements
- Filters out physically unrealistic values
- Handles ARGO fill values (bad data indicators)
- Selects only the most useful columns
- Resets multi-dimensional indexes to flat structure

### Export Formats

- **CSV**: Human-readable, works with Excel/Pandas
- **Parquet**: Compressed, efficient for large datasets
- **Both**: Creates both formats simultaneously

## 🗄️ Database Integration

### PostgreSQL Integration

Store processed data in a relational database:

```python
from database_integration import PostgreSQLIntegration

# Connect to PostgreSQL
pg = PostgreSQLIntegration("postgresql://user:pass@localhost:5432/argo_db")

# Create table
pg.create_argo_table()

# Insert processed data
pg.insert_dataframe(df, source_file="argo_file.nc")

# Query by geographic region
regional_data = pg.query_by_region(lat_min=30, lat_max=60, lon_min=-50, lon_max=-10)
```

### Vector Database Integration

For similarity search and machine learning:

```python
from database_integration import FAISSVectorStore, ChromaVectorStore

# FAISS for fast similarity search
faiss_store = FAISSVectorStore()
faiss_store.add_profiles(df)
similar_profiles = faiss_store.search_similar(lat=45.0, lon=-30.0, temp=15.0, salinity=35.0)

# ChromaDB for document-style vector search
chroma_store = ChromaVectorStore()
chroma_store.add_profiles(df)
results = chroma_store.search_similar(45.0, -30.0, 15.0, 35.0)
```

## 📊 Data Structure

### Input (NetCDF)
ARGO NetCDF files typically contain:
- Multi-dimensional arrays (time, depth/pressure)
- Temperature, salinity, pressure measurements
- Geographic coordinates and timestamps
- Quality control flags and metadata

### Output (CSV/Parquet)
Flattened structure with columns:
- `LATITUDE`, `LONGITUDE`: Geographic position
- `TIME`: Measurement timestamp  
- `PRES`: Pressure/depth (dbar)
- `TEMP`: Temperature (°C)
- `PSAL`: Practical salinity (PSU)

## 🛠️ Customization

### Modify Data Cleaning

Edit the `process_argo_netcdf()` function in `data_processor.py`:

```python
# Add custom quality filters
df_clean = df_clean[(df_clean['TEMP'] > -2) & (df_clean['TEMP'] < 40)]

# Include additional columns
columns_to_keep = ['LATITUDE', 'LONGITUDE', 'TIME', 'PRES', 'TEMP', 'PSAL', 'DOXY']
```

### Add Custom Processing

Extend the `ArgoDataPipeline` class:

```python
class CustomArgoPipeline(ArgoDataPipeline):
    def custom_processing_step(self, df):
        # Add your custom processing here
        df['DEPTH'] = df['PRES'] * 1.02  # Convert pressure to approximate depth
        return df
```

## 📈 Performance Tips

1. **Use Parquet for large datasets** - Much faster loading than CSV
2. **Process in batches** - Don't load all files into memory at once
3. **Filter early** - Remove unnecessary data before export
4. **Use appropriate data types** - Reduces memory usage

## 🔍 Example Workflows

### Workflow 1: Basic Conversion
```bash
# Convert all NetCDF files in a directory to CSV
python -c "
from data_processor import ArgoDataPipeline
pipeline = ArgoDataPipeline()
results = pipeline.process_directory('raw_data/', export_format='csv')
print(f'Processed {len(results)} files')
"
```

### Workflow 2: Database Loading
```python
# Process and load into PostgreSQL
from data_processor import ArgoDataPipeline
from database_integration import PostgreSQLIntegration

pipeline = ArgoDataPipeline()
pg = PostgreSQLIntegration("postgresql://user:pass@localhost/argo")
pg.create_argo_table()

results = pipeline.process_directory("raw_data/")
for result in results:
    df = pd.read_csv(result['output_files'][0])  # Load CSV
    pg.insert_dataframe(df, source_file=result['input_file'])
```

### Workflow 3: Streamlit Dashboard
```python
import streamlit as st
import pandas as pd

# Load processed data
@st.cache_data
def load_argo_data():
    return pd.read_parquet("processed_data/argo_profiles.parquet")

df = load_argo_data()

# Create interactive plots
st.scatter_chart(df, x='LONGITUDE', y='LATITUDE', color='TEMP')
```

## 🚨 Troubleshooting

### Common Issues

1. **"No module named 'netcdf4'"**
   ```bash
   pip install netcdf4
   ```

2. **"Memory error with large files"**
   - Process files individually instead of batch
   - Increase system memory or use cloud processing

3. **"Empty DataFrame after processing"**
   - Check if NetCDF file has expected variable names
   - Adjust column names in `essential_cols` list

4. **"Database connection failed"**
   - Verify PostgreSQL is running
   - Check connection string format
   - Ensure database exists

### Getting Help

1. Check the demo output for expected file structure
2. Verify your NetCDF files have standard ARGO variable names
3. Test with the sample data first before using real files

## 📋 Next Steps

1. **Replace sample data** with your real ARGO NetCDF files
2. **Customize data cleaning** rules for your specific needs  
3. **Set up databases** (PostgreSQL, FAISS, Chroma) as needed
4. **Build analysis tools** using the CSV/Parquet outputs
5. **Create dashboards** with Streamlit, Plotly, or similar tools
6. **Automate processing** with scheduled scripts or workflows

## 🤝 Contributing

Feel free to extend this pipeline with:
- Additional data quality checks
- More export formats (HDF5, JSON, etc.)
- Integration with other databases
- Advanced oceanographic calculations
- Visualization components

---

**Happy oceanographic data processing! 🌊📊**
## 🌊 System
 Components Explained

### 1. **FloatChat App (`floatchat_app.py`)** - The Main Interface
**What it does:**
- Complete Streamlit web application
- Natural language chat interface
- Interactive visualizations (maps, profiles, time series)
- Real-time query processing and results display

**Key Features:**
- AI-powered query understanding
- Multiple visualization types
- Chat history and query examples
- Geographic and temporal filtering

### 2. **LLM Integration (`llm_integration.py`)** - The AI Brain
**What it does:**
- Processes natural language queries using LLMs (GPT, Claude, local models)
- Implements Retrieval-Augmented Generation (RAG)
- Model Context Protocol (MCP) integration
- Converts English questions to SQL queries

**Supported Models:**
- OpenAI GPT-3.5/GPT-4
- Anthropic Claude
- Local models (Llama, Mistral, Qwen)
- Rule-based fallback system

### 3. **Data Processor (`data_processor.py`)** - The Data Engine
**What it does:**
- Converts ARGO NetCDF files to clean DataFrames
- Handles complex multi-dimensional oceanographic data
- Exports to CSV/Parquet for easy analysis
- Batch processing capabilities

**Processing Pipeline:**
```
NetCDF Files → Clean DataFrames → CSV/Parquet → Database Storage
```

### 4. **Database Integration (`database_integration.py`)** - The Storage Layer
**What it does:**
- PostgreSQL integration for relational queries
- FAISS vector database for similarity search
- ChromaDB for document-style vector search
- Geographic and temporal indexing

### 5. **FloatChat System (`floatchat_system.py`)** - The Query Engine
**What it does:**
- Natural language query parsing
- SQL query generation
- Results visualization
- Sample data management

## 🎯 Meeting Problem Statement Requirements

### ✅ **End-to-End Pipeline**
- ✅ Ingests ARGO NetCDF files
- ✅ Converts to structured formats (SQL/Parquet)
- ✅ Stores in PostgreSQL and vector databases

### ✅ **AI-Powered Query System**
- ✅ RAG pipeline with multimodal LLMs
- ✅ Model Context Protocol (MCP) integration
- ✅ Natural language to SQL translation

### ✅ **Interactive Dashboards**
- ✅ Streamlit-based web interface
- ✅ Plotly visualizations (profiles, trajectories, maps)
- ✅ Geospatial visualizations with Folium

### ✅ **Conversational Interface**
- ✅ Chatbot-style natural language queries
- ✅ Handles complex oceanographic questions
- ✅ Provides contextual explanations

### ✅ **Example Queries Supported**
- ✅ "Show me salinity profiles near the equator in March 2023"
- ✅ "Compare BGC parameters in the Arabian Sea for the last 6 months"
- ✅ "What are the nearest ARGO floats to this location?"

## 🚀 Deployment Options

### Option 1: Local Development
```bash
# Clone and setup
git clone <repository>
cd floatchat
pip install -r requirements.txt

# Run the application
streamlit run floatchat_app.py
```

### Option 2: Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "floatchat_app.py"]
```

### Option 3: Cloud Deployment
- **Streamlit Cloud**: Direct deployment from GitHub
- **AWS/Azure/GCP**: Container-based deployment
- **Heroku**: Web app deployment

## 🔧 Configuration

### Environment Variables
```bash
# Optional: OpenAI API key for advanced LLM features
OPENAI_API_KEY=your_openai_api_key

# Optional: Database connections
POSTGRES_URL=postgresql://user:pass@localhost:5432/argo_db
```

### LLM Model Configuration
```python
# In floatchat_app.py, configure your preferred model:
llm_processor = ArgoLLMProcessor(
    api_key="your_api_key",
    model="gpt-4"  # or "claude-3-sonnet", "llama2", etc.
)
```

## 📊 Data Sources

### Primary Data Source
- **ARGO Global Data Repository**: ftp.ifremer.fr/ifremer/argo
- **Indian ARGO Project**: https://incois.gov.in/OON/index.jsp

### Supported Data Types
- **Core ARGO**: Temperature, Salinity, Pressure
- **BGC ARGO**: Oxygen, Chlorophyll, Backscattering, CDOM
- **Deep ARGO**: Extended depth profiles (0-6000m)

## 🎮 Usage Examples

### Basic Queries
```
"Show temperature profiles in the Indian Ocean"
"Find high salinity regions near the equator"
"Display oxygen data from the last 6 months"
```

### Advanced Queries
```
"Compare temperature between Arabian Sea and Bay of Bengal in 2023"
"Show me BGC parameters where chlorophyll > 1 mg/m³"
"Find ARGO floats that measured temperature below 2°C at 1000m depth"
```

### Geographic Queries
```
"Show all floats within 100km of Mumbai"
"Find data in the Exclusive Economic Zone of India"
"Display float trajectories crossing the equator"
```

## 🔍 Technical Features

### Natural Language Processing
- Intent recognition and parameter extraction
- Geographic and temporal entity recognition
- Oceanographic domain knowledge integration
- Multi-language support potential

### Visualization Capabilities
- **Interactive Maps**: Float locations and trajectories
- **Depth Profiles**: Temperature, salinity, BGC parameters
- **Time Series**: Temporal variations and trends
- **Statistical Analysis**: Correlations and distributions

### Performance Optimizations
- Efficient NetCDF processing with xarray
- Parquet format for fast data loading
- Database indexing for geographic queries
- Caching for repeated queries

## 🤝 Contributing

### Adding New Features
1. **New Parameters**: Add to `domain_knowledge` in `llm_integration.py`
2. **New Visualizations**: Extend `FloatChatVisualizer` class
3. **New Data Sources**: Modify `data_processor.py`
4. **New LLM Models**: Add to `ArgoLLMProcessor`

### Testing
```bash
# Test data processing
python pipeline_demo.py

# Test LLM integration
python llm_integration.py

# Test complete system
streamlit run floatchat_app.py
```

## 📈 Future Enhancements

### Planned Features
- **Multi-modal Input**: Image-based queries (satellite data)
- **Real-time Data**: Live ARGO data feeds
- **Advanced Analytics**: Machine learning predictions
- **Mobile App**: React Native interface
- **API Endpoints**: RESTful API for external integration

### Extensibility
- **Additional Data Sources**: Gliders, buoys, satellite data
- **More LLM Models**: Local deployment options
- **Enhanced Visualizations**: 3D ocean plots
- **Collaborative Features**: Shared queries and results

## 🏛️ Acknowledgments

**Developed for:**
- **Ministry of Earth Sciences (MoES)**
- **Indian National Centre for Ocean Information Services (INCOIS)**

**Data Sources:**
- ARGO Global Data Repository
- Indian ARGO Project
- International ARGO Program

**Technologies:**
- Streamlit for web interface
- Plotly for interactive visualizations
- OpenAI/Anthropic for LLM integration
- PostgreSQL and vector databases for storage

---

**🌊 FloatChat - Making Ocean Data Accessible to Everyone! 📊**