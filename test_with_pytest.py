import numpy as np
import pytest
PI = np.pi
atol = 1e-12

from figures import Point, Line, Polygon, Circle



def test_create_line_from_points_1():
    p1 = Point('p1', 0, -0.2)
    p2 = Point('p2', 0.6, 0)
    line = Line.create_line_from_points(p2, p1)
    assert np.isclose(line.intercept, -0.2)
    assert np.isclose(line.slope, 1/3)

    
def test_create_line_from_points_2():
    p1 = Point('p1', 0.1, 0.3)
    p2 = Point('p2', 0.3, 0.1)
    line = Line.create_line_from_points(p1, p2)
    assert np.isclose(line.intercept, 0.4)
    assert np.isclose(line.slope, -1)
    
    
def test_create_line_from_points_3():
    p1 = Point('p1', 0.5, 0.2)
    p2 = Point('p2', 0.5, 0.4)
    line = Line.create_line_from_points(p2, p1)
    assert np.isinf(line.slope)
    assert np.isnan(line.intercept)

    
def test_get_crossing_point_1():
    
    a = Point('A', 1.0, 0.4)
    b = Point('B', 0.2, 0.0)
    c = Point('C', 0.4, 0.6)
    d = Point('D', 0.2, 1.0)
    
    line_AB = Line.create_line_from_points(a,b)
    line_CD = Line.create_line_from_points(c,d)
    crossing_point_AB_CD = line_AB.get_crossing_point(line_CD)
    assert crossing_point_AB_CD == Point('', 0.6, 0.2)

    
    
def test_get_crossing_point_2():
    a = Point('A', 1, 0) 
    b = Point('B', 0, 0)
    c = Point('C', 0.6, 0.2)
    d = Point('D', 0.6, 0.9)
    line_AB = Line.create_line_from_points(a,b)
    line_CD = Line.create_line_from_points(c,d)
    crossing_point_AB_CD = line_AB.get_crossing_point(line_CD)
    assert crossing_point_AB_CD == Point('', 0.6, 0.0)

def test_is_point_in_line_1():
    a = Point('A', 1, 0) 
    b = Point('B', 0, 0)
    c = Point('C', 0.6, 0.2)
    d = Point('D', 0.6, 0.9)
    p = Point('', 0.6, 0.0) 
    line_AB = Line.create_line_from_points(a,b)
    line_CD = Line.create_line_from_points(c,d)
    assert line_AB.is_point_in_line(p) == True
    assert line_CD.is_point_in_line(p) == False
    
def test_is_point_in_line_2():
    a = Point('A', 0.3, 0.0) 
    b = Point('B', 0.0, 0.0)
    c = Point('C', 0.6, 0.0)
    d = Point('D', 0.6, 0.9)
    p = Point('', 0.6, 0.0) 
    line_AB = Line.create_line_from_points(a,b)
    line_CD = Line.create_line_from_points(c,d)
    assert line_AB.is_point_in_line(p) == False
    assert line_CD.is_point_in_line(p) == True  

def test_convex():   
    a = Point('A', 0.2, 0.9)
    b = Point('B', 0.7, 0.6)
    c = Point('C', 0.5, 0.2)
    d = Point('D', 0.2, 0.2)
    polygon_convex = Polygon([a,b,c,d])
    assert polygon_convex.is_convex() == True

def test_concave():
    a = Point('A', 1, 0)
    b = Point('B', 0.2, 0.9)
    c = Point('C', 0.7, 0.6)
    d = Point('D', 0, 0)
    e = Point('E', 0.5, 0.2)
    polygon_concave = Polygon([a,b,c,d,e])
    assert polygon_concave.is_convex() == False
    
    

