import logging
from functools import lru_cache

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import back_to_menu_kb
from texts import INSTRUCTIONS, IMAGES
from photo_cache import PhotoCache

cache = PhotoCache("data/photo_cache.json")

router = Router(name=__name__)
log = logging.getLogger(__name__)


@router.startup()
async def _load_cache() -> None:
    await cache.load()


@lru_cache
async def _load_instructions(key: str) -> str:
    return INSTRUCTIONS.get(key, "Инструкция не найдена.")


async def _send_instruction_text_then_photos(callback: CallbackQuery, key: str) -> None:

    text = await _load_instructions(key)
    await callback.message.answer(text)

    for item in IMAGES.get(key, []):
        src = item["src"]
        caption = item.get("caption", "")

        media = await cache.resolve(src)
        try:
            msg = await callback.message.answer_photo(media, caption=caption)
            await cache.remember_from_message(src, msg)
        except Exception as e:
            log.exception("Failed to send photo: %s | Error: %s", src, e)

    await callback.message.answer(
        text="Что делаем дальше?  ⬇️", reply_markup=back_to_menu_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "error1")
async def error1_handler(callback: CallbackQuery):
    await _send_instruction_text_then_photos(callback, "error1")


@router.callback_query(F.data == "error2")
async def error2_handler(callback: CallbackQuery):
    await _send_instruction_text_then_photos(callback, "error2")


@router.callback_query(F.data == "error3")
async def error3_handler(callback: CallbackQuery):
    await _send_instruction_text_then_photos(callback, "error3")


@router.callback_query(F.data == "error4")
async def error4_handler(callback: CallbackQuery):
    await _send_instruction_text_then_photos(callback, "error4")


@router.callback_query(F.data == "error5")
async def error5_handler(callback: CallbackQuery):
    await _send_instruction_text_then_photos(callback, "error5")


@router.callback_query(F.data == "error6")
async def error6_handler(callback: CallbackQuery):
    await _send_instruction_text_then_photos(callback, "error6")
