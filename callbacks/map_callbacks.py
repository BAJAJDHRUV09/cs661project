from dash import callback, Output, Input
from visualizations.plots.world_map import create_global_earthquake_map
import globals

data_processor = globals.data_processor  # Access the global data processor

@callback(
    Output('global-map', 'figure'),
    Input('year-slider', 'value')
)
def update_map(year):
    return create_global_earthquake_map(data_processor, selected_year=year)
