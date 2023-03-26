1. Создать файл cfg.env с полями:\n
1.1.SHORT_NAME="имя автора(скрыто)"
    AUTHOR_NAME="публичное имя автора"
    AUTHOR_URL="ссылка на автора(группу, канал)"

2. Закинуть папку со страницами в src
3. python3 -m venv venv
4. pip install -r requirements.txt
5. docker-compose up -d --no-deps --build
6. python main.py и выбрать нужную папку
