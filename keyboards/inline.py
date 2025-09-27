from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import settings


def instructions_kb() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="Заряд не вставляется в станцию", callback_data="error1"
            )
        ],
        [
            InlineKeyboardButton(
                text="QR отсканирован, деньги списаны но заряд не выдан",
                callback_data="error2",
            )
        ],
        [InlineKeyboardButton(text="Кабинет не онлайн", callback_data="error3")],
        [
            InlineKeyboardButton(
                text="Заряд вставлен в станцию но заказ не завершен",
                callback_data="error4",
            )
        ],
        [
            InlineKeyboardButton(
                text="Вставили пауэрбанк, а он не горит цветным индикатором",
                callback_data="error5",
            )
        ],
        [
            InlineKeyboardButton(
                text="Ничего из выше перечисленного", callback_data="error6"
            )
        ],
        [InlineKeyboardButton(text="Стартовое меню ◀️", callback_data="to_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb, resize_keyboard=True)


def start_kb(
    support_url: str = settings.support_url,
) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text="📋 Самые популярные проблемы", callback_data="to_commands"
            )
        ],
        [
            InlineKeyboardButton(text="❓ Помощь", callback_data="to_help"),
            InlineKeyboardButton(text="ℹ️ Подробнее", callback_data="to_about"),
        ],
        [InlineKeyboardButton(text="🛟 написать нам в телеграм", url=support_url)],
        [
            InlineKeyboardButton(
                text="📲 Получить контакты сотрудников", callback_data="to_support"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def back_to_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="К остальным инструкциям", callback_data="to_commands"
                )
            ],
            [InlineKeyboardButton(text="В основное меню", callback_data="to_menu")],
        ]
    )
