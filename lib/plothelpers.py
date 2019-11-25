from chiplotle import *
from chiplotle.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from chiplotle.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
import datetime
import math

def sign(filename,x,y):
    now = datetime.datetime.now()
    t = shapes.label(str(filename + "    " + now.strftime("%Y-%m-%d %H:%M")),0.15, 0.15, None, None, 'bottom-left')
    transforms.rotate(t, math.radians(90))
    transforms.offset(t, (x,y)) #used to be 160000
    return t


def plotgroup(plotter, g,paddingfactor,zone,noisexy,pen):
	plotter.select_pen(pen)
	x1,y1 = zone[0]
	x2,y2 = zone[1]
	maxx = abs(x2-x1)
	maxy = abs(y2-y1)
	xfactor = maxx / g.width/paddingfactor
	yfactor = maxy / g.height/paddingfactor
	if (yfactor <= xfactor):
		scale = yfactor
		transforms.scale(g, scale)
		# transforms.offset(g,((recordsize/plotunit - g.width)/2 , (recordsize/plotunit - g.height)/2))

	else:
		scale = xfactor
		transforms.scale(g, scale)
                # transforms.offset(g,((recordsize/plotunit - g.width)/2 , (recordsize/plotunit - g.height)/2))

		# transforms.offset(g,(0,(y2-y1+g.height)/2))

	print ("SCALE = " + str(scale))
	transforms.offset(g, (x1,y1))
	if not noisexy == (0,0):
		transforms.noise(g,noisexy)
	# plotter.write(g)
	return g