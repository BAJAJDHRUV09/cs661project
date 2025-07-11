import plotly.express as px
import plotly.graph_objects as go
from ..geo_utils import get_world_geojson, get_fault_lines_geojson, get_all_country_centroids
from typing import Optional

def create_global_risk_map(data_processor, metric: str = 'count', top_n: int = 20, show_fault_lines: bool = False) -> go.Figure:
    """
    Enhanced global risk map showing earthquake activity by country, fault lines,
    and labeled high-risk zones.
    """

    # Fetch risk data
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

    # Load world boundaries
    geojson_data = get_world_geojson()

    # Base choropleth (with or without custom geojson)
    if geojson_data:
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

    # Overlay Fault Lines 
    fault_geojson = get_fault_lines_geojson()
    if show_fault_lines and fault_geojson:
        for feature in fault_geojson['features']:
            geometry = feature['geometry']
            coords = geometry['coordinates']

            if geometry['type'] == 'LineString':
                lons, lats = zip(*coords)  # unpack as lon, lat
                fig.add_trace(go.Scattergeo(
                    lon=lons,
                    lat=lats,
                    mode='lines',
                    line=dict(color='black', width=1.5, dash = 'dot'),
                    name='Fault Line',
                    hoverinfo='skip'
                ))

            elif geometry['type'] == 'MultiLineString':
                for line in coords:
                    lons, lats = zip(*line)
                    fig.add_trace(go.Scattergeo(
                        lon=lons,
                        lat=lats,
                        mode='lines',
                        line=dict(color='black', width=1),
                        name='Fault Line',
                        hoverinfo='skip',
                        showlegend=False
                    ))


    # Annotate High-Risk Countries (top N)
    top_countries = risk_data.nlargest(top_n, 'value')
    centroids = get_all_country_centroids()

    for _, row in top_countries.iterrows():
         centroid = centroids.get(row['country'])
         if centroid:
            fig.add_trace(go.Scattergeo(
                lon=[centroid[1]],
                lat=[centroid[0]],
                text=[f"{row['country']}<br>{metric.title()}: {row['value']:.2f}"],
                mode='text',
                showlegend=False,
                textfont=dict(color="black", size=10)
            ))

    # Final layout cleanup
    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    return fig
