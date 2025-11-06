"""
TO-DO:
Easy
1. ==DONE== Input city, and get current weather
2. Save queries in CSV, JSON
Intermediate
3. Plot hourly temperature
4. Show today's min/max
5. Compute averages for next 7 days
Advanced
6. Use streamlit for interactive web dashboard
"""


import requests
import json
import datetime
import os


today = datetime.datetime.now().replace(microsecond=0)


def get_coordinates(name):
    cityPath = f"queries/geodata/{name}.json"
    if os.path.exists(cityPath):
        with open(cityPath, "r") as f:
            cityData = json.load(f)
            return cityData[0]["latitude"], cityData[0]["longitude"]

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={name}&count=1&language=en&format=json"
    response = requests.get(url)
    cityData = response.json()["results"]
    with open(cityPath, "w") as f:
        json.dump(cityData, f, indent=4)

    return cityData[0]["latitude"], cityData[0]["longitude"]


def get_current_weather(city):
    datePath = f"queries/weatherdata/{today.strftime('%Y-%m-%d')}"
    weatherPath = f"{datePath}/{city}.json"
    if os.path.exists(weatherPath):
        with open(weatherPath, "r") as f:
            weatherData = json.load(f)

    else:
        url = "https://api.open-meteo.com/v1/forecast?"
        city = city.lower().capitalize()
        lat, long = get_coordinates(city)
        params = {
            "latitude": lat,
            "longitude": long,
            "current": ["temperature_2m", "apparent_temperature", "relative_humidity_2m", "wind_speed_10m", "is_day"]
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            weatherData = response.json()["current"]
        else:
            raise requests.exceptions.HTTPError(
                f"Request failed with status code {response.status_code}: {response.text}")

        if not os.path.exists(datePath):
            os.makedirs(datePath)

        with open(weatherPath, "w") as f:
            json.dump(weatherData, f, indent=4)

    print(f"{'Current Weather at: ':<25}{city}")
    print(f"{'Temperature:':<25} {weatherData["temperature_2m"]}")
    print(
        f"{'Apperent Temperature:':25} {weatherData["apparent_temperature"]}")
    print(
        f"{'Relative Humidity:':<25} {weatherData["relative_humidity_2m"]}")
    print(f"{'Wind Speed:':<25} {weatherData["wind_speed_10m"]}")
    print(
        f"{'Day or Night:':<25} {'Day' if weatherData["is_day"] else 'Night'}")


while True:
    print("===========================")
    print("1. Get current weather")
    print("2. Exit")
    userInput = int(input("Enter your choice: "))
    print("---------------------------")
    match userInput:
        case 1:
            city = input("Enter name of the city: ")
            print("---------------------------")
            get_current_weather(city)
        case 2:
            break
        case __:
            print("Incorrect input")
