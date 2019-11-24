##emacs instructions
## C-c C-c evaluates whole file


from chiplotle import *
from chiplotle.tools.io import export
from chiplotle.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from chiplotle.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from chiplotle.geometry.core.label import Label
from chiplotle.core.interfaces.interface import _Interface
from chiplotle.plotters.margins.marginssoft import MarginsSoft
from chiplotle.plotters.margins.marginshard import MarginsHard
from lib.plothelpers import sign
from lib.texttools import writeword
# from lib.perlin import writeword
import sys
import random
import math
from noise import pnoise1, pnoise2, pnoise3


# import pickle
# from svgpathtools import svg2paths, Path, Line, Arc, CubicBezier, QuadraticBezier
# from texttools import *

from chiplotle.tools.plottertools import instantiate_virtual_plotter
filename = sys.argv[1]
virtualplotting = sys.argv[2]

#print(virtualplotting)
if (virtualplotting == 'virtual'):
		plotter = instantiate_virtual_plotter(type="DXY1300")
if (virtualplotting == 'real'):
		plotter = instantiate_plotters()[0]
		print("plotting for real")

# Instantiated plotter DXY-1300 in port VirtualSerialPort:
#    Drawing limits: (left 0; bottom 0; right 10320; top 7920)

# plotter = instantiate_plotters( )[0]
# Drawing limits: (left 0; bottom 0; right 16158; top 11040)


# print(MarginsHard(plotter))

pltmax = [10320, 7920]
plotunit = 0.025 # 1 coordinate unit per plotter = 0.025 mm
# plotunits = (10320/432, 7920/297)

globaloffset = (0,0)

# print plotunits
plotter.select_pen(1)
# plotter.margins.hard.draw_outline()
pltmax = [9000 , 9000]
bounds =shapes.rectangle(pltmax[0],pltmax[1])
transforms.offset(bounds,(pltmax[0]/2,pltmax[1]/2) )
plotter.write(bounds)

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

def remap(x, in_min, in_max, out_min, out_max):
	a = (in_max - in_min) + out_min
	if (a == 0):
		a = 1
	return (x - in_min) * (out_max - out_min) / a


def generatemodulation(len,range, base, scale):
	a = []
	for x in xrange(len):
		# a.append(random.randint(0,range))
		print(x)
		v = scale * pnoise1(float(x + base) / len, 16)
		# if (v < 0):
		# 	v = v*0.01
		# a.append(v)
		a.append(v)
	
	return a



print(len(inputdata))







def renderline(indata, moddata, miny, maxy):
	# print(len(data))
	# minindata = min(indata)
	# maxindata = max(indata)
	# remappedindata = list(map(lambda x: remap(x, minindata, maxindata, miny, maxy), indata))
	# print(remappedindata)
	# minmoddata = min(moddata)
	# maxmoddata = max(moddata)
	# remappedmoddata = list(map(lambda x: remap(x, minmoddata, maxmoddata, miny, maxy), moddata))
	g1 = shapes.group([])
	g2 = shapes.group([])
	c = 1.8 #curvature
	p = -4 #perspective stretch
	compression = 4000
	# //do perspective correction
	# modulationdata = remappedmoddata
	# inputdata = remappedindata
	ax1 = []
	ax2 = []
	bx1 = []
	bx2 = []
	ay1 = []
	ay2 = []
	by1 = []
	by2 = []
	for y in xrange(1,len(modulationdata)-1):
		# for x in xrange(1,len(inputdata)-1-(int(len(inputdata)/2))+y):
		for x in xrange(1,len(inputdata)-1):

			x1 = -x * compression / y
			y1 = (compression/10-c*y)*y+(y*compression/10+(inputdata[x]*compression/100 * modulationdata[y]))
			x2 = -(x+1)*compression/(y)
			y2 = (compression/10-c*y)*y+(y*compression/10+inputdata[x+1]*compression/100 * modulationdata[y])
			# print(x1,y1,x2,y2)
			ax1.append(x1)
			ax2.append(x2)
			ay1.append(y1)
			ay2.append(y2)
			# y2 = 5000
			# if ( x1 < -pltmax[0]):
			# 	if (x2 < -pltmax[0]):
			# 		pass
			# 	else:
			# 		g.append(shapes.line((x1,y1),(pltmax[0],y2)))
			# else:
			# 	g.append(shapes.line((x1,y1),(x2,y2)))
	minay1 = min(ay1)
	maxay1 = max(ay1)
	ay1new = list(map(lambda x: remap(x, minay1, maxay1, miny,maxy), ay1))
	minay2 = min(ay2)
	maxay2 = max(ay2)
	ay2new = list(map(lambda x: remap(x, minay2, maxay2, miny,maxy), ay2))

	pathpoints = []
	for i in xrange(len(ax1)):
		if ( ax1[i] > -pltmax[0]):
			pathpoints.append((ax1[i],ay1new[i]))

		# 	if (ax2[i] < -pltmax[0]):
		# 		pass
		# 	else:
		# 		pass
		# 		# g.append(shapes.line((x1,y1),(x2,y2)))
		else:
			g1.append(shapes.path(pathpoints))
			pathpoints = []
		# 	g.append(shapes.line((ax1[i],ay1new[i]),(ax2[i],ay2new[i])))
	g1.append(shapes.catmull_path(pathpoints))


			# g.append(shapes.line((x1,y1),(x2,y2)))
	# ///we split the loops for effcient polylines construction

	# for x in xrange(1,len(inputdata)-1-(int(len(inputdata)/2))+y):
	for x in xrange(1,len(inputdata)):
		for y in xrange(1,len(modulationdata)-2):
			x1 = -x * compression / y
			y1 = (compression/10-c*y)*y+(y*compression/10+(inputdata[x]*compression/100 * modulationdata[y]))
			x2 = -x * compression / (y+1)
			y2 = (compression/10-c*(y+1))* (y+1)+((y+1)*compression/10+(inputdata[x]*compression/100 * modulationdata[y+1]))
			# y2 = 0
			bx1.append(x1)
			bx2.append(x2)
			by1.append(y1)
			by2.append(y2)
			# if ( x1 < -pltmax[0]):
			# 	if (x2 < -pltmax[0]):
			# 		pass
			# 	else:
			# 		pass
			# 		# g.append(shapes.line((x1,y1),(x2,y2)))
			# else:
			# 	g.append(shapes.line((x1,y1),(x2,y2)))
	minby1 = min(by1)
	maxby1 = max(by1)
	by1new = list(map(lambda x: remap(x, minby1, maxby1, miny,maxy), by1))
	minby2 = min(by2)
	maxby2 = max(by2)
	by2new = list(map(lambda x: remap(x, minby2, maxby2, miny,maxy), by2))

	pathpoints = []
	# for i in xrange(len(bx1)):
	# 	if ( bx1[i] < -pltmax[0]):
	# 		if (bx2[i] < -pltmax[0]):
	# 			pass
	# 		else:
	# 			pass
	# 			# g.append(shapes.line((x1,y1),(x2,y2)))
	# 	else:
	# 		# g.append(shapes.line((bx1[i],by1new[i]),(bx2[i],by2new[i])))
	# 		pathpoints.append((bx1[i],by1new[i]))
	for i in xrange(len(bx1)-1):
		if ( bx1[i+1] > -pltmax[0]):
			if (bx1[i+1] > bx1[i]):
				pathpoints.append((bx1[i],by1new[i]))
			else:
				print(pathpoints)
				g2.append(shapes.path(pathpoints))
				pathpoints = []

			# g.append(shapes)
	# transforms.scale(g/ 4.5)
	# transforms.rotate(g,90)
	transforms.offset(g1, (pltmax[0],0))
	transforms.offset(g2, (pltmax[0],0))
	# print(g.width)
	plotter.write(g1)
	plotter.write(g2)

def renderline(indata, moddata, miny, maxy):
	offsetY = 250

	# pointsH = []
	g = shapes.group([])
	random.seed(10)
	for yi in xrange(len(moddata)):
		pointsY = []
		pointsX = []
		for xi in xrange(len(indata)):
			x = xi * (200 +random.randint(10,30))
			y = indata[xi] * moddata[yi]  # + yi*yi/offsetY
			pointsX.append(x)
			pointsY.append(y)
		minY = min(pointsY)
		maxY = max(pointsY)
		newpointsY= list(map(lambda x: remap(x, minY, maxY, miny,maxy), pointsY))
		print(newpointsY)
		points = []
		for x in xrange(len(pointsX)):
			for y in xrange(len(newpointsY)):
				points.append((pointsX[x],newpointsY[y]))
		g.append(shapes.path(points))
	plotter.write(g)


#### text
def bytext():
	plotter.select_pen(2)
	t = shapes.label("recorded in Tushetii Georgia", 0.15, 0.15)
	transforms.offset(t,(200,300))
	transforms.offset(t,globaloffset)
	plotter.write(t)
	t = shapes.label("kaotec []<> 2019", 0.15, 0.15)
	transforms.offset(t,(200,200))
	transforms.offset(t,globaloffset)
	plotter.write(t)
	t = shapes.label("bandcamp downloadcode XXXX-XXXX", 0.15, 0.15)
	transforms.offset(t,(200,-100))
	transforms.offset(t,globaloffset)
	plotter.write(t)

def maintext():
	maintext = shapes.group([])
	mainoffset=(500,3400)

	maintext.append(writeword("ElfenWander", 6, "magnetar.ttf", mainoffset[0],mainoffset[1]+3100))
	maintext.append(writeword("DistressFrequency", 6, "magnetar.ttf", mainoffset[0],mainoffset[1]+2600))
	maintext.append(writeword("TheEdgeOfWhatIs", 6, "magnetar.ttf", mainoffset[0],mainoffset[1]+2100))
	maintext.append(writeword("Administratively", 6, "magnetar.ttf", mainoffset[0],mainoffset[1]+1800))
	maintext.append(writeword("Possible", 6, "magnetar.ttf", mainoffset[0],mainoffset[1]+1500))
	maintext.append(writeword("SineRave", 6, "magnetar.ttf", mainoffset[0],mainoffset[1]+1000))
	maintext.append(writeword("Palonopsia", 6, "magnetar.ttf", mainoffset[0],mainoffset[1]+500))
	maintext.append(writeword("MountainDrone", 6, "magnetar.ttf", mainoffset[0],mainoffset[1]))

	maintext.append(writeword("KAOTEC-album001", 10, "subatomic.ttf", mainoffset[0]-200,mainoffset[1]+ 4000))

	transforms.scale(maintext, 0.5)
	transforms.offset(maintext, (0,2500))
	plotter.write(maintext)
# print(generatemodulation(40,10))

# for x in xrange(1,2):
# 	for y in xrange(1,2):
# 		plotPolygons(700,x*1800, -y*1800, x+3, y*100)
# 		plotCircles(1000, x*900, -y*1800, 50, 0)
# 		plotCircles(900, x*1800, -y*1800, 25, 0)
#         plotSquare(1000, x*1800, -y*1800, x*10, y*100)


inputdata = generatemodulation(40,10, random.randint(1,100), 80)
modulationdata = generatemodulation(80, 10, random.randint(1,100),100)

print(inputdata)

renderline(inputdata, modulationdata, 10, 5000)


# xlen = 10
# ylen = 10
# for x in xrange(xlen*2):
# 	for y in xrange(ylen*2):
# 		l = shapes.line(((x-xlen), y), (-x, y-ylen))
# 		transforms.scale(l, 100)
# 		plotter.write(l)
  

# p = shapes.path([(0,0), (2500,1000), (5000,5000) ])
# plotter.write(p)

bytext()
maintext()

plotter.write(sign("album001cover test", pltmax[0]+100, 100 ))
io.export(plotter, filename, fmt='jpg')
io.export(plotter, filename, fmt='svg')
io.view(plotter)


