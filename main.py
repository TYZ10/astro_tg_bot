import asyncio

from example_bot.main_bot import TelegramBot



bot = TelegramBot(token="7659082455:AAHdpz86IgJ8hIVuKH2MVEfeHTHMZegoxLY",
                  url_bot="https://t.me/CZcryptocash_bot")


async def main():
    await bot.start_bot()
    
    
if __name__ == "__main__":
    asyncio.run(main())