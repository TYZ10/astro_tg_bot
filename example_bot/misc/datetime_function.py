from datetime import datetime


def get_day_and_hours_from_date(
        date_string: str,
        get_hour: bool = False,
        past: bool = False
):
    """Функция для получения дней/часов до какого то времени"""

    if date_string is None:
        return 0

    # Укажите дату окончания
    end_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    # Получите текущую дату и время
    now = datetime.now()

    # Вычислите разницу между текущей датой и датой окончания
    time_difference = end_date - now

    day: int
    hour: int

    # Если дата окончания еще не наступила, выведите количество дней и часов
    if time_difference.total_seconds() > 0:
        day = time_difference.days
        hour = time_difference.seconds // 3600
        if day == 0 and hour != 0:
            day = 1
    elif past:
        day = abs(time_difference.days)
        hour = abs(time_difference.seconds // 3600)
    else:
        return 0

    if get_hour:
        return hour
    else:
        return day

