from typing import Union
from enum import Enum
from pydantic import BaseModel, constr, conlist, confloat


class Colors(str, Enum):
    black = "black"
    red = "red"
    blue = "blue"
    green = "green"
    purple = "purple"
    pink = "pink"


class ItemPoint(BaseModel):
    x: confloat(strict=False, gt=-1.0, le=1.0)
    y: confloat(strict=False, gt=-1.0, le=1.0)
    name: Union[str, None] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "P",
                "x": 0.5,
                "y": 0.1,
            }
        }


class ItemColoredPoint(BaseModel):
    x: confloat(strict=False, gt=-1.0, le=1.0)
    y: confloat(strict=False, gt=-1.0, le=1.0)
    name: Union[str, None] = None
    color: Colors
    size: int

    class Config:
        schema_extra = {
            "example": {
                "name": "P",
                "x": 0.5,
                "y": 0.1,
                'color': 'black',
                'size': 10
            }
        }


class ItemLine(BaseModel):
    starting_point: ItemPoint
    ending_point: ItemPoint

    class Config:
        schema_extra = {
            "example": {
                "starting_point": {"name": 'A', 'x': 0.2, 'y': 0.2},
                "ending_point": {"name": 'B', 'x': 0.3, 'y': 0.5}
            }
        }


class ItemCircle(BaseModel):
    center: ItemPoint
    radius: confloat(gt=0, le=1.0)

    class Config:
        schema_extra = {
            "example": {
                "center": {"name": '0', 'x': 0.5, 'y': 0.5},
                "radius": 0.25
            }
        }


class ItemTriangle(BaseModel):
    a: ItemPoint
    b: ItemPoint
    c: ItemPoint

    class Config:
        schema_extra = {
            "example": {
                "a": {"name": 'A', 'x': 0.0, 'y': 0.0},
                "b": {"name": 'B', 'x': 0.5, 'y': 0.5},
                "c": {"name": 'C', 'x': 1.0, 'y': 0.0}
            }
        }


class ItemPolygon(BaseModel):
    name: Union[str, None] = None
    vertices: conlist(ItemPoint, min_items=3, max_items=7, unique_items=True)

    class Config:
        schema_extra = {
            "example": {
                "name": "my_poly",
                "vertices": [
                    {
                        "name": "A",
                        "x": 0.5,
                        "y": 0.3
                    },
                    {
                        "name": "B",
                        "x": 0.5,
                        "y": 0.8
                    },
                    {
                        "name": "C",
                        "x": 0.8,
                        "y": 0.8
                    },
                    {
                        "name": "D",
                        "x": 0.8,
                        "y": 0.3
                    }
                ]
            }
        }


class SuccessfulResponse(BaseModel):
    message: constr(min_length=2, max_length=30) = 'Example success response'


class AreaResponse(BaseModel):
    figure: str
    area: float
    time: float

    class Config:
        schema_extra = {
            "example": {
                "figure": "poly",
                "area": 0.81,
                "time": 0.25
            }
        }


class LineInfoResponse(BaseModel):
    length: float
    slope: confloat(strict=True, allow_inf_nan=True)
    intercept: confloat(strict=True, allow_inf_nan=True)

    class Config:
        schema_extra = {
            "example": {
                "length": 3.1623,
                "slope": 0.3334,
                "intercept": 0.1
            }
        }
