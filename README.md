# Сервис микроблогов

## Документация API
[Ссылка](https://editor.swagger.io/?_gl=1*vaxfv9*_gcl_au*MTE4OTgxMjMzMi4xNzA5NTYzMjE2&_ga=2.197194927.1617675863.1709740220-1936030370.1709563211)

## Технологический стек
Python, Flask

## Установка и запуск
1. Убедитесь, что у вас установлен и запущен **Docker**.
2. Склонируйте этот репозиторий: 
    ```shell
   git clone https://gitlab.skillbox.ru/viacheslav_chuchmanov/python_advanced_diploma.git
   ```
3. Перейдите в склонированную папку используя терминал
4. Создайте файл .env и добавьте DATABASE переменную, эта переменная определяет движок SQLAlchemy.
   ```python
   engine = create_engine(os.getenv("DATABASE"))
   ```
4. В терминале введите команду:
   ```shell
   docker-compose up -d
   ```
5. Приложение запущено.
6. Приложение будет доступно по локальному хосту и порту 7134. (127.0.0.1:7134)
