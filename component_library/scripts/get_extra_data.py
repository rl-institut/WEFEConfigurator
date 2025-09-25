## This script provides extra site-specfic data

#TODO fetch lat, lon from WEFEDemand Survey Data

#TODO get population from WEFEDemand Survey Data


# Elevation data from lat lon

import requests

def get_elevation(lat, lon):
    # Try Open-Meteo first
    try:
        om_url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
        om_response = requests.get(om_url, timeout=5)
        om_response.raise_for_status()
        elevation = om_response.json().get("elevation", [None])[0]
        if elevation is not None:
            return {
                "source": "Open-Meteo",
                "elevation_m": elevation
            }
    except Exception as e:
        print(f"Open-Meteo failed: {e}")

    # Fallback to Open Topo Data
    try:
        ot_url = f"https://api.opentopodata.org/v1/srtm90m?locations={lat},{lon}"
        ot_response = requests.get(ot_url, timeout=5)
        ot_response.raise_for_status()
        result = ot_response.json().get("results", [{}])[0]
        elevation = result.get("elevation")
        if elevation is not None:
            return {
                "source": "Open Topo Data",
                "elevation_m": elevation
            }
    except Exception as e:
        print(f"Open Topo Data failed: {e}")

    return {
        "source": None,
        "elevation_m": None,
        "error": "Both APIs failed"
    }


# example usage
result = get_elevation(49.34808212250057, 12.38701975049237)
print(f"Elevation: {result['elevation_m']} meters (source: {result['source']})")
