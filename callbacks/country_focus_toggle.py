from dash import Output, Input, callback

@callback(
    Output('single-year-slider-container', 'style'),
    Output('year-range-slider-container', 'style'),
    Input('year-mode-toggle', 'value')
)
def toggle_slider_visibility(mode):
    if mode == 'single':
        return {'marginBottom': '20px'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'marginBottom': '20px'}
