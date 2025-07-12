from dash import callback, Output, Input, callback_context
from components.global_map_section import get_global_map
from components.scatter_section import get_scatter_section
from components.timeseries_section import get_timeseries_section
from components.risk_map_section import get_risk_map
from components.country_focus_section import get_country_focus_section
import globals

button_ids = globals.button_ids
@callback(
    Output("main-plot-content", "children"),
    [Input(btn_id, "n_clicks") for btn_id in button_ids]
)
def update_main_content(*args):
    ctx = callback_context
    triggered = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'btn-map'
    data_processor = globals.data_processor  # Access the global data processor

    if triggered == "btn-scatter":
        return get_scatter_section(data_processor)
    elif triggered == "btn-timeseries":
        return get_timeseries_section(data_processor)
    elif triggered == "btn-riskmap":
        return get_risk_map(data_processor)
    elif ctx.triggered_id == "btn-country-focus":
        return get_country_focus_section()
    else:
        return get_global_map()
