from dash import Output, Input, callback
from globals import data_processor

@callback(
    Output('country-focus-dropdown', 'options'),
    Input('year-mode-toggle', 'value'),
    Input('country-focus-year-slider', 'value'),
    Input('country-focus-year-range-slider', 'value')
)
def update_country_dropdown(mode, single_year, year_range):
    df = data_processor.get_filtered_data()

    if mode == 'single' and single_year:
        df = df[df['year'] == single_year]
    elif mode == 'range' and year_range:
        start_year, end_year = year_range
        df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]

    countries = df['country'].dropna().unique()
    return [{'label': c, 'value': c} for c in sorted(countries)]
