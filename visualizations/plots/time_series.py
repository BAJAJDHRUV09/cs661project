import plotly.graph_objects as go
from typing import Optional
import pandas as pd

def create_count_time_series_plot(
    data_processor,
    magnitude_filter: str = 'all',
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    country: Optional[str] = None,
    show_moving_avg: bool = False,
    show_cumulative: bool = False,
    mode: str = 'single'
) -> go.Figure:
    """
    Create time series plot showing earthquake count trends.
    """
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
            title="Earthquake Count Trends",
            xaxis_title="Date",
            yaxis_title="Number of Earthquakes",
            height=600
        )
        return fig

    if show_cumulative:
        time_series_data['count'] = time_series_data['count'].cumsum()

    if show_moving_avg:
        time_series_data['count_ma'] = time_series_data['count'].rolling(window=5, min_periods=1).mean()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=time_series_data['date'],
        y=time_series_data['count'],
        mode='lines+markers',
        name='Earthquake Count' if not show_cumulative else 'Cumulative Count',
        line=dict(color='#e74c3c', width=2),
        marker=dict(size=4)
    ))

    if show_moving_avg:
        fig.add_trace(go.Scatter(
            x=time_series_data['date'],
            y=time_series_data['count_ma'],
            mode='lines',
            name='5-Year Moving Avg',
            line=dict(color='#3498db', dash='dot', width=2)
        ))

    # Title formatting
    title = "Earthquake Count Trends"
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

    # Layout
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Cumulative Earthquakes" if show_cumulative else "Number of Earthquakes",
        hovermode='x unified',
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Tick formatting
    if mode == 'single':
        fig.update_xaxes(
            dtick="M1",
            tickformat="%b",  # Jan, Feb...
            tickangle=0
        )
    else:
        # Range mode — cap ticks to 10
        dates = time_series_data['date']
        if not dates.empty:
            min_year = dates.min().year
            max_year = dates.max().year
            span = max_year - min_year + 1
            num_ticks = min(span, 10)

            tick_years = pd.Series(pd.date_range(
                start=f"{min_year}-01-01",
                end=f"{max_year}-12-31",
                periods=num_ticks
            )).dt.year.unique()

            tick_vals = [pd.Timestamp(f"{y}-01-01") for y in tick_years]
            tick_texts = [str(y) for y in tick_years]

            fig.update_xaxes(
                tickvals=tick_vals,
                ticktext=tick_texts,
                tickangle=45
            )

    return fig

def create_magnitude_time_series_plot(
    data_processor,
    magnitude_filter: str = 'all',
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    country: Optional[str] = None,
    show_moving_avg: bool = False,
    mode: str = 'single'
) -> go.Figure:
    """
    Create time series plot showing magnitude trends.
    """
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
            title="Magnitude Trends",
            xaxis_title="Date",
            yaxis_title="Magnitude",
            height=600
        )
        return fig

    if show_moving_avg:
        time_series_data['avg_mag_ma'] = time_series_data['avg_magnitude'].rolling(window=5, min_periods=1).mean()

    fig = go.Figure()

    # Average magnitude
    fig.add_trace(go.Scatter(
        x=time_series_data['date'],
        y=time_series_data['avg_magnitude'],
        mode='lines+markers',
        name='Average Magnitude',
        line=dict(color='#f39c12', width=2),
        marker=dict(size=4)
    ))



    if show_moving_avg:
        fig.add_trace(go.Scatter(
            x=time_series_data['date'],
            y=time_series_data['avg_mag_ma'],
            mode='lines',
            name='Avg Magnitude (5Y MA)',
            line=dict(color='#f39c12', dash='dot', width=1.5),
            opacity=0.7
        ))
        


    # Highlight peak average magnitude
    max_mag_row = time_series_data.loc[time_series_data['avg_magnitude'].idxmax()]
    peak_date = pd.to_datetime(max_mag_row['date']).to_pydatetime()

    fig.add_shape(
        type="line",
        x0=peak_date,
        x1=peak_date,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="red", dash="dot"),
    )

    fig.add_annotation(
        x=peak_date,
        y=1,
        xref="x",
        yref="paper",
        text="Peak Avg Magnitude",
        showarrow=True,
        arrowhead=2,
        yanchor="bottom",
        font=dict(color="red")
    )

    # Title formatting
    title = "Magnitude Trends"
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

    # Layout
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Magnitude",
        yaxis=dict(range=[0, 10]),  # Magnitude scale
        hovermode='x unified',
        height=600,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Tick formatting
    if mode == 'single':
        fig.update_xaxes(
            dtick="M1",
            tickformat="%b",  # Jan, Feb...
            tickangle=0
        )
    else:
        # Range mode — cap ticks to 10
        dates = time_series_data['date']
        if not dates.empty:
            min_year = dates.min().year
            max_year = dates.max().year
            span = max_year - min_year + 1
            num_ticks = min(span, 10)

            tick_years = pd.Series(pd.date_range(
                start=f"{min_year}-01-01",
                end=f"{max_year}-12-31",
                periods=num_ticks
            )).dt.year.unique()

            tick_vals = [pd.Timestamp(f"{y}-01-01") for y in tick_years]
            tick_texts = [str(y) for y in tick_years]

            fig.update_xaxes(
                tickvals=tick_vals,
                ticktext=tick_texts,
                tickangle=45
            )

    return fig

def create_time_series_plot(
    data_processor,
    magnitude_filter: str = 'all',
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    country: Optional[str] = None,
    show_moving_avg: bool = False,
    show_cumulative: bool = False,
    mode: str = 'single'  # <-- new
) -> go.Figure:
    """
    Create enhanced time series plot showing earthquake trends.
    """
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

    if show_cumulative:
        time_series_data['count'] = time_series_data['count'].cumsum()

    if show_moving_avg:
        time_series_data['count_ma'] = time_series_data['count'].rolling(window=5, min_periods=1).mean()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=time_series_data['date'],
        y=time_series_data['count'],
        mode='lines+markers',
        name='Earthquake Count' if not show_cumulative else 'Cumulative Count',
        line=dict(color='#e74c3c', width=2),
        marker=dict(size=4)
    ))

    if show_moving_avg:
        fig.add_trace(go.Scatter(
            x=time_series_data['date'],
            y=time_series_data['count_ma'],
            mode='lines',
            name='5-Year Moving Avg',
            line=dict(color='blue', dash='dot')
        ))

    fig.add_trace(go.Scatter(
        x=time_series_data['date'],
        y=time_series_data['avg_magnitude'],
        mode='lines',
        name='Average Magnitude',
        yaxis='y2',
        line=dict(color='#f39c12', width=2, dash='dash')
    ))

    max_mag_row = time_series_data.loc[time_series_data['avg_magnitude'].idxmax()]
    peak_date = pd.to_datetime(max_mag_row['date']).to_pydatetime()

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

    # Layout
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

    # 🧠 Final Tick Fix
    if mode == 'single':
        fig.update_xaxes(
            dtick="M1",
            tickformat="%b",  # Jan, Feb...
            tickangle=0
        )
    else:
        # Range mode — cap ticks to 10
        dates = time_series_data['date']
        if not dates.empty:
            min_year = dates.min().year
            max_year = dates.max().year
            span = max_year - min_year + 1
            num_ticks = min(span, 10)

            tick_years = pd.Series(pd.date_range(
                start=f"{min_year}-01-01",
                end=f"{max_year}-12-31",
                periods=num_ticks
            )).dt.year.unique()

            tick_vals = [pd.Timestamp(f"{y}-01-01") for y in tick_years]
            tick_texts = [str(y) for y in tick_years]

            fig.update_xaxes(
                tickvals=tick_vals,
                ticktext=tick_texts,
                tickangle=45
            )

    return fig
