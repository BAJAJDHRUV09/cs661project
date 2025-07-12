from dash import html, dcc

def get_country_focus_section():
    return html.Div([
        html.H3("Country Focus: Local Earthquake Details", style={'color': '#2c3e50'}),

        # Country dropdown
        html.Div([
            html.Label("Select Country:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='country-focus-dropdown',
                placeholder='Select a country...',
                style={'width': '100%'}
            )
        ], style={'marginBottom': '20px'}),

        # Toggle: single year vs range
        html.Div([
            html.Label("Select Mode:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
            dcc.RadioItems(
                id='year-mode-toggle',
                options=[
                    {'label': 'Single Year', 'value': 'single'},
                    {'label': 'Year Range', 'value': 'range'}
                ],
                value='single',
                labelStyle={'display': 'inline-block', 'marginRight': '15px'}
            )
        ], style={'marginBottom': '10px'}),

        # Single Year Slider
        html.Div(id='single-year-slider-container', children=[
            html.Label("Select Year:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
            dcc.Slider(
                id='country-focus-year-slider',
                min=1900,
                max=2023,
                step=1,
                value=2023,
                marks={y: str(y) for y in range(1900, 2024, 20)},
                tooltip={"placement": "bottom", "always_visible": False}
            )
        ], style={'marginBottom': '20px'}),

        # Year RangeSlider
        html.Div(id='year-range-slider-container', children=[
            html.Label("Select Year Range:", style={'color': '#2c3e50', 'fontWeight': 'bold'}),
            dcc.RangeSlider(
                id='country-focus-year-range-slider',
                min=1900,
                max=2023,
                step=1,
                value=[2000, 2023],
                marks={1900: '1900', 1950: '1950', 2000: '2000', 2023: '2023'},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ]),

        # Graph
        dcc.Graph(id='country-focus-map', style={'height': '500px'})
    ], style={'padding': '20px'})
