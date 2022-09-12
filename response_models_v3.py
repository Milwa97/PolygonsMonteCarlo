from pydantic import BaseModel, Field, constr
from typing import Union, List, Dict

from enum import Enum


class Colors(str, Enum):
    black = "black"
    red = "red"
    blue = "blue"
    green = "green"
    purple = "purple"
    pink = "pink"


class SuccessfulResponse(BaseModel):
    message: str = Field(default='Example success response', min_length=10, max_length=30)


class ItemPoint(BaseModel):
    x: float = Field(ge=-1.0, le=1.0, description='1\'st coordinate of the point', default=0.5)
    y: float = Field(ge=-1.0, le=1.0, description='2\'nd coordinate of the point', default=0.1)
    name: Union[str, None] = Field(max_length=4, description='point name', default='P')


class ItemColoredPoint(BaseModel):

    x: float = Field(ge=-1.0, le=1.0, description='1\'st coordinate of the point', default=0.5)
    y: float = Field(ge=-1.0, le=1.0, description='2\'nd coordinate of the point', default=0.1)
    name: Union[str, None] = Field(max_length=4, description='point name', default='P')
    color: Colors = Field(default='black', description='point color', exclude=True)
    size: int = Field(default=10, description='point size', exclude=True)

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
    starting_point: ItemPoint = Field(default={"name": "A", "x": 0.2, "y": 0.2}, description='line starting point')
    ending_point: ItemPoint = Field(default={"name": "B", "x": 0.3, "y": 0.5}, description='line ending point')


class ItemCircle(BaseModel):
    center: ItemPoint = Field(default={"name": "O", "x": 0.2, "y": 0.2}, description='center point of the circle')
    radius: float = Field(default=0.3, gt=0, lt=0.5, description="Circle radius, must be greater than zero")


class ItemTriangle(BaseModel):
    a: ItemPoint = Field(default={"name": 'A', 'x': 0.0, 'y': 0.0}, description='1\'st point of the triangle')
    b: ItemPoint = Field(default={"name": 'B', 'x': 0.5, 'y': 0.5}, description='2\'nd point of the triangle')
    c: ItemPoint = Field(default={"name": 'C', 'x': 1.0, 'y': 0.0}, description='3\'rd point of the triangle')


example_vertices = [{"name": "A", "x": 0.0, "y": 0.0},
                    {"name": "B", "x": 0.0, "y": 0.2},
                    {"name": "C", "x": 0.5, "y": 0.0},
                    {"name": "D", "x": 0.5, "y": 0.2}
                    ]


class ItemPolygon(BaseModel):
    name: Union[str, None] = Field(default=None, description='polygon name', max_length=10)
    vertices: List[ItemPoint] = Field(default=example_vertices, min_items=3, max_items=7, unique_items=True)


class AreaResponse(BaseModel):
    figure: str = Field(default='poly', description='figure name')
    area: float = Field(gt=0, default=12.0, description='figure area')
    time: Union[None, float] = Field(ge=0, default=None, description='time in seconds taken to calculate area')
    #area: Decimal = Field(gt=0, decimal_places=2, max_digits=2, description='figure area')


class LineInfoResponse(BaseModel):
    length: float = Field(default=3.16, description='line length')
    slope: float = Field(default=0.3334, description='line slope')
    intercept: float = Field(default=0, description='line intercept')


"""
from functools import wraps
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time-start_time

        return result
    return wrapper()
"""