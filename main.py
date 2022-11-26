import sys
import requests
from settings import LIVE_URL, WEATHER_URL
import matplotlib.pyplot as plt
from db import connect_to_db
import datetime

con, cur = connect_to_db()


def insert_current_weather():
    request = requests.get(LIVE_URL)
    if request.status_code == 200:
        data = request.json()
        date = datetime.datetime.fromtimestamp(data['dt'])
        desc = data['weather'][0]['main'].lower()
        temp, feels_like, pressure, humidity = data['main']['temp'], data['main']['feels_like'], \
                                               data['main']['pressure'], data['main']['humidity']
        cur.execute(f"""REPLACE INTO weather(
               date, temperature, description, feels_like, pressure, humidity)
               VALUES ('{date}', {temp}, '{desc}', {feels_like}, {pressure}, {humidity})""")
        con.commit()
    else:
        print("Error, unable to connect to the API")


def insert_weather_forecast():
    request = requests.get(WEATHER_URL)
    if request.status_code == 200:
        data = request.json()

        length = len(data.get('list'))
        for i in range(length):
            temp = data['list'][i]['main']['temp']
            date = data['list'][i]['dt_txt'][5:]
            cur.execute(f"""
            INSERT INTO forecast (date, temperature)
            VALUES ('{date}', {temp})
            ON CONFLICT(date) DO UPDATE SET temperature = {temp};""")
        con.commit()
    else:
        print("Error, unable to connect to the API")


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
        while True:
            try:
                user_choice = int(
                    input(
                        "For accurate weather data, select 1, if you want a 5-day weather forecast, select 2, if you want to leave select 0: "))
                if user_choice == 0:
                    sys.exit()
                if user_choice not in (1, 2):
                    raise ValueError

                break
            except ValueError:
                print("Please input only 1, 2 or 0")

        if user_choice == 1:
            show_current_weather()

        elif user_choice == 2:
            temp, date = get_weather_forecast()
            draw_weather_forecast(temp, date)


insert_current_weather()
insert_weather_forecast()
select_mode()
