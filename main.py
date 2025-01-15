import asyncio

from example_bot.main_bot import TelegramBot

bot = TelegramBot()


async def main():
    pass
    # await bot.start_bot()
    
    
if __name__ == "__main__":
    asyncio.run(main())