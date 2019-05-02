from __future__ import division
from chiplotle import *

from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")


# interesting https://en.wikipedia.org/wiki/3D_projection#Perspective_projection

import math
import random
import numpy as np
from scipy import signal

plotsize = [10, 10]
objects = []

#helpers
def fib(n):
    return ((1+math.sqrt(5))**n-(1-math.sqrt(5))**n)/(2**n*math.sqrt(5))

def addobject1(x,y,size):
	g = shapes.group([])
	g.append(shapes.rectangle(size,size))
	transforms.offset(g, (size/2,size/2))
	g.append(shapes.line((size/2,0),(size/2,size/2)))
	g.append(shapes.line((0,size/2),(size/10,size/2)))
	g.append(shapes.line((size/10*9,size/2),(size,size/2)))
	transforms.offset(g, (x, y))
	objects.append({'class': 'obj1', 'x': x, 'y': y, 'size':size, 'connections' : 3, 'dots' : {(size/2,0),(0,size/2),(size,size/2) } })
	plotter.write(g)

def addobject2(x,y,size):
	g = shapes.group([])
	g.append(shapes.circle(size/2))
	transforms.offset(g, (size/2,size/2))
	g.append(shapes.line((size/2,0),(size/2,size/2)))
	g.append(shapes.line((0,size/2),(size/10,size/2)))
	g.append(shapes.line((size/10*9,size/2),(size,size/2)))
	transforms.offset(g, (x, y))
	objects.append({'class': 'obj1', 'x': x, 'y': y, 'size':size, 'connections' : 3, 'dots' : {(size/2,0),(0,size/2),(size,size/2) } })
	plotter.write(g)



def connectthedots(object1,object2):
	x1 = object1.get('x') + object1.get('size')/2
	y1 = object1.get('y') + object1.get('size')/2
	x2 = object2.get('x') + object2.get('size')/2
	y2 = object2.get('y') + object2.get('size')/2
	# g = shapes.group([])
	# g.append(shapes.line((x1,y1),(x2,y2)))
	# plotter.write(g)
	kartelpathconnect((x1,y1),(x2,y2),abs(int(math.floor((x2-y2)/100))),object1.get('size'),object2.get('size'),True)
	# plotter.write(g)

def kartelconnect(p1,p2,size,size1,size2,log):
	#p1 = np.array([1,1])
	g = shapes.group([])
	length = np.linalg.norm(np.array(p1)-np.array(p2))
	xlength = (p2[0]-p1[0])
	sublength = xlength/size
	parts = int(abs(math.floor(xlength/sublength)))
	partsspace = np.logspace(0 ,2, parts, endpoint=True)
	partsYspace = np.linspace(p1[1], p2[1], parts)
	# print(length)
	# print("partsYspace = " )
	# print(partsYspace)
	for i in xrange(0,parts-1):
		print(" partsspace = ") 
		print partsspace[i] 
		print(" partsYspace = ") 
		print partsYspace[i] 
		yoffset = random.randint(0,1000)
		y1 = partsYspace[i] + yoffset
		#y1 = random.uniform(partsYspace[i]-1000,partsYspace[i]+1000)
		if (i % 2 == 0):
			y1= partsYspace[i] - yoffset
		if (log == False):
			g.append(shapes.line((i*sublength,partsYspace[i]),(i*sublength,y1)))
			g.append(shapes.line((i*sublength,y1),((i+1)*sublength,y1)))
			g.append(shapes.line(((i+1)*sublength,y1),((i+1)*sublength,partsYspace[i+1])))
		else:
			g.append(shapes.line((partsspace[i]*xlength/100,partsYspace[i]),(partsspace[i]*xlength/100,y1)))
			g.append(shapes.line((partsspace[i]*xlength/100,y1),(partsspace[i+1]*xlength/100,y1)))
			g.append(shapes.line((partsspace[i+1]*xlength/100,y1),(partsspace[i+1]*xlength/100,partsYspace[i+1])))
	if (log == False):
		# transforms.offset(g,(-sublength,0))
		# g.append(shapes.line((partsspace[-1]*xlength/100,partsYspace[-1]),p2))
		transforms.offset(g, (p1[0],0-size1/2))
	if (log == True):
		# transforms.offset(g,(-sublength,0))
		# g.append(shapes.line((partsspace[-1]*xlength/100,partsYspace[-1]),p2))
		transforms.offset(g, (p1[0],0))
	g.append(shapes.line(p1,p2))
	
	plotter.write(g)

def kartelpathconnect(p1,p2,size,size1,size2,log):
	#p1 = np.array([1,1])
	# print size
	g = shapes.group([])
	length = np.linalg.norm(np.array(p1)-np.array(p2))
	xlength = (p2[0]-p1[0])
	sublength = xlength/size
	# print sublength
	parts = int(abs(math.floor(xlength/sublength)))
	print parts
	partsspace = np.logspace(0 ,2, parts, endpoint=True)
	partsYspace = np.linspace(p1[1], p2[1], parts)
	# print(length)
	# print("partsYspace = " )
	# print(partsYspace)
	path = []
	for i in xrange(0,parts-1):
		# print(" partsspace = ") 
		# print partsspace[i] 
		# print(" partsYspace = ") 
		# print partsYspace[i] 
		yoffset = random.randint(0,1000)
		y1 = partsYspace[i] + yoffset
		#y1 = random.uniform(partsYspace[i]-1000,partsYspace[i]+1000)
		if (i % 2 == 0):
			y1= partsYspace[i] - yoffset
		if (log == False):
			path.append((i*sublength,partsYspace[i]))
			path.append((i*sublength,y1))
			path.append(((i+1)*sublength,y1))
			path.append(((i+1)*sublength,partsYspace[i+1]))
		else:
			path.append((partsspace[i]*xlength/100,partsYspace[i]))
			path.append((partsspace[i]*xlength/100,y1))
			path.append((partsspace[i+1]*xlength/100,y1))
			path.append((partsspace[i+1]*xlength/100,partsYspace[i+1]))
	# print path
	path = Path(path)
	if (log == False):
		# transforms.offset(g,(-sublength,0))
		# g.append(shapes.line((partsspace[-1]*xlength/100,partsYspace[-1]),p2))
		transforms.offset(path, (p1[0],0-size1/2))
	if (log == True):
		# transforms.offset(g,(-sublength,0))
		# g.append(shapes.line((partsspace[-1]*xlength/100,partsYspace[-1]),p2))
		transforms.offset(path, (p1[0],0))
	# g.append(shapes.line(p1,p2))
	
	plotter.write(path)

def bezierpathconnect(p1,p2,size,size1,size2,curvature,log):
	#p1 = np.array([1,1])
	g = shapes.group([])
	length = np.linalg.norm(np.array(p1)-np.array(p2))
	xlength = (p2[0]-p1[0])
	sublength = xlength/size
	parts = int(abs(math.floor(xlength/sublength)))
	partsspace = np.logspace(0 ,2, parts, endpoint=True)
	partsYspace = np.linspace(p1[1], p2[1], parts)
	# print(length)
	# print("partsYspace = " )
	# print(partsYspace)
	path = []
	for i in xrange(0,parts-1):
		print(" partsspace = ") 
		print partsspace[i] 
		print(" partsYspace = ") 
		print partsYspace[i] 
		yoffset = random.randint(0,1000)
		y1 = partsYspace[i] + yoffset
		#y1 = random.uniform(partsYspace[i]-1000,partsYspace[i]+1000)
		if (i % 2 == 0):
			y1= partsYspace[i] - yoffset
		if (log == False):
			path.append((i*sublength,partsYspace[i]))
			path.append((i*sublength,y1))
			path.append(((i+1)*sublength,y1))
			path.append(((i+1)*sublength,partsYspace[i+1]))
		else:
			path.append((partsspace[i]*xlength/100,partsYspace[i]))
			path.append((partsspace[i]*xlength/100,y1))
			path.append((partsspace[i+1]*xlength/100,y1))
			path.append((partsspace[i+1]*xlength/100,partsYspace[i+1]))
	# print path
	g.append(shapes.bezier_path(path, 1, 5))
	if (log == False):
		# transforms.offset(g,(-sublength,0))
		# g.append(shapes.line((partsspace[-1]*xlength/100,partsYspace[-1]),p2))
		transforms.offset(g, (p1[0],0-size1/2))
	if (log == True):
		# transforms.offset(g,(-sublength,0))
		# g.append(shapes.line((partsspace[-1]*xlength/100,partsYspace[-1]),p2))
		transforms.offset(g, (p1[0],0))
	# g.append(shapes.line(p1,p2))
	
	plotter.write(g)

def plot(start, end): #(left 0; bottom 0; right 16158; top 11040)
	plotter.clear()
	plotter.set_origin_center()
	plotter.select_pen(2)
	# plotter.write(shapes.rectangle(16158,11040))
	offsetx = -2000
	offsety = 0	
	# kartelconnect((1000,-5000), (3000,3000),50, False)
	# kartelconnect((1000,5000), (300,3000),10, True)

	# for x in xrange(1,30):
	# 	addobject1(random.randint(-8000,6500),random.randint(-5000,3800),random.randint(220,2000))
	# 	# print(len(objects))
	# plotter.select_pen(1)

	# for x in xrange(0,len(objects)-1):
	#  	# print(objects[x].get('x'))
	#  	connectthedots(objects[x],objects[x+1])
	
	s = 300
	r = 10
	f = 2.15
	g = shapes.group([])
	for x in xrange(0,r):
		g.append(shapes.line((0,-s*x*f),(-s*x,-r*s*f)))
		g.append(shapes.line((0,s*x*f-(r*s*2*f)),(-s*x,r*s*f-(r*s*2*f))))
		g.append(shapes.line((0,s*x*f-(r*s*2*f)),(s*x,r*s*f-(r*s*2*f))))
		g.append(shapes.line((0,-s*x*f),(s*x,-r*s*f)))

		#draw central line
		# g.append(shapes.line((0,-r*s*4),(0,s)))
		g.append(shapes.line((-r*s,-r*s*f),(r*s,-r*s*f)))
		# g.append(shapes.line((s*r,s*x*2),(s*x,0)))
		# g.append(shapes.line((s*r,s*x*2),(s*x,0)))
		# g.append(shapes.line((-s*r,-s*x*2),(-s*x,0)))
	r2 = 20
	s2 = 120
	transforms.rotate(g, -np.pi/4)
	transforms.center_at(g, (0,0))
	plotter.write(g)
	g = shapes.group([])
	for x in xrange(1,r2):
		g.append(shapes.line((0,4*s2*x),(4*s2*x,4*r2*s2)))
	transforms.center_at(g, (0,0))
	transforms.rotate(g,np.pi)
	# transforms.scale(g, s/r)

	plotter.write(g)
	g = shapes.group([])
	for x in xrange(1,r2):
		g.append(shapes.line((0,4*s2*x),(4*s2*x,4*r2*s2)))
	transforms.center_at(g, (0,0))
	# transforms.scale(g, s/r)

	plotter.write(g)
	io.view(plotter)


plot(0,1)
