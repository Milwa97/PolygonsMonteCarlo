import matplotlib.pyplot as plt
import numpy as np

PI = np.pi
atol = 1e-12


class Point:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.r = np.sqrt(x ** 2 + y ** 2)
        self.phi = round(np.arcsin(y / self.r) * 360 / (2 * PI), 2) if self.r > 0 else 0

    def get_distance(self, p):
        return np.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)

    def get_relative_angle(self, p):
        relative_x = p.x - self.x
        relative_y = p.y - self.y
        return np.angle(relative_x + 1j * relative_y, deg=True)

    def draw_point(self, fig, ax, **kwargs):
        ax.scatter(self.x, self.y, **kwargs)
        ax.text(self.x, self.y, self.name, size=12, ha='right', va='bottom')

    def __eq__(self, p):
        if np.isclose(self.x, p.x, atol=atol) and np.isclose(self.y, p.y, atol=atol):
            return True
        return False

    def __repr__(self):
        if self.name:
            return f"{self.name}=({self.x}, {self.y})"
        else:
            return f"({self.x}, {self.y})"


class Line:

    def __init__(self, slope, intercept, starting_point=None, ending_point=None):
        self.name = "line_" + starting_point.name + ending_point.name if (starting_point and ending_point) else "line"
        self.slope = slope
        self.intercept = intercept
        self.starting_point = starting_point
        self.ending_point = ending_point

    @classmethod
    def create_line_from_points(cls, starting_point, ending_point):
        if ending_point.x == starting_point.x:
            slope = np.inf
            intercept = np.NAN
        else:
            slope = (ending_point.y - starting_point.y) / (ending_point.x - starting_point.x)
            intercept = starting_point.y - slope * starting_point.x
        return cls(slope, intercept, starting_point, ending_point)

    def get_length(self):
        delta_x = self.starting_point.x - self.ending_point.x
        delta_y = self.starting_point.y - self.ending_point.y
        return np.round(np.sqrt(delta_x ** 2 + delta_y ** 2), 4)

    def get_relative_angle(self, line):
        if self.slope == line.slope:
            return None

    def get_crossing_point(self, line):
        if self.slope == line.slope:
            return None
        elif np.isinf(line.slope):
            x = line.starting_point.x
            y = self.slope * x + self.intercept
        elif np.isinf(self.slope):
            x = self.starting_point.x
            y = line.slope * x + line.intercept
        else:
            x = -(self.intercept - line.intercept) / (self.slope - line.slope)
            y = self.slope * x + self.intercept
        return Point("CP", x, y)

    def get_line_to_point(self, p):
        if np.isinf(self.slope):
            ending_point = Point("", self.starting_point.x, p.y)
        elif self.slope == 0:
            ending_point = Point("", p.x, self.intercept)
        else:
            slope = -1 / self.slope
            intercept = p.y - slope * p.x
            perpendicular_line = Line(slope, intercept)
            ending_point = self.get_crossing_point(perpendicular_line)
        return Line.create_line_from_points(p, ending_point)

    def is_point_in_line(self, p):

        min_x = min(self.starting_point.x, self.ending_point.x)
        max_x = max(self.starting_point.x, self.ending_point.x)
        min_y = min(self.starting_point.y, self.ending_point.y)
        max_y = max(self.starting_point.y, self.ending_point.y)

        if np.isinf(self.slope) and np.isclose(p.x, min_x) and min_y <= p.y <= max_y:
            return True
        elif self.slope == 0.0 and np.isclose(p.y, min_y) and min_x <= p.y <= max_x:
            return True

        elif not np.isclose(p.x * self.slope + self.intercept, p.y, atol=atol):
            return False

        elif not (min_x <= p.x <= max_x):
            return False
        return True

    def draw_line(self, fig, ax, **kwargs):
        x_values = [self.starting_point.x, self.ending_point.x]
        y_values = [self.starting_point.y, self.ending_point.y]
        ax.plot(x_values, y_values, **kwargs)

    def __repr__(self):
        return self.name


class Figure:

    def __init__(self):
        raise NotImplementedError("Subclasses should implement this!")

    def is_point_inside(self, p):
        raise NotImplementedError("Subclasses should implement this!")

    def draw(self):
        raise NotImplementedError("Subclasses should implement this!")

    def get_area(self):
        raise NotImplementedError("Subclasses should implement this!")


class Circle(Figure):

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def is_point_inside(self, p):
        if ((p.x - self.center.x) ** 2 + (p.y - self.center.y) ** 2) < self.radius ** 2:
            return True
        return False

    def get_circumference(self):
        return 2 * PI * self.radius

    def get_area(self):
        return PI * self.radius ** 2

    def draw(self, fig, ax, **kwargs):
        phi = np.linspace(0, 2 * PI, 1000)
        x = np.sin(phi) * self.radius + self.center.x
        y = np.cos(phi) * self.radius + self.center.y
        ax.plot(x, y, **kwargs)
        self.center.draw_point(fig, ax, color='black')

    def __repr__(self):
        return f"circle ({self.center}, {self.radius})"


class Polygon(Figure):

    def __init__(self, vertices):
        if len(vertices) < 3:
            return None
        self.number_of_vertices = len(vertices)
        self.vertices, self.edges = self.create_vertices_and_edges(vertices)
        self.left_border = min([p.x for p in self.vertices])
        self.right_border = max([p.x for p in self.vertices])
        self.bottom_border = min([p.y for p in self.vertices])
        self.top_border = max([p.y for p in self.vertices])

    def create_vertices_and_edges(self, vertices):
        first_verticle = min(vertices, key=lambda p: p.r)
        vertices_sorted = sorted(vertices, key=lambda v: first_verticle.get_relative_angle(v))
        vertices_sorted.remove(first_verticle)
        vertices_sorted = [first_verticle] + vertices_sorted + [first_verticle]
        edges = [Line.create_line_from_points(vertices_sorted[i], vertices_sorted[i + 1])
                 for i in range(self.number_of_vertices)]
        return vertices_sorted[:-1], edges

    def is_convex(self):
        for i in range(self.number_of_vertices):
            relative_angles = np.array([self.vertices[i].get_relative_angle(self.vertices[j])
                                        for j in range(i + 1, self.number_of_vertices)])
            if np.any(relative_angles[1:] - relative_angles[:-1] < 0):
                return False
        return True


    def is_point_inside(self, p):

        if self.left_border < p.x < self.right_border and self.bottom_border < p.y < self.top_border:
            for vertex in self.vertices:
                line = Line.create_line_from_points(p, vertex)
                for edge in self.edges:
                    crossing_point = line.get_crossing_point(edge)
                    if (edge.is_point_in_line(crossing_point) and
                            line.is_point_in_line(crossing_point) and
                            crossing_point not in self.vertices):
                        return False
            return True
        else:
            return False

    def get_perimeter(self):
        return round(sum(edge.get_length() for edge in self.edges), 2)

    def draw(self, fig, ax, pointcolor='black', linecolor='black'):
        for line in self.edges:
            line.draw_line(fig, ax, **{'color': linecolor})
        for point in self.vertices:
            point.draw_point(fig, ax, **{'color': pointcolor})

    def __repr__(self):
        return ", ".join([str(v) for v in self.vertices])
