import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, List
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
