# pylint: disable=missing-module-docstring

import sys
import requests

BASE_URI = "https://weather.lewagon.com"


def search_city(query):
    '''
    Look for a given city. If multiple options are returned, have the user choose between them.
    Return one city (or None)
    '''
    response = requests.get(f"{BASE_URI}/geo/1.0/direct?q={query}&limit=5").json()

    # No city (error treatment for some random/wrong city)
    if not response:
        print(f"Sorry! OpenWeather doesn't know about {query}!")
        return None

    # When the city has an unique name
    if len(response) == 1:
        return response[0]

    # When we have more than one similar name for different cities
    else:
        for i, city in enumerate(response):
            print(f"{i + 1}. {city['name']}, {city['country']}")

    index = int(input("Multiple matches found, which city did you mean?\n> ")) - 1
    return response[index]

def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    response = requests.get(f"{BASE_URI}/data/2.5/forecast?lat={lat}&lon={lon}&units=metric").json()['list']

    # list index [start:end:step], going from index 0 until index 40 (excludent) with steps of 8
    return response[0:40:8]

def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_city(query)

    if city:
        daily_forecasts = weather_forecast(city['lat'], city['lon'])

        for forecast in daily_forecasts:

            max_temp = round(forecast['main']['temp_max'])
            description = forecast['weather'][0]['main']
            date = forecast['dt_txt'][:10] #:10 to remove hours

            print(f"{date}: {description} ({max_temp}°C)")

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
