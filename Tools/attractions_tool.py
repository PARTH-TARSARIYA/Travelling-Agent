import json
from langchain.tools import tool

@tool
def search_attractions(destination : str) -> str:
    """
    Search available attraction placeses for a destination city.
    """
    with open('Data/places.json') as f:
        places = json.load(f)
    
    result = []

    for place in places:
        if place['city'].lower() == destination.lower():
            result.append(place)

    if not result:
        return f'Attraction placeses not found for {destination}'

    return json.dumps(result, indent = 2)