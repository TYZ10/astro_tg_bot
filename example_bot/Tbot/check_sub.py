from aiogram import Bot
from example_bot.Config_bot import ConfigBot


async def check_sub(bot: Bot, config: ConfigBot, user_id: int) -> bool:
    """
    Проверяет подписку на канал, если не получилось проверить возвращает True,
    Если пользователь подписан на канал, возвращает True иначе False

    :param bot: aiogram.Bot
    :param config: ConfigBot
    :param user_id: Айди пользователя
    :return: True если подписан, False если не подписан
    """
    try:
        user_channel_status = await bot.get_chat_member(
            chat_id=config.CHANEL_ID,
            user_id=user_id
        )

        if user_channel_status.status != 'left':
           return True
        else:
           return False
    except Exception as error:
        print(error)
        return True
