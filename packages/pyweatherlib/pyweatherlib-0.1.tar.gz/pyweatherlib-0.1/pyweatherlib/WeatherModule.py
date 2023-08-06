import requests
import os

# Get your api key from # https://home.openweathermap.org/api_keys
api_key = '&APPID=' + '54f85bac7eca8e2557da760211b208e4'


def weather_data(query):
    res = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?' + query + api_key + '&units=metric')
    return res.json()


def print_weather(result):
    print("Temperature: {}°C ".format(round(result['main']['temp'])))
    print("Wind Speed: {} m/s".format(result['wind']['speed']))
    print("Humidity: {}%".format(round(result['main']['humidity'])))
    print("Pressure: {} hPa".format(result['main']['pressure']))
    print("Description: {}".format(result['weather'][0]['description']))
    print("Weather: {}".format(result['weather'][0]['main']))


def main():
    city = input("Enter City: ")
    try:
        query = 'q=' + city
        w_data = weather_data(query)
        print_weather(w_data)
    except:
        print('City name not found...')


if __name__ == '__main__':
    main()
