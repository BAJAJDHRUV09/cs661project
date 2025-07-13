from dash import Output, Input, State, callback
import pandas as pd
from visualizations.plots.country_focus import create_country_focus_view
from globals import data_processor

@callback(
    Output('country-focus-map', 'figure'),
    Input('country-focus-dropdown', 'value'),
    Input('year-mode-toggle', 'value'),
    Input('country-focus-year-slider', 'value'),
    Input('country-focus-year-range-slider', 'value')
)
def update_country_focus_map(selected_country, mode, single_year, year_range):
    # Set default start and end dates
    start_date, end_date = None, None

    if mode == 'single' and single_year:
        start_date = pd.to_datetime(f"{single_year}-01-01").tz_localize("UTC")
        end_date = pd.to_datetime(f"{single_year}-12-31").tz_localize("UTC")
    elif mode == 'range' and year_range:
        start_year, end_year = year_range
        start_date = pd.to_datetime(f"{start_year}-01-01").tz_localize("UTC")
        end_date = pd.to_datetime(f"{end_year}-12-31").tz_localize("UTC")

    # If no country is selected, still filter by date
    if not selected_country:
        return create_country_focus_view(
            data_processor=data_processor,
            country=None,  # or '' if you prefer
            start_date=start_date,
            end_date=end_date
        )

    # Otherwise, pass country and dates
    return create_country_focus_view(
        data_processor=data_processor,
        country=selected_country,
        start_date=start_date,
        end_date=end_date
    )
