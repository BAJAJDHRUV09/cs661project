import numpy as np
import plotly.graph_objects as go
from ..geo_utils import get_world_geojson
from ..style_utils import get_magnitude_color
from typing import Optional
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
    
    # Add a background layer to ensure complete coverage
    # This creates a full-world rectangle to eliminate any white regions
    fig.add_trace(go.Scattergeo(
        lon=[-180, 180, 180, -180, -180],
        lat=[-90, -90, 90, 90, -90],
        mode='lines',
        line=dict(color='#282a36', width=0),
        fill='toself',
        fillcolor='#282a36',  # Dracula background
        opacity=1.0,
        showlegend=False,
        hoverinfo='skip'
    ))
    
    if geojson_data:
        # Add filled land areas to eliminate white gaps
        for feature in geojson_data['features']:
            coordinates = feature['geometry']['coordinates']
            
            if feature['geometry']['type'] == 'Polygon':
                # Single polygon - add filled area first
                lons = [coord[0] for coord in coordinates[0]]
                lats = [coord[1] for coord in coordinates[0]]
                
                # Add filled land area
                fig.add_trace(go.Scattergeo(
                    lon=lons,
                    lat=lats,
                    mode='lines',
                    line=dict(color='#34495e', width=0.8),
                    fill='toself',
                    fillcolor='#282a36',  # Dracula background color
                    opacity=0.3,
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                # Add boundary line on top
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
                    
                    # Add filled land area
                    fig.add_trace(go.Scattergeo(
                        lon=lons,
                        lat=lats,
                        mode='lines',
                        line=dict(color='#34495e', width=0.8),
                        fill='toself',
                        fillcolor='#282a36',  # Dracula background color
                        opacity=0.3,
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                    
                    # Add boundary line on top
                    fig.add_trace(go.Scattergeo(
                        lon=lons,
                        lat=lats,
                        mode='lines',
                        line=dict(color='#34495e', width=0.8),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
    
    # # Define magnitude colors with Dracula theme palette
    # def get_magnitude_color(mag):
    #     if mag < 6.0:
    #         return '#ffb86c'  # Dracula orange
    #     elif mag < 6.5:
    #         return '#ff79c6'  # Dracula pink
    #     elif mag < 7.0:
    #         return '#ff5555'  # Dracula red
    #     elif mag < 7.5:
    #         return '#bd93f9'  # Dracula purple
    #     else:
    #         return '#ff5555'  # Dracula red (brightest for highest magnitude)
    
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
            
            # Add epicentre point with minimal styling - just enough to identify location
            fig.add_trace(go.Scattergeo(
                lon=[lon_center],
                lat=[lat_center],
                mode='markers',
                marker=dict(
                    size=2,  # Very small fixed size - just to identify epicenter
                    color=color,
                    opacity=0.9,
                    line=dict(color='white', width=0.5),
                    symbol='circle'
                ),
                text=f"<b>{eq['Place']}</b><br>Magnitude: {mag}<br>Impact Radius: ~{int(radius)} km<br>Year: {eq['year']}",
                hoverinfo='text',
                showlegend=False
            ))
    
    # Add legend traces for magnitude color ranges
    legend_colors = ['#fff7bc', '#fec44f', '#fe9929', '#d7301f', '#b30000']
    legend_labels = ['< 6.0', '6.0-6.5', '6.5-7.0', '7.0-7.5', '≥ 7.5']
    
    for i, (color, label) in enumerate(zip(legend_colors, legend_labels)):
        fig.add_trace(go.Scattergeo(
            lon=[None],  # Invisible trace for legend only
            lat=[None],
            mode='markers',
            marker=dict(
                size=8,
                color=color,
                symbol='circle'
            ),
            name=f'Magnitude {label}',
            showlegend=True,
            hoverinfo='skip'
        ))
    
    # Update layout with sophisticated styling
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor='#6272a4',  # Dracula blue
            coastlinewidth=1.5,
            showland=True,
            landcolor='#282a36',  # Dracula background - ensures complete land coverage
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
            resolution=110,
            # Additional settings to ensure complete coverage
            showlakes=True,
            lakecolor='#1e1f29',  # Same as ocean
            showrivers=True,
            rivercolor='#6272a4',  # Dracula blue
            riverwidth=0.5
        ),
        height=700,  # Fixed height
        width=None,  # Auto-width to fit container
        margin=dict(l=0, r=0, t=0, b=80),  # Increased bottom margin for legend outside plot
        paper_bgcolor='#282a36',  # Dracula background
        plot_bgcolor='#282a36',  # Dracula background
        font=dict(family="Arial, sans-serif", size=12, color='#f8f8f2'),  # Dracula foreground
        # Disable autosize to prevent shrinking
        autosize=False,
        # Better hover styling
        hovermode='closest',
        # Legend styling - small and at bottom, outside plot area
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,  # Below the plot area
            xanchor="center",
            x=0.5,  # Center horizontally
            bgcolor='rgba(40, 42, 54, 0.9)',  # Semi-transparent Dracula background
            bordercolor='#6272a4',  # Dracula blue border
            borderwidth=1,
            font=dict(size=10, color='#f8f8f2'),  # Smaller font
            itemsizing='constant'  # Consistent marker sizes
        )
    )
    
    return fig