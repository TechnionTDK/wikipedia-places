import requests
import constants
import utils

S = requests.Session()


def get_place_details_by_name(name: str) -> dict:
    params = {
        "q": name.replace(" ", "+"),
        "format": "json",
        "polygon": 1,
        "addressdetails": 1
    }

    place_details = S.get(url=f'{constants.NOMINATIM_API_URL}/search', params=params).json()
    return {
        'name': utils.full_address_to_displayed_address(place_details[0]['display_name']) if place_details != [] and 'display_name' in place_details[0] else "",
        'lon': float(place_details[0]['lon']) if place_details != [] and 'lon' in place_details[0] else -1,
        'lat': float(place_details[0]['lat']) if place_details != [] and 'lat' in place_details[0] else -1
    }


def get_place_details_by_coordinates(lat: float, lon: float) -> dict:
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "zoom": 18,
        "addressdetails": 1
    }

    place_details = S.get(url=f'{constants.NOMINATIM_API_URL}/reverse', params=params).json()
    return {
        'name': utils.full_address_to_displayed_address(place_details['display_name']) if place_details != [] and 'display_name' in place_details else ""
    }


def get_suggestions(pattern: str) -> dict:
    pattern = utils.filter_suggestions(pattern)
    params = {
        "q": pattern,
        "format": "json",
        "accept-language": "he"
    }

    suggestions_response = S.get(url=f'{constants.NOMINATIM_API_URL}/search', params=params).json()
    suggestions, suggestions_names = [], []
    for suggestion in suggestions_response:
        new_suggestion = {
            'name': utils.full_address_to_displayed_address(suggestion['display_name']) if suggestion != {} and 'display_name' in suggestion else "",
            'lon': float(suggestion['lon']) if suggestion != {} and 'lon' in suggestion else -1,
            'lat': float(suggestion['lat']) if suggestion != {} and 'lat' in suggestion else -1,
            'icon': suggestion['icon'] if suggestion != {} and 'icon' in suggestion else ""
        }

        if new_suggestion['name'] not in suggestions_names:
            suggestions.append(new_suggestion)
            suggestions_names.append(new_suggestion['name'])

    return {"suggestions": suggestions}
