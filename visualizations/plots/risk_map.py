import plotly.express as px
from ..geo_utils import get_world_geojson
import plotly.graph_objects as go
from typing import Optional
def create_global_risk_map(data_processor, metric: str = 'count') -> go.Figure:
    """
    Create global risk map showing earthquake activity by country.
    """
    # Get risk map data
    risk_data = data_processor.get_risk_map_data(metric)
    
    if risk_data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for risk map",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title="Global Earthquake Risk Map",
            height=600
        )
        return fig
    
    # Get world GeoJSON
    geojson_data = get_world_geojson()
    
    if geojson_data:
        # Create choropleth map with proper GeoJSON
        fig = px.choropleth(
            risk_data,
            geojson=geojson_data,
            locations='country',
            featureidkey='properties.name',
            color='value',
            hover_name='country',
            hover_data=['count', 'avg_magnitude', 'max_magnitude'],
            color_continuous_scale='Reds',
            title=f"Global Earthquake Risk Map - {metric.replace('_', ' ').title()}"
        )
        
        fig.update_geos(
            showframe=False,
            showcoastlines=True,
            coastlinecolor='darkblue',
            projection_type='natural earth'
        )
    else:
        # Fallback to simple choropleth
        fig = px.choropleth(
            risk_data,
            locations='country',
            locationmode='country names',
            color='value',
            hover_name='country',
            hover_data=['count', 'avg_magnitude', 'max_magnitude'],
            color_continuous_scale='Reds',
            title=f"Global Earthquake Risk Map - {metric.replace('_', ' ').title()}"
        )
        
        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            )
        )
    
    # Update layout
    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig