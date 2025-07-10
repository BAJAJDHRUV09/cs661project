import requests

def get_world_geojson():
    """Get world GeoJSON data for country boundaries."""
    try:
        url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching GeoJSON: {e}")
        return None
