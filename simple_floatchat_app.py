#!/usr/bin/env python3
"""
Simplified FloatChat App - Guaranteed to Work
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from datetime import datetime
import logging

# Import our components
from floatchat_system import FloatChatQueryProcessor, FloatChatVisualizer, load_sample_data_to_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="FloatChat - ARGO Data Explorer",
        page_icon="🌊",
        layout="wide"
    )
    
    st.title("🌊 FloatChat - AI-Powered ARGO Ocean Data Explorer")
    st.markdown("**Natural language interface for oceanographic data discovery and visualization**")
    
    # Initialize components
    if 'query_processor' not in st.session_state:
        st.session_state.query_processor = FloatChatQueryProcessor()
        st.session_state.visualizer = FloatChatVisualizer()
        
        # Load sample data
        with st.spinner("Loading sample data..."):
            load_sample_data_to_db()
        st.success("✅ Sample data loaded!")
    
    # Sidebar with examples
    st.sidebar.header("💡 Example Queries")
    example_queries = [
        "Show me temperature profiles near the equator",
        "Find salinity data in the Arabian Sea",
        "Display oxygen levels in the Indian Ocean",
        "Show me all data from the last 6 months",
        "Compare temperature profiles from different regions"
    ]
    
    for query in example_queries:
        if st.sidebar.button(query, key=f"example_{hash(query)}"):
            st.session_state.selected_query = query
    
    # Main interface
    st.header("💬 Ask About Ocean Data")
    
    # Query input
    user_query = st.text_input(
        "What would you like to know about ocean data?",
        value=st.session_state.get('selected_query', ''),
        placeholder="e.g., Show me salinity profiles near the equator in March 2023"
    )
    
    # Clear selected query after using it
    if 'selected_query' in st.session_state:
        del st.session_state.selected_query
    
    col1, col2 = st.columns([1, 1])
    with col1:
        search_clicked = st.button("🔍 Search Ocean Data", type="primary", use_container_width=True)
    with col2:
        if st.button("🧹 Clear Results", use_container_width=True):
            st.session_state.current_data = pd.DataFrame()
            st.rerun()
    
    # Process query
    if search_clicked and user_query:
        process_query(user_query)
    
    # Show current data if available
    if 'current_data' in st.session_state and not st.session_state.current_data.empty:
        display_results(st.session_state.current_data)

def process_query(user_query: str):
    """Process user query and display results"""
    with st.spinner("🤖 Processing your query..."):
        try:
            # Process the query
            result = st.session_state.query_processor.process_natural_language_query(user_query)
            
            if result['success']:
                df = result['results']
                st.session_state.current_data = df
                
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
            logger.error(f"Query processing error: {str(e)}")

def display_results(df: pd.DataFrame):
    """Display query results"""
    if df.empty:
        st.warning("No data to display")
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
            map_viz = st.session_state.visualizer.create_map_visualization(df)
            st_folium(map_viz, width=700, height=500)
        else:
            st.info("Map visualization not available - missing coordinates")
    
    with tab2:  # Profiles
        st.write("**Depth Profiles**")
        available_params = [col for col in ['temperature', 'salinity', 'oxygen', 'chlorophyll'] if col in df.columns]
        
        if available_params:
            selected_param = st.selectbox("Select Parameter", available_params, key="profile_param")
            profile_plot = st.session_state.visualizer.create_profile_plot(df, selected_param)
            st.plotly_chart(profile_plot, use_container_width=True)
        else:
            st.info("No oceanographic parameters available")
    
    with tab3:  # Time Series
        if 'date_time' in df.columns:
            st.write("**Time Series Analysis**")
            available_params = [col for col in ['temperature', 'salinity', 'oxygen', 'chlorophyll'] if col in df.columns]
            
            if available_params:
                selected_param = st.selectbox("Select Parameter", available_params, key="ts_param")
                ts_plot = st.session_state.visualizer.create_time_series_plot(df, selected_param)
                st.plotly_chart(ts_plot, use_container_width=True)
            else:
                st.info("No parameters available for time series")
        else:
            st.info("Time series requires date data")
    
    with tab4:  # Data Table
        st.write("**Raw Data**")
        st.dataframe(df, use_container_width=True, height=400)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"argo_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
