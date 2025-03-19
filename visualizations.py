import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_total_cases_chart(data, country):
    """Create line chart for total cases"""
    fig = px.line(
        data,
        x='Date',
        y='Confirmed',
        title=f'Total COVID-19 Cases in {country}',
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Cases",
        hovermode='x unified'
    )
    return fig

def create_daily_cases_chart(data, country):
    """Create bar chart for daily new cases with 7-day moving average"""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add daily new cases bars
    fig.add_trace(
        go.Bar(
            x=data['Date'],
            y=data['Daily_New'],
            name="Daily New Cases",
            marker_color='lightblue'
        ),
        secondary_y=False
    )
    
    # Add 7-day moving average line
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data['Seven_Day_Average'],
            name="7-day Moving Average",
            line=dict(color='red', width=2)
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title=f'Daily New COVID-19 Cases in {country}',
        xaxis_title="Date",
        yaxis_title="Daily New Cases",
        hovermode='x unified'
    )
    
    return fig

def create_growth_rate_chart(data, country):
    """Create line chart for growth rate"""
    growth_rate = data['Daily_New'].pct_change() * 100
    
    fig = px.line(
        x=data['Date'],
        y=growth_rate,
        title=f'Daily Growth Rate in {country} (%)',
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Growth Rate (%)",
        hovermode='x unified'
    )
    return fig
