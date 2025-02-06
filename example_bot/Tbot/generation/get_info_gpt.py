from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from example_bot.misc import generate_gpt_txt, create_aspects
from example_bot.Tbot import ConfigBot


async def main_get_info_gpt(config: ConfigBot, all_info, promt: str,
                            next: bool = False, next_day: bool = False):
    today = date.today()
    if next:
        today = today + relativedelta(years=1, months=1, days=1)
    if next_day:
        today = today + timedelta(days=1)

    promt = promt + f"\n{all_info}\n\nСегодняшняя дата: {today}"

    text = await generate_gpt_txt(
        config.client_gpt,
        promt
    )
    try:
        text = text.replace('#', '').replace('*', '')
    except:
        pass

    return text
