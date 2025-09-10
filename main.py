import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand

from setup_logging import setup_logger
from config import settings

from handlers.common import router as common_router
from handlers.instructions import router as instructions_router


async def _set_bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="Начать"),
        BotCommand(command="menu", description="К меню"),
        BotCommand(command="commands", description="К инструкциям"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="about", description="Подробнее о боте"),
        BotCommand(command="support", description="Написать в поддержку"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    setup_logger()
    bot = Bot(
        token=settings.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher()
    dp.include_router(common_router)
    dp.include_router(instructions_router)

    await _set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
