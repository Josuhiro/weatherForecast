import sys
import requests
from settings import LIVE_URL, WEATHER_URL
import matplotlib.pyplot as plt
from db import connect_to_db
import datetime

con, cur = connect_to_db()


def insert_current_weather() -> None:
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
    cur.execute('SELECT * FROM weather')
    result = cur.fetchone()
    if not result:
        print('No data')
    else:
        print(f'\nCurrent weather for {result[1]} is {result[2]} degrees Celcius with {result[3]} sky')
        print(
            f'Feels like temperature is {result[4]} degrees Celcius, the pressure is {result[5]} hPa and humidity is {result[6]}%\n')


def show_temperatures() -> None:
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
        print(f'Min temperature on K2 is {temperatures[0]} degree Celcius')
        print(f'Max temperature on K2 is {temperatures[1]} degree Celcius')
        print(f'Average temperature on K2 is {round(temperatures[2], 2)} degree Celcius\n')


def get_weather_forecast() -> tuple[[list], [list]]:
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


def draw_weather_forecast(temp: list, date: list) -> None:
    if temp and date:
        plt.plot(date, temp, marker='o', markerfacecolor='blue', markersize=4)
        plt.xlabel('Date')
        plt.xticks(rotation=90, fontsize=7)
        plt.ylabel('Temperature')
        plt.show()
    else:
        print('No data')


def select_mode() -> None:
    while True:
        while True:
            try:
                user_choice = int(
                    input(
                        'For accurate weather data, select 1, if you want a 5-day weather forecast, select 2,'
                        ' if you want min, max and avg temperature select 3 if you want to leave select 0: '))
                if user_choice == 0:
                    sys.exit()
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
