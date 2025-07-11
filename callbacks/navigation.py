from dash import callback, Output, Input, callback_context
import globals
button_ids = globals.button_ids

def get_button_style(is_active):
    return {
        'width': '100%',
        'textAlign': 'left',
        'padding': '12px 15px',
        'marginBottom': '8px',
        'backgroundColor': '#2c3e50' if is_active else '#ecf0f1',
        'color': 'white' if is_active else '#2c3e50',
        'border': 'none',
        'borderRadius': '5px',
        'cursor': 'pointer',
        'fontSize': '14px'
    }

@callback(
    [Output(btn_id, 'style') for btn_id in button_ids],
    [Input(btn_id, 'n_clicks') for btn_id in button_ids]
)
def highlight_active_button(*_):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else button_ids[0]

    return [get_button_style(triggered_id == btn_id) for btn_id in button_ids]
