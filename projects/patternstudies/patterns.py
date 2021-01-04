##emacs instructions
## C-c C-c evaluates whole file
from chiplotle import *
from chiplotle.tools.io import export
from chiplotle.tools.plottertools import instantiate_virtual_plotter
import sys



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


def vertdigo():
    # (vertical diagonal going)
    x = 0
    y = 0
    ycursor = 0
    xcursor = 0
    vertsize = 1000
    horsize = vertsize/30
    direction = 1
    f = shapes.group([])
    for _ in range(100):
        points = []
        points.append((x,y))
        y = random.randint(0,vertsize)
        # if y < vertsize/2:
        #     y = y + random.randint(0,vertsize)
        # else:
        #     y = y + random.randint
        points.append((x,y))

        x = x + random.randint(0,horsize)
        y = random.randint(0,vertsize)
        points.append((x,y))
        # y = y + random.randint(0,vertsize)
        # points.append((x,y))

        f.append(shapes.path(points))
    plotter.write(f)

plotter.select_pen(1)
vertdigo()
plotter.select_pen(2)
plotter.write(sign('circkles', 7580, 50))
io.view(plotter)