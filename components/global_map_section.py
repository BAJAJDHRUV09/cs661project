from dash import html, dcc

def get_global_map():
    return html.Div([
        dcc.Graph(
            id='global-map',
            style={
                'height': '600px',
                'width': '90%',
                'minWidth': '1000px',
                'minHeight': '500px',
                'display': 'block',
                'margin': '0 auto'
            },
            config={
                'displayModeBar': True,
                'scrollZoom': True,
                'showTips': True
            }
        ),
        html.Div([
            html.Label("Year:", style={
                'marginRight': '15px', 
                'fontWeight': 'bold',
                'fontSize': '16px',
                'color': '#2c3e50'
            }),
            dcc.Slider(
                id='year-slider',
                min=1900,
                max=2023,
                step=1,
                value=2023,
                marks={y: str(y) for y in range(1900, 2024, 20)},
                tooltip={"placement": "bottom", "always_visible": True},
                included=False
            )
        ], style={
            'width': '800px',
            'margin': '0 auto',
            'padding': '20px',
            'backgroundColor': '#f8f9fa',
            'borderRadius': '10px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'border': '1px solid #dee2e6'
        })
    ], style={
        'width': '100%',
        'minWidth': '1200px',
        'marginBottom': '20px',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center'
    })
