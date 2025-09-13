FROM python:3.12-alpine

COPY . ./bot_app

WORKDIR /bot_app

RUN pip install --upgrade pip && pip install poetry && poetry install --no-root

CMD ["poetry", "run", "python", "main.py"]
