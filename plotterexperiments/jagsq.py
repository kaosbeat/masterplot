from chiplotle import *
from PIL import Image

from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")
plotter.margins.hard.draw_outline()
# plotter = instantiate_plotters( )[0]
# real plotter says
#    Drawing limits: (left 0; bottom 0; right 16158; top 11040)

pltmax = [16158, 11040]
#coords = plotter.margins.soft.all_coordinates
# plotter.select_pen(1)
b = 0

# viewport = (10320,7920)
# horizon = (viewport[0] / 2, viewport[1] / 2)

import math
import random
import numpy as np
from scipy import signal
# from texttools  import *
import freetype





plotter.select_pen(1)





def dosquare1():
    l = shapes.group([])
    size = 1000
    x = 0
    y = 0
    dx = size
    dy = size
    xvec = [-1,1]
    yvec = [-1,1]


    for i in xrange(10):
        print x,y
        #horizontal/vertical/diagonal?
        direc = random.randint(0,10)

        if direc < 5:  #horizontal
            sign = random.randint(0,1)
            dy = 0
            if sign == 0:
                if x == 0:
                    x = 1
                dx = -random.randint(0,x)
            else:
                if x == size:
                    x = size - 1
                dx = random.randint(0,size-x)


        if  4 < direc < 8: #vertical
            sign = random.randint(0,1)
            dx = 0
            if sign == 0:
                if y == 0:
                    y = 1
                dy = -random.randint(0,y)
            else:
                if y == size:
                    y = size - 1
                dy = random.randint(0,size-y)

        if direc > 8: #diagonal
            signh = random.randint(0,1)
            signv = random.randint(0,1)
            dx = random.randint(x,size)
            dy = random.randint(y,size)



        print x,y
        print dx,dy
        l.append(shapes.line((x,y),(x+dx,y+dy)))
        x=dx
        y=dy
        plotter.write(l)

#dosquare1()

def dosquare2(depth,size,xoff,yoff):
    l = shapes.group([])

    #size = 250
    x = 0
    dx = 0
    y = 0
    dy = 0
    pa = [(x,y)]
    for i in xrange(depth):
        h = random.randint(0,2)
        v = random.randint(0,2)
        if h == 1:
            dx = random.randint(0,size)
        if v == 1:
            dy = random.randint(0,size)
        #print((x,y),(dx,dy))
        pa.append((dx,dy))
        #l.append(shapes.line((x,y),(dx,dy)))
        x = dx
        y = dy
    p = shapes.path(pa)
    transforms.offset(p, (xoff, yoff))
    plotter.write(p)


#for x in xrange(20):
#    for y in xrange(20):
        #dosquare2((x+1)*3,450, x*500, y*500)

        #pass


def image2droodle(img):
    img = Image.open(img).convert('L')  # convert image to 8-bit grayscale
    WIDTH, HEIGHT = img.size
    data = list(img.getdata()) # convert image data to a list of integers
    # convert that to 2D list (list of lists of integers)
    data = [data[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]
    # At this point the image's pixels are all in memory and can be accessed
    # individually using data[row][col].
    # For example:
    y=0
    space = 10000/img.size[0]
    for row in data:
        y = y+1
        x = 0
        for val in row:
            print("about to plot")
            #print(' '.join('{:3}'.format(value) for x,value in row))
            dosquare2((255-val)/5+3,int(0.9*space) ,x*space,y*space)
            x = x+1

    # Here's another more compact representation.
    #chars = '@%#*+=-:. '  # Change as desired.
    #scale = (len(chars)-1)/255.
    #print()
    #for row in data:
    #    print(' '.join(chars[int(value*scale)] for value in row))


image2droodle('smalpic.png')

io.view(plotter)
