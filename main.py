import sqlite3
import time, os, sys
import requests
import random
from errors import E401, E404, E429, E500504
#from constants import API_KEY

"""
Техническая документация:
    + SDK должно принимать API KEY для OpenWeatherAPI при инициализации.
    + SDK должно принимать название города и возвращать информацию о погоде на текущий момент. SDK возвращает информацию о первом городе, который был найден при поиске по названию города.
    + SDK должно хранить информацию о погоде о запрошенных городах и, если это актуально, возвращать сохраненное значение (погода считается актуальной, если прошло менее 10 минут).
    + Для экономии памяти SDK может хранить информацию не более чем о 10 городах одновременно.
    + SDK должно иметь два типа поведения: по запросу и режим опроса. 
            В режиме по запросу SDK обновляет информацию о погоде только по запросам клиента. 
            В режиме опроса SDK запрашивает новую информацию о погоде для всех сохраненных местоположений, чтобы обеспечить нулевую задержку при ответе на запросы клиентов. Режим SDK должен передаваться в качестве параметра при инициализации.
    + Методы SDK должны выбрасывать исключение с описанием причины в случае сбоя.
    
    + Преимущество: разработать процесс создания SDK таким образом, чтобы можно было работать с разными ключами, при этом создание двух копий объекта с одинаковым ключом невозможно. Также добавить метод для удаления объекта.
    - Большое преимущество: наличие модульных тестов для методов SDK (использовать заглушки для сетевых запросов)."""

abspath = os.path.dirname(os.path.abspath(__file__))
db_name = os.path.join(abspath, "weather.db")
table_name = 'cities'
conn = sqlite3.connect(db_name)
cur = conn.cursor()

def create_table():
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS {table_name}(
    unix_time INT,
    weather_main TEXT,
    weather_description TEXT,
    temperature_temp REAL,
    temperature_feels_like REAL,
    visibility INT,
    wind_speed REAL,
    datetime INT,
    sys_sunrise INT,
    sys_sunset INT,
    timezone INT,
    name TEXT);
    """
    )
    conn.commit()
    print("DB is CREATE!")


def get_weather(api_key, city_name):
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    count_idx = cur.fetchone()[0]  # Получаем значение из результата запроса
    print(count_idx)

    #Проверить есть ли город в базе и подходит ли время.
    print(city_name)
    cur.execute(f"SELECT unix_time, name FROM {table_name} WHERE name=?;", (city_name,))
    count = cur.fetchall()
    print(count)
    print(len(count))
    len_c = len(count)

    time_now = time.time()

    if len_c > 0:
        timer = count[0][0]

    else:
        timer = time_now
    print(time_now, timer)

    if len_c > 0 and timer + 600 >= time_now:
        cur.execute(f"SELECT * FROM {table_name} WHERE name=?", (city_name,))
        row = cur.fetchall()[0]
        print(row)
        weather_main = row[1]
        weather_description = row[2]
        temperature_temp = row[3]
        temperature_feels_like = row[4]
        visibility = row[5]
        wind_speed = row[6]
        datetime = row[7]
        sys_sunrise = row[8]
        sys_sunset = row[9]
        timezone = row[10]
        name = row[11]

    else:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
        r = requests.get(url)

        if r.status_code == 401:
            print(f'Error {r.status_code}')
            return E401

        elif r.status_code == 404:
            print(f'Error {r.status_code}')
            return E404

        elif r.status_code == 429:
            print(f'Error {r.status_code}')
            return E429

        elif r.status_code in [500, 502, 503, 504]:
            print(f'Error {r.status_code}')
            return E500504

        elif r.status_code == 200:
            r = r.json()
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

            if timer + 600 < time_now:
                #Удалить старую строку
                cur.execute(f"DELETE FROM {table_name} WHERE name=?", (city_name,))
                print(f'Delete old data {city_name}')

            cur.execute(
                f"INSERT INTO {table_name} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                [int(time.time()),
                 weather_main,
                 weather_description,
                 temperature_temp,
                 temperature_feels_like,
                 visibility,
                 wind_speed,
                 datetime,
                 sys_sunrise,
                 sys_sunset,
                 timezone,
                 name],
            )

            if count_idx < 10:
                conn.commit()
                print(f"Commit! {city_name}")

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
        "New York",
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
    print(city)

    API_KEY = input('Введите API key: ')
    LOCK_FILE = f".lock_{API_KEY}"

    if os.path.exists(LOCK_FILE):
        print("API key is already in use. Exiting.")
        sys.exit(1)

    with open(LOCK_FILE, "w"):
        # Создаем файл блокировки
        pass

    print("1 - Информация оп одному городу.\n2 - Обновление данные по имеющимся городам.")
    mode = int(input("Выберете режим работы: "))

    if mode == 1:
        city = input('Укажите город: ')
        weather_data = get_weather(API_KEY, city)

    else:
        cur.execute(f"SELECT name FROM {table_name};")
        cities = [i[0] for i in cur.fetchall()]

        for city in cities:
            weather_data = get_weather(API_KEY, city)

    print(weather_data)

    cur.close()
    conn.close()

    os.remove(LOCK_FILE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
