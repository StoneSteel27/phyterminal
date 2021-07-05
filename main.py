import pymunk  # Import pymunk..
import blessed
import os
import curses

screen = curses.initscr()
t = blessed.Terminal()
import line
from time import sleep
from functools import reduce
import sys
from prompt_toolkit.formatted_text import ANSI


space = pymunk.Space()  # Create a Space which contain the simulation
space.gravity = 0, -1  # Set its gravity
lines = []
bodies = []
ppm = 1.5
height, width = curses.LINES - 1, curses.COLS - 1
body = pymunk.Body(10, 1)  # Create a Body with mass and moment
body.position = 90, 90  # Set the position of the body
body.name = "h"
body1 = pymunk.Body(1, 1)  # Create a Body with mass and moment
body1.position = 90, 150  # Set the position of the body
body1.name = "h"
bodies.append(body1)
bodies.append(body)
curses.start_color()
curses.use_default_colors()
for i in range(curses.COLORS):
    try:
        curses.init_color(i, i, i, i)
    except Exception as e:
        print(i, curses.COLORS)
        raise Exception(e)
poly = pymunk.Poly.create_box(
    body, size=(20, 10)
)
poly1 = pymunk.Poly.create_box(
    body1, size=(20, 10)
) # Create a box shape and attach to body
b0 = space.static_body
segment = pymunk.Segment(b0, (60, 10), (120, 10), 1)
segment.elasticity = 10
segment.friction = 1
space.add(body, poly)
space.add(body1,poly1)
space.add(segment)  # Add both body and shape to the simulation
lines.append(segment)
print_options = pymunk.SpaceDebugDrawOptions()  # For easy printing

vertices_poly = lambda body: [
    p.rotated(body.angle) + body.position for p in list(body.shapes)[0].get_vertices()
]
vertices_line = lambda line: [
    line.body.position + line.a.rotated(line.body.angle),
    line.body.position + line.b.rotated(line.body.angle)
]

height, width = curses.LINES - 1, curses.COLS - 1

print(space.bodies)

for i in range(5000):
    for body in bodies:
        vert = vertices_poly(body)
        vert = [v / ppm for v in vert]
        vert = [(int(v[0]*2), height - int(v[1])) for v in vert]
        # print(vert)
        j = line.polygon(line.drawDDA, vert)

        for i in j:
            if (i[0] > width or i[1] > height) or (i[0] < 0 or i[1] < 0):
                continue
            else:
                try:
                    screen.addch(i[1], i[0], (i[2]))
                except Exception as e:
                    print(i, height, width)
                    raise Exception(e)
    for i in lines:
        vert = vertices_line(i)
        vert = [v / ppm for v in vert]
        vert = [(int(v[0]*2), height - int(v[1])) for v in vert]
        j = line.drawDDA(vert[0][0], vert[0][1], vert[1][0], vert[1][1])
        for i in j:
            if (i[0] > width or i[1] > height) or (i[0] < 0 or i[1] < 0):
                continue
            else:
                try:
                    screen.addch(i[1], i[0], i[2])
                except Exception as e:
                    print(i, height, width)
                    raise Exception(e)

    screen.refresh()
    space.step(0.03)
    screen.clear()

    # Infinite loop simulation

curses.endwin()
