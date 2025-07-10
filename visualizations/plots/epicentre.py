import numpy as np
import plotly.graph_objects as go

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