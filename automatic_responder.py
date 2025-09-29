import logging
import os

from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.types import User
from telethon.errors import SessionPasswordNeededError, FloodWaitError

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("bot.log")],
)
logger = logging.getLogger(__name__)


load_dotenv()


TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")  # integer only
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")  # string
TELEGRAM_PHONE = os.getenv("SUPPORT_CONTACT_PHONE")  # format example: +79999999999

SUPPORT_BOT = os.getenv("LINK_BOT")  # format example: @support_bot

if not all([TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE]):
    logger.error(
        "Missing required environment variables: TELEGRAM_API_ID, TELEGRAM_API_HASH, or TELEGRAM_PHONE"
    )
    raise ValueError(
        "Please set TELEGRAM_API_ID, TELEGRAM_API_HASH, and TELEGRAM_PHONE in .env"
    )


client = TelegramClient("support", int(TELEGRAM_API_ID), TELEGRAM_API_HASH)


async def get_existing_chats(current_id: int) -> bool:
    try:
        dialogs = await client.get_dialogs()
        user_ids = {
            dialog.entity.id for dialog in dialogs if isinstance(dialog.entity, User)
        }
        logger.debug("Fetched %d existing chats", len(user_ids))
        return current_id in user_ids
    except Exception as error:
        logger.exception("Failed to fetch dialogs: %s", error)


async def send_auto_response(event, user_id: int) -> None:
    """Отправляет автоответ пользователю."""
    try:
        await event.reply(
            f"Здравствуйте! 👋\n\n"
            f"Сначала проверьте инструкции в нашем боте <a href='https://t.me/{SUPPORT_BOT}'>{SUPPORT_BOT}</a>. "
            f"Он поможет быстро решить частые проблемы с пауэрбанками и станциями.\n\n"
            f"Если ответа там нет, напишите сюда подробно описав проблему. "
            f"Мы ответим вам как можно скорее! 😊",
            parse_mode="HTML",
        )
        logger.info("Sent auto-response to user %d", user_id)
    except FloodWaitError as e:
        logger.warning("Flood wait for %d seconds for user %d", e.seconds, user_id)
    except Exception as e:
        logger.exception("Failed to send auto-response to user %d: %s", user_id, e)


@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event: events.NewMessage.Event) -> None:
    sender = await event.get_sender()
    if not isinstance(sender, User):
        return
    if await get_existing_chats(sender.id):
        return
    # если нет диалога с пользователем и он не является ботом - отправляем автоответ
    await send_auto_response(event, sender.id)


async def main() -> None:
    try:
        await client.start(phone=TELEGRAM_PHONE)
        logger.info("Userbot started successfully")
        await client.run_until_disconnected()
    except SessionPasswordNeededError:
        logger.error("Two-factor authentication required. Please provide password.")
        raise
    except Exception as error:
        logger.error("Failed to start userbot: %s", error)
        raise


if __name__ == "__main__":
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Userbot stopped by user")
    except Exception as error:
        logger.error("Userbot crashed: %s", error)
