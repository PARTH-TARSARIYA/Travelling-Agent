import json
from langchain.tools import tool

@tool
def search_flights(destination: str) -> str:
    """
    Search cheapest available flights for a destination city.
    """

    try:
        with open('Data/flights.json', 'r') as f:
            flights = json.load(f)

        result = []

        for flight in flights:

            if flight['to'].lower() == destination.lower():
                result.append(flight)

        if not result:
            return f'Flights not found for {destination}'

        return json.dumps(result, indent=2)

    except Exception as e:
        return f"ERROR: {str(e)}"