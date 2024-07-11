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

from src.authentication.utils import get_current_user
from src.catalogue.models.pydantic import ProductModel
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    ProductRoutesPrefixes,
)
from src.catalogue.services import get_product_service
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse
from src.users.models.pydantic import UserAddressModel, UserAddressBaseModel
from src.users.models.sqlalchemy import User
from src.users.services import UserAddressService, get_user_address_service

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
    ProductRoutesPrefixes.detail,
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


user_address_router = APIRouter()


@user_address_router.get(
    "/addresses",
    response_model=List[UserAddressBaseModel],
    status_code=status.HTTP_200_OK,
)
async def list_addresses(
    user=Depends(get_current_user),
    service: UserAddressService = Depends(get_user_address_service),
) -> List[UserAddressBaseModel]:
    return await service.get_addresses_by_user(user.id)


@user_address_router.get(
    "/addresses/{address_id}",
    response_model=Union[UserAddressModel, ErrorResponse],
    status_code=status.HTTP_200_OK,
)
async def get_address(
    address_id: int,
    response: Response,
    user=Depends(get_current_user),
    service: UserAddressService = Depends(get_user_address_service),
) -> Union[UserAddressModel, ErrorResponse]:
    try:
        address = await service.detail(pk=address_id)
        if address.user_id != user.id:
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(message="Access forbidden to this address")
        return address
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

