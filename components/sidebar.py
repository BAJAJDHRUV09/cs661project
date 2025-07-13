from dash import html

def get_sidebar():
    return html.Div([
        html.Div([
            html.H3("Earthquake Analysis", style={'color': '#2c3e50', 'marginBottom': '20px', 'marginLeft': '60px'}),
            html.Div([
                html.H4("Select Visualization:", style={'color': '#2c3e50', 'marginBottom': '15px'}),
                html.Div([
                    html.Button("Global Map", id='btn-map', style=get_button_style(selected=True)),
                    html.Button("Depth vs Magnitude Scatter Plot", id='btn-scatter', style=get_button_style()),
                    html.Button("Time Series Analysis", id='btn-timeseries', style=get_button_style()),
                    html.Button("Global Risk Map", id='btn-riskmap', style=get_button_style()),
                    html.Button("Country Focus", id='btn-country-focus', style=get_button_style())
                ])
            ], style={'padding': '20px'})
        ], style={'padding': '20px'})
    ], id="sidebar", style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'width': '300px',
        'height': '100vh',
        'backgroundColor': 'white',
        'boxShadow': '2px 0 5px rgba(0,0,0,0.1)',
        'zIndex': 999,
        'transform': 'translateX(-100%)',
        'transition': 'transform 0.3s ease-in-out',
        'overflowY': 'auto'
    })

def get_button_style(selected=False):
    if selected:
        return {
            'width': '100%',
            'textAlign': 'left',
            'padding': '12px 15px',
            'marginBottom': '8px',
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'border': 'none',
            'borderRadius': '5px',
            'cursor': 'pointer',
            'fontSize': '14px'
        }
    else:
        return {
            'width': '100%',
            'textAlign': 'left',
            'padding': '12px 15px',
            'marginBottom': '8px',
            'backgroundColor': '#ecf0f1',
            'color': '#2c3e50',
            'border': 'none',
            'borderRadius': '5px',
            'cursor': 'pointer',
            'fontSize': '14px'
        }
