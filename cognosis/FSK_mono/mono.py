from pydantic import BaseModel, Field


class Name(BaseModel):  # pydantic BaseModel
    name: str = Field(..., description="name/description-if-not-name")
    # abstract class
    def subscriber(self, topic: str):
        def decorator(func):
            async def wrapper():
                await func(self)
            return wrapper
        return decorator

    def publisher(self, topic: str):
        def decorator(func):
            async def wrapper():
                await func(self)
            return wrapper
        return decorator

    def after_startup(self, func):
        async def wrapper():
            await func(self)
        return wrapper

    def before_shutdown(self, func):
        async def wrapper():
            await func(self)
        return wrapper


class UUID(BaseModel):
    uuid: str = Field(..., description="uuid")