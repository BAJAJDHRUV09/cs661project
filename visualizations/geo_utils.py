import os
import requests
import json 
from shapely.geometry import shape

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

# Fault line data sourced from the United States Geological Survey (USGS):
# https://github.com/fraxen/tectonicplates (Public domain)
def get_fault_lines_geojson(path: str = "data/fault_lines.geojson"): 
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading fault lines: {e}")
        return None

def get_all_country_centroids() -> dict:
    """
    Returns a dictionary of { country_name: (lat, lon) } using the world GeoJSON.
    """
    geojson = get_world_geojson()
    centroids = {}

    for feature in geojson['features']:
        country_name = feature['properties'].get('name')
        geometry = feature['geometry']
        if country_name and geometry:
            try:
                geom_shape = shape(geometry)
                centroid = geom_shape.centroid
                centroids[country_name] = (centroid.y, centroid.x)  # lat, lon
            except Exception as e:
                print(f"Failed to get centroid for {country_name}: {e}")
    
    os.makedirs("data", exist_ok=True)
    
    # Save once for future fast use
    with open("data/country_centroids.json", "w") as f:
        json.dump(centroids, f)
        
    return centroids
