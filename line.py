from math import floor
global p
import blessed
from rich.style import Style
global t
t = blessed.Terminal()
p = []
def plot(x, y, c) :
    r = 255-clamp(int(255*c),0,255)
    g = 255-clamp(int(255*c),0,255)
    b = 255-clamp(int(255*c),0,255)
    #(t.color_rgb(r,g,b)
    p.append([x, y, ('█'),r])

# integer part of x
def ipart(x) :
    return floor(x)

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def round(x) :
    return int(x + 0.5)

# fractional part of x
def fpart(x) :
    return x - floor(x)

def rfpart(x) :
    return 1 - float(x)

def drawLine(x0,y0,x1,y1) :
    global p
    p = []
    steep = abs(y1 - y0) > abs(x1 - x0)

    if steep :
        x0, y0 = y0, x0
        x1,y1 = y1,x1

    if x0 > x1 :
        x0,x1 = x1,x0
        y0,y1 = y1,y0


    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx
    if dx == 0.0 :
        gradient = 1.0


    # handle first endpoint
    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = rfpart(x0 + 0.5)
    xpxl1 = xend # th: will be used in the main loop
    ypxl1 = ipart(yend)
    if steep :
        plot(ypxl1,   xpxl1, rfpart(yend) * xgap)
        plot(ypxl1+1, xpxl1,  fpart(yend) * xgap)
    else:
        plot(xpxl1, ypxl1  , rfpart(yend) * xgap)
        plot(xpxl1, ypxl1+1,  fpart(yend) * xgap)

    intery = yend + gradient # first y-intersection for the main loop

    # handle second endpoint
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = fpart(x1 + 0.5)
    xpxl2 = xend #th: will be used in the main loop
    ypxl2 = ipart(yend)
    if steep :
        plot(ypxl2  , xpxl2, rfpart(yend) * xgap)
        plot(ypxl2+1, xpxl2,  fpart(yend) * xgap)
    else:
        plot(xpxl2, ypxl2,  rfpart(yend) * xgap)
        plot(xpxl2, ypxl2+1, fpart(yend) * xgap)


    # main loop
    if steep :
        for x in range(xpxl1 + 1, xpxl2) :

                plot(ipart(intery)  , x, rfpart(intery))
                plot(ipart(intery)+1, x,  fpart(intery))
                intery = intery + gradient
    else:
        for x in range(xpxl1 + 1, xpxl2) :
                plot(x, ipart(intery),  rfpart(intery))
                plot(x, ipart(intery)+1, fpart(intery))
                intery = intery + gradient
    h = p[:]
    return h

def drawDDA(x1,y1,x2,y2):
  h = []
  x,y = x1,y1
  length = abs((x2-x1)) if abs((x2-x1)) > abs((y2-y1)) else abs((y2-y1))
  if length ==0:
      return [(x1,y1,'█')]
  dx = (x2-x1)/float(length)
  dy = (y2-y1)/float(length)


  h.append([int(x+0.5),int(y+0.5),'█'])

  for i in range(length):
    x += dx
    y += dy
    h.append([int(x+0.5),int(y+0.5),'█'])
  return h

def plotLine(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    D = 2*dy - dx
    y = y0

    for x in range(x0, x1+1):
        print(t.move_xy(int(x),int(y))+'█',end = '')
        if D > 0:
            y = y + 1
            D = D - 2*dx
        D = D + 2*dy

def polygon(f,coords):
    j = []
    prev = ''
    for i,n in enumerate(coords):
        if i==0:
            prev = n
            continue
        h = f(prev[0],prev[1],n[0],n[1])
        j += h
        prev = n
    else:
        h = f(coords[0][0],coords[0][1],prev[0],prev[1])
        j += h
    return j
