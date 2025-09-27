import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from keyboards.inline import back_to_menu_kb
from texts import IMAGES

router = Router(name=__name__)
log = logging.getLogger(__name__)


async def _send_instruction_text_then_photos(
    callback: CallbackQuery,
    text_in_button: str,
) -> None:
    for item in IMAGES.get(text_in_button):
        text = item.get("text", "")
        src = item.get("src", "")
        src2 = item.get("src2", "")
        caption = item.get("caption", "")
        try:
            if text:
                await callback.message.answer(text=text, disable_notification=True)
            if src and not src2:
                await callback.message.answer_photo(
                    FSInputFile(src), caption=caption, disable_notification=True
                )
            if src and src2:
                media = [
                    InputMediaPhoto(media=FSInputFile(src), caption=caption),
                    InputMediaPhoto(media=FSInputFile(src2)),
                ]

                await callback.message.answer_media_group(
                    media=media, disable_notification=True
                )
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
