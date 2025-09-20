#!/usr/bin/env python3
"""
Working FloatChat App - Direct and Simple
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
from floatchat_system import FloatChatQueryProcessor, FloatChatVisualizer, load_sample_data_to_db

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
    
    selected_example = st.sidebar.selectbox("Choose an example:", [""] + example_queries)
    
    # Main interface
    st.header("💬 Ask About Ocean Data")
    
    # Query input
    if selected_example:
        user_query = st.text_input(
            "What would you like to know about ocean data?",
            value=selected_example,
            placeholder="e.g., Show me salinity profiles near the equator"
        )
    else:
        user_query = st.text_input(
            "What would you like to know about ocean data?",
            placeholder="e.g., Show me salinity profiles near the equator"
        )
    
    # Search button
    if st.button("🔍 Search Ocean Data", type="primary"):
        if user_query:
            # Process the query directly
            with st.spinner("🤖 Processing your query..."):
                try:
                    result = st.session_state.query_processor.process_natural_language_query(user_query)
                    
                    if result['success']:
                        df = result['results']
                        
                        # Show success message
                        st.success(f"✅ Found {len(df)} profiles from {df['float_id'].nunique()} ARGO floats")
                        
                        # Show query details
                        with st.expander("🔧 Query Details"):
                            st.write("**Your Query:**", user_query)
                            st.write("**Generated SQL:**")
                            st.code(result['sql_query'], language='sql')
                            st.write("**Parsed Query:**")
                            st.json(result['parsed_query'])
                        
                        # Display results
                        display_results(df)
                        
                    else:
                        st.error(f"Query failed: {result['message']}")
                        if 'error' in result:
                            st.error(f"Error details: {result['error']}")
                            
                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")
                    import traceback
                    st.error(f"Traceback: {traceback.format_exc()}")
        else:
            st.warning("Please enter a query first!")

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
