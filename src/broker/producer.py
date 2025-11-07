from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672/")


async def send_order():
    await broker.publish("process", "transaction")
    print("Заказ отправлен в обработку")
