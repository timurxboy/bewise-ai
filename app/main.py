from fastapi import FastAPI
from app.applications.router import router as application_router
from app.integrations.kafka import init_kafka_producer, stop_kafka_producer
from app.config import settings

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_kafka_producer(f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}")  # Запуск продюсера


@app.on_event("shutdown")
async def shutdown_event():
    await stop_kafka_producer()  # Остановка продюсера


app.include_router(application_router)
