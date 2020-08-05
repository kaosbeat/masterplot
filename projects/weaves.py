from chiplotle import *
from chiplotle.tools.io import export
from PIL import Image
import math
import sys
from lib.plothelpers import sign

from chiplotle.tools.plottertools import instantiate_virtual_plotter
virtualplotting = sys.argv[2]

#print(virtualplotting)
if (virtualplotting == 'virtual'):
		plotter = instantiate_virtual_plotter(type="DXY1300")
if (virtualplotting == 'real'):
		plotter = instantiate_plotters()[0]
		print("plotting for real")


#plotter = instantiate_plotters( )[0]
# real plotter says
#    Drawing limits: (left 0; bottom 0; right 16158; top 11040)
# plotter.select_pen(3)
# plotter.margins.hard.draw_outline()

pltmax = [16158, 11040]
bounds =shapes.rectangle(pltmax[0],pltmax[1])
transforms.offset(bounds,(pltmax[0]/2,pltmax[1]/2) )
plotter.select_pen(3)
plotter.write(bounds)
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


#image2droodle('smalpic.png')



def brokencircle (x,y, num, decay, segs, size):
    s = 2*math.pi/segs
    for i in xrange(num):
        c = shapes.group([])
        d = random.randint(1,segs)
        e = 0
        while e < segs:
            g = random.randint(0,segs/d)
            seg = shapes.arc_circle(size*math.pow(decay,i), s*e, s*(e+g), segs, '2PI')
            e = e + g + g/2
            c.append(seg)

        transforms.offset(c, (x+random.randint(0,size/20),y+random.randint(0,size/20)))
        plotter.write(c)



def brokenrotatedcircle (x,y, num, decay, segs, size):
    s = 2*math.pi/segs
    for i in xrange(num):
        c = shapes.group([])
        d = random.randint(1,int(segs/20))
        e = 0
        while e < segs:
            g = random.randint(0,segs/d)
            seg = shapes.arc_circle(size*math.pow(decay,i), s*e, s*(e+g), segs, '2PI')
            e = e + g + g/2
            c.append(seg)
        transforms.rotate(c, math.degrees(360/segs/num*i))
        transforms.offset(c, (x+random.randint(0,size/20),y+random.randint(0,size/20)))
        plotter.write(c)



plotter.select_pen(2)
size = 4500
#brokencircle(1.1*size+500,1.1*size+800, 40 ,0.993, 130, size)
#brokenrotatedcircle(size/2,size/2, 40 , 0.92, 8, size)

x= 40
y=0
#brokenrotatedcircle(size/2+2500,size/2+2500, 49 + 20*y , 0.978, 10 + x + 2*y, size)

size = 2500
for x in xrange(3):
    for y in xrange(2):
        #brokenrotatedcircle(2.1*size*x+size+150,2.1*size*y+size+150, 20 + 20*y , 0.9 + x/111 +y/111, 8 + x + 2*y, size)
        pass


# def noisestudy():
#     for x in xrange(10):
#         for y in xrange(10):
#             for z in xrange(10):

def weave(size):
    g = shapes.group([])
    for x in xrange(30):
        for y in xrange(x):
            xpos = x*4*size + y*size*y 
            ypos = x*y*0.1*size + y*6*size
            rect = shapes.rectangle(2*size+(5*x),3*size+(2*y))
            line = shapes.line((xpos,ypos),(xpos+random.random()*100,ypos+100))
            # transforms.rotate(line, random.random()*3.14)
            transforms.rotate(rect, x*3)
            transforms.offset(rect, (xpos,ypos))
            g.append(rect)
            g.append(line)
    # transforms.rotate(g, math.degrees(180))
    plotter.write(g)

weave(50)


export(plotter, sys.argv[1], fmt='jpg')
plotter.write(sign('weaves.py'))
export(plotter, sys.argv[1], fmt='svg')
io.view(plotter)


