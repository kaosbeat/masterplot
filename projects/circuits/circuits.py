from chiplotle import *
from PIL import Image
import sys
from lib.plothelpers import sign

filename = sys.argv[1]
virtualplotting = sys.argv[2]

#print(virtualplotting)
if (virtualplotting == 'virtual'):
		plotter = instantiate_virtual_plotter(type="DXY1300")
if (virtualplotting == 'real'):
		plotter = instantiate_plotters()[0]
		print("plotting for real")

# plotter.margins.hard.draw_outline()
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



topCoord = []

plotter.select_pen(1)


def drawParallelTops(number, bumps):
    if len(topCoord) == 0:
        x = 0
        y = 10000
        for b in range(bumps):
            topCoord.append((x,y))
            x = x + random.randint(300,500)
            topCoord.append((x,y))
            b = random.randint(100,300)
            y = y + b
            x = x + b
            topCoord.append((x,y))
            x = x + random.randint(300,500)
            topCoord.append((x,y))
            b = random.randint(100,300)
            x = x + b
            y = y - b
            topCoord.append((x,y))
            x = x + random.randint(300,500)
            topCoord.append((x,y))


def recursions(sizex,sizey, depth):
    notdone = True
    g = shapes.group()
    cursizex=sizex
    cursizey=sizey
    curoffset=50
    
    while notdone:
        g.append







r = shapes.rectangle(8000,8000)
transforms.offset(r,(4000,4000))
plotter.write(r)
plotter.write(sign("circuits proto", 8100, 100 ))
io.export(plotter, filename, fmt='jpg')
io.export(plotter, filename, fmt='svg')
io.view(plotter)
