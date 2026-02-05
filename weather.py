import requests
import json
import datetime
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


today = datetime.datetime.now().replace(microsecond=0)

# get city coordinates by city name


def get_city(name):
    # Data Path to where the city data should be
    cityPath = f"queries/geodata/{name}.json"
    # If it exists load it into cityData
    if os.path.exists(cityPath):
        with open(cityPath, "r") as f:
            cityData = json.load(f)

    # If not, request for data and load it into cityData, and save in the Data Path
    # Only loads coordinates, cityData[0]
    else:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={name}&count=1&language=en&format=json"
        response = requests.get(url)
        cityData = response.json()["results"]
        with open(cityPath, "w") as f:
            json.dump(cityData, f, indent=4)

    return cityData[0]


def get_temp(city):
    city = city.lower().capitalize()
    cityData = get_city(city)
    lat, lon, timezone = cityData["latitude"], cityData["longitude"], cityData["timezone"]
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "apparent_temperature"],
        "timezone": timezone,
        "forecast_days": 1,
    }
    response = requests.get(url, params=params)
    tempData = response.json()

    return {
        "times": tempData["hourly"]["time"],
        "temp": tempData["hourly"]["temperature_2m"],
        "feels like": tempData["hourly"]["apparent_temperature"],
    }


def plot_temp_figure(city):
    tempData = get_temp(city)

    times = [
        datetime.datetime.fromisoformat(t)
        for t in tempData["times"]
    ]
    temps = tempData["temp"]
    feels_like = tempData["feels like"]
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(times, temps, label="Temperature (°C)")
    ax.plot(times, feels_like, label="Feels like (°C)", linestyle="--")

    ax.set_title(f"Hourly Temperature — {city.capitalize()}")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:00"))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))

    ax.legend()
    ax.grid(True)
    fig.autofmt_xdate()

    return fig, min(temps), max(temps)


# old function
"""
def get_current_weather(city):
    # Data Path to where the data should be
    datePath = f"queries/weatherdata/{today.strftime('%Y-%m-%d')}"
    weatherPath = f"{datePath}/{city}.json"
    # If exists just load it into weatherData
    if os.path.exists(weatherPath):
        with open(weatherPath, "r") as f:
            weatherData = json.load(f)

    # If not, have to request for data and load it into weatherData, and save in the Data Path
    else:
        url = "https://api.open-meteo.com/v1/forecast?"
        city = city.lower().capitalize()
        cityData = get_city(city)
        lat, lon = cityData["latitude"], cityData["longitude"]
        params = {
            "latitude": lat,
            "longitude": lon,
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
        f"{'Apparent Temperature:':25} {weatherData["apparent_temperature"]}")
    print(
        f"{'Relative Humidity:':<25} {weatherData["relative_humidity_2m"]}")
    print(f"{'Wind Speed:':<25} {weatherData["wind_speed_10m"]}")
    print(
        f"{'Day or Night:':<25} {'Day' if weatherData["is_day"] else 'Night'}")
"""
