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
from lib.plothelpers import sign, plotgroup
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
preview = shapes.group([])
# print plotunits
# plotter.select_pen(1)
# plotter.margins.hard.draw_outline()
pltmax = [9000 , 9000]
bounds =shapes.rectangle(pltmax[0],pltmax[1])
transforms.offset(bounds,(pltmax[0]/2,pltmax[1]/2))
plotOutline = True

if (plotOutline):
	# preview.append(bounds)
	plotter.select_pen(1)
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
	preview.append(g)
	# plotter.write(g)




def plotSquare(size,x,y,depth, random):
	g = shapes.group([])
	for d in xrange(1,depth):
		t = shapes.group([])
		t.append(shapes.rectangle(size, size))
		# transforms.rotate(t, random.randint(0,30))
		g.append(t)
	print ("offsetting" + str(x))
	transforms.offset(g,(x,y))
	preview.append(g)
	# plotter.write(g)

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
	preview.append(g)
	# plotter.write(g)

def plotPolygons(size, x, y, depth, rdm):
	g = shapes.group([])
	for d in xrange(1,depth):
		t = shapes.group([])
		t.append(shapes.symmetric_polygon_side_length(depth,size/depth*d))
		transforms.offset(t, (random.randint(0,rdm),random.randint(0,rdm)))
		g.append(t)
	print ("offsetting" + str(x))
	transforms.offset(g,(x,y))
	preview.append(g)
	# plotter.write(g)
	
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
		# print(x)
		v = scale * pnoise1(float(x + base) / len, 16)
		# if (v < 0):
		# 	v = v*0.01
		# a.append(v)
		a.append(v)
	
	return a



# print(len(inputdata))



def renderline(indata, moddata, miny, maxy):
	# pointsH = []
	g = shapes.group([])
	# random.seed(10)
	for yi in xrange(len(moddata)):
		yoffset = spacingA * pow(spacingB, yi)
		points = []
		for xi in xrange(len(indata)):
			x = xi * (spacingC/(yi +1))
			if (x < pltmax[0]):
				y = yoffset + indata[xi]* moddata[yi]
				if (y > maxy):
					y = maxy - (y - maxy)
				if (y < miny):
					y = miny + (miny - y)
				# y=y*-1
				points.append((x,y))
			elif (points[-1][0] != pltmax[0]):
				y = yoffset + indata[xi]* moddata[yi]
				if (y > maxy):
					y = maxy - (y - maxy)
				if (y < miny):
					y = miny + (miny - y)
				# y = y*-1
				points.append((pltmax[0],y))
		g.append(shapes.path(points))
	f = shapes.group([])
	for xi in xrange(len(indata)):
		points = []
		print(xi)
		for yi in xrange(len(moddata)):
			yoffset = spacingA * pow(spacingB, yi)
			x = xi * (spacingC/(yi +1))
			if (x < pltmax[0]):
				y = yoffset + indata[xi]* moddata[yi]
				if (y > maxy):
					y = maxy - (y - maxy)
				if (y < miny):
					y = miny + (miny - y)
				# y = y*-1
				points.append((x,y))
			elif (len(points) > 1): 
				if (points[-1][0] != pltmax[0]):
					y = yoffset + indata[xi]* moddata[yi]
				if (y > maxy):
					y = maxy - (y - maxy)
				if (y < miny):
					y = miny + (miny - y)
				# y=y*-1
				points.append((pltmax[0],y))
		f.append(shapes.path(points))
	g.append(f)
	return g
	# plotter.write(g)
	# plotter.write(f)

#### text
def bytext(start, end):
	t = shapes.label(str(start) + "/" + str(end), 0.15, 0.15)
	transforms.offset(t,(200,50))
	transforms.offset(t,globaloffset)
	plotter.write(t)
	t = shapes.label("recorded in AQTushetii Georgia", 0.15, 0.15)
	transforms.offset(t,(1000,50))
	transforms.offset(t,globaloffset)
	plotter.write(t)
	# preview.append(t)
	t = shapes.label("kaotec []<> 2019", 0.15, 0.15)
	transforms.offset(t,(7400,50))
	transforms.offset(t,globaloffset)
	plotter.write(t)

	t = shapes.label("now is the right moment to say wow", 0.15, 0.15)
	transforms.offset(t,(4000,50))
	transforms.offset(t,globaloffset)
	plotter.write(t)
	# preview.append(t)
	# t = shapes.label("bandcamp downloadcode XXXX-XXXX", 0.15, 0.15)
	# transforms.offset(t,(5200,0))
	# transforms.offset(t,globaloffset)
	# preview.append(t)
	# plotter.write(t)


def maintext():
	maintext = shapes.group([])
	mainoffset=(17500,4400)
	font = "sqd.ttf"
	fontsize = 7

	maintext.append(writeword("ElfenWander", fontsize, font, mainoffset[0],mainoffset[1]+3100, "right"))
	maintext.append(writeword("DistressFrequency", fontsize, font, mainoffset[0],mainoffset[1]+2600, "right"))
	maintext.append(writeword("TheEdgeOfWhatIs", fontsize, font, mainoffset[0],mainoffset[1]+2100, "right"))
	maintext.append(writeword("Administratively", fontsize, font, mainoffset[0],mainoffset[1]+1800, "right"))
	maintext.append(writeword("Possible", fontsize, font, mainoffset[0],mainoffset[1]+1500, "right"))
	maintext.append(writeword("SineRave", fontsize, font, mainoffset[0],mainoffset[1]+1000, "right"))
	maintext.append(writeword("Palonopsia", fontsize, font, mainoffset[0],mainoffset[1]+500, "right"))
	maintext.append(writeword("MountainDrone", fontsize, font, mainoffset[0],mainoffset[1], "right"))

	maintext.append(writeword("Modular_Mountains", 10, "subatomic.ttf", 17500,10000, "right"))
	maintext.append(writeword("KAOTEC", 10, "subatomic.ttf", 17500,9200, "right"))

	transforms.scale(maintext, 0.8)
	transforms.offset(maintext, (-5000,0))
	# preview.append(maintext)
	plotter.write(maintext)


# def debuglayer():
# 	plotter.select_pen(2)
# 	t = shapes.label("Spacing Parameters" + str(end), 0.15, 0.15)
# 	transforms.offset(t,(200,0))
# 	transforms.offset(t,globaloffset)
# 	t = shapes.label("" + str(end), 0.15, 0.15)
# 	transforms.offset(t,(200,0))
# 	transforms.offset(t,globaloffset)

# 	plotter.write(t)



# print(generatemodulation(40,10))





# for x in xrange(1,2):
# 	for y in xrange(1,2):
# 		plotPolygons(700,x*1800, -y*1800, x+3, y*100)
# 		plotCircles(1000, x*900, -y*1800, 50, 0)
# 		plotCircles(900, x*1800, -y*1800, 25, 0)
#         plotSquare(1000, x*1800, -y*1800, x*10, y*100)

def generateBackground():
	inputdata = generatemodulation(40,10, random.randint(1,100), 80)
	modulationdata = generatemodulation(30, 10, random.randint(1,100),1200)
	r = renderline(inputdata, modulationdata, -1000, 6000)
	preview.append(plotgroup(r, 1, [(0,0),pltmax], (0,0), 1))
	# plotter.write(plotgroup(plotter, r, 1, [(0,0),pltmax], (0,0), 1))

# xlen = 10
# ylen = 10
# for x in xrange(xlen*2):
# 	for y in xrange(ylen*2):
# 		l = shapes.line(((x-xlen), y), (-x, y-ylen))
# 		transforms.scale(l, 100)
# 		plotter.write(l)
  

# p = shapes.path([(0,0), (2500,1000), (5000,5000) ])
# plotter.write(p)


# preview.append(sign("album001cover test", pltmax[0]+100, 100 ))

def debuggrid(interval):
	grid = shapes.group([])
	i = 0
	x = 0
	y = 0
	while (x < pltmax[0]):
		i = i + 1
		x = i*interval
		grid.append(shapes.line((x,0),(x,pltmax[1])))
	i = 0
	while (y < pltmax[1]):
		i = i + 1
		y = i*interval
		grid.append(shapes.line((0,y),(pltmax[0],y)))	
	plotter.write(grid)	


spacingA = 10000
spacingB = 0.99
spacingC = 1500
print('startnumber/stopnumber will be plotted')
startnumber = input('enter startnumber: ')
stopnumber = input('enter stopnumber (eg. 300): ')
for x in xrange(startnumber,stopnumber+1):
	# random.seed(startnumber + x)
	preview = shapes.group([])
	generateBackground()
	io.view(preview)
	print("spacingA = " + str(spacingA))
	print("spacingB = " + str(spacingB))
	print("spacingC = " + str(spacingC))
	ready = input('drawing ok? press 1 to continue, press 2 for rerun:, press 3 for new parameters: ')
	print(ready)
	if(ready == 1):
		plotter.select_pen(1)
		plotter.write(preview)
		plotter.select_pen(2)
		maintext()
		plotter.select_pen(3)
		bytext(startnumber, stopnumber)
		plotter.write(sign("modular mountains", pltmax[0]+100, 100 ))
		# debuggrid(1000)
		io.view(plotter)
		io.export(plotter, filename, fmt='jpg')
		io.export(plotter, filename, fmt='svg')
		startnumber = startnumber + 1
		plotter.clear()
	if(ready == 2):
		print "rerunning"

	if (ready == 3):
		spacingA = int(raw_input("spacingA: " + str(spacingA) + "new value?") or spacingA)
		spacingB = float(raw_input("spacingB: " + str(spacingB) + "new value?") or spacingB)
		spacingC = int(raw_input("spacingC: " + str(spacingC) + "new value?") or spacingC)

	else:
		print('press CTRL-C')
print("all done!")




