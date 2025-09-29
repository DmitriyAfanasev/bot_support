# Telegram-бот для поддержки пользователей пауэрбанков

Этот проект включает два компонента:

1. **Основа** : Telegram-бот, который помогает пользователям решать проблемы с пауэрбанками и станциями через пошаговые
   инструкции с текстом и изображениями. Использует библиотеку `aiogram`.
2. **Скрипт-автоответчик**: При запуске от имени аккаунта автоматически отвечает новым пользователям сообщением в
   котором перенаправляят их к боту для просмотра инструкций. Использует библиотеку `telethon`.

---

## Возможности

### Основной бот

- Отображает меню с командами и инструкциями для решения проблем с пауэрбанками (например, "пауэрбанк выпадает", "
  станция оффлайн").
- Предоставляет контактные данные техподдержки и Telegram ID пользователя.
- Поддерживает inline-клавиатуры для навигации.
- Основные команды:
    - `/start`: Приветственное сообщение и главное меню.
    - `/menu`: Показывает меню с доступными опциями.
    - `/instructions`: Список инструкций для возможных проблем.
    - `/help`: Информация о боте.
    - `/about`: Описание бота.
    - `/contact`: Возвращает Telegram ID пользователя и контакт поддержки.
    - `/support`: Ссылка на техподдержку.

### Скрипт-автоответчик

- Отправляет автоответ новым пользователям, с которыми нет диалога.
- Сообщение перенаправляет к основному боту для просмотра там возможных проблем.
- Пример автоответа:
  ```
  Здравствуйте! 👋
  Сначала проверьте инструкции в нашем боте @some_bot. Он поможет быстро решить частые проблемы с пауэрбанками и станциями.
  Если ответа там нет, напишите сюда подробно описав проблему. Мы ответим вам как можно скорее! 😊
  ```
- Логирует действия в `bot.log` для отладки.

---

## Требования

- **Операционная система**: Linux (рекомендуется Ubuntu) для macOS или Windows здесь инструкции немного иначе.
- **Python**: Версия 3.12 или выше.
- **Docker**: Для запуска в контейнерах (опционально).
- **Poetry**: Для управления зависимостями Python.
- **Telegram**:
    - Токен бота (`BOT_TOKEN`) от [@BotFather](https://t.me/BotFather) для основного бота.
    - API ID, API Hash и номер телефона для скрипта автоответчика (получаются
      на [my.telegram.org](https://my.telegram.org)).
    - LINK_BOT - тэг вашего бота
- **Файлы**:
    - Папка `images/` с файлами инструкций (`instruct1.1.jpg`, `instruct1.3.jpg`, и т.д.).
    - Файл `.env` с настройками (см. ниже).

---

## Установка и настройка

### 1. Клонирование репозитория

Склонируйте репозиторий на сервер:

```bash
git clone https://github.com/DmitriyAfanasev/bot_support.git
cd bot_support
```

### 2. Настройка `.env`

Создайте файл `.env` на основе `.env.template`:

```bash
cp .env.template .env
nano .env
```

Пример `.env`:

```bash
# Для бота
BOT_TOKEN=your_bot_token_from_botfather
SUPPORT_URL=https://t.me/YourSupportAccount  !!!без @
SUPPORT_CONTACT_PHONE=+79999999999
SUPPORT_CONTACT_FIRST_NAME=Игорь
SUPPORT_CONTACT_LAST_NAME=Великий

# Для автоответчика
TELEGRAM_API_ID=ваш id полученый на 
TELEGRAM_API_HASH=your_api_hash
LINK_BOT=@YourSupportAccount !!! здесь с @
```

- **Обязательные переменные**:
    - `BOT_TOKEN`: Токен основного бота, полученный через `/newbot` у [@BotFather](https://t.me/BotFather).
    - `TELEGRAM_API_ID`: Целое число, полученное на [my.telegram.org](https://my.telegram.org).
    - `TELEGRAM_API_HASH`: Строка, полученная на [my.telegram.org](https://my.telegram.org).

    - `LINK_BOT`: Имя основного бота (например, `@MisterWacky_bot`).
- **Опциональные переменные**:
    - `SUPPORT_URL`: Ссылка на техподдержку (Telegram, например, `https://t.me/@YourSupportAccount`, или сайт, например,
      `http://example.com/support`).
    - `SUPPORT_CONTACT_PHONE`, `SUPPORT_CONTACT_FIRST_NAME`, `SUPPORT_CONTACT_LAST_NAME`: Контактные данные для команды
      `/contact`.

### 3. Проверка папки `images/`

Убедитесь, что папка `images/` содержит файлы инструкций:

- `instruct1.1.jpg`
- `instruct1.3.jpg`
- `instruct2.jpg`
- `instruct3.0.jpg`
- `instruct3.1.jpg`
- `instruct4.jpg`
- `instruct5.jpg`

Папка должна быть доступна для чтения (права `chmod -R 755 images/`).

### 4. Установка зависимостей

#### Без Docker

1. Установить `python`, если вдруг он не установлен на сервере (ubuntu):
   ```bash
   sudo apt update && sudo apt install python3
   ```
   (или ищете команду для своего дистибутива, или ОС)
   <br>
2. Создать вирутальное окружение:
   ```bash
   python3 venv .venv
   ```
4. Активировать его:
   ```bash
     source .venv/bin/activate
   ```
3. Установить `poetry`:
   ```bash
   pip install poetry
   ```
4. Установите зависимости из `pyproject.toml`:
   ```bash
   poetry install --no-root
   ```

#### С Docker

- Убедитесь, что Docker и Docker Compose установлены:
    - [Инструкция для Ubuntu](https://timeweb.cloud/tutorials/docker/kak-ustanovit-docker-na-ubuntu)
    - Проверка:
      ```bash
      docker --version
      docker-compose --version
      ```
- Зависимости устанавливаются автоматически при сборке контейнера.

---

## Запуск

### Вариант 1: Без Docker

1. Активируйте виртуальное окружение:
   ```bash
   poetry shell
   ```
2. Запустите основной бот:
   ```bash
   poetry run python main.py
   ```
3. В отдельном терминале запустите скрп:
   ```bash
   poetry run python automatic_responder.py
   ```
    - При первом запуске скрирт запросит код авторизации (придёт в Telegram как сообщение от самого телеграмма).
    - Если включена двухфакторная аутентификация, введите пароль.

### Вариант 2: Через Docker

1. Соберите образ:
   ```bash
   docker build -t bot .
   ```
    - `-t bot`: Задаёт имя образа (`bot`).
2. Запустите контейнер для основного бота:
   ```bash
   docker run --env-file .env bot
   ```
    - `--env-file .env`: Передаёт переменные из `.env`.
    - Альтернативно, задайте переменные через `-e`:
      ```bash
      docker run -e BOT_TOKEN=your_bot_token -e SUPPORT_URL=https://t.me/@YourSupportAccount bot
      ```

### Вариант 3: Через Docker Compose

1. Обновите `docker-compose.yaml` для запуска обоих компонентов:

```yaml
# docker-compose.yaml
services:
  bot:
    build:
      context: .
      dockerfile: Dockerfile
    env_file:
      - .env
    restart: unless-stopped
```

2. Запустите сервис:
   ```bash
   docker compose up -d
   ```
    - `-d`: Запуск в фоновом режиме.
    - `restart: unless-stopped`: Автоматический перезапуск при сбоях.

3. Проверьте статус:
   ```bash
   docker compose ps
   ```

---

## Разработка и поддержка

### Структура проекта

- `main.py`: Точка входа основного бота (`aiogram`).
- `telegram_auto_responder.py`: Скрипт для автоответов (`telethon`).
- `handlers/`: Обработчики команд и callback'ов.
- `instructions_data.py`: Данные инструкций (текст, изображения).
- `keyboards/`: Inline-клавиатуры.
- `images/`: Изображения для инструкций.
- `bot.log`: Логи работы бота и userbot.
- `.env.template`: Шаблон для `.env`.

### Добавление новых инструкций

1. Откройте `instructions_data.py` и добавьте новый ключ в `ERROR_INSTRUCTIONS`:
   ```python
   "new_issue": [
       InstructionStep(
           text="Описание новой проблемы.",
           image_paths=["images/new_issue.jpg"],
           caption="Подпись к изображению."
       )
   ]
   ```
2. Добавьте файл `new_issue.jpg` в `images/`.
3. Обновите `keyboards/inline.py`, добавив новый `callback_data` для клавиатуры.

### Просмотр логов

- Логи пишутся в `bot.log`. Для просмотра:
  ```bash
  tail -f bot.log
  ```
- Уровни логов:
    - `INFO`: Запуск/остановка, отправка автоответов.
    - `DEBUG`: Детали (например, загрузка диалогов).
    - `ERROR`: Ошибки (например, проблемы с API).

### Обновление бота

1. Обновите репозиторий:
   ```bash
   git pull
   ```
2. Пересоберите образ (если используете Docker):
   ```bash
   docker compose build
   docker compose up -d
   ```
