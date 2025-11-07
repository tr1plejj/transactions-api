from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.schemas.base import STransaction

broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672/")
app = FastStream(broker)


@broker.subscriber("transaction")
async def process_transaction(transaction: STransaction):
    print(f"Transaction received: {transaction}")


@broker.subscriber("users")
async def handle_user_login(user_id: int):
    print(f"User logged with id {user_id}")
