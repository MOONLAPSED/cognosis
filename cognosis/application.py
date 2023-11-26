=================>mono.py
# Subscribers: bs_Name, bs_UUID, tbd  # ========================>mono.py
# Publishers: to_Name, to_UUID, to_UFS, tbd  # ========================>mono.py
broker = KafkaBroker()  # Initialize KafkaBroker
app = FastStream(  # Create the FastStream app with the broker
    broker,
    title=title,
    version=version,
    description=description,
)  # The FastStream app instance provides the framework for defining subscribers, publishers, and other application components.
=======
import asyncio

from cognosis.FSK_mono.mono import UUID
from faststream import FastStream
from faststream.kafka import KafkaBroker

version = "0.1.10"
title = "FSK_mono"
description = "FastStream_Kafka_Monolith"
# Basemodels: Name, UUID, tbd  # ========================>mono.py
# Subscribers: bs_Name, bs_UUID, tbd  # ========================>mono.py
# Publishers: to_Name, to_UUID, to_UFS, tbd  # ========================>mono.py
broker = KafkaBroker()  # Initialize KafkaBroker
app = FastStream(  # Create the FastStream app with the broker
    broker,
    title=title,
    version=version,
    description=description,
)  # The FastStream app instance provides the framework for defining subscribers, publishers, and other application components.
from cognosis.application import *

# Subscribers: bs_Name, bs_UUID, tbd  # ========================>mono.py
# Publishers: to_Name, to_UUID, to_UFS, tbd  # ========================>mono.py
broker = KafkaBroker()  # Initialize KafkaBroker
app = FastStream(  # Create the FastStream app with the broker
    broker,
    title=title,
    version=version,
    description=description,
)  # The FastStream app instance provides the framework for defining subscribers, publishers, and other application components.
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
=======
)  # The FastStream app instance provides the framework for defining subscribers, publishers, and other application components.


@broker.publisher("to_Name")
@broker.publisher(
    "to_UUID"
)  # This indicates that the decorated function will be called whenever a message is published to any of these topics.
@broker.publisher("to_UFS")
@app.after_startup  # This line decorates a function as the after_startup event handler. The after_startup event is triggered once the FastStream application has been fully initialized.


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
from cognosis.application import *


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
