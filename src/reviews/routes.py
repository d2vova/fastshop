from src.common.routes import BaseCrudPrefixes


class ReviewsRoutesPrefixes:
    product_reviews: str = '/product-reviews'


class ProductReviewRoutesPrefixes(BaseCrudPrefixes):
    add_reply: str = '/{pk}/reply'

class ProductAnalyticsRoutesPrefixes(BaseCrudPrefixes):
    add_reply: str = '/{pk}/analytics'