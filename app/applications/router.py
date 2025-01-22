from typing import Annotated

from fastapi import APIRouter, Depends

from app.applications.schemas import SApplication, SApplicationCreate
from app.applications.service import ApplicationsService
from app.service.pagination_schema import SPagination, pagination_params

router = APIRouter(
    prefix="/applications",
    tags=["Заявления"]
)


@router.get("")
async def get_applications(
    pagination: Annotated[SPagination, Depends(pagination_params)],
    user_name: str = None,
):
    result = await ApplicationsService.get_all(pagination=pagination, user_name=user_name)
    return result


@router.post("")
async def create_application(request: SApplicationCreate) -> SApplication:
    result = await ApplicationsService.create(user_name=request.user_name, description=request.description)
    return result