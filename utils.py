#! /usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from figures import Point

def get_fig_base():
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(color='gray', alpha = 0.4)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    return fig, ax


def calculate_area_monte_carlo(figure, number_of_points, draw_final_result):
    
    coordinates = np.random.uniform(size=(number_of_points, 2))
    points = [Point('', x, y) for i, (x,y) in enumerate(coordinates)]
    points_inside_figure = list(filter(lambda p: figure.is_point_inside(p), points))
    area = len(points_inside_figure)/number_of_points
    
    if draw_final_result:
        fig, ax = get_fig_base()
        figure.draw(fig, ax)
        for p in points:
            if p in points_inside_figure:
                p.draw_point(fig, ax, color='green', s=5)
            else:
                p.draw_point(fig, ax, color='red', s=5)
        
    return area