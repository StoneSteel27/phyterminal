from typing import Callable, Iterable


class Shape:
    """The main Shape drawing class"""

    def __init__(self, pixel_drawing_func: Callable):
        self.pixel_drawing_func = pixel_drawing_func

    def polygon(self, coords: list[int, int]) -> None:
        """Draws a polygon using the given pixel_drawing_func"""
        prev = ""
        for i, n in enumerate(coords):
            if i == 0:
                prev = n
                continue
            self.line((prev[0], prev[1]), (n[0], n[1]))
            prev = n
        else:
            self.line((coords[0][0], coords[0][1]), (prev[0], prev[1]))

    def line(self, point1: list[int, int], point2: list[int, int]) -> None:
        """Draws a line using the given pixel_drawing_func"""
        x1, y1 = point1
        x2, y2 = point2
        x, y = x1, y1
        length = abs((x2 - x1)) if abs((x2 - x1)) > abs((y2 - y1)) else abs((y2 - y1))
        if length == 0:
            self.pixel_drawing_func(x1, y1)
        dx = (x2 - x1) / float(length)
        dy = (y2 - y1) / float(length)

        self.pixel_drawing_func(int(x + 0.5), int(y + 0.5))
        for i in range(length):
            x += dx
            y += dy
            self.pixel_drawing_func(int(x + 0.5), int(y + 0.5))

    def ellipse(self, rx: int, ry: int, xc: int, yc: int) -> None:
        """Draws a ellipse using the given pixel_drawing_func"""
        x = 0
        y = ry

        # Initial decision parameter of region 1
        d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
        dx = 2 * ry * ry * x
        dy = 2 * rx * rx * y

        # For region 1
        while dx < dy:

            # Print points based on 4-way symmetry
            self.pixel_drawing_func(x + xc, y + yc)
            self.pixel_drawing_func(-x + xc, y + yc)
            self.pixel_drawing_func(x + xc, -y + yc)
            self.pixel_drawing_func(-x + xc, -y + yc)

            # Checking and updating value of
            # decision parameter based on algorithm
            if d1 < 0:
                x += 1
                dx = dx + (2 * ry * ry)
                d1 = d1 + dx + (ry * ry)
            else:
                x += 1
                y -= 1
                dx = dx + (2 * ry * ry)
                dy = dy - (2 * rx * rx)
                d1 = d1 + dx - dy + (ry * ry)
        # Decision parameter of region 2
        d2 = (
            ((ry * ry) * ((x + 0.5) * (x + 0.5)))
            + ((rx * rx) * ((y - 1) * (y - 1)))
            - (rx * rx * ry * ry)
        )

        # Plotting points of region 2
        while y >= 0:

            # printing points based on 4-way symmetry
            self.pixel_drawing_func(x + xc, y + yc)
            self.pixel_drawing_func(-x + xc, y + yc)
            self.pixel_drawing_func(x + xc, -y + yc)
            self.pixel_drawing_func(-x + xc, -y + yc)

            # Checking and updating parameter
            # value based on algorithm
            if d2 > 0:
                y -= 1
                dy = dy - (2 * rx * rx)
                d2 = d2 + (rx * rx) - dy
            else:
                y -= 1
                x += 1
                dx = dx + (2 * ry * ry)
                dy = dy - (2 * rx * rx)
                d2 = d2 + dx - dy + (rx * rx)
