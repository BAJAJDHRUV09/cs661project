import numpy as np
import plotly.graph_objects as go

def create_epicentre_impact(data_processor,
                             earthquake_id: str,
                             radius: float = 0) -> go.Figure:
    if data_processor.processed_data is None or data_processor.processed_data.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No earthquake data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(title="Epicentre Impact Analysis", height=500)
        return fig

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
        fig.update_layout(title="Epicentre Impact Analysis", height=500)
        return fig

    eq = earthquake.iloc[0]
    lat_center = eq['Latitude']
    lon_center = eq['Longitude']
    mag = eq['mag']

    if not radius or radius == 0:
        radius = 10 ** (0.5 * mag - 1.8)

    angles = np.linspace(0, 2*np.pi, 100)

    fig = go.Figure()

    # Fancy concentric impact zones
    for scale in [1.0, 0.7, 0.4]:
        lat_circle = lat_center + (radius * scale / 111.32) * np.cos(angles)
        lon_circle = lon_center + (radius * scale / (111.32 * np.cos(np.radians(lat_center)))) * np.sin(angles)

        fig.add_trace(go.Scattermapbox(
            lat=lat_circle,
            lon=lon_circle,
            mode='lines',
            line=dict(width=0),
            fill='toself',
            fillcolor=f'rgba(255, 0, 0, {0.05 + scale * 0.1})',
            hoverinfo='skip',
            showlegend=False
        ))

    # Epicentre marker
    fig.add_trace(go.Scattermapbox(
        lat=[lat_center],
        lon=[lon_center],
        mode='markers+text',
        marker=dict(
            size=20,
            color='red',
            symbol='star',
            opacity=0.9
        ),
        name='Epicentre',
        text=["Epicentre"],
        textposition="top center",
        hoverinfo='text',
        hovertext=[f"<b>{eq['Place']}</b><br>Magnitude: {mag}<br>Depth: {eq['depth']}km<br>Time: {eq['time']}"]
    ))

    # Nearby earthquakes within ~5° (approx)
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
                colorscale='YlOrRd',
                showscale=True,
                opacity=0.75,
                colorbar=dict(title="Magnitude", titleside='top')
            ),
            name='Nearby Earthquakes',
            text=[f"{place}<br>Mag: {mag}" for place, mag in zip(nearby_data['Place'], nearby_data['mag'])],
            hoverinfo='text'
        ))

    fig.update_layout(
        mapbox_style='carto-darkmatter',
        mapbox=dict(
            center=dict(lat=lat_center, lon=lon_center),
            zoom=6
        ),
        title=dict(
            text=f"🌋 Impact Zone - {eq['Place']} (Radius: ~{int(radius)} km)",
            x=0.5,
            font=dict(size=20)
        ),
        height=600,
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#ccc",
            borderwidth=1
        )
    )

    return fig
