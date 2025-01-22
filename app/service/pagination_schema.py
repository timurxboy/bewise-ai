from enum import Enum
from typing import TypeVar

from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")


class OrderEnum(Enum):
    ASC = "asc"
    DESC = "desc"


class SPagination(BaseModel):
    perPage: int
    page: int
    order: OrderEnum

    class Config:
        from_attributes = True


def pagination_params(
        page: int = Query(ge=1, le=500000, required=False, default=1),
        perPage: int = Query(ge=1, le=100, required=False, default=10),
        order: OrderEnum = OrderEnum.DESC,
) -> SPagination:
    return SPagination(perPage=perPage, page=page, order=order.value)

