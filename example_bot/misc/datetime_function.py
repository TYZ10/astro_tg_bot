from datetime import datetime, timedelta


def get_day_and_hours_from_date(
        date_string: str,
        get_hour: bool = False,
        past: bool = False
):
    """Функция для получения дней/часов до какого то времени"""

    if date_string is None:
        return 0

    # Укажите дату окончания
    try:
        end_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    except:
        end_date = date_string

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


def create_new_payments_end(payments_end):
    days_to_add = 30

    if get_day_and_hours_from_date(payments_end) == 0:
        now = datetime.now()

        new_pay_end_date = now + timedelta(days=days_to_add)
    else:
        end_date = datetime.strptime(payments_end,
                                     "%Y-%m-%d %H:%M:%S")

        new_pay_end_date = (end_date +
                            timedelta(days=days_to_add))

    return new_pay_end_date