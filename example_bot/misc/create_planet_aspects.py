from datetime import datetime, timedelta

import ephem
import math
import swisseph as swe


def create_aspects(date: str,
                   latitude: float,
                   longitude: float) -> dict:
    # Данные
    date = str(date)  # Дата и время рождения
    date, time = date.split()
    latitude = latitude  # Широта
    longitude = longitude  # Долгота

    # Создание наблюдателя для расчёта планет и аспектов
    observer = ephem.Observer()
    observer.date = date
    observer.lat = str(latitude)
    observer.lon = str(longitude)

    year, month, day = map(int, date.split("-"))
    hour, minute, seconds = map(int, time.split(":"))
    local_time = datetime(year, month, day, hour, minute)
    utc_time = local_time - timedelta(hours=3)
    jd_utc = \
    swe.utc_to_jd(utc_time.year, utc_time.month, utc_time.day, utc_time.hour,
                  utc_time.minute, 0, swe.GREG_CAL)[0]

    # Функция преобразования абсолютных градусов в знак и градус
    def convert_to_sign(degrees):
        signs = [
            "Овен", "Телец", "Близнецы", "Рак", "Лев",
            "Дева", "Весы", "Скорпион", "Стрелец", "Козерог",
            "Водолей", "Рыбы"
        ]
        sign_index = int(degrees // 30)  # Определяем знак
        sign_degree = degrees % 30  # Определяем градус в знаке
        return f"{signs[sign_index]} {sign_degree:.2f}°"

    # Позиции планет
    planets = {
        "Солнце": swe.SUN,
        "Луна": swe.MOON,
        "Меркурий": swe.MERCURY,
        "Венера": swe.VENUS,
        "Марс": swe.MARS,
        "Юпитер": swe.JUPITER,
        "Сатурн": swe.SATURN,
        "Уран": swe.URANUS,
        "Нептун": swe.NEPTUNE,
        "Плутон": swe.PLUTO,
    }

    planet_positions = {}
    planet_degrees = {}
    for planet_name, planet_id in planets.items():
        position, _ = swe.calc_ut(jd_utc, planet_id)
        ecliptic_longitude = position[0] % 360
        zodiac = convert_to_sign(ecliptic_longitude)
        planet_positions[planet_name] = zodiac
        planet_degrees[planet_name] = ecliptic_longitude

    # Вычисление аспектов
    def calculate_aspects(planets):
        aspects = []
        aspect_orb = {
            0: "Соединение",
            60: "Секстиль",
            90: "Квадрат",
            120: "Тригон",
            180: "Оппозиция"
        }
        planet_list = list(planets.items())
        for i, (p1_name, p1_pos) in enumerate(planet_list):
            for p2_name, p2_pos in planet_list[i + 1:]:
                diff = abs(p1_pos - p2_pos)
                if diff > 180:
                    diff = 360 - diff  # Нормализация аспекта
                for aspect_angle, aspect_name in aspect_orb.items():
                    if abs(diff - aspect_angle) <= 5:  # Орбис 5 градусов
                        aspects.append({
                            "планета_1": p1_name,
                            "планета_2": p2_name,
                            "аспект": aspect_name,
                            "градусы": round(diff, 2)
                        })
        return aspects

    aspects = calculate_aspects(planet_degrees)
    jd = swe.julday(year, month, day, hour + minute / 60.0)
    houses, ascmc = swe.houses_ex(jd, latitude, longitude, b'P')
    ascendant = convert_to_sign(ascmc[swe.ASC])
    houses_positions = {f"{i + 1}": convert_to_sign(houses[i]) for i in
                        range(12)}

    result = {
        "асцендент": ascendant,
        "дома": houses_positions,
        "положения_планет": planet_positions,
        "аспекты": aspects
    }

    #import json
    #print(json.dumps(result, ensure_ascii=False, indent=4))
    return result



"""

example_result = {
    "асцендент": "Скорпион 22.04°",
    "дома": {
        "1": "Скорпион 22.04°",
        "2": "Стрелец 23.07°",
        "3": "Водолей 10.99°",
        "4": "Рыбы 23.93°",
        "5": "Овен 21.19°",
        "6": "Телец 9.09°",
        "7": "Телец 22.04°",
        "8": "Близнецы 23.07°",
        "9": "Лев 10.99°",
        "10": "Дева 23.93°",
        "11": "Весы 21.19°",
        "12": "Скорпион 9.09°"
    },
    "положения_планет": {
        "Солнце": "Дева 9.21°",
        "Луна": "Скорпион 25.83°",
        "Меркурий": "Дева 19.34°",
        "Венера": "Дева 11.85°",
        "Марс": "Дева 7.72°",
        "Юпитер": "Овен 27.97°",
        "Сатурн": "Стрелец 13.51°",
        "Уран": "Стрелец 22.06°",
        "Нептун": "Козерог 5.74°",
        "Плутон": "Скорпион 10.46°"
    },
    "аспекты": [
        {
            "планета_1": "Солнце",
            "планета_2": "Венера",
            "аспект": "Соединение",
            "градусы": 2.64
        },
        {
            "планета_1": "Солнце",
            "планета_2": "Марс",
            "аспект": "Соединение",
            "градусы": 1.49
        },
        {
            "планета_1": "Солнце",
            "планета_2": "Сатурн",
            "аспект": "Квадрат",
            "градусы": 94.31
        },
        {
            "планета_1": "Солнце",
            "планета_2": "Нептун",
            "аспект": "Тригон",
            "градусы": 116.53
        },
        {
            "планета_1": "Солнце",
            "планета_2": "Плутон",
            "аспект": "Секстиль",
            "градусы": 61.25
        },
        {
            "планета_1": "Меркурий",
            "планета_2": "Уран",
            "аспект": "Квадрат",
            "градусы": 92.72
        },
        {
            "планета_1": "Венера",
            "планета_2": "Марс",
            "аспект": "Соединение",
            "градусы": 4.13
        },
        {
            "планета_1": "Венера",
            "планета_2": "Сатурн",
            "аспект": "Квадрат",
            "градусы": 91.67
        },
        {
            "планета_1": "Венера",
            "планета_2": "Плутон",
            "аспект": "Секстиль",
            "градусы": 58.61
        },
        {
            "планета_1": "Марс",
            "планета_2": "Нептун",
            "аспект": "Тригон",
            "градусы": 118.02
        },
        {
            "планета_1": "Марс",
            "планета_2": "Плутон",
            "аспект": "Секстиль",
            "градусы": 62.74
        },
        {
            "планета_1": "Нептун",
            "планета_2": "Плутон",
            "аспект": "Секстиль",
            "градусы": 55.28
        }
    ]
}

"""
