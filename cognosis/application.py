import asyncio

from cognosis.application import main as application_main
from cognosis.FSK_mono.mono import UUID
from faststream import FastStream
from faststream.kafka import KafkaBroker

version = "0.1.10"
title = "FSK_mono"
description = "FastStream_Kafka_Monolith"
# Basemodels: Name, UUID, tbd  # ========================>mono.py
# Subscribers: bs_Name, bs_UUID, tbd  # ========================>mono.py
# Publishers: to_Name, to_UUID, to_UFS, tbd  # ========================>mono.py
# =====async-section============
async def my_async_function(*args, **kwargs):
    pass  # The decorated function is called when the application starts up.


async def publish_UUID():
    await broker.publish(UUID(uuid="1234567890"), "greetings")
    pass  # The decorated function publishes a UUID object with the value "1234567890" to the "greetings" topic when the application starts up.


async def main(arg1, arg2):
    await app.run()


if __name__ == "__main__":
    arg1 = {"hello", str}
    arg2 = {"world", str}
    asyncio.run(main(arg1, arg2))

if __name__ == "__main__":
    arg1 = {"hello", str}
    arg2 = {"world", str}
    asyncio.run(application_main(arg1, arg2))
