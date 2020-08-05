#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
# address = ["Gianni Degryse", "Rozenhoed 30", "9921 Vinderhoute"]
# address = ["Nana Takvarelia", "27 Betlemi street", "0105 Tbilisi", "Georgia"]
# address = ["Kasper Jordaens", "Londenstraat 40", "9000 Gent", u"Belgie"]
# address = ["KAOTEC []<>", "Modular Mountains", "kaotec.bandcamp.com"]
# address   = ["Johannes Taelman", "Axoloti HQ", "Ghent", "Belgium"]
# address   = ["Tom", "Van de Wiele"] 
address   = ["Today is the oldest you have been, and the youngest you will ever be. Make the most of it!"]
address   = ["Just remember," ,"once you're over the hill,", "you begin to pick up speed."] #Charles Schulz
#"You don't get older, you get better." #Shirley Bassey
#“You are only young once, but you can be immature for a lifetime. Happy birthday!”
address = ["Forget about the past, you can't change it.", "Forget about the future, you can't predict it.","Forget about the present, and just drink it"]


##plot adress and artwork on envelopes
from chiplotle import *
from chiplotle.tools.io import export
from chiplotle.tools.plottertools import instantiate_virtual_plotter
from lib.plothelpers import plotgroup, plotzone, plotgroupnew, addAndPlotTextmm, calculatesvggroup
from lib.texttools import writeword
import random
import sys
import math
from noise import pnoise1, pnoise2, pnoise3
plotPlotterOutline = False
plotPaperOutline = False
plotDrawingOutline = False

# pltmax = [10320, 7920] >>> ???
pltmax = [16158, 11040]
plotunit = 0.025 # 1 coordinate unit per plotter = 0.025 mm
envelopesizemm = [230,100]
addresszone = [(10/plotunit, 80/plotunit), (230/plotunit, 100/plotunit)]
logozone = [(280/plotunit, 10/plotunit), (320/plotunit, 30/plotunit)]   ## verhouding X/y = 1/2
backgroundzone = [[5/plotunit, 0/plotunit],[80/plotunit, 40/plotunit]] 
filename = sys.argv[1]
virtualplotting = sys.argv[2]

#print(virtualplotting)
if (virtualplotting == 'virtual'):
		plotter = instantiate_virtual_plotter(type="DXY1300")
if (virtualplotting == 'real'):
		plotter = instantiate_plotters()[0]
		print("plotting for real")

if (plotPlotterOutline):
    bounds = shapes.rectangle(pltmax[0],pltmax[1])
    transforms.offset(bounds,(pltmax[0]/2,pltmax[1]/2))

    plotter.write(bounds)

if (plotPaperOutline):
    paper = shapes.rectangle(envelopesizemm[0]/plotunit, envelopesizemm[1]/plotunit)
    transforms.offset(paper,(envelopesizemm[0]/plotunit/2,envelopesizemm[1]/plotunit/2))

    plotter.write(paper)

def testgroup():
    g = shapes.group([])
    for x in xrange(10):
        r = shapes.rectangle(random.randint(0,1000),random.randint(0,1000))
        transforms.offset(r, (random.randint(-3000,3000),random.randint(-3000,3000)))
        g.append(r)
    return g


def writeaddress(address, adresszone):

    addressgroup = shapes.group([])
    maxheight = addresszone[1][1] - addresszone[0][1]
    rowheight = maxheight/len(address)
    maxlength = addresszone[1][0] - addresszone[0][0]
    for i,l in enumerate(address):
        chars = len(l)
        if (maxlength/chars < 400):
            charwidth = 0.33/400*maxlength/chars
        else:
            charwidth = 0.33
        # t = shapes.label(l, 0.3, 0.3)
        # transforms.offset(t,(0,i*-150))
        # transforms.offset(t,(x,y))
        t =  shapes.label(str(l.encode('utf-8')), charwidth, charwidth)
        transforms.offset(t, (addresszone[0][0],addresszone[0][1] - i*(charwidth/0.33*400)))
        # print ("textwidth =" , str(t.width))
        addressgroup.append(t)
    return addressgroup

def dosquare2(depth,size,xoff,yoff):
    l = shapes.group([])

    #size = 250
    x = 0
    dx = 0
    y = 0
    dy = 0
    pa = [(x,y)]
    for i in xrange(depth):
        h = random.randint(0,2)
        v = random.randint(0,2)
        if h == 1:
            dx = random.randint(0,size)
        if v == 1:
            dy = random.randint(0,size)
        #print((x,y),(dx,dy))
        pa.append((dx,dy))
        #l.append(shapes.line((x,y),(dx,dy)))
        x = dx
        y = dy
    p = shapes.path(pa)
    transforms.offset(p, (xoff, yoff))
    # plotter.write(p)
    return p




def decorate():
    g = shapes.group([])
    for x in xrange(4):
        for y in xrange(2):
            g.append(dosquare2(10 + 15*x + 10*y, 900, x*950, y*1000))
    return g


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

spacingA = 10000
spacingB = 0.99
spacingC = 1500

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

def generateBackground():
    inputdata = generatemodulation(20,20, random.randint(1,100), 80)
    modulationdata = generatemodulation(10, 10, random.randint(1,100),1500)
    r = renderline(inputdata, modulationdata, 0, 4000)
    g = plotgroup(r, 1, [(0,0),(5000,5000)], (0,0), 1)
    return g



# ruler = shapes.ruler((0,0),(320/plotunit,0), [40, 400], 200, False)



plotter.select_pen(1)
plotter.write(writeaddress(address, addresszone))
p = decorate()
transforms.offset(p, (500,500))
plotter.write(p)
globaloffset = (0,0)

b = generateBackground()
transforms.offset(b, (globaloffset[0], globaloffset[1]))
# plotter.write(b)

# file = "kaotec2.svg"
# kaotec = calculatesvggroup(file.encode('utf-8'))
# logo = plotgroup(kaotec['group'],1,logozone,(0,0),2)
# # # print(kaotec)
# plotter.write(logo)
# plotter.select_pen(2)
# file = "kaotec1.svg"
# kaotec = calculatesvggroup(file.encode('utf-8'))
# logo = plotgroup(kaotec['group'],1,logozone,(0,0),2)
# # # print(kaotec)
# plotter.write(logo)

plotter.select_pen(2)
text = shapes.group([])
text.append(writeword("Happy", 15, "USSR.ttf",0,0, "right"))
transforms.offset(text, ( 230/plotunit,70/plotunit))
plotter.write(text)
text = shapes.group([])
text.append(writeword("Birthday", 15, "USSR.ttf",0,0, "right"))
transforms.offset(text, ( 230/plotunit,40/plotunit))
plotter.write(text)
text = shapes.group([])
text.append(writeword("Julie", 15, "USSR.ttf",0,0, "right"))
transforms.offset(text, ( 230/plotunit,10/plotunit))
# transforms.rotate(text, math.radians(45))
plotter.write(text)

# plotter.write(ruler)
# plotter.select_pen(1)
# plotter.write(bounds)
# plotter.write(paper)
# plotter.write(a)
io.view(plotter)
