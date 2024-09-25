# 1. Используем официальный образ Python
FROM python:3.11-slim

# 2. Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y gcc libev-dev libffi-dev build-essential

# 3. Обновляем pip до последней версии
RUN pip install --upgrade pip

# 4. Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# 5. Копируем все файлы проекта из корня репозитория в контейнер
COPY . /app

# 6. Устанавливаем зависимости из requirements.txt
RUN pip install -r requirements.txt

# 7. Открываем порт 10000 для доступа к приложению
EXPOSE 10000

# 8. Указываем команду для запуска вашего приложения
CMD ["python", "web_server.py"]
