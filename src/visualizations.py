import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Optional, List, Dict
from datetime import datetime
import requests
import json

def get_world_geojson():
    """Get world GeoJSON data for country boundaries."""
    try:
        url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching GeoJSON: {e}")
        return None

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

def create_global_earthquake_map(data_processor, 
                                selected_year: Optional[int] = None) -> go.Figure:
    """
    Create 2D global map showing earthquake locations with impact radius circles.
    """
    # Get filtered data
    data = data_processor.get_filtered_data()
    
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No earthquake data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(height=600)
        return fig
    
    # Filter by year if specified
    if selected_year:
        data = data[data['year'] == selected_year]
    
    # Get world GeoJSON for country boundaries
    geojson_data = get_world_geojson()
    
    # Create the base map with country boundaries
    fig = go.Figure()
    
    if geojson_data:
        # Add country boundaries
        for feature in geojson_data['features']:
            coordinates = feature['geometry']['coordinates']
            
            if feature['geometry']['type'] == 'Polygon':
                # Single polygon
                lons = [coord[0] for coord in coordinates[0]]
                lats = [coord[1] for coord in coordinates[0]]
                
                fig.add_trace(go.Scattergeo(
                    lon=lons,
                    lat=lats,
                    mode='lines',
                    line=dict(color='#34495e', width=0.8),
                    showlegend=False,
                    hoverinfo='skip'
                ))
            elif feature['geometry']['type'] == 'MultiPolygon':
                # Multiple polygons
                for polygon in coordinates:
                    lons = [coord[0] for coord in polygon[0]]
                    lats = [coord[1] for coord in polygon[0]]
                    
                    fig.add_trace(go.Scattergeo(
                        lon=lons,
                        lat=lats,
                        mode='lines',
                        line=dict(color='#34495e', width=0.8),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
    
    # Define magnitude colors with Dracula theme palette
    def get_magnitude_color(mag):
        if mag < 6.0:
            return '#ffb86c'  # Dracula orange
        elif mag < 6.5:
            return '#ff79c6'  # Dracula pink
        elif mag < 7.0:
            return '#ff5555'  # Dracula red
        elif mag < 7.5:
            return '#bd93f9'  # Dracula purple
        else:
            return '#ff5555'  # Dracula red (brightest for highest magnitude)
    
    # Add earthquake points with impact radius circles
    if not data.empty:
        for _, eq in data.iterrows():
            lat_center = eq['Latitude']
            lon_center = eq['Longitude']
            mag = eq['mag']
            
            # Calculate impact radius using new formula: exp(magnitude * 0.666 + 1.6)
            radius = np.exp(mag * 0.666 + 1.6)
            
            # Generate circle coordinates with more points for smoother circles
            angles = np.linspace(0, 2*np.pi, 100)
            lat_circle = lat_center + (radius / 111.32) * np.cos(angles)
            lon_circle = lon_center + (radius / (111.32 * np.cos(np.radians(lat_center)))) * np.sin(angles)
            
            # Get color based on magnitude
            color = get_magnitude_color(mag)
            
            # Add impact circle with sophisticated styling
            fig.add_trace(go.Scattergeo(
                lon=lon_circle,
                lat=lat_circle,
                mode='lines',
                line=dict(color=color, width=2),
                fill='toself',
                fillcolor=color,
                opacity=0.2,
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Add epicentre point with sophisticated styling
            fig.add_trace(go.Scattergeo(
                lon=[lon_center],
                lat=[lat_center],
                mode='markers',
                marker=dict(
                    size=mag * 0.8 + 3,  # Much smaller size based on magnitude
                    color=color,
                    opacity=0.7,
                    line=dict(color='white', width=1),
                    symbol='circle'
                ),
                text=f"<b>{eq['Place']}</b><br>Magnitude: {mag}<br>Impact Radius: ~{int(radius)} km<br>Year: {eq['year']}",
                hoverinfo='text',
                showlegend=False
            ))
    
    # Update layout with sophisticated styling
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor='#6272a4',  # Dracula blue
            coastlinewidth=1.5,
            showland=True,
            landcolor='#282a36',  # Dracula background
            showocean=True,
            oceancolor='#1e1f29',  # Dracula darker background
            projection_type='equirectangular',
            projection_scale=1.2,  # Increased scale to prevent shrinking
            center=dict(lat=20, lon=0),
            bgcolor='#282a36',  # Dracula background
            # Fixed zoom constraints to prevent infinite shrinking
            lonaxis=dict(range=[-180, 180]),
            lataxis=dict(range=[-90, 90]),
            # Prevent excessive zooming out
            scope='world',
            showcountries=True,
            countrycolor='#6272a4',  # Dracula blue
            countrywidth=0.8,
            # Set minimum zoom level to prevent map from shrinking too much
            projection=dict(
                scale=1.2,  # Minimum scale to prevent shrinking
                rotation=dict(lon=0, lat=0, roll=0)
            ),
            # Set fixed aspect ratio and prevent shrinking
            domain=dict(x=[0, 1], y=[0, 1]),
            # Set minimum resolution to prevent excessive zoom out
            resolution=110
        ),
        height=700,  # Fixed height
        width=None,  # Auto-width to fit container
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='#282a36',  # Dracula background
        plot_bgcolor='#282a36',  # Dracula background
        font=dict(family="Arial, sans-serif", size=12, color='#f8f8f2'),  # Dracula foreground
        # Disable autosize to prevent shrinking
        autosize=False,
        # Better hover styling
        hovermode='closest'
    )
    
    return fig

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

def create_scatter_plot(data_processor,
                       country_filter: Optional[str] = None,
                       magnitude_range: Optional[List[float]] = None) -> go.Figure:
    """
    Create scatter plot showing depth vs magnitude relationship.
    """
    # Get filtered data
    data = data_processor.get_filtered_data(country=country_filter)
    
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for scatter plot",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title="Depth vs Magnitude Relationship",
            xaxis_title="Magnitude",
            yaxis_title="Depth (km)",
            height=500
        )
        return fig
    
    # Apply magnitude range filter
    if magnitude_range:
        data = data[data['mag'].between(magnitude_range[0], magnitude_range[1])]
    
    # Create scatter plot
    fig = px.scatter(
        data,
        x='mag',
        y='depth',
        color='magnitude_category',
        size='mag',
        hover_name='Place',
        hover_data=['time', 'country'],
        title="Depth vs Magnitude Relationship",
        labels={
            'mag': 'Magnitude',
            'depth': 'Depth (km)',
            'magnitude_category': 'Magnitude Category'
        }
    )
    
    # Update layout
    fig.update_layout(
        height=500,
        xaxis_title="Magnitude",
        yaxis_title="Depth (km)",
        showlegend=True
    )
    
    return fig

def create_epicentre_impact(data_processor,
                           earthquake_id: str,
                           radius: float = 0) -> go.Figure:
    """
    Create map showing earthquake epicentre and impact zone.
    If radius==0, use the empirical formula: 10**(0.5*M - 1.8)
    """
    # Get earthquake data
    if data_processor.processed_data is None or data_processor.processed_data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No earthquake data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title="Epicentre Impact Analysis",
            height=500
        )
        return fig

    # Find the specific earthquake
    earthquake = data_processor.processed_data[
        data_processor.processed_data['ID'] == earthquake_id
    ]

    if earthquake.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Earthquake not found",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title="Epicentre Impact Analysis",
            height=500
        )
        return fig

    eq = earthquake.iloc[0]
    lat_center = eq['Latitude']
    lon_center = eq['Longitude']
    mag = eq['mag']

    # Use empirical formula if radius==0
    if not radius or radius == 0:
        radius = 10 ** (0.5 * mag - 1.8)

    # Generate circle coordinates (simplified)
    angles = np.linspace(0, 2*np.pi, 100)
    lat_circle = lat_center + (radius / 111.32) * np.cos(angles)
    lon_circle = lon_center + (radius / (111.32 * np.cos(np.radians(lat_center)))) * np.sin(angles)

    # Create map
    fig = go.Figure()

    # Add impact circle
    fig.add_trace(go.Scattermapbox(
        lat=lat_circle,
        lon=lon_circle,
        mode='lines',
        line=dict(color='red', width=2),
        name=f'Impact Zone (~{int(radius)}km)',
        fill='toself',
        fillcolor='rgba(255, 0, 0, 0.1)'
    ))

    # Add epicentre
    fig.add_trace(go.Scattermapbox(
        lat=[lat_center],
        lon=[lon_center],
        mode='markers',
        marker=dict(
            size=15,
            color='red',
            symbol='star'
        ),
        name='Epicentre',
        text=[f"Magnitude: {mag}<br>Depth: {eq['depth']}km<br>Time: {eq['time']}"],
        hoverinfo='text'
    ))

    # Add nearby earthquakes
    nearby_data = data_processor.processed_data[
        ((data_processor.processed_data['Latitude'] - lat_center)**2 + 
         (data_processor.processed_data['Longitude'] - lon_center)**2)**0.5 < 5
    ].head(50)

    if not nearby_data.empty:
        fig.add_trace(go.Scattermapbox(
            lat=nearby_data['Latitude'],
            lon=nearby_data['Longitude'],
            mode='markers',
            marker=dict(
                size=nearby_data['mag'] * 2,
                color=nearby_data['mag'],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Magnitude")
            ),
            name='Nearby Earthquakes',
            text=nearby_data['Place'],
            hoverinfo='text'
        ))

    # Update layout
    fig.update_layout(
        mapbox_style='carto-positron',
        mapbox=dict(
            center=dict(lat=lat_center, lon=lon_center),
            zoom=6
        ),
        title=f"Epicentre Impact Analysis - {eq['Place']} (Felt Radius: ~{int(radius)} km)",
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    return fig

def create_magnitude_distribution(data_processor, country: Optional[str] = None) -> go.Figure:
    """
    Create histogram showing magnitude distribution.
    """
    data = data_processor.get_filtered_data(country=country)
    
    if data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for magnitude distribution",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title="Magnitude Distribution",
            xaxis_title="Magnitude",
            yaxis_title="Frequency",
            height=400
        )
        return fig
    
    # Create histogram
    fig = px.histogram(
        data,
        x='mag',
        nbins=50,
        title="Magnitude Distribution",
        labels={'mag': 'Magnitude', 'count': 'Frequency'}
    )
    
    # Update layout
    fig.update_layout(
        height=400,
        xaxis_title="Magnitude",
        yaxis_title="Frequency",
        showlegend=False
    )
    
    return fig 
