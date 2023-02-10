from typing import List
from fastapi import FastAPI
from app.figures import Point, Line, Polygon, Circle

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello! This is a practical introduction to FastApi"}


@app.post("/create_point")
def create_point(x: float, y: float, name: str = 'P'):
    point = Point(name, x, y)
    return {"message": f"Point: {point} has been created"}


@app.post("/create_line")
def create_line(x1: float, y1: float, x2: float, y2: float, name_1: str = 'A', name_2: str = 'B'):
    point_1 = Point(name_1, x1, y1)
    point_2 = Point(name_2, x2, y2)
    line = Line.create_line_from_points(point_1, point_2)
    return {"message": f"Line {line} has been created"}


@app.post("/create_circle")
def create_circle(coordinate_x: float, coordinate_y: float, radius: float):
    if radius > 0:
        o = Point('O', coordinate_x, coordinate_y)
        circle = Circle(o, radius)
        return {"message": f"Circle: {circle} has been created"}
    return {"message": f"Can not create circle with non-positive radius r={radius}!"}


@app.post("/create_triangle")
def create_triangle(x_coordinates: List[float], y_coordinates: List[float]):
    if len(x_coordinates) == 3 and len(y_coordinates) == 3:
        points = [Point('', x, y) for x, y, in zip(x_coordinates, y_coordinates)]
        triangle = Polygon(points)
        return {"message": f"Triangle: {triangle} has been created"}
    if len(x_coordinates) == len(y_coordinates):
        return {"message": f"Can not create triangle out of {len(x_coordinates)} points!"}
    return {"message": "Number of x coordinates is not equal to the number of y coordinates!"}


@app.get("/get_area_circle")
def get_area_circle(coordinate_x: float, coordinate_y: float, radius: float):
    if radius > 0:
        o = Point('O', coordinate_x, coordinate_y)
        circle = Circle(o, radius)
        area = circle.get_area()
        return {"area": area}
    return {"message": "Can not create circle with non-positive radius!"}


@app.get("/get_line_length")
def get_line_length(x1: float, y1: float, x2: float, y2: float, name_1: str = 'A', name_2: str = 'B'):
    point_1 = Point(name_1, x1, y1)
    point_2 = Point(name_2, x2, y2)
    line = Line.create_line_from_points(point_1, point_2)
    return {"length": line.get_length()}


@app.get("/get_line_slope_intercept")
def get_line_slope_intercept(x1: float, y1: float, x2: float, y2: float, name_1: str = 'A', name_2: str = 'B'):
    point_1 = Point(name_1, x1, y1)
    point_2 = Point(name_2, x2, y2)
    line = Line.create_line_from_points(point_1, point_2)
    return {"message": f"line slope = {line.slope}, intercept = {line.intercept}"}
