#!/usr/bin/env python3
"""
Fixed FloatChat App - Proper State Management
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from datetime import datetime

# Import our components
# Removed dependency on deleted floatchat_system module
import sqlite3
from pathlib import Path

class FloatChatQueryProcessor:
    """Simple query processor for ARGO data"""
    
    def __init__(self, db_path: str = "argo_data.db"):
        self.db_path = db_path
        self.ensure_database()
    
    def ensure_database(self):
        """Ensure database exists"""
        if not Path(self.db_path).exists():
            self.create_sample_database()
    
    def create_sample_database(self):
        """Create sample database if no real data exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS argo_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                float_id TEXT,
                latitude REAL,
                longitude REAL,
                date_time TEXT,
                pressure REAL,
                temperature REAL,
                salinity REAL,
                source_file TEXT
            )
        ''')
        
        # Create sample data
        import numpy as np
        np.random.seed(42)
        sample_data = []
        
        for i in range(100):
            depth = np.random.uniform(10, 1000)
            temp = 25 - (depth / 50) + np.random.normal(0, 2)
            
            sample_data.append({
                'float_id': f'SAMPLE_{i//25}',
                'latitude': np.random.uniform(-30, 30),
                'longitude': np.random.uniform(-50, 50),
                'date_time': '2024-01-01',
                'pressure': depth,
                'temperature': temp,
                'salinity': 35 + np.random.normal(0, 0.5),
                'source_file': 'sample_data.nc'
            })
        
        df = pd.DataFrame(sample_data)
        df.to_sql('argo_profiles', conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()
    
    def execute_query(self, sql_query: str) -> pd.DataFrame:
        """Execute SQL query"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(sql_query, conn)
            conn.close()
            return df
        except Exception as e:
            return pd.DataFrame()
    
    def process_natural_language_query(self, user_query: str) -> dict:
        """Process natural language query"""
        query_lower = user_query.lower()
        
        sql_query = "SELECT * FROM argo_profiles WHERE 1=1"
        conditions = []
        
        if 'temperature' in query_lower:
            conditions.append("temperature IS NOT NULL")
        if 'deep' in query_lower:
            conditions.append("pressure > 500")
        if 'shallow' in query_lower:
            conditions.append("pressure < 100")
        
        if conditions:
            sql_query += " AND " + " AND ".join(conditions)
        
        sql_query += " ORDER BY date_time DESC LIMIT 1000"
        
        results_df = self.execute_query(sql_query)
        
        return {
            'success': True,
            'results': results_df,
            'sql_query': sql_query,
            'parsed_query': {'keywords': query_lower.split()},
            'message': f"Found {len(results_df)} matching profiles"
        }

class FloatChatVisualizer:
    """Simple visualizer for ARGO data"""
    
    @staticmethod
    def create_profile_plot(df: pd.DataFrame, parameter: str = 'temperature'):
        """Create depth profile plot"""
        if df.empty or parameter not in df.columns:
            fig = go.Figure()
            fig.add_annotation(text="No data available", x=0.5, y=0.5)
            return fig
        
        fig = go.Figure()
        
        for float_id in df['float_id'].unique()[:5]:
            float_data = df[df['float_id'] == float_id]
            
            fig.add_trace(go.Scatter(
                x=float_data[parameter],
                y=-float_data['pressure'],
                mode='lines+markers',
                name=f'Float {float_id}',
                line=dict(width=2),
                marker=dict(size=4)
            ))
        
        fig.update_layout(
            title=f'{parameter.title()} Profiles',
            xaxis_title=f'{parameter.title()}',
            yaxis_title='Depth (m)',
            height=600
        )
        
        return fig
    
    @staticmethod
    def create_map_visualization(df: pd.DataFrame):
        """Create map visualization"""
        if df.empty or 'latitude' not in df.columns:
            return None
        
        # Create a simple folium map
        center_lat = df['latitude'].mean()
        center_lon = df['longitude'].mean()
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=4)
        
        for idx, row in df.iterrows():
            if idx > 50:  # Limit markers
                break
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,
                popup=f"Float: {row['float_id']}<br>Temp: {row.get('temperature', 'N/A')}°C",
                color='blue',
                fill=True
            ).add_to(m)
        
        return m
    
    @staticmethod
    def create_time_series_plot(df: pd.DataFrame, parameter: str = 'temperature'):
        """Create time series plot"""
        if df.empty or parameter not in df.columns:
            fig = go.Figure()
            fig.add_annotation(text="No data available", x=0.5, y=0.5)
            return fig
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(df['date_time']),
            y=df[parameter],
            mode='markers',
            name=parameter.title()
        ))
        
        fig.update_layout(
            title=f'{parameter.title()} Time Series',
            xaxis_title='Date',
            yaxis_title=parameter.title(),
            height=500
        )
        
        return fig

def load_sample_data_to_db():
    """Load sample data - compatibility function"""
    processor = FloatChatQueryProcessor()
    return True

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="FloatChat - ARGO Data Explorer",
        page_icon="🌊",
        layout="wide"
    )
    
    st.title("🌊 FloatChat - AI-Powered ARGO Ocean Data Explorer")
    st.markdown("**Natural language interface for oceanographic data discovery and visualization**")
    
    # Initialize session state
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.query_processor = None
        st.session_state.visualizer = None
        st.session_state.current_data = pd.DataFrame()
        st.session_state.last_query = ""
    
    # Initialize components
    if st.session_state.query_processor is None:
        with st.spinner("Initializing system..."):
            st.session_state.query_processor = FloatChatQueryProcessor()
            st.session_state.visualizer = FloatChatVisualizer()
            load_sample_data_to_db()
        st.success("✅ Sample data loaded!")
    
    # Sidebar with examples
    st.sidebar.header("💡 Example Queries")
    example_queries = [
        "Show me temperature profiles near the equator",
        "Find salinity data in the Arabian Sea",
        "Display oxygen levels in the Indian Ocean",
        "Show me all data from the last 6 months"
    ]
    
    # Example query selection
    selected_example = st.sidebar.selectbox("Choose an example:", [""] + example_queries)
    
    # Main interface
    st.header("💬 Ask About Ocean Data")
    
    # Query input - use session state to maintain value
    if selected_example and selected_example != st.session_state.get('last_query', ''):
        st.session_state.last_query = selected_example
    
    user_query = st.text_input(
        "What would you like to know about ocean data?",
        value=st.session_state.get('last_query', ''),
        placeholder="e.g., Show me salinity profiles near the equator",
        key="query_input"
    )
    
    # Update session state when query changes
    if user_query != st.session_state.get('last_query', ''):
        st.session_state.last_query = user_query
    
    # Search button
    search_clicked = st.button("🔍 Search Ocean Data", type="primary")
    
    # Clear button
    if st.button("🧹 Clear Results"):
        st.session_state.current_data = pd.DataFrame()
        st.session_state.last_query = ""
        st.rerun()
    
    # Process query when search is clicked
    if search_clicked and user_query:
        with st.spinner("🤖 Processing your query..."):
            try:
                result = st.session_state.query_processor.process_natural_language_query(user_query)
                
                if result['success']:
                    df = result['results']
                    st.session_state.current_data = df  # Store in session state
                    
                    # Show success message
                    st.success(f"✅ Found {len(df)} profiles from {df['float_id'].nunique()} ARGO floats")
                    
                    # Show query details
                    with st.expander("🔧 Query Details"):
                        st.write("**Your Query:**", user_query)
                        st.write("**Generated SQL:**")
                        st.code(result['sql_query'], language='sql')
                        st.write("**Parsed Query:**")
                        st.json(result['parsed_query'])
                    
                else:
                    st.error(f"Query failed: {result['message']}")
                    if 'error' in result:
                        st.error(f"Error details: {result['error']}")
                        
            except Exception as e:
                st.error(f"Error processing query: {str(e)}")
                import traceback
                st.error(f"Traceback: {traceback.format_exc()}")
    
    # Always display results if they exist in session state
    if not st.session_state.current_data.empty:
        st.markdown("---")  # Separator
        display_results(st.session_state.current_data)

def display_results(df: pd.DataFrame):
    """Display query results"""
    if df.empty:
        return
    
    # Data summary
    st.subheader("📊 Data Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Profiles", len(df))
    with col2:
        st.metric("Unique Floats", df['float_id'].nunique())
    with col3:
        if 'date_time' in df.columns:
            st.metric("Date Range", f"{df['date_time'].min()[:10]} to {df['date_time'].max()[:10]}")
    with col4:
        if 'pressure' in df.columns:
            st.metric("Depth Range", f"{df['pressure'].min():.0f} - {df['pressure'].max():.0f} dbar")
    
    # Visualizations
    st.subheader("📈 Data Visualizations")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Map", "📊 Profiles", "⏱️ Time Series", "📋 Data Table"])
    
    with tab1:  # Map
        if 'latitude' in df.columns and 'longitude' in df.columns:
            st.write("**Geographic Distribution of ARGO Floats**")
            try:
                map_viz = st.session_state.visualizer.create_map_visualization(df)
                st_folium(map_viz, width=700, height=500)
            except Exception as e:
                st.error(f"Map error: {str(e)}")
        else:
            st.info("Map visualization not available - missing coordinates")
    
    with tab2:  # Profiles
        st.write("**Depth Profiles**")
        available_params = [col for col in ['temperature', 'salinity', 'oxygen', 'chlorophyll'] if col in df.columns]
        
        if available_params:
            selected_param = st.selectbox("Select Parameter", available_params, key="profile_param")
            try:
                profile_plot = st.session_state.visualizer.create_profile_plot(df, selected_param)
                st.plotly_chart(profile_plot, use_container_width=True)
            except Exception as e:
                st.error(f"Profile plot error: {str(e)}")
        else:
            st.info("No oceanographic parameters available")
    
    with tab3:  # Time Series
        if 'date_time' in df.columns:
            st.write("**Time Series Analysis**")
            available_params = [col for col in ['temperature', 'salinity', 'oxygen', 'chlorophyll'] if col in df.columns]
            
            if available_params:
                selected_param = st.selectbox("Select Parameter", available_params, key="ts_param")
                try:
                    ts_plot = st.session_state.visualizer.create_time_series_plot(df, selected_param)
                    st.plotly_chart(ts_plot, use_container_width=True)
                except Exception as e:
                    st.error(f"Time series error: {str(e)}")
            else:
                st.info("No parameters available for time series")
        else:
            st.info("Time series requires date data")
    
    with tab4:  # Data Table
        st.write("**Raw Data**")
        st.dataframe(df, use_container_width=True, height=400)
        
        # Download button
        try:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"argo_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Download error: {str(e)}")

if __name__ == "__main__":
    main()
