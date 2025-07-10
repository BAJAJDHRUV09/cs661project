from dash import callback, Output, Input, State

@callback(
    [Output("sidebar", "style"),
     Output("main-content", "style")],
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "style"),
     State("main-content", "style")]
)
def toggle_sidebar(n_clicks, sidebar_style, main_style):
    if n_clicks is None:
        return sidebar_style, main_style

    if sidebar_style.get("transform") == "translateX(0px)":
        sidebar_style["transform"] = "translateX(-100%)"
        main_style["marginLeft"] = "0px"
    else:
        sidebar_style["transform"] = "translateX(0px)"
        main_style["marginLeft"] = "300px"

    return sidebar_style, main_style