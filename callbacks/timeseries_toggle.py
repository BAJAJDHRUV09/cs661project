from dash import callback, Output, Input

@callback(
    Output('single-controls', 'style'),
    Output('range-controls', 'style'),
    Input('timeseries-view-mode', 'value')
)
def toggle_timeseries_controls(mode):
    if mode == 'single':
        return {'marginBottom': '20px'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'marginBottom': '20px'}
