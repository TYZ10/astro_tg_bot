from datetime import date

from example_bot.misc import generate_gpt_txt
from example_bot.Tbot import ConfigBot


async def main_get_info_gpt(config: ConfigBot, all_info, promt: str):
    promt = promt + f"\n{all_info}\n\nСегодняшняя дата: {date.today()}"

    text = await generate_gpt_txt(
        config.client_gpt,
        promt
    )
    try:
        text = text.replace('#', '').replace('*', '')
    except:
        pass

    return text
