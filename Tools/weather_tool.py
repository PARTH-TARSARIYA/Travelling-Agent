import openmeteo_requests
import requests
import requests_cache

from retry_requests import retry
from langchain.tools import tool


# Setup Open-Meteo client
cache_session = requests_cache.CachedSession(
    '.cache',
    expire_after=3600
)

retry_session = retry(
    cache_session,
    retries=5,
    backoff_factor=0.2
)

openmeteo = openmeteo_requests.Client(
    session=retry_session
)


@tool
def get_weather(city: str) -> str:
    """
    Get current weather information for a city.
    Use this when user asks about weather,
    temperature, humidity, wind speed,
    rain, or climate conditions.
    """

    try:

        # STEP 1 — Convert city to coordinates
        geo_url = (
            f"https://geocoding-api.open-meteo.com/v1/search"
            f"?name={city}&count=1"
        )

        geo_response = requests.get(
            geo_url,
            timeout=10
        )

        geo_data = geo_response.json()

        if (
            "results" not in geo_data
            or len(geo_data["results"]) == 0
        ):
            return f"Could not find coordinates for {city}"

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        # STEP 2 — Fetch weather data
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "wind_speed_10m"
            ]
        }

        responses = openmeteo.weather_api(
            url,
            params=params
        )

        response = responses[0]

        current = response.Current()

        temperature = current.Variables(0).Value()
        humidity = current.Variables(1).Value()
        apparent_temp = current.Variables(2).Value()
        wind_speed = current.Variables(3).Value()

        return (
            f"Current weather in {city}:\n\n"
            f"Temperature: {temperature}°C\n"
            f"Feels Like: {apparent_temp}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} km/h"
        )

    except Exception as e:
        return f"Weather API Error: {str(e)}"