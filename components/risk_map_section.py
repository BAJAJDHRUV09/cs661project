from dash import html, dcc
from visualizations.plots.risk_map import create_global_risk_map

def get_risk_map(data_processor):
    # Create the figure
    fig = create_global_risk_map(data_processor, metric='count')

    return html.Div([
        html.Div([
            html.H3("Global Risk Map: High-Risk Zones and Fault Lines", style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'marginBottom': '10px',
                'fontWeight': 'bold'
            }),
            html.P(
                "This view highlights regions that experience frequent or strong earthquakes. "
                "Click on countries for local statistics. Fault lines and top risk zones are marked.",
                style={
                    'textAlign': 'center',
                    'fontSize': '15px',
                    'color': '#6c757d',
                    'marginBottom': '25px'
                }
            )
        ]),

        dcc.Checklist(
            id='toggle-faultlines',
            options=[{'label': 'Show Fault Lines', 'value': 'fault'}],
            value=[], # default: do NOT show fault lines
            inline=True,
            style={'textAlign': 'center', 'marginBottom': '10px'}
        ),

        dcc.Graph(
            id='global-risk-map',
            figure=fig,
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
        )
    ], style={
        'width': '100%',
        'minWidth': '1200px',
        'marginBottom': '20px',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center'
    })
