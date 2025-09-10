import json
from pathlib import Path

from aiogram.types import Message
import aiofiles


class PhotoCache:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._data: dict[str, str] = {}
        self.path.parent.mkdir(parents=True, exist_ok=True)

    async def load(self) -> None:
        """Загрузить данные из файла в self._data."""
        try:
            async with aiofiles.open(self.path, "r", encoding="utf-8") as f:
                content = await f.read()
                self._data = json.loads(content)
        except FileNotFoundError:
            self._data = {}
        except Exception:
            self._data = {}

    async def save(self) -> None:
        """Сохранить self._data в файл (через временный .tmp)."""
        tmp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        async with aiofiles.open(tmp_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(self._data, ensure_ascii=False, indent=2))
        # Атомарная замена
        tmp_path.replace(self.path)

    async def resolve(self, src: str) -> str:
        """
        Вернёт file_id, если уже известен; иначе вернёт исходный src (URL или file_id).
        Если src уже выглядит как file_id (не URL), используем его как есть.
        """
        if src in self._data:
            return self._data[src]
        if not src.startswith("http"):
            return src
        return src

    async def remember_from_message(self, src: str, message: Message) -> None:
        """
        Если отправляли по URL — извлекаем file_id из сообщения и кладём в кэш.
        """
        if not src.startswith("http"):
            return
        if not message.photo:
            return
        file_id = message.photo[-1].file_id
        self._data[src] = file_id
        await self.save()
