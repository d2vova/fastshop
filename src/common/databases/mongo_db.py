"""
Provide connection to MongoDB. Default database "casafari".
"""
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.base_settings import base_settings
from src.common.singleton import SingletonMeta
from src.reviews.models.mongo import ProductReview, ProductAnalytics


class AsyncMongoDBClient(AsyncIOMotorClient, metaclass=SingletonMeta):
    """
    Provide singleton client for MongoDB.
    """


async def init_mongo_db():
    client = AsyncMongoDBClient(base_settings.mongo.url)
    await init_beanie(
        database=client.get_database(),
        document_models=[
            ProductReview,
            ProductAnalytics
        ],
    )
