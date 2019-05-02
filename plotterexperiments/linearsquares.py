from chiplotle import *
import datetime
from PIL import Image
import freetype
from chiplotle.tools.plottertools import instantiate_virtual_plotter
#plotter =  instantiate_virtual_plotter(type="DXY1300")
#plotter.margins.hard.draw_outline()
plotter = instantiate_plotters( )[0]
plotter.clear()
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



####helpers
def max_Xvalue(inputlist):
    return max([sublist[0] for sublist in inputlist])

def min_Xvalue(inputlist):
    return min([sublist[0] for sublist in inputlist])

def max_Yvalue(inputlist):
    return max([sublist[1] for sublist in inputlist])

def min_Yvalue(inputlist):
    return min([sublist[1] for sublist in inputlist])

def sign(filename):
    now = datetime.datetime.now()
    t = shapes.label(str(filename + "    " + now.strftime("%Y-%m-%d %H:%M")),0.15, 0.15, None, None, 'bottom-left')
    transforms.rotate(t, math.radians(90))
    transforms.offset(t, (16000,0))
    plotter.write(t)

def gensquare(xoff,yoff,size,generations):
    gg = []
    plotter.select_pen(1)
    #    size = 10000
    bounds = [(0,0),(0,size),(size,size),(size,0)]
    pointlist = []
    x = random.randint(0,size)
    y = random.randint(0,size)
    pointlist = [[[bounds[0],bounds[1],(x,y)], [bounds[1],bounds[2],(x,y)] , [bounds[2],bounds[3],(x,y)], [bounds[3],bounds[0], (x,y)]]]
    gen = 0
    print("pointlistlength" , len(pointlist))
    for generation in xrange(generations):
    #draw first gen
        for tri in pointlist[generation]:
            g = shapes.group([])
            #plotter.select_pen(generation)
            #print(tri)
            #t = shapes.path(tri)
            #plotter.write(t)
            #calc midpoint
            minmaxY = (min_Yvalue(tri), max_Yvalue(tri))
            minmaxX = (min_Xvalue(tri), max_Xvalue(tri))
    #        print("tri",tri)
     #       print("minmaxY", minmaxY)
     #       print("minmaxX", minmaxX)
            yval = random.randint(minmaxY[0], minmaxY[1])
            divx = (tri[0][1]-tri[1][1])
            if divx == 0:
                x1 = minmaxX[0]
            else:
                x1 = abs((tri[0][0]-tri[1][0])/divx)*yval
            divx = (tri[1][1]-tri[2][1])
            if divx == 0:
                x2 = minmaxX[0]
            else:
                x2 = abs((tri[1][0]-tri[2][0])/divx)*yval
            divx = (tri[2][1]-tri[0][1])
            if divx == 0:
                x3 = minmaxX[0]
            else:
                x3 = abs((tri[2][0]-tri[0][0])/divx)*yval
            #print (x1,x2,x3)
            xbounds = []

            xmin = max(min(minmaxX), min([x1,x2,x3]))
            xmax = min(max(minmaxX), max([x1,x2,x3]))

            # if xmin < 0:
            #     xmin = 0
            if xmax > size:
                xmax = size
            if xmin > size:
                xmin = size

            xbounds = (xmin,xmax)
            if max([tri[0][0], tri[1][0], tri[2][0]]) > size:
                print (tri)
                print ("xbounds", xbounds)
            xval = random.randint(sorted(xbounds)[0], sorted(xbounds)[1])

            #add new generation if not there yet
            if len(pointlist) == generation+1:
                pointlist.append([])
            #calcgen
            #print("pointlistlength" , len(pointlist))

            pointlist[generation+1].append([tri[0],tri[1],(xval,yval)])
            g.append(shapes.path([tri[0],(xval,yval),tri[1]]))
            pointlist[generation+1].append([tri[1],tri[2],(xval,yval)])
            g.append(shapes.path([tri[1],(xval,yval),tri[2]]))
            pointlist[generation+1].append([tri[0],tri[2],(xval,yval)])
            g.append(shapes.path([tri[0],(xval,yval),tri[2]]))
            transforms.offset(g,(xoff,yoff))
            gg.append(g)
        #gen = gen + 1

            #print (pointlist)
    return gg


i = 1
for x in xrange(2):
    for y in xrange(2):
        for g in gensquare(5500*x,5500*y,5000,2):
            plotter.select_pen(i)
            plotter.write(g)
    i = i + 1


#for g in gensquare(0,0,10000,3):
    #plotter.write(g)

sign("linearsquares.py")

io.view(plotter)
