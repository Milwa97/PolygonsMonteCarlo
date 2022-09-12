from pydantic import BaseModel
from typing import Union, List, Dict


class ItemPoint(BaseModel):
    x: float
    y: float
    name: Union[str, None] = None


class ItemLine(BaseModel):
    starting_point: ItemPoint
    ending_point: ItemPoint


class ItemCircle(BaseModel):
    center: ItemPoint
    radius: float


class ItemTriangle(BaseModel):
    a: ItemPoint
    b: ItemPoint
    c: ItemPoint


class ItemPolygon(BaseModel):
    name: Union[str, None] = None
    vertices: List[ItemPoint]


class AreaResponse(BaseModel):
    figure: str = "my poly"
    area: float = 12.0


class LineInfoResponse(BaseModel):
    length: float = 3.1623
    slope: float = 0.3334
    intercept: float = 0
