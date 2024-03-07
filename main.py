import sqlite3
import time, os
import requests
import random
from errors import E401, E404, E429, E500504
from constants import API_KEY

"""
Техническая документация:
    + SDK должно принимать API KEY для OpenWeatherAPI при инициализации.
    + SDK должно принимать название города и возвращать информацию о погоде на текущий момент. SDK возвращает информацию о первом городе, который был найден при поиске по названию города.
    SDK должно хранить информацию о погоде о запрошенных городах и, если это актуально, возвращать сохраненное значение (погода считается актуальной, если прошло менее 10 минут).
    Для экономии памяти SDK может хранить информацию не более чем о 10 городах одновременно.
    SDK должно иметь два типа поведения: по запросу и режим опроса. В режиме по запросу SDK обновляет информацию о погоде только по запросам клиента. В режиме опроса SDK запрашивает новую информацию о погоде для всех сохраненных местоположений, чтобы обеспечить нулевую задержку при ответе на запросы клиентов. Режим SDK должен передаваться в качестве параметра при инициализации.
    Методы SDK должны выбрасывать исключение с описанием причины в случае сбоя.
    Преимущество: разработать процесс создания SDK таким образом, чтобы можно было работать с разными ключами, при этом создание двух копий объекта с одинаковым ключом невозможно. Также добавить метод для удаления объекта.
    Большое преимущество: наличие модульных тестов для методов SDK (использовать заглушки для сетевых запросов)."""

abspath = os.path.dirname(os.path.abspath(__file__))
db_name = os.path.join(abspath, "weather.db")
table_name = 'cities'
conn = sqlite3.connect(db_name)
cur = conn.cursor()

def create_table():
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS {table_name}(
    Unix_time INT,
    Name TEXT);
    """
    )
    conn.commit()
    print("DB is CREATE!")

class WeatherInCity:
    def __init__(self, api_key, city_name):
        self.api_key = api_key
        self.city_name = city_name

    def get_weather(self):
        #Проверить есть ли город в базе и подходит ли время.
        cur.execute(f"SELECT Link FROM {table_name} WHERE Link=?;", [link])




        url = f'https://api.openweathermap.org/data/2.5/weather?q={self.city_name}&appid={self.api_key}'
        r = requests.get(url)

        if r.status_code == 401:
            return E401

        elif r.status_code == 404:
            return E404

        elif r.status_code == 429:
            return E429

        elif r.status_code in [500, 502, 503, 504]:
            return E500504

        elif r.status_code == 200:
            r = r.json()
            print(r)
            weather_main = r['weather'][0]['main']
            weather_description = r['weather'][0]['description']
            temperature_temp = r['main']['temp']
            temperature_feels_like = r['main']['feels_like']
            visibility = r['visibility']
            wind_speed = r['wind']['speed']
            datetime = r['dt']
            sys_sunrise = r['sys']['sunrise']
            sys_sunset = r['sys']['sunset']
            timezone = r['timezone']
            name = r['name']

        else:
            return f"status_code = {r.status_code}"

        return {
            "weather": {
                "main": weather_main,
                "description": weather_description,
            },
            "temperature": {
                "temp": temperature_temp,
                "feels_like": temperature_feels_like,
            },
            "visibility": visibility,
            "wind": {
                "speed": wind_speed,
            },
            "datetime": datetime,
            "sys": {
                "sunrise": sys_sunrise,
                "sunset": sys_sunset,
            },
            "timezone": timezone,
            "name": name}

cities = [
        "Tokyo",
        "Delhi",
        "Shanghai",
        "São Paulo",
        "Mumbai",
        "Mexico City",
        "Beijing",
        "Osaka",
        "Cairo",
        "New York City",
        "Dhaka",
        "Karachi",
        "Buenos Aires",
        "Istanbul",
        "Chongqing",
        "Kolkata",
        "Manila",
        "Lagos",
        "Rio de Janeiro",
        "Kinshasa"
    ]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_table()

    city = random.choice(cities)
    weather_instance = WeatherInCity(API_KEY, city)
    weather_data = weather_instance.get_weather()
    print(weather_data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
