from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.catalogue.models.database import Product, Category
from src.common.databases.postgres import get_session
from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository


class ProductRepository(BaseSQLAlchemyRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Product, session=session)


def get_product_repository(session: AsyncSession = Depends(get_session)) -> ProductRepository:
    return ProductRepository(session=session)

class CategoryRepository(BaseSQLAlchemyRepository[Category]):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(model=Category, session=session)

def get_category_repository(session: AsyncSession = Depends(get_session)) -> CategoryRepository:
    return CategoryRepository(session=session)