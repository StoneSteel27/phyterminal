import curses
import threading
from typing import Any, Iterable, Union

import numpy as np
import pymunk
from keys import KBHit

from shape import Shape


def vertices(obj: Any) -> Union[list[pymunk.Vec2d], bool]:
    """
    Returns vertices of a polygon or a segment

    Returns the vertices of the object passed into the function,
    if the object is a pymunk.shapes.Poly or pymunk.Segment objects

    :param obj: object of pymunk.shapes.Poly or pymunk.Segment
    :return: list of coordinates, if found and object is vaild, else False
    """
    if isinstance(obj, pymunk.shapes.Poly):
        return [
            p.rotated(obj.body.angle) + obj.body.position for p in obj.get_vertices()
        ]
    elif isinstance(obj, pymunk.Segment):
        return [
            obj.body.position + obj.a.rotated(obj.body.angle),
            obj.body.position + obj.b.rotated(obj.body.angle),
        ]
    else:
        return False


class Renderer:
    """The main rendering class for phyterminal"""

    def __init__(
        self, space: pymunk.space, meters_per_pixel: float, threaded_world: bool = False
    ):
        self.shape = Shape(pixel_drawing_func=self.set_world)
        self.meters_per_pixel = meters_per_pixel
        self._world = np.array([[""] * 1000] * 1000)
        self.space = space
        self.kb = KBHit()
        self.screen = curses.initscr()
        self.height = curses.LINES - 1
        self.width = curses.COLS - 1
        self.threaded_world = threaded_world

        # self.screen.timeout(0)

    def set_world(self, x: int, y: int, value: str = "█") -> None:
        """
        Sets the index of given index to the value

        :param x y: index to be changed to the given value in world numpy array
        :param value: the value to be set in the world numpy array
        """
        try:
            self._world[y,x] = value
        except IndexError:
            pass

    def body_frame_coords(self) -> None:
        """Calculating and Drawing objects on the screen from coordinates"""
        for i in self.space.shapes:
            if (
                (vertices1 := vertices(i))
                and (isinstance(i, pymunk.shapes.Poly))
                and getattr(i, "visible", True)
            ):
                # print(vertices1)
                vert = vertices1
                vert = [v / self.meters_per_pixel for v in vert]
                vert = [(int(v[0] * 2), self.height - int(v[1])) for v in vert]
                self.shape.polygon(vert)
            elif (
                (vertices1 := vertices(i))
                and (isinstance(i, pymunk.Segment))
                and getattr(i, "visible", True)
            ):
                vert = vertices1
                vert = [v / self.meters_per_pixel for v in vert]
                vert = [(int(v[0] * 2), self.height - int(v[1])) for v in vert]
                self.shape.line((vert[0][0], vert[0][1]), (vert[1][0], vert[1][1]))

    def run_world(self) -> None:
        """
        Runs the simulation

        Starts the physics simulations, and the rendering of the physics objects.
        Can be in threaded mode for interactions with the simulation
        """

        def threaded():  # noqa: ANN201
            while True:
                if self.kb.kbhit():
                    self.c = self.kb.getch()
                    if ord(self.c) == 27:
                        self.stop = True  # ESC
                        curses.endwin()
                        break
                self.body_frame_coords()
                ys, xs = np.where(
                    self._world[: (curses.LINES - 1), : (curses.COLS - 1)] == "█"
                )
                # print((curses.LINES - 1),(curses.COLS - 1))
                for y, x in zip(ys, xs):
                    self.screen.addch(y, x, "█")
                    self.set_world(x,y, "")
                # self._world = np.array([['']*1000]*1000)
                # key = self.screen.getch()
                # self.stringer(0,0,'mx, my = %i,%i,%i \r'%(mx,my,b))
                # self.space.bodies
                self.screen.refresh()
                self.space.step(1 / 50)
                self.screen.clear()

        if self.threaded_world:
            threading.Thread(target=threaded).start()
        else:
            threaded()


if __name__ == "__main__":
    space = pymunk.Space()
    space.gravity = 0, -10

    def create_box(mass, pos_x, pos_y, lenght, breath):  # noqa: ANN001,ANN201
        """Just creates some boxes"""
        body1 = pymunk.Body(mass, 1)
        body1.position = pos_x, pos_y
        poly = pymunk.Poly.create_box(body1, size=(lenght, breath))
        space.add(body1, poly)

    create_box(10, 90, 90, 10, 10)
    create_box(1, 90, 150, 10, 10)
    create_box(1, 90, 200, 10, 10)
    b0 = space.static_body
    segment = pymunk.Segment(b0, (-120, 10), (240, 10), 1)
    # segment.elasticity = 1.0
    segment.friction = 1.0
    space.add(segment)

    a = Renderer(space, 1.5, threaded_world=False)
    # threading.Thread(target=a.mouser).start()
    a.run_world()
