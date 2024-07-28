from typing import (
    Annotated,
    Union, List,
)

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from src.catalogue.models.database import Product, AdditionalProducts, RecommendedProducts
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    ProductRoutesPrefixes,
)
from src.catalogue.services import (
    get_product_service,
    AdditionalProductsService,
    RecommendedProductsService,
    get_additional_products_service,
    get_recommended_products_service,
)
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse


router = APIRouter(prefix=CatalogueRoutesPrefixes.product)


@router.get(
    ProductRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[Product],
)
async def product_list(product_service: Annotated[get_product_service, Depends()]) -> list[Product]:
    """
    Get list of products.

    Returns:
        Response with list of products.
    """
    return await product_service.list()


@router.get(
    ProductRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': Product},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[Product, ErrorResponse],
)
async def product_detail(
    response: Response,
    pk: int,
    service: Annotated[get_product_service, Depends()],
) -> Union[Response, ErrorResponse]:
    """
    Retrieve product.

    Returns:
        Response with product details.
    """
    try:
        response = await service.detail(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response

@router.post(
    "/{product_id}/additional",
    status_code=status.HTTP_201_CREATED,
    response_model=AdditionalProducts,
)
async def add_additional_product(
        product_id: int,
        additional_id: int,
        service: Annotated[AdditionalProductsService, Depends(get_additional_products_service)],
) -> AdditionalProducts:
    """
    Add additional product.
    Returns:
        Response with created additional product.
    """
    return await service.add_additional_product(primary_id=product_id, additional_id=additional_id)


@router.put(
    "/{product_id}/additional/{additional_id}",
    status_code=status.HTTP_200_OK,
    response_model=AdditionalProducts,
)
async def update_additional_product(
        product_id: int,
        additional_id: int,
        service: Annotated[AdditionalProductsService, Depends(get_additional_products_service)],
) -> AdditionalProducts:
    """
    Update additional product.
    Returns:
        Response with updated additional product.
    """
    return await service.update_additional_product(primary_id=product_id, additional_id=additional_id)


@router.delete(
    "/{product_id}/additional/{additional_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_additional_product(
        product_id: int,
        additional_id: int,
        service: Annotated[AdditionalProductsService, Depends(get_additional_products_service)],
) -> Response:
    """
    Remove additional product.
    Returns:
        Response with no content.
    """
    await service.delete_additional_product(primary_id=product_id, additional_id=additional_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{product_id}/additional",
    status_code=status.HTTP_200_OK,
    response_model=List[AdditionalProducts],
)
async def list_additional_products(
        product_id: int,
        service: Annotated[AdditionalProductsService, Depends(get_additional_products_service)],
) -> AdditionalProducts:
    """
    List additional products.
    Returns:
        Response with list of additional products.
    """
    return await service.get_additional_product(primary_id=product_id)


# Recommended Products Endpoints

@router.post(
    "/{product_id}/recommended",
    status_code=status.HTTP_201_CREATED,
    response_model=RecommendedProducts,
)
async def add_recommended_product(
        product_id: int,
        recommended_id: int,
        service: Annotated[RecommendedProductsService, Depends(get_recommended_products_service)],
) -> RecommendedProducts:
    """
    Add recommended product.
    Returns:
        Response with created recommended product.
    """
    return await service.add_recommended_products(primary_id=product_id, recommended_id=recommended_id)


@router.put(
    "/{product_id}/recommended/{recommended_id}",
    status_code=status.HTTP_200_OK,
    response_model=RecommendedProducts,
)
async def update_recommended_product(
        product_id: int,
        recommended_id: int,
        new_recommended_id: int,
        service: Annotated[RecommendedProductsService, Depends(get_recommended_products_service)],
) -> RecommendedProducts:
    """
    Update recommended product.
    Returns:
        Response with updated recommended product.
    """
    return await service.update_recommended_products(primary_id=product_id, recommended_id=new_recommended_id)


@router.delete(
    "/{product_id}/recommended/{recommended_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_recommended_product(
        product_id: int,
        recommended_id: int,
        service: Annotated[RecommendedProductsService, Depends(get_recommended_products_service)],
) -> Response:
    """
    Remove recommended product.
    Returns:
        Response with no content.
    """
    await service.delete_recommended_products(primary_id=product_id, recommended_id=recommended_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{product_id}/recommended",
    status_code=status.HTTP_200_OK,
    response_model=List[RecommendedProducts],
)
async def list_recommended_products(
        product_id: int,
        service: Annotated[RecommendedProductsService, Depends(get_recommended_products_service)],
) -> RecommendedProducts:
    """
    List recommended products.
    Returns:
        Response with list of recommended products.
    """
    return await service.get_recommended_products(primary_id=product_id)
