from dash import callback, Output, Input
from visualizations.plots.risk_map import create_global_risk_map
import globals

data_processor = globals.data_processor  # Use global DataProcessor

@callback(
    Output('global-risk-map', 'figure'),
    Input('toggle-faultlines', 'value')
)
def update_risk_map(selected_options):
    show_fault_lines = 'fault' in selected_options if selected_options else False
    return create_global_risk_map(data_processor, metric='count', show_fault_lines=show_fault_lines)
