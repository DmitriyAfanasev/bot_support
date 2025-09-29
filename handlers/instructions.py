import logging

from aiogram import Router, F
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.types import CallbackQuery

from keyboards.inline import back_to_menu_kb
from instructions_data import ERROR_INSTRUCTIONS, InstructionStep

router = Router(name=__name__)
logger = logging.getLogger(__name__)


async def _send_text(callback: CallbackQuery, step: InstructionStep) -> None:
    """Отправляет текст шага (с клавиатурой или без)."""
    if not step.text:
        return
    await callback.message.answer(
        text=step.text,
        reply_markup=step.keyboard,
        disable_notification=True,
    )


async def _send_images(callback: CallbackQuery, step: InstructionStep) -> None:
    """Отправляет одно или несколько изображений."""
    images = step.image_paths
    if not images:
        return

    if len(images) == 1:
        await callback.message.answer_photo(
            photo=FSInputFile(images[0]),
            caption=step.caption or None,
            disable_notification=True,
        )
    else:
        media = [
            InputMediaPhoto(
                media=FSInputFile(path),
                caption=step.caption or None if i == 0 else None,
            )
            for i, path in enumerate(images)
        ]
        await callback.message.answer_media_group(
            media=media, disable_notification=True
        )


async def send_instruction_steps(callback: CallbackQuery) -> None:
    """Отправляет шаги инструкции (текст/фото) для указанной проблемы и возвращает меню."""
    steps = ERROR_INSTRUCTIONS.get(callback.data, [])

    for step in steps:
        await _send_text(callback, step)
        await _send_images(callback, step)

    await callback.message.answer(
        text="Что делаем дальше? ⬇️",
        reply_markup=back_to_menu_kb(),
        disable_notification=True,
    )
    await callback.answer()


INSTRUCTIONS_MAPPING = {
    "powerbank_falls_out",
    "powerbank_not_issued",
    "station_offline",
    "deposit_not_unfrozen",
    "no_indicator",
    "other_issues",
}


@router.callback_query(F.data.in_(INSTRUCTIONS_MAPPING))
async def error_handler(callback: CallbackQuery) -> None:
    """Обработчик для всех инструкций."""
    await send_instruction_steps(callback)
