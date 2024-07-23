from src.common.repository.beanie import BaseMongoRepository
from src.reviews.models.mongo import ProductReview, ProductAnalytics
from datetime import datetime


class ProductReviewRepository(BaseMongoRepository[ProductReview]):
    __model__ = ProductReview

class ProductAnalyticsRepository(BaseMongoRepository[ProductAnalytics]):
    __model__ = ProductAnalytics

    async def create_analytics(self, product_id: int) -> ProductAnalytics:
        analytics = await ProductAnalytics.create(product_id=product_id, timestamp=datetime.utcnow())
        await analytics.insert()
        return analytics