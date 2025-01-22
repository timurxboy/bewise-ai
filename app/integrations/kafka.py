from aiokafka import AIOKafkaProducer

kafka_producer: AIOKafkaProducer | None = None


async def init_kafka_producer(bootstrap_servers: str):
    """
    Инициализация Kafka продюсера.
    """
    global kafka_producer
    kafka_producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
    await kafka_producer.start()


async def stop_kafka_producer():
    """
    Остановка Kafka продюсера.
    """
    global kafka_producer
    if kafka_producer:
        await kafka_producer.stop()


def get_kafka_producer() -> AIOKafkaProducer:
    """
    Возвращает Kafka-продюсер.
    """
    if not kafka_producer:
        raise RuntimeError("Kafka Producer не инициализирован")
    return kafka_producer
