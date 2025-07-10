import plotly.express as px
import plotly.graph_objects as go
from typing import Optional
def create_country_focus_view(data_processor, 
                             country: str,
                             start_date: Optional[str] = None,
                             end_date: Optional[str] = None) -> go.Figure:
    """
    Create detailed map view for a specific country.
    """
    # Get country data
    country_data = data_processor.get_filtered_data(
        start_date, end_date, country=country
    )
    
    if country_data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text=f"No earthquake data available for {country}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title=f"Earthquake Map - {country}",
            height=500
        )
        return fig
    
    # Create scatter map
    fig = px.scatter_mapbox(
        country_data,
        lat='Latitude',
        lon='Longitude',
        size='mag',
        color='mag',
        hover_name='Place',
        hover_data=['time', 'depth'],
        color_continuous_scale='Reds',
        size_max=20,
        zoom=4,
        title=f"Earthquake Locations - {country}"
    )
    
    # Update layout
    fig.update_layout(
        mapbox_style='carto-positron',
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig