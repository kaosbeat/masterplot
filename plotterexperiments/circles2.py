from __future__ import division
from chiplotle import *

from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")


import math
import random
import numpy as np
from scipy import signal

plotsize = [10, 10]


#helpers
def fib(n):
    return ((1+math.sqrt(5))**n-(1-math.sqrt(5))**n)/(2**n*math.sqrt(5))



# Y = np.linspace(p1[1] ,p2[1], len(spaceX))
# #
# The parametric equation for a circle is

def verticalfilledcircle(cx,cy,radius,rate, full):
	# a = np.linspace(0, 2*np.pi, rate)
	g = shapes.group([])
	for i in xrange(0,rate+1):
		if (i ==0):
			x0 = 0
		else: 
			x0 = radius/rate*i
		# y0 = np.sqrt(radius^2 - int(x0)^2)
		y0 = np.sqrt(radius**2 - x0**2)	
		# print(x0)
		
		if (full == 1):
			g.append(shapes.line((-x0,-y0),(-x0,y0)))
			if (x0 != 0):
				g.append(shapes.line((x0,-y0),(x0,y0)))
		if (full == 0):
			g.append(shapes.line((x0,y0),(x0,0)))
			if (x0 != 0):
				g.append(shapes.line((-x0,y0),(-x0,0)))

	transforms.offset(g, (cx,cy))
	plotter.write(g)


def verticalfibcircle(cx,cy,radius,rate, full):
	# a = np.linspace(0, 2*np.pi, rate)
	g = shapes.group([])
	for i in xrange(0,rate+1):
		if (i ==0):
			x0 = 0
		else: 
			x0 = fib(i)/radius/10
		# y0 = np.sqrt(radius^2 - int(x0)^2)
		print x0
		y0 = np.sqrt(radius**2 - x0**2)	
		# print(x0)
		
		if (full == 1):
			g.append(shapes.line((-x0,-y0),(-x0,y0)))
			if (x0 != 0):
				g.append(shapes.line((x0,-y0),(x0,y0)))
		if (full == 0):
			g.append(shapes.line((x0,y0),(x0,0)))
			if (x0 != 0):
				g.append(shapes.line((-x0,y0),(-x0,0)))

	transforms.offset(g, (cx,cy))
	plotter.write(g)
def filledcircle(cx,cy,radius,rate, full):

	a = np.linspace(0, 2*np.pi, rate)		
	g = shapes.group([])
	for i in xrange(1,rate):
		# print((x[i-1]*radius,y[i]*radius),(x[i]*radius, y[i]*radius))
		# g.append(shapes.line())
		# g.append(shapes.line((x[i-1]*radius,y[i]*radius),(x[i]*radius, y[i]*radius)))
		# g.append(shapes.line(
		# 	( cx + radius * np.cos(a[i-1]) , cy + radius * np.sin(a[i-1]) ),
		# 	( cx + radius * np.cos(a[i]),cy + radius * np.sin(a[i]) )))
		#figure out how to get point at certin y-value
		# x^2 + y^2 = r^2
		x0 = radius * np.cos(a[i-1])
		# y0 = np.sqrt(radius^2 - int(x0)^2)
		y0 = np.sqrt(radius**2 - x0**2)

		# x1 = np.sqrt(radius^2 - y0^2)

		g.append(shapes.line((x0,y0),(-x0,y0)))
		if (full == 1):
			g.append(shapes.line((x0,-y0),(-x0,-y0)))
	transforms.offset(g, (cx,cy))
	plotter.write(g)




def takeawalk(size, rate):
	g = shapes.group([])
	# for x in xrange(1,10):
	path = []
	for k in xrange (1,8):
		for x in xrange(1,size):
			print(x % 4)
			if (0 == (x % 4)):
				path.append((x*rate,0-(k*50)))
			if (1 == (x % 4)):
				y = x*1*(random.randint(0,x))
				path.append(((x-1)*rate,y-(k*50)))
			if (2 == (x % 4)):
				path.append((x*rate,y-(k*50)))
			if (3 == (x % 4)):
				path.append(((x-1)*rate,00-(k*50)))
			
			# else:
				# path.append((x*100,x*1*(random.randint(0,x))))
		g.append(shapes.bezier_path(path, 0.1 * k ,5))
	transforms.offset(g, (-5000,-3000))
	plotter.write(g)
	plotter.pen_up([(0,0)])
		
		
	

def takeacirclewalk(steps):
	g = shapes.group([])
	g.append(shapes.random_walk_polar(steps, step_size=1000))
	plotter.write(g)

def plot(start, end): #(left 0; bottom 0; right 16158; top 11040)
	plotter.clear()
	plotter.set_origin_center()
	# plotter.select_pen(1)
	plotter.write(shapes.rectangle(16158,11040))
	# t = shapes.label(str(start) + "/" + str(end), 0.5, 0.5)
	# transforms.offset(t,(-2500, -plotsize[1]/2 + 200))
	# plotter.write(t)
	# filledcircle(0,0,1000,50,0)
	# filledcircle(1000,500,1000,50,1)
	# filledcircle(1000,-500,1500,150,0)
	offsetx = -2000
	offsety = 0
	# for x in xrange(1,10):
		# print(x % 4)
		# plotter.select_pen((x % 4)+1)
		# verticalfilledcircle(x*500 + offsetx, 0 + offsety, 3200+(x*250), 25,1)
		# verticalfibcircle(x*500 + offsetx, 0 + offsety, 200+(x*250), 5,0)

	# for x in xrange(1,12):
		# filledcircle(x*400 - 5000, 0, x*400, x*10,1 )
	takeawalk(80, 100)

	io.view(plotter)

# print(fib(1))
plot(0,1)
