from fastapi import Depends

from src.catalogue.models.database import Product, AdditionalProducts, RecommendedProducts
from src.catalogue.repository import (
    ProductRepository,
    get_product_repository,
    AdditionalProductsRepository, get_additional_products_repository,
    RecommendedProductsRepository, get_recommended_products_repository,
)
from src.common.service import BaseService


class ProductService(BaseService[Product]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)

class AdditionalProductsService(BaseService[AdditionalProducts]):
    def __init__(self, repository: AdditionalProductsRepository):
        super().__init__(repository)

    async def add_additional_product(self, primary_id: int, secondary_id: int) -> AdditionalProducts:
        additional_products = AdditionalProducts(primary_id=primary_id, secondary_id=secondary_id)
        return await additional_products.create(instance=additional_products)

    async def update_additional_product(self, primary_id: int, secondary_id: int) -> AdditionalProducts:
        updated_additional_products = AdditionalProducts(primary_id=primary_id, secondary_id=secondary_id)
        return await updated_additional_products.update(instance=updated_additional_products)

    async def delete_additional_product(self, primary_id: int, secondary_id: int) -> None:
        await AdditionalProducts.delete(primary_id=primary_id, secondary_id=secondary_id)

    async def get_additional_product(self, primary_id: int, secondary_id: int) -> AdditionalProducts:
        return await AdditionalProducts.get(primary_id=primary_id, secondary_id=secondary_id)


class RecommendedProductsService(BaseService[RecommendedProducts]):
    def __init__(self, repository: RecommendedProductsRepository):
        super().__init__(repository)

    async def add_recommended_products(self, primary_id: int, secondary_id: int) -> RecommendedProducts:
        recommended_products = RecommendedProducts(primary_id=primary_id, secondary_id=secondary_id)
        return await recommended_products.create(instance=recommended_products)

    async def update_recommended_products(self, primary_id: int, secondary_id: int) -> RecommendedProducts:
        recommended_products = RecommendedProducts(primary_id=primary_id, secondary_id=secondary_id)
        return await recommended_products.update(instance=recommended_products)

    async def delete_recommended_products(self, primary_id: int, secondary_id: int) -> None:
        await RecommendedProducts.delete(primary_id=primary_id, secondary_id=secondary_id)

    async def get_recommended_products(self, primary_id: int, secondary_id: int) -> RecommendedProducts:
        return await RecommendedProducts.get(primary_id=primary_id, secondary_id=secondary_id)


def get_additional_products_service(
        repo: AdditionalProductsRepository = Depends(get_additional_products_repository)) -> AdditionalProductsService:
    return AdditionalProductsService(repository=repo)


def get_recommended_products_service(repo: RecommendedProductsRepository = Depends(get_recommended_products_repository))\
        -> RecommendedProductsService:
    return RecommendedProductsService(repository=repo)