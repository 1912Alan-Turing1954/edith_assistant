import re
import requests


def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def get_weather(location):
    url = f"https://forecast9.p.rapidapi.com/rapidapi/forecast/{location}/hourly/"

    headers = {
        "X-RapidAPI-Key": "58271e6f67msh373701dab4007fdp1dc301jsn615fd58f41b8",
        "X-RapidAPI-Host": "forecast9.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers)
    weather_data = response.json()

    return weather_data


def extract_location_from_string(input_string):
    patterns = [
        r"\bweather\s*in\s*(.+)\b",
        r"\bforecast\s*(?:on|for)\s*(.+)\b",
        r"\bweather\s*update\s*(?:on|for)\s*(.+)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, input_string, re.IGNORECASE)
        if match:
            location = match.group(1)
            location = location.strip("?.,")
            location = location.replace("please", "").strip()
            return location
    return None
