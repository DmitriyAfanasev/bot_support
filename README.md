# Инструкции для запуска бота

<br>

### Запуск напрямую без Docker

```shell
    python main.py
```

<br>

###### ОБЯЗАТЕЛЬНО создать файл `.env` по шаблону `.env.template` и указать туда данные для бота

### Команды для запуска бота через Docker:

###### [Если Docker нет на сервере, то вот ссылка на инструкцию](https://timeweb.cloud/tutorials/docker/kak-ustanovit-docker-na-ubuntu)

## Билд контейнера

```shell
    docker build -t bot .
```

## Запуск контейнера

```shell
    docker run -e BOT_TOKEN=рандомный+токен  bot
```

-t - флаг для имени образа, в нашем случае `bot` <br>
-e - флаг для указания переменных окружения, в нашем случае токен для бота `BOT_TOKEN` <br>

###### опционально задаать

`SUPPORT_URL` для ссылки на поддержку, например, на страницу суппорта сайта, или теллеграм ссылку.

Пример для двух комманд:

```shell
    docker run -e BOT_TOKEN=рандомный+токен SUPPORT_URL=http://домен.ру/поддержка bot
```

или с указанием на телеграмм

```shell
    docker run -e BOT_TOKEN=рандомный+токен SUPPORT_URL=https://t.me/@Sheldon_Kuper1 bot
```