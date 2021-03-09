from chiplotle import *
from chiplotle.tools.io import export
from chiplotle.tools.plottertools import instantiate_virtual_plotter
import sys
import uuid


from chiplotle import *
from chiplotle.tools.io import export
from chiplotle.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from chiplotle.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from chiplotle.geometry.core.label import Label
from chiplotle.core.interfaces.interface import _Interface
from chiplotle.plotters.margins.marginssoft import MarginsSoft
from chiplotle.plotters.margins.marginshard import MarginsHard
from lib.plothelpers import sign, plotgroup, plotgroupnew
from lib.texttools import writeword
# from lib.perlin import writeword
import sys
import random
import math
from noise import pnoise1, pnoise2, pnoise3

plotPlotterOutline = False
plotPaperOutline = True
plotDrawingOutline = False
pltmax = [16158, 11040]
plotunit = 0.025 # 1 coordinate unit per plotter = 0.025 mm
papersize = [200,200]
plotzone = [(0/plotunit, 0/plotunit), (200/plotunit, 200/plotunit)]


filename = sys.argv[1]
virtualplotting = sys.argv[2]
#print(virtualplotting)
if (virtualplotting == 'virtual'):
		plotter = instantiate_virtual_plotter(type="DXY1300")

if (virtualplotting == 'real'):
		plotter = instantiate_plotters()[0]
		print("plotting for real")

if (plotPlotterOutline):
    plotter.select_pen(3)
    bounds = shapes.rectangle(pltmax[0],pltmax[1])
    transforms.offset(bounds,(pltmax[0]/2,pltmax[1]/2))

    plotter.write(bounds)

if (plotPaperOutline):
    plotter.select_pen(4)
    paper = shapes.rectangle(papersize[0]/plotunit, papersize[1]/plotunit)
    transforms.offset(paper,(papersize[0]/plotunit/2,papersize[1]/plotunit/2))
    plotter.write(paper)


def setSeed(): ####needs to be written to tmp file in order to save at in git
    seed = uuid.uuid1()
    f= open("tmp/seed.txt","w+")
    f.write(str(seed))
    f.close()
    return seed

def drawMintLines(size, seed, interx, intery, xnoise, ynoise):
    random.seed(seed)
    f = shapes.group([])
    
    for x in xrange(0,size):
        points = []
        g = shapes.group([])
        normx = x/float(size)
        # if (x == 5):
        #     print(x, size, normx)
        #     print(math.asin(normx))
        for y in xrange(0,size):          
            # if (x < size*0.4 or x > size*0.6):
            #     xn = 0
            #     yn = 0
            # # if (y < size*0.1 or y > size*0.9):
            # #     yn = 0
            # else: 
            #     xn = xnoise
            #     yn = ynoise
            yoff = math.cos(math.asin(normx))*size/2
            ybuf = (size/2 - yoff)
            if ((y < ybuf ) or y > size-ybuf) :
                xn = xnoise
            else:
                    xn = 0
            yn = xn
            xpos = x*interx + random.random() * xn
            ypos = y*intery + random.random() * yn
            # if (x == 12):
            #     print(y, size*0.1)
            #     print(xpos,ypos, ynoise)
            points.append((xpos,ypos))     
        g.append(shapes.path(points))
        f.append(g)

    return f







plotter.select_pen(1)
seed = setSeed()
plot = drawMintLines(100,seed,50,50,300,30)
# "center and scale"

plotter.write(plotgroupnew(plot, plotzone, 1.3))

plotter.select_pen(2)
plotter.write(sign('minting' +  str(seed) , 7580, 50))

io.export(plotter, "tmp/out2" , fmt='jpg')
io.view(plotter)
