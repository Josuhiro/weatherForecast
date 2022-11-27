import os
import signal
import threading
import requests
from settings import LIVE_URL, WEATHER_URL
import matplotlib.pyplot as plt
from db import connect_to_db
import datetime
from typing import Tuple, List
con, cur = connect_to_db()


def insert_current_weather() -> None:
    """
    When starting the program and after every 11 minutes inserts the current weather information from the API into the database in the weather table.
    :return: None
    """
    threading.Timer(660, insert_current_weather).start()
    request = requests.get(LIVE_URL)
    if request.status_code == 200:
        data = request.json()
        date = datetime.datetime.fromtimestamp(data['dt'])
        desc = data['weather'][0]['main'].lower()
        temp, feels_like, pressure, humidity = data['main']['temp'], data['main']['feels_like'], \
                                               data['main']['pressure'], data['main']['humidity']
        cur.execute(f"""REPLACE INTO weather(
               id, date, temperature, description, feels_like, pressure, humidity)
               VALUES (1, '{date}', {temp}, '{desc}', {feels_like}, {pressure}, {humidity});""")
        con.commit()
    else:
        print('Error, unable to connect to the API')


def insert_weather_forecast() -> None:
    """
    When starting the program and after every 30 minutes inserts forecast information from the API into the database in the forecast table.
    :return: None
    """
    threading.Timer(1800, insert_weather_forecast).start()
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
        print('Error, unable to connect to the API')


def show_current_weather() -> None:
    """
    Displays information about the current weather from the database.
    :return: None
    """
    cur.execute('SELECT * FROM weather')
    result = cur.fetchone()
    if not result:
        print('No data')
    else:
        print(f'\nCurrent weather for {result[1]} is {result[2]} degrees Celsius with {result[3]} sky')
        print(
            f'Feels like temperature is {result[4]} degrees Celsius, the pressure is {result[5]} hPa and humidity is {result[6]}%\n')


def show_temperatures() -> None:
    """
    Displays information about the minimum, maximum and average temperature since the beginning of data storage from the database.
    :return: None
    """
    cur.execute('SELECT MIN(temperature), MAX(temperature), AVG(temperature) FROM forecast;')
    temperatures = cur.fetchone()
    cur.execute('SELECT date FROM forecast LIMIT 1;')
    date_start = cur.fetchone()
    cur.execute('SELECT date FROM forecast ORDER BY rowid DESC LIMIT 1;')
    date_end = cur.fetchone()
    if not temperatures:
        print('No data')
    else:
        print(f'\nData are from {date_start[0]} to {date_end[0]}')
        print(f'Min temperature on K2 is {temperatures[0]} degree Celsius')
        print(f'Max temperature on K2 is {temperatures[1]} degree Celsius')
        print(f'Average temperature on K2 is {round(temperatures[2], 2)} degree Celsius\n')


def get_weather_forecast() -> Tuple[List, List]:
    """
    Retrieves dates and temperatures from the databases from the forecast table.
    :return: `Tuple`[`List`, `List`]
    Tuple contains list of dates and list of temperatures
    """
    temp = []
    date = []
    cur.execute('SELECT rowid, date, temperature FROM forecast ORDER BY rowid DESC LIMIT 39;')
    result = cur.fetchall()
    if not result:
        return temp, date
    else:
        for i in range(len(result)):
            date.append(result[i][1])
            temp.append(result[i][2])
        return temp[::-1], date[::-1]


def draw_weather_forecast(temp: List, date: List) -> None:
    """
    Draws a graph of the weather forecast for 5 days.
    :param temp: temperature list
    :param date: date list
    :return: None
    """
    if temp and date:
        plt.plot(date, temp, marker='o', markerfacecolor='blue', markersize=4)
        plt.xlabel('Date')
        plt.xticks(rotation=90, fontsize=7)
        plt.ylabel('Temperature')
        plt.show()
    else:
        print('No data')


def select_mode() -> None:
    """
    Allows to choose between showing the current temperature, a graph of temperatures and minimum, maximum and average temperatures
    :return: None
    """
    while True:
        while True:
            try:
                user_choice = int(
                    input(
                        'For accurate weather data, select 1, if you want a 5-day weather forecast, select 2,'
                        ' if you want min, max and avg temperature select 3 if you want to leave select 0: '))
                if user_choice == 0:
                    os.kill(os.getpid(), signal.SIGTERM)
                if user_choice not in (1, 2, 3):
                    raise ValueError
                break
            except ValueError:
                print('Please input only 1, 2, 3 or 0')
        if user_choice == 1:
            show_current_weather()

        elif user_choice == 2:
            temp, date = get_weather_forecast()
            draw_weather_forecast(temp, date)
        elif user_choice == 3:
            show_temperatures()


insert_current_weather()
insert_weather_forecast()
select_mode()
