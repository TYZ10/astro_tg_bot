import ephem
import math
import swisseph as swe

# Данные
date = "1987-08-31 11:00:00"  # Дата и время рождения
latitude = 59.93428  # Широта Зеленогорска
longitude = 30.3351  # Долгота Зеленогорска

# Создание наблюдателя для расчёта планет и аспектов
observer = ephem.Observer()
observer.date = date
observer.lat = str(latitude)
observer.lon = str(longitude)


# Функция преобразования абсолютных градусов в знак и градус
def convert_to_sign(degrees):
    signs = [
        "Овен", "Телец", "Близнецы", "Рак", "Лев",
        "Дева", "Весы", "Скорпион", "Стрелец", "Козерог",
        "Водолей", "Рыбы"
    ]
    sign_index = int(degrees // 30)  # Определяем знак
    sign_degree = degrees % 30      # Определяем градус в знаке
    return f"{signs[sign_index]} {sign_degree:.2f}°"

# Позиции планет
planets = {
    "Солнце": ephem.Sun(observer),
    "Луна": ephem.Moon(observer),
    "Меркурий": ephem.Mercury(observer),
    "Венера": ephem.Venus(observer),
    "Марс": ephem.Mars(observer),
    "Юпитер": ephem.Jupiter(observer),
    "Сатурн": ephem.Saturn(observer),
    "Уран": ephem.Uranus(observer),
    "Нептун": ephem.Neptune(observer),
    "Плутон": ephem.Pluto(observer),
}

planet_positions = {}
for planet_name, planet in planets.items():
    planet.compute(observer)
    ecliptic_longitude = math.degrees(planet.ra) % 360  # Эклиптическая долгота
    zodiac = convert_to_sign(ecliptic_longitude)
    planet_positions[planet_name] = zodiac

# Вычисление аспектов
def calculate_aspects(planets):
    aspects = []
    aspect_types = {
        0: "Соединение",
        60: "Секстиль",
        90: "Квадрат",
        120: "Тригон",
        180: "Оппозиция"
    }
    planet_list = list(planets.items())
    for i, (p1_name, p1_pos) in enumerate(planet_list):
        for p2_name, p2_pos in planet_list[i + 1:]:
            diff = abs(p1_pos - p2_pos) % 360
            diff = min(diff, 360 - diff)  # Угол между планетами
            for aspect_angle, aspect_name in aspect_types.items():
                if abs(diff - aspect_angle) < 5:  # Орбис 5 градусов
                    aspects.append({
                        "планета_1": p1_name,
                        "планета_2": p2_name,
                        "аспект": aspect_name,
                        "градусы": round(diff, 2)
                    })
    return aspects

# Конвертация положений планет в градусы
planet_degrees = {name: math.degrees(planet.ra) % 360 for name, planet in planets.items()}
aspects = calculate_aspects(planet_degrees)

# Расчёт домов (система Плацидус) с использованием swisseph
year, month, day = map(int, date.split(" ")[0].split("-"))
hour, minute, second = map(int, date.split(" ")[1].split(":"))
jd = swe.julday(year, month, day, hour + minute / 60 + second / 3600)

houses, ascmc = swe.houses(jd, latitude, longitude, b'P')  # 'P' — Плацидус
ascendant_deg = ascmc[0]
ascendant = convert_to_sign(ascendant_deg)
houses_positions = {f"{i + 1}": convert_to_sign(houses[i]) for i in range(12)}

# Вывод данных
result = {
    "асцендент": ascendant,
    "дома": houses_positions,
    "положения_планет": planet_positions,
    "аспекты": aspects
}

import json
print(json.dumps(result, ensure_ascii=False, indent=4))
