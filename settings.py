import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')
LIVE_URL = f'http://api.openweathermap.org/data/2.5/weather?lat=35.88&lon=76.51&APPID={API_KEY}&units=metric'
WEATHER_URL = f'http://api.openweathermap.org/data/2.5/forecast?lat=35.88&lon=76.51&APPID={API_KEY}&units=metric'