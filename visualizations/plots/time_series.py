import plotly.graph_objects as go
from typing import Optional

def create_time_series_plot(data_processor, 
                           magnitude_filter: str = 'all',
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None,
                           country: Optional[str] = None) -> go.Figure:
    """
    Create time series plot showing earthquake trends over time.
    """
    # Get time series data
    time_series_data = data_processor.get_time_series_data(
        magnitude_filter, start_date, end_date, country
    )
    
    if time_series_data.empty:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for the selected filters",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title="Earthquake Trends Over Time",
            xaxis_title="Date",
            yaxis_title="Number of Earthquakes",
            height=400
        )
        return fig
    
    # Create the plot
    fig = go.Figure()
    
    # Add earthquake count line
    fig.add_trace(go.Scatter(
        x=time_series_data['date'],
        y=time_series_data['count'],
        mode='lines+markers',
        name='Earthquake Count',
        line=dict(color='#e74c3c', width=2),
        marker=dict(size=4)
    ))
    
    # Add average magnitude line (secondary y-axis)
    fig.add_trace(go.Scatter(
        x=time_series_data['date'],
        y=time_series_data['avg_magnitude'],
        mode='lines',
        name='Average Magnitude',
        yaxis='y2',
        line=dict(color='#f39c12', width=2, dash='dash')
    ))
    
    # Update layout
    title = "Earthquake Trends Over Time"
    if country:
        title += f" - {country}"
    if magnitude_filter != 'all':
        title += f" ({magnitude_filter.title()} earthquakes)"
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Number of Earthquakes",
        yaxis2=dict(
            title="Average Magnitude",
            overlaying="y",
            side="right",
            range=[0, 10]
        ),
        hovermode='x unified',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig