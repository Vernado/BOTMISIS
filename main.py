import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import start, subjects, search, help, feedback

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    
    dp.include_routers(
        start.router,
        help.router,
        feedback.router,
        search.router,
        subjects.router,
    )

    await bot.set_my_commands([
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Help information"),
        BotCommand(command="feedback", description="Send feedback"),
    ])

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
