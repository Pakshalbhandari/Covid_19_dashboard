import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from data_processor import CovidDataProcessor
from visualizations import (
    create_total_cases_chart,
    create_daily_cases_chart,
    create_growth_rate_chart
)

# Page config
st.set_page_config(
    page_title="COVID-19 Analytics Dashboard",
    page_icon="🦠",
    layout="wide"
)

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = CovidDataProcessor()

# Header
st.title("🦠 COVID-19 Analytics Dashboard")
st.markdown("""
This dashboard provides interactive visualizations of COVID-19 data worldwide.
""")

# Load data
try:
    with st.spinner('Loading data...'):
            data = st.session_state.data_processor.load_data()

    # Ensure the data has been processed and Date column exists
    if 'Date' not in data.columns:
        st.session_state.data_processor.log_debug(f"No date for you")
        raise ValueError("Datesss column is missing from the data.")

    # Sidebar filters
    st.sidebar.header("📊 Filters")
    
    # Country selection
    countries = st.session_state.data_processor.get_country_list()
    selected_country = st.sidebar.selectbox(
        "Select Country",
        countries,
        index=countries.index('India') if 'India' in countries else 0
    )
    st.session_state.data_processor.log_debug(f"Selected country: {selected_country}")

    # Ensure that 'Date' exists and calculate min_date and max_date
    try:
        if 'Date' not in data.columns:
            st.error(f"Date column missing after country selection. Available columns: {list(data.columns)}")
            st.stop()
            
        min_date = data['Date'].min()
        max_date = data['Date'].max()
        st.session_state.data_processor.log_debug(f"Date range: {min_date} to {max_date}")
    
    except Exception as e:
        st.error(f"Error accessing date range: {str(e)}")
        st.session_state.data_processor.log_debug(f"Error in date range: {str(e)}")
        st.stop()

    # Date range selection
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=[max_date - timedelta(days=90), max_date],
        min_value=min_date,
        max_value=max_date
    )
    st.session_state.data_processor.log_debug(f"Attemsps")
    if len(date_range) == 2:
        start_date, end_date = date_range
        
        # Attempt to filter data for the selected country and date range
        st.session_state.data_processor.log_debug(f"Attempting to filter data for {selected_country}")
        filtered_data = st.session_state.data_processor.filter_data(
            selected_country,
            pd.to_datetime(start_date),
            pd.to_datetime(end_date)
        )
        
        if filtered_data.empty:
            st.warning(f"No data available for {selected_country} between {start_date} and {end_date}.")
        else:
            # Key metrics
            st.header("📈 Key Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Cases",
                    f"{filtered_data['Confirmed'].iloc[-1]:,.0f}",
                    f"{filtered_data['Daily_New'].iloc[-1]:,.0f} new"
                )
                
            with col2:
                avg_daily = filtered_data['Daily_New'].mean()
                st.metric(
                    "Avg. Daily Cases",
                    f"{avg_daily:,.0f}"
                )
                
            with col3:
                peak_daily = filtered_data['Daily_New'].max()
                st.metric(
                    "Peak Daily Cases",
                    f"{peak_daily:,.0f}"
                )
                
            with col4:
                growth_rate = (
                    (filtered_data['Confirmed'].iloc[-1] - filtered_data['Confirmed'].iloc[-2])
                    / filtered_data['Confirmed'].iloc[-2] * 100
                )
                st.metric(
                    "Latest Daily Growth",
                    f"{growth_rate:.2f}%"
                )
            
            # Charts
            st.header("📊 Visualizations")
            
            # Total cases chart
            st.subheader("Total Cases Over Time")
            st.plotly_chart(
                create_total_cases_chart(filtered_data, selected_country),
                use_container_width=True
            )
            
            # Daily cases chart
            st.subheader("Daily New Cases")
            st.plotly_chart(
                create_daily_cases_chart(filtered_data, selected_country),
                use_container_width=True
            )
            
            # Growth rate chart
            st.subheader("Daily Growth Rate")
            st.plotly_chart(
                create_growth_rate_chart(filtered_data, selected_country),
                use_container_width=True
            )
        
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please try refreshing the page or check your internet connection.")
