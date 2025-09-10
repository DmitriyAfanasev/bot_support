from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import settings


def instructions_kb() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="1. Заряд не вставляется в станцию", callback_data="error1"
            )
        ],
        [
            InlineKeyboardButton(
                text="2. QR отсканирован, деньги списаны, но заряд не выдан",
                callback_data="error2",
            )
        ],
        [InlineKeyboardButton(text="3. Кабинет не онлайн", callback_data="error3")],
        [
            InlineKeyboardButton(
                text="4. Заряд вставлен, заказ не завершен", callback_data="error4"
            )
        ],
        [
            InlineKeyboardButton(
                text="5. Пауэрбанк не горит индикатором", callback_data="error5"
            )
        ],
        [
            InlineKeyboardButton(
                text="6. Ничего из выше перечисленного", callback_data="error6"
            )
        ],
        [InlineKeyboardButton(text="7. Стартовое меню ◀️", callback_data="to_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def start_kb(
    support_url: str | None = settings.support_url,
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
    ]
    if support_url:
        rows.append(
            [
                InlineKeyboardButton(
                    text="🛟 написать в телеграм",
                    url=support_url,
                )
            ],
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text="📲 Получить контакты сотрудников",
                    callback_data="to_support",
                )
            ],
        )
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
