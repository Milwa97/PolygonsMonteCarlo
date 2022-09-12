from io import BytesIO
import os
import json
import time
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from utils import get_fig_base, calculate_area_monte_carlo, directory
from figures import Point, Line, Polygon, Circle
from response_models_v3 import *

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello! This is a practical introduction to FastApi"}


@app.get("/get_figure/{filename}")
def get_figure(filename: str):
    """
    Returns png file specified by filename or 404 error if the file does not exist.
    """
    path_to_file = os.path.join(directory, filename)
    if os.path.isfile(path_to_file):
        return FileResponse(path=path_to_file, filename=filename, media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail=f"File {filename} not found!")


@app.delete("/delete_figure/")
def delete_figure(filename: str):
    """
    Deletes file specified by filename or 404 error if the file does not exist.
    """
    path_to_file = os.path.join(directory, filename)
    if os.path.isfile(path_to_file):
        os.remove(path_to_file)
        return {"message": f"figure {filename} has been deleted"}
    else:
        raise HTTPException(status_code=404, detail=f"File {filename} not found!")


@app.post("/create_points", response_class=StreamingResponse)
def create_points(points: List[ItemColoredPoint]):
    """
    Method creates a point based on the given coordinates in 2D.
    """
    fig, ax = get_fig_base()
    for colored_point in points:
        point = Point(**colored_point.dict())
        point.draw_point(fig, ax, color=colored_point.color, s=colored_point.size)

    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    return StreamingResponse(BytesIO(output.getvalue()), media_type="image/png")


@app.post("/create_line", status_code=201, response_class=StreamingResponse)
def create_line(line: ItemLine, color: Colors = 'black', linewidth: int = 2):
    """
    Method creates a line from the two uploaded points.
    """
    line_dict = line.dict()
    point_1 = Point(**line_dict['starting_point'])
    point_2 = Point(**line_dict['ending_point'])
    line = Line.create_line_from_points(point_1, point_2)

    fig, ax = get_fig_base()
    line.draw_line(fig, ax, color=color, linewidth=linewidth)
    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    return StreamingResponse(BytesIO(output.getvalue()), media_type="image/png")


@app.post("/create_circle", status_code=201, response_class=StreamingResponse)
def create_circle(circle: ItemCircle, color: Colors = 'black', linewidth: int = 2):
    o = Point(**circle.center.dict())
    circle = Circle(o, circle.radius)

    fig, ax = get_fig_base()
    circle.draw(fig, ax, color=color, linewidth=linewidth)
    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    return StreamingResponse(BytesIO(output.getvalue()), media_type="image/png")


@app.post("/calculate_area_circle", response_model=AreaResponse)
def calculate_area_circle(circle: ItemCircle, number_of_points: int = 100, filename: Union[None, str] = None):
    """
    Calculates area of the circle with specified radius. The whole circle should fit in square between 0 and 1
    (required by monte carlo function).
    """

    o = Point(**circle.center.dict())
    min_x = min(o.x, 1-o.x)
    min_y = min(o.y, 1-o.y)
    if not (min_x > circle.radius  and min_y > circle.radius):
        raise HTTPException(status_code=400, detail="Wrong center coordinates! This circle wont fit into unit square")

    o = Point(**circle.center.dict())
    start_time = time.time()
    circle = Circle(o, circle.radius)
    area = calculate_area_monte_carlo(circle, number_of_points, filename=filename)
    time_taken = round(time.time()-start_time, 2)

    if filename:
        path = os.path.join(directory, filename)
        headers = {'figure': filename, "time": str(time_taken), "area": str(area)}
        return FileResponse(path=path, filename=filename, media_type="image/png", headers=headers)
    else:
        return {'figure': 'circle', 'area': area, 'time': time_taken}


@app.post("/calculate_area_poly_from_bytes/")
def calculate_area_poly_from_bytes(file: bytes = File(default=..., description="file to be uploaded"),
                                   number_of_points: int = 100, filename: Union[str, None] = None):
    """
    Calculates area of the polygon build from the specified vertices. The whole polygon should fit in square between 0 and 1
    (required by monte carlo function). This method accepts json file as the input data.
    """
    json_data = json.load(BytesIO(file))
    print(type(file))
    print(json_data)

    start_time = time.time()
    vertices_points = [Point(**v) for v in json_data['vertices']]
    polygon = Polygon(vertices_points)
    area = calculate_area_monte_carlo(polygon, number_of_points, filename=filename)
    time_taken = round(time.time()-start_time, 2)

    if filename:
        path = os.path.join(directory, filename)
        headers = {'figure': json_data['name'], "time": str(time_taken), "area": str(area)}
        return FileResponse(path=path, filename=filename, media_type="image/png", headers=headers)
    else:
        return {'figure': json_data['name'], 'area': area, 'time': time_taken}


@app.post("/calculate_area_poly_from_file/")
def calculate_area_poly_from_file(file: UploadFile, number_of_points: int = 100,
                                  filename: Union[str, None] = None):
    """
    Calculates area of the polygon build from the specified vertices. The whole polygon should fit in square between 0 and 1
    (required by monte carlo function). This method accepts json file as the input data.
    """

    json_data = json.load(file.file)
    print(file.file)
    print(file.content_type)
    print(json_data)

    start_time = time.time()
    vertices_points = [Point(**v) for v in json_data['vertices']]
    polygon = Polygon(vertices_points)
    area = calculate_area_monte_carlo(polygon, number_of_points, filename=filename)
    time_taken = round(time.time()-start_time, 2)

    if filename:
        path = os.path.join(directory, filename)
        headers = {'figure': json_data['name'], "time": str(time_taken), "area": str(area)}
        return FileResponse(path=path, filename=filename, media_type="image/png", headers=headers)
    else:
        return {'figure': json_data['name'], 'area': area, 'time': time_taken}



"""

@app.put("/calculate_area_poly_raw/")
def calculate_area_poly_raw(vertices: Dict[str, ItemPoint]):

    number_of_points = 100
    filename = 'test.png'

    start_time = time.time()
    vertices_points = [Point(**v) for v in vertices]
    polygon = Polygon(vertices_points)
    area = calculate_area_monte_carlo(polygon, number_of_points, filename=filename)
    time_taken = round(time.time()-start_time, 2)

    if filename:
        path = os.path.join(directory, filename)
        headers = {'figure': json_data['name'], "time": str(time_taken), "area": str(area)}
        return FileResponse(path=path, filename=filename, media_type="image/png", headers=headers)
    else:
        return {'figure': json_data['name'], 'area': area, 'time': time_taken}
"""