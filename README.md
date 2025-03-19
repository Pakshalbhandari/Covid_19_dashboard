# COVID-19 Analytics Dashboard

This is an interactive web dashboard built with Streamlit that visualizes COVID-19 confirmed case data worldwide. The dashboard pulls data from the Johns Hopkins University CSSE GitHub repository, processes it, and presents various insights and visualizations, including total cases, daily new cases, peak daily cases, and growth rates.

## Features

- **Country Selection**: Allows the user to select a country and view its COVID-19 data.
- **Date Range Filter**: Users can filter the data based on a specific date range.
- **Key Metrics**: Displays key metrics, including total cases, average daily cases, peak daily cases, and the latest daily growth rate.
- **Visualizations**: Provides interactive charts for:
  - Total Cases Over Time
  - Daily New Cases
  - Daily Growth Rate

## Technologies Used

- **Streamlit**: For building the interactive dashboard.
- **Pandas**: For data processing and transformation.
- **Plotly**: For creating interactive charts.
- **GitHub - Johns Hopkins University CSSE COVID-19 Data**: For sourcing the COVID-19 data.

## Setup

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Pakshalbhandari/Covid_19_dashboard.git
    cd Covid_19_dashboard
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

5. Open the web browser at the URL shown in the terminal (usually `http://localhost:8501`).

## How it Works

1. **Loading Data**: The dashboard loads the COVID-19 confirmed case data from the Johns Hopkins University CSSE GitHub repository.
   
2. **Processing Data**: The data is processed to aggregate confirmed cases by country and date. The daily new cases and 7-day moving average of daily new cases are also calculated.

3. **Visualizations**: 
   - **Total Cases Over Time**: Shows the total number of confirmed COVID-19 cases in the selected country over time.
   - **Daily New Cases**: Visualizes the daily new confirmed cases.
   - **Daily Growth Rate**: Displays the daily growth rate of COVID-19 cases.

4. **Key Metrics**: The app calculates and shows key metrics such as:
   - Total confirmed cases
   - Average daily cases
   - Peak daily cases
   - Latest daily growth rate
   
5. **Filters**: Users can filter data based on a selected country and a custom date range.
