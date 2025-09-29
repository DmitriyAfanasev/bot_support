from typing import Final

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.filters import Command, CommandStart

from config import settings
from keyboards.inline import instructions_kb, start_kb


router = Router(name=__name__)

HELP_TEXT: Final[str] = (
    "❓ <b>Как пользоваться ботом</b>\n\n"
    "Этот бот помогает решить частые проблемы с пауэрбанками и станциями для аренды. "
    "Следуйте этим шагам:\n"
    "1. Используйте команду <b>/instructions</b> или кнопку «Самые популярные проблемы», чтобы получить инструкции с картинками.\n"
    "2. Если проблема не решилась, напишите в техподдержку через <b>/support</b> или кнопку «Поддержка».\n"
    "3. Укажите ваш <b>ID аккаунта</b> (его можно найти в приложении для аренды пауэрбанков).\n\n"
    f"📞 Связь с поддержкой: {settings.support_url}\n"
    "📋 Другие команды: /menu, /about, /contact\n"
    "Если что-то неясно, пишите нам — мы поможем! 😊"
)

ABOUT_TEXT: Final[str] = (
    "ℹ️ <b>О боте</b>\n\n"
    "Этот бот создан, чтобы помочь вам быстро решить проблемы с арендой пауэрбанков и станциями. "
    "Он предоставляет пошаговые инструкции с картинками для таких случаев, как:\n"
    "- Пауэрбанк выпадает из станции.\n"
    "- Станция не выдаёт пауэрбанк.\n"
    "- Проблемы с депозитом или индикаторами.\n\n"
    "🔧 Используйте <b>/instructions</b>, чтобы найти нужную инструкцию.\n"
    f"📞 Не нашли ответ? Напишите в техподдержку: {settings.support_url}\n"
    "Бот работает 24/7, чтобы вы могли арендовать пауэрбанки без лишних хлопот! 🚀"
)


async def send_response(
    obj: Message | CallbackQuery,
    text: str,
    reply_markup=None,
) -> None:
    """Отправляет ответ для Message или CallbackQuery."""
    if isinstance(obj, Message):
        await obj.answer(text, reply_markup=reply_markup, parse_mode="HTML")
    else:  # CallbackQuery
        await obj.message.answer(text, reply_markup=reply_markup, parse_mode="HTML")
        await obj.answer()


def get_support_info() -> dict[str, str]:
    """Возвращает данные для контакта техподдержки, проверяя настройки."""
    return {
        "phone_number": settings.support_contact_phone,
        "first_name": settings.support_contact_first_name,
        "last_name": settings.support_contact_last_name,
        "vcard": (
            f"BEGIN:VCARD\nVERSION:3.0\n"
            f"FN:{settings.support_contact_first_name} {settings.support_contact_last_name or ''}\n"
            f"TEL:{settings.support_contact_phone}\n"
            f"URL:{settings.support_url}\n"
            f"END:VCARD"
        ),
    }


async def send_support_contact(obj: Message | CallbackQuery) -> None:
    """Отправляет контакт техподдержки с ID пользователя и инструкциями."""
    user_id = obj.from_user.id if isinstance(obj, Message) else obj.message.from_user.id
    contact_kwargs = get_support_info()

    support_text = (
        f"👤 Ваш ID в Telegram: <code>{user_id}</code>\n\n"
        f"📞 <b>Связь с техподдержкой</b>\n"
        f"Если проблема не решилась через инструкции, напишите в <a href='{settings.support_url}'>техподдержку</a>.\n"
        f"Укажите ваш ID и подробно опишите проблему, чтобы мы могли помочь быстрее.\n\n"
        f"📱 Альтернативно, звоните: {settings.support_contact_phone}"
    )

    await send_response(obj, text=support_text, reply_markup=start_kb())

    if isinstance(obj, Message):
        await obj.answer_contact(**contact_kwargs)
    else:
        await obj.message.answer_contact(**contact_kwargs, disable_notification=True)


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    """Обработчик команды /start: приветствие с меню."""
    await message.answer(
        text="👋 Привет! Это бот-помощник.\n\nВы можете открыть инструкции через кнопки ниже:",
        reply_markup=start_kb(),
        parse_mode="HTML",
    )


@router.message(Command("menu"))
@router.callback_query(F.data == "to_menu")
async def handle_menu(obj: Message | CallbackQuery) -> None:
    """Обработчик команды /menu и callback to_menu."""
    await send_response(obj, "📖 Основное меню\n", reply_markup=start_kb())


@router.message(Command("instructions"))
@router.callback_query(F.data == "to_instructions")
async def handle_commands(obj: Message | CallbackQuery) -> None:
    """Обработчик команды /instructions и callback to_instructions."""
    await send_response(
        obj, "📋 Самые популярные проблемы", reply_markup=instructions_kb()
    )


@router.message(Command("help"))
@router.callback_query(F.data == "to_help")
async def handle_help(obj: Message | CallbackQuery) -> None:
    """Обработчик команды /help и callback to_help."""
    await send_response(obj, HELP_TEXT, reply_markup=start_kb())


@router.message(Command("about"))
@router.callback_query(F.data == "to_about")
async def handle_about(obj: Message | CallbackQuery) -> None:
    """Обработчик команды /about и callback to_about."""
    await send_response(obj, ABOUT_TEXT, reply_markup=start_kb())


@router.message(Command("contact"))
@router.callback_query(F.data == "to_contact")
async def handle_contact(obj: Message | CallbackQuery) -> None:
    """Обработчик команды /contact и callback to_contact."""
    await send_support_contact(obj)


@router.message(Command("support"))
async def handle_support(msg: Message) -> None:
    """Обработчик команды /support: ссылка на техподдержку."""
    await msg.answer(
        text=f"⛑ Написать в техподдержку 👇\n\n<a href='{settings.support_url}'>Техподдержка</a>",
        parse_mode="HTML",
        reply_markup=start_kb(),
    )
