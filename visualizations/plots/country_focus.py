import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Tuple
from src.country_centers import get_country_center , get_country_zoom

def create_country_focus_view(
    data_processor,
    country: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> go.Figure:
    """
    Create detailed map view for a specific country.
    """

    # Get country-specific filtered data
    country_data = data_processor.get_filtered_data(
        start_date=start_date,
        end_date=end_date,
        country=country
    )

    if country_data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text=f"No earthquake data available for {country} in the selected range. ",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(title=f"Earthquake Map - {country}", height=500)
        return fig

    center_coords = get_country_center(country)
    if center_coords is None:
        center_coords = (0, 0)
        zoom_level = 1
    else:
        zoom_level = get_country_zoom(country)

    fig = px.scatter_mapbox(
        country_data,
        lat="Latitude",
        lon="Longitude",
        size="mag",
        color="depth",
        hover_name="Place",
        hover_data=["time", "mag", "depth"],
        color_continuous_scale="Viridis",
        size_max=20,
        zoom=zoom_level,
        height=500,
        center={"lat": center_coords[0], "lon": center_coords[1]} if center_coords else {"lat": 0, "lon": 0},
        title=f"Earthquake Epicentres - {country}"
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
    )

    return fig


def create_country_barcharts(
    data_processor,
    country: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Tuple[go.Figure, go.Figure]:
    """
    Create two bar charts for a country:
    1. Magnitude distribution (low, medium, high)
    2. Earthquake count by year
    """

    df = data_processor.get_filtered_data(
        start_date=start_date,
        end_date=end_date,
        country=country
    )

    if df.empty:
        return go.Figure(), go.Figure()

    # --- Bar chart 1: Magnitude distribution ---
    def classify_magnitude(mag):
        if mag < 5.0:
            return 'Low (<5.0)'
        elif mag < 6.5:
            return 'Medium (5.0–6.5)'
        else:
            return 'High (≥6.5)'

    df['mag_class'] = df['mag'].apply(classify_magnitude)
    mag_counts = df['mag_class'].value_counts().reindex(['Low (<5.0)', 'Medium (5.0–6.5)', 'High (≥6.5)'], fill_value=0)

    mag_bar = go.Figure(go.Bar(
        x=mag_counts.index,
        y=mag_counts.values,
        marker_color=['#3498db', '#f1c40f', '#e74c3c']
    ))
    mag_bar.update_layout(
        title=f"Magnitude Distribution - {country}",
        xaxis_title="Magnitude Range",
        yaxis_title="Number of Earthquakes",
        height=350
    )

    # --- Bar chart 2: Earthquake count by year ---
    year_counts = df['year'].value_counts().sort_index()
    year_bar = go.Figure(go.Bar(
        x=year_counts.index.astype(str),
        y=year_counts.values,
        marker_color='#9b59b6'
    ))
    year_bar.update_layout(
        title=f"Year-wise Earthquake Count - {country}",
        xaxis_title="Year",
        yaxis_title="Count",
        height=350
    )

    return mag_bar, year_bar
