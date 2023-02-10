import os
import numpy as np
from fastapi.testclient import TestClient
from app.main_v2 import app

#path = pathlib.PurePath(os.path.abspath(__file__))
#if path.parent.name == 'tests':
os.chdir('../')


client = TestClient(app)


def test_get_figure_good():
    response = client.get("/get_figure/circle.png")
    assert response.status_code == 200


def test_get_figure_bad():
    response = client.get("/get_figure/ellipse.png")
    assert response.status_code == 404


def test_circle_good():
    radius = 0.25
    area = np.pi * radius ** 2
    response = client.post("/calculate_area_circle/?number_of_points=500",
                           json={
                               "center": {
                                   "name": "O",
                                   "x": 0.5,
                                   "y": 0.5
                               },
                               "radius": radius
                           })
    assert response.status_code == 200
    assert area * 0.8 < response.json()['area'] < area * 1.2


def test_circle_bad():
    response = client.post("/calculate_area_circle",
                           json={
                               "center": {
                                   "name": "O",
                                   "x": 0.2,
                                   "y": 0.2
                               },
                               "radius": 0.25
                           })
    assert response.status_code == 400
