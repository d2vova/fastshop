from typing import (
    Annotated,
    Union,
)

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Response,
    status,
)

from src.catalogue.models.database import Product
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    ProductRoutesPrefixes, CategoryRoutesPrefixes,
)
from src.catalogue.services import get_product_service, get_category_service
from src.common.enums import TaskStatus
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse
from src.general.schemas.task_status import TaskStatusModel


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


@router.get(
    ProductRoutesPrefixes.search,
    status_code=status.HTTP_200_OK,
)
async def search(
    keyword: str,
    service: Annotated[get_product_service, Depends()],
):
    """
    Search products.

    Returns:
        Response with products.
    """
    response = await service.search(keyword=keyword)

    return response


@router.post(
    ProductRoutesPrefixes.update_index,
    status_code=status.HTTP_200_OK,
)
async def update_elastic(
    background_tasks: BackgroundTasks,
    service: Annotated[get_product_service, Depends()],
):
    """
    Update products index.

    Returns:
        None.
    """
    status_model = await TaskStatusModel(status=TaskStatus.IN_PROGRESS).save_to_redis()

    background_tasks.add_task(service.update_search_index, status_model.uuid)

    return await TaskStatusModel().get_from_redis(uuid=status_model.uuid)


@router.get(
    CategoryRoutesPrefixes.search_category,
    status_code=status.HTTP_200_OK,
)
async def search_categories(
        keyword: str,
        service: Annotated[get_category_service, Depends()],
):
    """
    Search categories.
    Returns:
        Response with categories.
    """
    response = await service.search(keyword=keyword)

    return response


@router.post(
    CategoryRoutesPrefixes.update_category_index,
    status_code=status.HTTP_200_OK,
)
async def update_elastic(
        background_tasks: BackgroundTasks,
        service: Annotated[get_category_service, Depends()],
):
    """
    Update categories index.
    Returns:
        None.
    """
    status_model = await TaskStatusModel(status=TaskStatus.IN_PROGRESS).save_to_redis()

    background_tasks.add_task(service.update_category_index, status_model.uuid)

    return await TaskStatusModel().get_from_redis(uuid=status_model.uuid)