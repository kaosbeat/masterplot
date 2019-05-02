##emacs instructions
## C-c C-c evaluates whole file


from chiplotle import *
from chiplotle.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from chiplotle.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from chiplotle.geometry.core.label import Label
from chiplotle.core.interfaces.interface import _Interface
from chiplotle.plotters.margins.marginssoft import MarginsSoft
from chiplotle.plotters.margins.marginshard import MarginsHard
import random
import math

# import pickle
# from svgpathtools import svg2paths, Path, Line, Arc, CubicBezier, QuadraticBezier
# from texttools import *

plotter = instantiate_virtual_plotter(type="DXY1300")
# Instantiated plotter DXY-1300 in port VirtualSerialPort:
#    Drawing limits: (left 0; bottom 0; right 10320; top 7920)

# plotter = instantiate_plotters( )[0]
# Drawing limits: (left 0; bottom 0; right 16158; top 11040)


print(MarginsHard(plotter))

pltmax = [10320, 7920]
plotunit = 0.025 # 1 coordinate unit per plotter = 0.025 mm
# plotunits = (10320/432, 7920/297)

# print plotunits
plotter.select_pen(1)
# plotter.margins.hard.draw_outline()
# plotter.select_pen(2)
# g = shapes.group([])
# g.append(shapes.rectangle(16158,11040))
# transforms.offset(g, (16158/2,11040/2))
# plotter.write(g)
# plotter.select_pen(1)


objects = []
def addAndPlotObject(soort, x, y, size, maxsize, data):
	# g = shapes.group([])
	if (soort == 'text'):
		g = Label(str(data.encode('utf-8')), size, size)
		# check https://github.com/drepetto/chiplotle/blob/master/chiplotle/hpgl/label.py
	transforms.offset(g, (x, y))
	if (g.width > maxsize):
		transforms.scale(g, maxsize/g.width)
	objects.append({'class': soort, 'x': x, 'y': y, 'size':size, 'data': data })
	plotter.write(g)




def plotSquare(size,x,y,depth, random):
	g = shapes.group([])
	for d in xrange(1,depth):
		t = shapes.group([])
		t.append(shapes.rectangle(size, size))
		# transforms.rotate(t, random.randint(0,30))
		g.append(t)
	print ("offsetting" + str(x))
	transforms.offset(g,(x,y))
	plotter.write(g)

def plotCircles(size, x, y, depth, rdm):
        '''
        circles get drawn in a certain SIZE at X,Y with a recursion of DEPTH and random range of RDM
        '''
	g = shapes.group([])
	for d in xrange(1,depth):
		t = shapes.group([])
		t.append(shapes.circle(size/depth*d))
		transforms.offset(t, (random.randint(0,rdm),0))
		g.append(t)
	print ("offsetting" + str(x))
	transforms.offset(g,(x,y))
	plotter.write(g)

def plotPolygons(size, x, y, depth, rdm):
	g = shapes.group([])
	for d in xrange(1,depth):
		t = shapes.group([])
		t.append(shapes.symmetric_polygon_side_length(depth,size/depth*d))
		transforms.offset(t, (random.randint(0,rdm),random.randint(0,rdm)))
		g.append(t)
	print ("offsetting" + str(x))
	transforms.offset(g,(x,y))
	plotter.write(g)
	
inputdata = [0,0,1,3,4,3,5,3,6,3,0,0,0,0,0,0,0,0,2,4,2,4,3,5,4,6,7,9,7,5,3,1,0,0,0,3,4,3,5,3,6,3,0,0,0,0,0,0,0,0,2,4,2,3,4,3,5,3,6,3,0,0,0,0,0,0,0,0,2,4,2,3,4,3,5,3,6,3,0,0,0,0,0,0,0,0,2,4,2]
modulationdata = [0,0,3,4,4,4,3,2,1,0,0,0,0,1,2,3,4,5,4,3,4,5,0,0,3,4,4,4,3,2,1,0,0,0,0,1,2,3,4,5,4,3,4,5]
def renderline(data, y):
	print(len(data))
	g = shapes.group([])
	c = 1.8 #curvature
	p = -4 #perspective stretch
	# //do perspective correction
	for y in xrange(1,len(modulationdata)-1):
		for x in xrange(1,len(inputdata)-1-44+y):
			x1 = -x * 600 / y
			y1 = (60-c*y)*y+(y*50+(inputdata[x]*5 * modulationdata[y]))
			x2 = -(x+1)*600/(y)
			y2 = (60-c*y)*y+(y*50+inputdata[x+1]*5 * modulationdata[y])
			# if (x1 > -2000):
			g.append(shapes.line((x1,y1),(x2,y2)))
				# print(appending)
	# ///we split the loops for effcient polylines construction
	for x in xrange(1,len(inputdata)-1-44+y):
		for y in xrange(1,len(modulationdata)-2):
			x1 = -x * 600 / y
			y1 = (60-c*y)*y+(y*50+(inputdata[x]*5 * modulationdata[y]))
			x2 = -x * 600 / (y+1)
			y2 = (60-c*(y+1))* (y+1)+((y+1)*50+(inputdata[x]*5 * modulationdata[y+1]))
			# if (x1 > -2000):
			g.append(shapes.line((x1,y1),(x2,y2)))
			# g.append(shapes)
	# transforms.scale(g/ 4.5)
	# transforms.rotate(g,90)
	# transforms.offset(g, (16158/1.5,12040))

	print(g.width)
	plotter.write(g)



# for x in xrange(1,2):
# 	for y in xrange(1,2):
		# plotPolygons(700,x*1800, -y*1800, x+3, y*100)
		# plotCircles(1000, x*900, -y*1800, 50, 0)
		# plotCircles(900, x*1800, -y*1800, 25, 0)
        # plotSquare(1000, x*1800, -y*1800, x*10, y*100)

renderline(inputdata, 80)



# 
io.view(plotter)
