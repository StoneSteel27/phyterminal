import pymunk
import curses
import numpy as np
from keys import KBHit
import time


class Body(pymunk.Body):
    bodies = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bodies.append(self)

    def vertices(self):
        if hasattr(self, "shapes") and len(self.shapes) != 0:
            return [
                p.rotated(self.angle) + self.position
                for p in list(self.shapes)[0].get_vertices()
            ]
        else:
            return False


class Segment(pymunk.Segment):
    segments = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(self)

    def vertices(self):
        return [
            self.body.position + self.a.rotated(self.body.angle),
            self.body.position + self.b.rotated(self.body.angle),
        ]


class Renderer:
    def __init__(self, space, meters_per_pixel):
        self.meters_per_pixel = meters_per_pixel
        self._world = np.array([[""] * 1000] * 1000)
        self.space = space
        self.kb = KBHit()
        self.screen = curses.initscr()
        self.height = curses.LINES - 1
        self.width = curses.COLS - 1
        print_options = pymunk.SpaceDebugDrawOptions()

    def set_world(self, index, value):
        try:
            self._world[index] = value
        except IndexError:
            pass

    def drawDDA(self, x1, y1, x2, y2):
        h = []
        x, y = x1, y1
        length = abs((x2 - x1)) if abs((x2 - x1)) > abs((y2 - y1)) else abs((y2 - y1))
        if length == 0:
            self.world[y1, x1]
        dx = (x2 - x1) / float(length)
        dy = (y2 - y1) / float(length)

        self.set_world((int(y + 0.5), int(x + 0.5)), "█")

        for i in range(length):
            x += dx
            y += dy
            self.set_world((int(y + 0.5), int(x + 0.5)), "█")

    def polygon(self, f, coords):
        prev = ""
        for i, n in enumerate(coords):
            if i == 0:
                prev = n
                continue
            f(prev[0], prev[1], n[0], n[1])
            prev = n
        else:
            f(coords[0][0], coords[0][1], prev[0], prev[1])

    def body_frame_coords(self):
        for i in Body.bodies:
            if vertices := i.vertices():
                vert = vertices
                vert = [v / self.meters_per_pixel for v in vert]
                vert = [(int(v[0] * 2), self.height - int(v[1])) for v in vert]
                self.polygon(self.drawDDA, vert)

    def segment_frame_coords(self):
        for i in Segment.segments:
            if vertices := i.vertices():
                vert = vertices
                vert = [v / self.meters_per_pixel for v in vert]
                vert = [(int(v[0] * 2), self.height - int(v[1])) for v in vert]
                self.drawDDA(vert[0][0], vert[0][1], vert[1][0], vert[1][1])

    def run_world(self):
        while True:
            if self.kb.kbhit():
                c = self.kb.getch()
                if ord(c) == 27:  # ESC
                    curses.endwin()
                    break
            self.segment_frame_coords()
            self.body_frame_coords()
            ys, xs = np.where(self._world[: self.height + 1, : self.width + 1] == "█")
            for y, x in zip(ys, xs):
                self.screen.addch(y, x, "█")
                self.set_world((y, x), "")
            # self._world = np.array([['']*1000]*1000)
            self.screen.refresh()
            self.space.step(0.1)
            self.screen.clear()


if __name__ == "__main__":
    space = pymunk.Space()
    space.gravity = 0, -1

    def create_box(m, x, y, l, b):
        body1 = Body(m, 1)
        body1.position = x, y
        poly = pymunk.Poly.create_box(body1, size=(l, b))
        space.add(body1, poly)

    create_box(10, 90, 90, 10, 10)
    create_box(1, 90, 150, 10, 10)
    create_box(1, 90, 200, 10, 10)
    b0 = space.static_body
    segment = Segment(b0, (60, 10), (120, 10), 1)
    segment.elasticity = 1.0
    segment.friction = 1.0
    space.add(segment)

    a = Renderer(space, 1.5)
    a.run_world()
