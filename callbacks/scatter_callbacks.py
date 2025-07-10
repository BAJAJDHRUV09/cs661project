from dash import callback, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from visualizations.plots.scatter import create_scatter_plot
import globals

data_processor = globals.data_processor  # Access the global data processor

@callback(
    Output('scatter-plot', 'figure'),
    [Input('scatter-year-range', 'value'),
     Input('scatter-country-filter', 'value')]
)

def update_scatter_plot(year_range, country_filter):
    
    # start_year, end_year = year_range if year_range else (None, None)

    return create_scatter_plot(
        data_processor,
        country_filter=country_filter,
        magnitude_range=year_range,
    )