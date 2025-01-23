import datetime
import json

from sqlalchemy import select, asc, desc, func, insert
from typing import Annotated
from fastapi import Depends

from app.DB import async_session_maker


from app.integrations.kafka import get_kafka_producer
from app.applications.models import Applications
from app.applications.schemas import SApplication
from app.integrations.logger_config import setup_logger
from app.service.pagination_schema import SPagination, pagination_params, OrderByEnum


logger = setup_logger()


def json_serializer(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


class ApplicationsService:
    model = Applications

    @classmethod
    async def get_all(cls,
                      pagination: Annotated[SPagination, Depends(pagination_params)],
                      user_name):
        logger.info("Получен запрос на получение заявок с фильтрацией по имени пользователя: %s и пагинацией: %s",
                    user_name, pagination)

        async with async_session_maker() as session:
            order = desc if pagination.order_by == OrderByEnum.DESC else asc

            filter_by = {}
            if user_name:
                filter_by["user_name"] = user_name

            total_query = select(func.count()).select_from(cls.model).filter_by(**filter_by)
            total_result = await session.execute(total_query)
            total_count = total_result.scalar()

            total_pages = (total_count + pagination.per_page - 1) // pagination.per_page

            query = (
                select(cls.model)
                .filter_by(**filter_by)
                .order_by(order(getattr(cls.model, pagination.sort_by.value)))
                .limit(pagination.per_page)
                .offset((pagination.page - 1) * pagination.per_page)
            )

            result = await session.execute(query)
            items = result.scalars().all()

            return {
                "pages": total_pages,
                "values": items
            }

    @classmethod
    async def create(cls, **data) -> SApplication:
        logger.info("Получен запрос на создание заявки с данными: %s", data)
        async with (async_session_maker() as session):
            query = insert(cls.model).values(**data).returning(
                cls.model.id,
                cls.model.user_name,
                cls.model.description,
                cls.model.created_at)

            result = await session.execute(query)
            await session.commit()

            values = dict(result.fetchone()._mapping)
            logger.info("Заявка успешно создана с ID: %d", values["id"])

            producer = get_kafka_producer()

            try:
                await producer.send_and_wait(
                    "applications",
                    value=json.dumps(values, default=json_serializer).encode("utf-8"),
                    )
            except Exception as e:
                logger.error("Ошибка при отправке данных в Kafka: %s", str(e), exc_info=True)

        return SApplication(**values)
