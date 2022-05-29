import requests
from general import constants, utils
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
        'lon': float(place_details[0]['lon']) if place_details != [] and 'lon' in place_details[0] else None,
        'lat': float(place_details[0]['lat']) if place_details != [] and 'lat' in place_details[0] else None
    }


def get_place_details_by_coordinates(lat_lon: list) -> dict:
    params = {
        "lat": lat_lon[0],
        "lon": lat_lon[1],
        "format": "json",
        "zoom": 18,
        "addressdetails": 1
    }

    place_details = S.get(url=f'{constants.NOMINATIM_API_URL}/reverse', params=params).json()
    return {
        'name': utils.full_address_to_displayed_address(place_details['display_name']) if len(place_details) >= 0 and 'display_name' in place_details else ""
    }


'''

      for (int placeIndex = 0; placeIndex < response.body.length; placeIndex++) {
        Suggestion newSuggestion = Suggestion(
            name: fullAddressToDisplayedAddress(response.body[placeIndex]["display_name"]),
            coordinates: LatLng(double.parse(response.body[placeIndex]["lat"]), double.parse(response.body[placeIndex]["lon"])),
            icon: response.body[placeIndex]["icon"]
        );

        bool isAlreadyExist = suggestions.where((Suggestion suggestion) => suggestion.name == newSuggestion.name).toList().isNotEmpty;
        if (!isAlreadyExist && newSuggestion.name.contains(pattern)) {
          suggestions.add(newSuggestion);
        }
      }
    }
'''
def get_suggestions(pattern: str) -> dict:
    params = {
        "q": utils.filter_suggestions(pattern),
        "format": "json",
        "polygon": 1,
        "addressdetails": 1
    }

    suggestions = S.get(url=f'{constants.NOMINATIM_API_URL}/search', params=params).json()
    print(suggestions)


    # return { "suggestions": suggestions}


if __name__ == '__main__':
    # print(get_place_details_by_name("כרמיאל"))
    # print(get_place_details_by_coordinates([31.79592425, 35.21198075969497]))
    get_suggestions("כרמיאל")
    # print(get_suggestions("כרמיאל"))
