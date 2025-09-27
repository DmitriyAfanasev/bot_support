from typing import Final

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.filters import Command, CommandStart

from config import settings
from keyboards.inline import instructions_kb, start_kb


router = Router(name=__name__)

HELP_TEXT: Final[str] = (
    "❓ <b>Помощь</b>\n"
    "• Нажмите «Главное меню» и выберите проблему.\n"
    "• Для связи с поддержкой укажите ID аккаунта (в левом верхнем углу приложения).\n"
    "• Команды: /menu, /help, /about"
)

ABOUT_TEXT: Final[str] = (
    "ℹ️ <b>О боте</b>\n"
    "Бот показывает инструкции с картинками для частых ситуаций со станциями и пауэрбанками."
)


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer_photo(
        photo=FSInputFile("images/start.jpg"),
        caption="👋 Привет! Это бот-помощник.\n\nВы можете открыть инструкции через кнопки ниже:",
        reply_markup=start_kb(),
    )


@router.callback_query(F.data == "to_menu")
async def to_start(callback: CallbackQuery) -> None:
    await callback.message.answer("Команды:\n", reply_markup=start_kb())
    await callback.answer()


@router.callback_query(F.data == "to_commands")
async def to_main_menu(callback: CallbackQuery) -> None:
    await callback.message.answer(
        "📋 Самые популярные проблемы:", reply_markup=instructions_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "to_help")
async def to_help(callback: CallbackQuery) -> None:
    await callback.message.answer(HELP_TEXT, reply_markup=start_kb())
    await callback.answer()


@router.callback_query(F.data == "to_about")
async def to_about(callback: CallbackQuery) -> None:
    await callback.message.answer(ABOUT_TEXT, reply_markup=start_kb())
    await callback.answer()


@router.callback_query(F.data == "to_support")
async def to_sent_contact_support(callback: CallbackQuery) -> None:

    await callback.message.answer(
        text=(
            "📞 <b>Поддержка</b>\n\n"
            "Если у вас есть вопросы или предложения, вы можете связаться с нами.\n\n"
            f"👤 Ваш ID: <code>{callback.message.from_user.id}</code>"
        )
    )
    await callback.message.answer_contact(
        phone_number=settings.support_phone,
        first_name=settings.support_first_name,
        last_name=settings.support_last_name,
        vcard=f"BEGIN:VCARD\nVERSION:3.0\nFN:{settings.support_first_name} {settings.support_last_name}\nTEL:{settings.support_phone}\nEND:VCARD",
        disable_notification=True,
    )
    await callback.answer()


########################################################################


@router.message(Command("menu"))
async def to_start(message: Message) -> None:
    await message.answer("Команды:\n", reply_markup=start_kb())


@router.message(Command("commands"))
async def menu_cmd(message: Message) -> None:
    await message.answer(
        "📋 Самые популярные проблемы:", reply_markup=instructions_kb()
    )


@router.message(Command("help"))
async def help_cmd(message: Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=start_kb())


@router.message(Command("about"))
async def about_cmd(message: Message) -> None:
    await message.answer(ABOUT_TEXT, reply_markup=start_kb())


@router.message(Command("support"))
async def sent_contact_support(message: Message) -> None:
    await message.answer(
        text=(
            "📞 <b>Поддержка</b>\n\n"
            "Если у вас есть вопросы или предложения, вы можете связаться с нами.\n\n"
            f"👤 Ваш ID: <code>{message.from_user.id}</code>"
        )
    )

    await message.answer_contact(
        phone_number=settings.support_phone,
        first_name=settings.support_first_name,
        last_name=settings.support_last_name,
        vcard=f"BEGIN:VCARD\nVERSION:3.0\nFN:{settings.support_first_name} {settings.support_last_name}\nTEL:{settings.support_phone}\nEND:VCARD",
    )
