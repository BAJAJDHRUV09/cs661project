from dash import callback, Output, Input, callback_context
from components.global_map import get_global_map
from components.scatter_section import get_scatter_section
from components.timeseries_section import get_timeseries_section
import globals

@callback(
    Output("main-plot-content", "children"),
    [Input("btn-map", "n_clicks"),
     Input("btn-scatter", "n_clicks"),
     Input("btn-timeseries", "n_clicks")]
)
def update_main_content(b1, b2, b3):
    ctx = callback_context
    triggered = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'btn-map'
    data_processor = globals.data_processor  # Access the global data processor

    if triggered == "btn-scatter":
        return get_scatter_section(data_processor)
    elif triggered == "btn-timeseries":
        return get_timeseries_section(data_processor)
    else:
        return get_global_map()
