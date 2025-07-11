import plotly.graph_objects as go
from typing import Optional
import pandas as pd
def create_time_series_plot(
    data_processor,
    magnitude_filter: str = 'all',
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    country: Optional[str] = None,
    show_moving_avg: bool = False,
    show_cumulative: bool = False
) -> go.Figure:
    """
    Create enhanced time series plot showing earthquake trends.
    """
    # Get time series data
    time_series_data = data_processor.get_time_series_data(
        magnitude_filter, start_date, end_date, country
    )

    if time_series_data.empty:
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

    # Apply cumulative if requested
    if show_cumulative:
        time_series_data['count'] = time_series_data['count'].cumsum()

    # Calculate 5-year moving average if requested
    if show_moving_avg:
        time_series_data['count_ma'] = time_series_data['count'].rolling(window=5, min_periods=1).mean()

    # Create plot
    fig = go.Figure()

    # Earthquake count trace
    fig.add_trace(go.Scatter(
        x=time_series_data['date'],
        y=time_series_data['count'],
        mode='lines+markers',
        name='Earthquake Count' if not show_cumulative else 'Cumulative Count',
        line=dict(color='#e74c3c', width=2),
        marker=dict(size=4)
    ))

    # Moving average trace
    if show_moving_avg:
        fig.add_trace(go.Scatter(
            x=time_series_data['date'],
            y=time_series_data['count_ma'],
            mode='lines',
            name='5-Year Moving Avg',
            line=dict(color='blue', dash='dot')
        ))

    # Average magnitude trace
    fig.add_trace(go.Scatter(
        x=time_series_data['date'],
        y=time_series_data['avg_magnitude'],
        mode='lines',
        name='Average Magnitude',
        yaxis='y2',
        line=dict(color='#f39c12', width=2, dash='dash')
    ))

    # Highlight peak avg magnitude year
    max_mag_row = time_series_data.loc[time_series_data['avg_magnitude'].idxmax()]
    
    peak_date = pd.to_datetime(max_mag_row['date']).to_pydatetime()

    # Add vertical line
    fig.add_shape(
        type="line",
        x0=peak_date,
        x1=peak_date,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="gray", dash="dot"),
    )

    # Add annotation manually
    fig.add_annotation(
        x=peak_date,
        y=1,
        xref="x",
        yref="paper",
        text="Peak Avg Magnitude",
        showarrow=True,
        arrowhead=2,
        yanchor="bottom"
    )


    # Title formatting
    title = "Earthquake Trends Over Time"
    if country:
        title += f" - {country}"
    label_map = {
        "low": "Magnitude < 5.0",
        "medium": "5.0 ≤ Magnitude < 6.5",
        "high": "Magnitude ≥ 6.5",
        "all": "All Earthquakes"
    }
    if magnitude_filter in label_map:
        title += f" ({label_map[magnitude_filter]})"

    # Layout setup
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Cumulative Earthquakes" if show_cumulative else "Number of Earthquakes",
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

    # Improve x-axis tick format (Year only)
    fig.update_xaxes(dtick="M12", tickformat="%Y")

    return fig
