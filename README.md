# Сервис обработки заявок пользователей
## Описание проекта
Данный проект реализует сервис для обработки заявок пользователей. Он предоставляет REST API для создания и получения заявок, сохраняет данные в базе данных PostgreSQL и публикует информацию о новых заявках в Kafka. Проект полностью контейнеризован с использованием Docker и включает инструкции по настройке и запуску.

## Функциональность
1. **REST API**:
    - POST /applications: Эндпоинт для создания новой заявки. Заявка содержит следующие поля:
      - id (генерируется автоматически)
      - user_name (имя пользователя)
      - description (описание заявки)
      - created_at (дата и время создания, устанавливается автоматически)
    - GET /applications: Эндпоинт для получения списка заявок:
      - Поддержка фильтрации по имени пользователя (user_name).
      - Поддержка пагинации с параметрами page и size.
2. **PostgreSQL**:
      - Хранение данных заявок.
      - Использование SQLAlchemy для работы с базой данных. 

3. **Kafka**:
      - Публикация информации о новых заявках в топик Kafka.
      - В сообщение включаются:
          - id заявки
          - user_name
          - description
          - created_at
5. **Асинхронность**:
      - Все взаимодействия с PostgreSQL и Kafka реализованы асинхронно.
6. **Контейнеризация**:
      - Использование Docker для развертывания приложения, PostgreSQL и Kafka.

## Технологии
- Фреймворк: FastAPI
- База данных: PostgreSQL
- Брокер сообщений: Kafka
- Контейнеризация: Docker, Docker Compose
- ORM: SQLAlchemy
- Асинхронность: Asyncio и AIOKafka

# Установка и запуск
## Клонирование репозитория
```
git clone https://github.com/timurxboy/bewise-ai.git
cd bewise-ai
```

## Настройка окружения

#### Создайте файл .env в корневой директории проекта 
```
echo . > .env
```

и добавьте переменные окружения:

```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_post
KAFKA_HOST=your_kafka_host
KAFKA_PORT=your_kafka_post
```

## Docker

Соберите контейнеры и запустите проект:

```
docker-compose up --build
```

## Миграции базы данных

```
docker-compose exec fastapi alembic upgrade head
```

## API документация
После запуска веб-приложения документация будет доступна по следующим URL:

- Swagger: http://localhost:8000/docs
- KAFKA UI: http://localhost:8086/

