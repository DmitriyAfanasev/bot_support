from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup

from config import PATH_TO_IMAGES
from keyboards.inline import kb_by_support


@dataclass(eq=False, repr=False)
class InstructionStep:
    """Класс для хранения шагов инструкций."""

    text: str | None = None
    image_paths: list[str] | None = None
    caption: str | None = None
    keyboard: InlineKeyboardMarkup | None = None

    def __post_init__(self) -> None:
        self.image_paths = self.image_paths or []
        # if self.keyboard is not None and self.caption:
        #     self.caption += "\nваш ID аккаунта (в левом верхнем углу приложения)."


ERROR_INSTRUCTIONS = {
    "powerbank_falls_out": [
        InstructionStep(
            text=(
                "Если Ваш пауэрбанк выпадает после того как Вы его вставили, скорее всего наблюдается перебои в мобильной связи. "
                "Заказ будет завершен, как только появится мобильная сеть, а Ваш депозит будет разморожен. .\n\n"
                "Чтобы вернуть пауэрбанк:"
            ),
            image_paths=[f"{PATH_TO_IMAGES}/instruct1.1.JPG"],
            caption="Выключите станцию чёрным тумблером сзади.",
        ),
        InstructionStep(text="Вставьте пауэрбанк в выключенную станцию."),
        InstructionStep(
            image_paths=[f"{PATH_TO_IMAGES}/instruct1.3.JPG"],
            caption="Проверьте, чтобы заряд не вышел из станции и все индикаторы начали гореть разными цветами.",
        ),
    ],
    "powerbank_not_issued": [
        InstructionStep(
            image_paths=[f"{PATH_TO_IMAGES}/instruct2.JPG"],
            caption="Отсканируйте QR код еще раз, деньги списаны не будут, а заряд должен выйти.",
        ),
        InstructionStep(
            text=(
                "Если заряд всё же не был выдан напишите в телеграм аккаунт поддержки(не бота!) "
                "Ваш ID аккаунта, который находится в левом верхнем углу приложения."
            )
        ),
    ],
    "station_offline": [
        InstructionStep(
            image_paths=[
                f"{PATH_TO_IMAGES}/instruct3.0.JPG",
                f"{PATH_TO_IMAGES}/instruct3.1.JPG",
            ],
            caption=(
                "Если Вам высвечивается данная надпись значит станция не онлайн. Если в городе нет перебоев с мобильной связью, "
                "напишите, пожалуйста, в телеграм канал поддержки(не бота!) серийный номер станции или название заведения в котором она находится."
            ),
        ),
    ],
    "deposit_not_unfrozen": [
        InstructionStep(
            image_paths=[f"{PATH_TO_IMAGES}/instruct4.JPG"],
            caption=(
                "Если в городе нет перебоев с мобильным интернетом и Ваш депозит не разморожен "
                "напишите в телеграмм аккаунт поддержки(не бота!) Ваш ID аккаунта с описанием проблемы"
            ),
        ),
    ],
    "no_indicator": [
        InstructionStep(
            image_paths=[f"{PATH_TO_IMAGES}/instruct5.JPG"],
            caption="Пауэрбанк без цветного индикатора — напишите в техподдержку ваш ID и описание.",
        ),
    ],
    "other_issues": [
        InstructionStep(
            text="Если случай не из списка — напишите в техподдержку ваш ID и описание проблемы.",
            keyboard=kb_by_support(),
        ),
    ],
}
