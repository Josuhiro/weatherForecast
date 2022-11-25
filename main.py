import requests
from settings import LIVE_URL, WEATHER_URL
import matplotlib.pyplot as plt


def show_current_weather() -> None:
    request = requests.get(LIVE_URL)
    if request.status_code == 200:
        data = request.json()
        desc = data['weather'][0]['main'].lower()
        temp, feels_like, pressure, humidity = data['main']['temp'], data['main']['feels_like'], \
                                               data['main']['pressure'], data['main']['humidity']
        print(
            f'Current sky is {desc} temperature is {temp}, perceptible temperature is {feels_like} ,'
            f' the pressure is {pressure} hPa, humidity is {humidity}%')
    else:
        print("Error, unable to connect to the API")


def get_weather_forecast() -> tuple[[list], [list]]:
    temp = []
    date = []
    request = requests.get(WEATHER_URL)
    if request.status_code == 200:
        data = request.json()
        length = len(data.get('list'))
        for i in range(length):
            temp.append(data['list'][i]['main']['temp'])
            date.append(data['list'][i]['dt_txt'][5:])
        return temp, date
    else:
        print("Error, unable to connect to the API")
        return temp, date


def draw_weather_forecast(temp: list, date: list):
    if temp and date:
        plt.plot(date, temp, marker='o', markerfacecolor='blue', markersize=4)
        plt.xlabel('Date')
        plt.xticks(rotation=90, fontsize=7)
        plt.ylabel('Temperature')
        plt.show()


def select_mode() -> None:
    while True:
        try:
            user_choice = int(
                input("For accurate weather data, select 1, if you want a 5-day weather forecast, select 2: "))
            if user_choice not in (1, 2):
                raise ValueError
            break
        except ValueError:
            print("Please input only 1 or 2")

    if user_choice == 1:
        show_current_weather()

    elif user_choice == 2:
        temp, date = get_weather_forecast()
        draw_weather_forecast(temp, date)


select_mode()
