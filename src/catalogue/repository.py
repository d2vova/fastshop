from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.catalogue.models.database import Product, AdditionalProducts, RecommendedProducts
from src.common.databases.postgres import get_session
from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository


class ProductRepository(BaseSQLAlchemyRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Product, session=session)


def get_product_repository(session: AsyncSession = Depends(get_session)) -> ProductRepository:
    return ProductRepository(session=session)


class AdditionalProductsRepository(BaseSQLAlchemyRepository[AdditionalProducts]):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(model=AdditionalProducts, session=session)

def get_additional_products_repository(session: AsyncSession = Depends(get_session)) -> AdditionalProductsRepository:
    return AdditionalProductsRepository(session=session)

class RecommendedProductsRepository(BaseSQLAlchemyRepository[RecommendedProducts]):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(model=RecommendedProducts, session=session)

def get_recommended_products_repository(session: AsyncSession = Depends(get_session)) -> RecommendedProductsRepository:
    return RecommendedProductsRepository(session=session)


