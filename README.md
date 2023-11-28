# Рассылка email на Fast API

## Как развернуть проект
- скачать репозиторий, перейти в директорию с ```docker-compose.yml```

- заполнить переменные среды заполнив файл ```.env```

- собрать и запустить докер-сборку

```docker-compose up -d --build```

```docker-compose up```

- все работает http://localhost:8000/

- post запрос: http://localhost:8000/send-email/:

- параметры → {
    "to": ["test1@gmail.com", "test2@gmail.com"],
    "subject": "test",
    "message": "tetris"
}