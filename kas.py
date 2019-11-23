from chiplotle import *
from chiplotle.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from chiplotle.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from xml.dom import minidom
# import xpath
from lib.plothelpers import sign
from svgpathtools import svg2paths, svg2paths2, Path, Line, Arc, CubicBezier, QuadraticBezier
import sys



filename = sys.argv[1]
virtualplotting = sys.argv[2]

svgfile = "kas.svg"

#print(virtualplotting)
if (virtualplotting == 'virtual'):
		plotter = instantiate_virtual_plotter(type="DXY1300")
if (virtualplotting == 'real'):
		plotter = instantiate_plotters()[0]
		print("plotting for real")

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


polygons = []

def doSVGwarp(svg,polygons):
    paths, attributes, svg_attributes = svg2paths2(svg)
    print paths
    for idx, path in enumerate(paths):
        # p=[]
        if isinstance(path[0], Line):
            # print("Line instance found", path[0])
            # p = (path[0].start.real,path[0].start.imag)
            # if p in polygons:
            #     print("we ahve this one")
            #     pathtype = "line"
            # else:
            #     polygons.append(p)
            for segment in path:
                if isinstance(segment, Line):
                    p = (segment.end.real,segment.end.imag)
            if p in polygons:
                # print("we ahve this one")
                pathtype = "line"
            else:
                polygons.append(p)   
        # polygons.append(p)
    g = shapes.group([])
    h = shapes.group([])
    scale = 10
    # print(polygons)
    for point in polygons:
        dice = random.randint(0,5)
        if (dice > 4) :
            h.append(shapes.line((point[0]*scale, point[1]*scale),((point[0] + random.randint(80,120))*scale, (point[1] + random.randint(80,120))*scale) ))
            # transforms.scale(h, 10)    
        g.append(h)
        transforms.center_at(g, [0,0])
        # g.append(shapes.path(p))
    # transforms.scale(g, 5)
    bb = get_bounding_rectangle(g)
    bb = get_minmax_coordinates(bb.points)
    print(bb)
    # transforms.offset(g, (-bb[0][0], -bb[0][1] ))
    return({'group': g, 'bounds': bb})




shape = doSVGwarp(svgfile.encode('utf-8'),polygons)
print(shape)
#print(shape[1])
# print (shape['group'][0])
# print(shape['bounds'][0][0])
# for idx, gr in enumerate(shape["group"]):
	# print("plotting group", idx, len(gr))

		# plotter.select_pen(idx+1)
plotter.write(shape["group"])




# plotter.write(sign(sys.argv[1]))



io.export(plotter, filename, fmt='jpg')
io.export(plotter, filename, fmt='svg')
io.view(plotter)
