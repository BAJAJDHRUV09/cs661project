import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, List
def create_scatter_plot(data_processor,
                       country_filter: Optional[str] = None,
                       magnitude_range: Optional[List[float]] = None,
                       start_year: Optional[int] = None,
                       end_year: Optional[int] = None) -> go.Figure:
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
            xaxis_title="Depth (km)",
            yaxis_title="Magnitude",
            height=500
        )
        return fig, {'shallow': 0, 'intermediate': 0, 'deep': 0, 'total': 0}
    
    # Apply magnitude range filter
    if magnitude_range:
        data = data[data['mag'].between(magnitude_range[0], magnitude_range[1])]
    
    # Apply year range filter
    if start_year:
        data = data[data['time'].dt.year >= start_year]
    if end_year:    
        data = data[data['time'].dt.year <= end_year]
    # Create scatter plot
    fig = px.scatter(
        data,
        x='depth',
        y='mag',
        color='magnitude_category',
        size='mag',
        hover_name='Place',
        hover_data=['time', 'country'],
        title="Depth vs Magnitude Relationship",
        labels={
            'depth': 'Depth (km)',
            'mag': 'Magnitude',
            'magnitude_category': 'Magnitude Category'
        }
    )
    
    # Update layout
    fig.update_layout(
        height=500,
        xaxis_title="Depth (km)",
        yaxis_title="Magnitude",
        showlegend=True
    )

    # Count depth categories
    shallow = data[data['depth'] <= 70].shape[0]
    intermediate = data[(data['depth'] > 70) & (data['depth'] <= 300)].shape[0]
    deep = data[data['depth'] > 300].shape[0]
    total = data.shape[0]

    depth_counts = {
        'shallow': shallow,
        'intermediate': intermediate,
        'deep': deep,
        'total': total
    }
    
    return fig, depth_counts

