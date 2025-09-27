from telethon import TelegramClient, events
from telethon.tl.types import User
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("API_ID")  # integer only
api_hash = os.getenv("API_HASH")  # string
phone = os.getenv("PHONE")  # format example: +79999999999

client = TelegramClient("support", int(api_id), api_hash)

DB_PATH = "users.db"


def init_db():
    """Инициализация базы данных SQLite и создание таблицы, если не существует."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS replied_users (
            user_id INTEGER PRIMARY KEY
        )
    """
    )
    conn.commit()
    conn.close()


def has_user_replied(user_id) -> bool:
    """Проверка, получал ли пользователь автоответ."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM replied_users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def add_user(user_id) -> None:
    """Добавление пользователя в базу данных после отправки автоответа."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO replied_users (user_id) VALUES (?)", (user_id,)
    )
    conn.commit()
    conn.close()


@client.on(events.NewMessage(incoming=True, chats=None))
async def handler(event) -> None:
    """Обработчик новых сообщений: отвечает только новым пользователям."""
    sender = await event.get_sender()
    if isinstance(sender, User) and not has_user_replied(sender.id):
        await event.reply(
            "Здрасьте! Вот бот с инфой: @your_support_bot. Если там нет ответа, пишите мне."
        )
        add_user(sender.id)
        print(f"Отправлен автоответ пользователю {sender.id}")


async def main() -> None:
    """Основная функция: инициализация и запуск."""
    if not os.path.exists(DB_PATH):
        init_db()
    await client.start()
    print("Userbot запущен. Нажми Ctrl+C для остановки.")
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Userbot остановлен.")
