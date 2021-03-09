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
from lib.plothelpers import sign, plotgroup
from lib.texttools import writeword
# from lib.perlin import writeword
import sys
import random
import math
from noise import pnoise1, pnoise2, pnoise3


print("hello")

filename = sys.argv[1]
virtualplotting = sys.argv[2]
#print(virtualplotting)
if (virtualplotting == 'virtual'):
		plotter = instantiate_virtual_plotter(type="DXY1300")

if (virtualplotting == 'real'):
		plotter = instantiate_plotters()[0]
		print("plotting for real")



def setSeed(): ####needs to be written to tmp file in order to save at in git
    seed = uuid.uuid1()
    f= open("tmp/seed.txt","w+")
    f.write(str(seed))
    f.close()
    return seed

def drawMintLines(seed, interx, intery, xnoise, ynoise):
    random.seed(seed)
    g = shapes.group([])
    points = []
    for x in xrange(0,100):
        for y in xrange(0,100):
            
            if (x < 10 and x > 90):
                xnoise = 0
                ynoise = 0
            xpos = x*interx + random.random() * xnoise
            ypos = y*intery + random.random() * ynoise
            points.append((xpos,ypos))
            
    g.append(shapes.path(points))
    return g







plotter.select_pen(1)
seed = setSeed()
plotter.write(drawMintLines(seed,75,75,75,75))

plotter.select_pen(2)
plotter.write(sign('minting' +  str(seed) , 7580, 50))

io.export(plotter, "tmp/out2" , fmt='jpg')
io.view(plotter)
