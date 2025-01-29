from example_bot.misc import generate_gpt_txt, create_aspects
from example_bot.Tbot import ConfigBot


async def main_get_info_gpt(config: ConfigBot, all_info, promt: str):
    promt = promt + f"\n{all_info}"

    text = await generate_gpt_txt(
        config.client_gpt,
        promt
    )
    try:
        text = text.replace('#', '')
    except:
        pass

    return text
