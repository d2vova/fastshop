from typing import (
    Annotated,
    Union,
)

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from src.catalogue.models.pydantic import ProductModel
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    ProductRoutesPrefixes,
)
from src.catalogue.services import get_product_service, ProductService
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse
from src.reviews.services import ProductAnalyticsService

router = APIRouter(prefix=CatalogueRoutesPrefixes.product)


@router.get(
    ProductRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[ProductModel],
)
async def product_list(product_service: Annotated[get_product_service, Depends()]) -> list[ProductModel]:
    """
    Get list of products.

    Returns:
        Response with list of products.
    """
    return await product_service.list()


@router.get(
    "/products/detail/{pk}",
    responses={
        status.HTTP_200_OK: {'model': ProductModel},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[ProductModel, ErrorResponse],
)
async def product_detail(
    response: Response,
    pk: int,
    service: ProductService = Depends(get_product_service),
    analytics_service: ProductAnalyticsService = Depends(),
) -> Union[ProductModel, ErrorResponse]:
    """
    Retrieve product. Records analytics

    """
    try:
        product = await service.detail(pk=pk)
        await analytics_service.record_visit_product(product_id=pk)
        return product
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)
