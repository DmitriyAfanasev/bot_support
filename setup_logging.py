import logging
import logging.handlers
from logging.handlers import TimedRotatingFileHandler

from pathlib import Path
import sys

from config import settings


class PrefixedTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename: str, *args, **kwargs):
        # сохраняем базовую папку и имя
        self.base_path = Path(filename).resolve()
        super().__init__(filename, *args, **kwargs)

    def rotation_filename(self, default_name: str) -> str:
        """
        Telegram-style: переносим дату в начало имени файла
        default_name выглядит как ".../app.log.2025-09-10"
        """
        default = Path(default_name)
        # достаём дату (последний суффикс после .log.)
        suffix = default.suffixes[-1].lstrip(".")  # '2025-09-10'
        # собираем новое имя
        new_name = f"{suffix}_{self.base_path.name}"
        return str(self.base_path.parent / new_name)


class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[37m",  # cyan
        "INFO": "\033[36m",  # white/gray
        "WARNING": "\033[33m",  # yellow
        "ERROR": "\033[31m",  # red
        "CRITICAL": "\033[41m\033[97m",  # white on red bg
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        color = self.COLORS.get(levelname, "")
        # аккуратно подсветим только уровень
        record.levelname = f"{color}{levelname}{self.RESET}"
        try:
            return super().format(record)
        finally:
            # вернуть исходное имя уровня, чтобы не окрасить в файл
            record.levelname = levelname


def setup_logger(
    level: int = settings.logging.log_level,
    log_file: str = "logs/app.log",
    rotate_when: str = "midnight",
    backup_count: int = 14,
    *,
    size_rotation_bytes: int = 5 * 1024 * 1024,  # 5 MB
    utc_timestamps: bool = False,
) -> None:
    root = logging.getLogger()
    if getattr(root, "_configured_by_app", False):
        return

    root.setLevel(level)

    base_format = settings.logging.log_format
    datefmt = settings.logging.datefmt

    # Консоль
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(level)
    console_formatter = ColorFormatter(base_format, datefmt=datefmt)
    if utc_timestamps:
        console_formatter.converter = time.gmtime  # type: ignore
    console_handler.setFormatter(console_formatter)

    if size_rotation_bytes:
        file_handler: logging.Handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=size_rotation_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
    else:
        file_handler = PrefixedTimedRotatingFileHandler(
            log_file,
            when=rotate_when,
            backupCount=backup_count,
            encoding="utf-8",
            utc=utc_timestamps,
        )
    file_handler.setLevel(level=logging.DEBUG)
    file_formatter = logging.Formatter(base_format, datefmt=datefmt)
    if utc_timestamps:
        file_formatter.converter = time.gmtime  # type: ignore
    file_handler.setFormatter(file_formatter)

    root.addHandler(console_handler)
    root.addHandler(file_handler)
