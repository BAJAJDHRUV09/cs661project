from dash import html
from components.sidebar import get_sidebar

def create_layout(data_processor):
    return html.Div([
        html.Button("☰", id="sidebar-toggle", style={
            'position': 'fixed',
            'top': '20px',
            'left': '20px',
            'zIndex': 1000,
            'fontSize': '24px',
            'padding': '10px 15px',
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'border': 'none',
            'borderRadius': '5px',
            'cursor': 'pointer',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.2)'
        }),
        get_sidebar(),
        html.Div([
            html.Div(id="main-plot-content"),

            html.Div("CS661 Project - Group 15", style={
                'textAlign': 'center', 'color': '#95a5a6', 'marginTop': '30px'
            })
        ], id="main-content", style={
            'padding': '20px',
            'fontFamily': 'Arial, sans-serif',
            'backgroundColor': 'white',
            'minHeight': '100vh',
            'color': '#2c3e50'
        })
    ], id="app-container")
