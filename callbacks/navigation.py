from dash import callback, Output, Input, callback_context

@callback(
    [Output('btn-map', 'style'),
     Output('btn-scatter', 'style'),
     Output('btn-timeseries', 'style')],
    [Input('btn-map', 'n_clicks'),
     Input('btn-scatter', 'n_clicks'),
     Input('btn-timeseries', 'n_clicks')]
)
def highlight_active_button(b1, b2, b3):
    ctx = callback_context
    triggered = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'btn-map'

    def style(active): return {
        'width': '100%',
        'textAlign': 'left',
        'padding': '12px 15px',
        'marginBottom': '8px',
        'backgroundColor': '#2c3e50' if active else '#ecf0f1',
        'color': 'white' if active else '#2c3e50',
        'border': 'none',
        'borderRadius': '5px',
        'cursor': 'pointer',
        'fontSize': '14px'
    }

    return style(triggered == 'btn-map'), style(triggered == 'btn-scatter'), style(triggered == 'btn-timeseries')
