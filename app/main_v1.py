from fastapi import FastAPI
from app.figures import Point, Line, Polygon, Circle
from app.response_models_v1 import (ItemPoint, ItemLine, ItemCircle, ItemPolygon,
                                    ItemTriangle, AreaResponse, LineInfoResponse)

app = FastAPI()


@app.get("/")
def index():
    """
    Home page, method returns "Hello" message
    """
    return {"message": "Hello! This is a practical introduction to FastApi"}


@app.post("/create_point")
def create_point(point: ItemPoint):
    """
    Method creates a point based on the given coordinates in 2D.
    """
    point = Point(**point.dict())
    return {"message": f"Point: {point} has been created"}


@app.post("/create_line")
def create_line(line: ItemLine):
    """
    Method creates a line from the two uploaded points.
    """
    line_dict = line.dict()
    point_1 = Point(**line_dict['starting_point'])
    point_2 = Point(**line_dict['ending_point'])
    line = Line.create_line_from_points(point_1, point_2)
    return {"message": f"Line {line} has been created"}


@app.post("/create_circle")
def create_circle(circle: ItemCircle):
    """
    Method creates a circle from the uploaded radius and center point.
    """
    o = Point(**circle.center.dict())
    circle = Circle(o, circle.radius)
    return {"message": f"Circle: {circle} has been created"}


@app.post("/create_triangle")
def create_triangle(triangle: ItemTriangle):
    """
    Method creates a triangle from the three uploaded points,
    """
    triangle_dict = triangle.dict()
    a = Point(**triangle.a.dict())
    b = Point(**triangle_dict['b'])
    c = Point(**triangle_dict['c'])
    triangle = Polygon([a, b, c])
    return {"message": f"Triangle: {triangle} has been created"}


@app.post("/create_polygon")
def create_polygon(polygon: ItemPolygon):
    """
    Method creates a polygon from the uploaded points. The number of points must be between 3 and 7.
    """
    vertices_points = [Point(**v) for v in polygon.dict()['vertices']]
    polygon = Polygon(vertices_points)
    return {"message": f"Polygon: {polygon} has been created"}


@app.post("/calculate_area_circle", response_model=AreaResponse)
def calculate_area_circle(circle: ItemCircle):
    """
    Method calculates area of the circle with specified radius
    """
    o = Point(**circle.center.dict())
    circle = Circle(o, circle.radius)
    area = circle.get_area()
    return {'figure': 'circle', "area": area}


@app.post("/get_line_length")
def get_line_length(starting_point: ItemPoint, ending_point: ItemPoint):
    """
    Method takes two points and returns length of the line created out of those two points
    """
    point_1 = Point(**starting_point.dict())
    point_2 = Point(**ending_point.dict())
    line = Line.create_line_from_points(point_1, point_2)
    return {"length": line.get_length()}


@app.post("/get_line_info", response_model=LineInfoResponse)
def get_line_info(starting_point: ItemPoint, ending_point: ItemPoint):
    """
    Method takes two points and return length, slope and intercept of the line created
    from those two points.
    """
    point_1 = Point(**starting_point.dict())
    point_2 = Point(**ending_point.dict())
    line = Line.create_line_from_points(point_1, point_2)
    return {"length": line.get_length(), "slope": line.slope, "intercept": line.intercept}
