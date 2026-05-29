import json
from langchain.tools import tool

@tool
def search_hotels(destination : str) -> str:
    """
    Search available hotels for a destination city.
    """
    with open('Data/hotels.json') as f:
        hotels = json.load(f)

    result = []

    for hotel in hotels:
        if hotel['city'].lower() == destination.lower():
            result.append(hotel)

    if not result:
        return f'hotels not found for {destination}'

    return json.dumps(result, indent = 2)