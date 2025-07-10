import plotly.express as px
import plotly.graph_objects as go
from typing import Optional
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
