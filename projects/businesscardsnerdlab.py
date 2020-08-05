#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
address = ["kaotec.bandcamp.com","+32 474 436 640","info@kaotec.be","KAOTEC []<>","Kasper Jordaens"]
address = ["www.nerdlab.be", "+32 471 01 15 38", "marlies@nerdlab.be", "Marlies De Cock"]
##plot adress and artwork on businesscards

from chiplotle import *
from chiplotle.tools.io import export
from chiplotle.tools.plottertools import instantiate_virtual_plotter
import sys
filename = sys.argv[1]
virtualplotting = sys.argv[2]
#print(virtualplotting)
if (virtualplotting == 'virtual'):
		plotter = instantiate_virtual_plotter(type="DXY1300")

if (virtualplotting == 'real'):
		plotter = instantiate_plotters()[0]
		print("plotting for real")

from lib.plothelpers import plotgroup, plotzone, plotgroupnew, addAndPlotTextmm, calculatesvggroup,plotSVG
from lib.texttools import writeword
import random
import math
from noise import pnoise1, pnoise2, pnoise3

preview = shapes.group([])
globaloffset= [500,-2000]
# globaloffset = [0,0]
pltmax = [10320, 7920]
plotunit = 0.025 # 1 coordinate unit per plotter = 0.025 mm
papermm = [100,260]

businesscardsize=[85/plotunit,55/plotunit]

backgroundzone = [[5/plotunit, 0/plotunit],[80/plotunit, 40/plotunit]] 

addresszone = [[33/plotunit, 35/plotunit], [83/plotunit, 55/plotunit]]
logozone = [[5/plotunit, 40/plotunit], [25/plotunit, 50/plotunit]]   ## verhouding X/y = 2


plotPlotterOutline = True
plotPlotterOutline = False

plotPaperOutline = True
plotDrawingOutline = True
logooffset=(0,0)

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
    inputdata = generatemodulation(15,10, random.randint(1,100), 80)
    modulationdata = generatemodulation(10, 10, random.randint(1,100),400)
    r = renderline(inputdata, modulationdata, 0, 3000)
    g = plotgroup(r, 1, [(0,0),businesscardsize], (0,0), 1)
    return g


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


def brokenrotatedcircle (x,y, num, decay, segs, size):
    s = 2*math.pi/segs
    cg = shapes.group([])
    for i in xrange(num):
        c = shapes.group([])
        d = random.randint(1,int(segs/20)+2)
        e = 0
        while e < segs:
        # for x in xrange(10):
            g = random.randint(0,int(segs/d))
            seg = shapes.arc_circle(size*math.pow(decay,i), s*e, s*(e+g), segs, '2PI')
            e = e + g + g/2
            c.append(seg)
        transforms.rotate(c, math.degrees(360/segs/num*i))
        transforms.offset(c, (x+random.randint(0,size/20),y+random.randint(0,size/20)))
        cg.append(c)
    return cg

def fillsquare(xoffset,yoffset,width,height,angle,interval,outline):
    r = shapes.group([])
    if (outline == 1):
        o = shapes.rectangle(width,height)
        transforms.offset(o, (width/2,height/2))
        r.append(o)
    for x in xrange(int(width/interval)):
        r.append(shapes.line((x*interval,0),(x*interval,height)))
    transforms.offset(r,(xoffset,yoffset))
    return r

def subdivpattern(xoffset,yoffset,width,height,generations,numtypes):
    types = [60, 65, 75, 64, 80]
    p = shapes.group([])
    zones = [ [[0,0,3000,800]] ]

    for gen in xrange(generations):
        zones.append([])
        for sq in zones[gen]:
            print(sq[0],sq[2]-sq[0])
            print(sq[1],sq[3]-sq[1])
            x = random.randint(sq[0],sq[0]+(sq[2]-sq[0])/2)
            y = random.randint(sq[1],sq[1]+(sq[3]-sq[1])/2)

            zones[gen+1].append([sq[0],sq[1],x,y])
            zones[gen+1].append([sq[0],y,x,sq[3]])
            zones[gen+1].append([x,y,sq[2],sq[3]])
            zones[gen+1].append([x,sq[1],sq[2],y])
            print(zones)
    for idx,s in enumerate(zones[generations]):
        if idx < 2:
            filltype = types[1]
        else:
            filltype = types[random.randint(0,4)]
        r = fillsquare(s[0],s[1],s[2]-s[0],s[3]-s[1],90,filltype,0)
        transforms.offset(r,(xoffset,yoffset))
        # plotter.write(r)
        p.append(r)
    return p



def plotlogo(logozone):
    plotter.select_pen(1)
    file = "kaotec2.svg"
    kaotec = calculatesvggroup(file.encode('utf-8'))
    logo = plotgroupnew(kaotec['group'],logozone,1)
    # print(kaotec)
    transforms.offset(logo,logooffset )
    transforms.offset(logo,((logozone[1][0] - logozone[0][0])/2 , (logozone[1][1] - logozone[0][1])/2))
    preview.append(logo)
    plotter.write(logo)
    plotter.select_pen(2)
    file = "kaotec1.svg"
    kaotec = calculatesvggroup(file.encode('utf-8'))
    logo = plotgroupnew(kaotec['group'],logozone,1)
    transforms.offset(logo,logooffset )
    transforms.offset(logo,((logozone[1][0] - logozone[0][0])/2 , (logozone[1][1] - logozone[0][1])/2))
    # print(kaotec)
    plotter.write(logo)
    preview.append(logo)

# charwidthmax = 400 corresponds with charwidthfontunits = 0.66, 200 with 0.33 etc etc 
charwidthmax = 200
charwidthfontunits = 0.33


def writeaddress(address, adresszone):
    addressgroup = shapes.group([])
    maxheight = addresszone[1][1] - addresszone[0][1]
    rowheight = maxheight/len(address)
    maxlength = addresszone[1][0] - addresszone[0][0]
    lastheight = 0
    for i,l in enumerate(address):
        chars = len(l)
        if (maxlength/chars < charwidthmax):
            charwidth = charwidthfontunits/charwidthmax*maxlength/chars
        else:
            charwidth = charwidthfontunits
        # lastheight = charwidth/charwidthfontunits
        # t = shapes.label(l, 0.3, 0.3)
        # transforms.offset(t,(0,i*-150))
        # transforms.offset(t,(x,y))
        t =  shapes.label(str(l.encode('utf-8')), charwidth, charwidth)
        # transforms.offset(t, (addresszone[0][0]  - maxlength/2,addresszone[0][1] - i*(1.3 * lastheight)  - maxheight/2 ))
        transforms.offset(t, (addresszone[0][0], addresszone[0][1]))
        transforms.offset(t, (0,lastheight))
        # print ("textwidth =" , str(t.width))
        lastheight = lastheight + charwidth/charwidthfontunits*charwidthmax
        addressgroup.append(t)
    return addressgroup




logozone[0][0] = logozone[0][0] + globaloffset[0]
logozone[1][0] = logozone[1][0] + globaloffset[0]
logozone[0][1] = logozone[0][1] + globaloffset[1]
logozone[1][1] = logozone[1][1] + globaloffset[1]

addresszone[0][0] = addresszone[0][0] + globaloffset[0]
addresszone[1][0] = addresszone[1][0] + globaloffset[0]
addresszone[0][1] = addresszone[0][1] + globaloffset[1]
addresszone[1][1] = addresszone[1][1] + globaloffset[1]

backgroundzone[0][0] = backgroundzone[0][0] + globaloffset[0]
backgroundzone[1][0] = backgroundzone[1][0] + globaloffset[0]
backgroundzone[0][1] = backgroundzone[0][1] + globaloffset[1]
backgroundzone[1][1] = backgroundzone[1][1] + globaloffset[1]


yoffset = 2200


rulerX = shapes.ruler((0,0),(85/plotunit,0), [40, 400], 200, False)
rulerY = shapes.ruler((0,0),(0,55/plotunit), [40, 400], 200, False)

# plotter.write(rulerX)
# plotter.write(rulerY)



for i,y in enumerate(xrange(4)):
    
    # plotter.select_pen(1)
    # preview = shapes.group([])

    # if (i == 0):
    #     b = generateBackground()
    #     transforms.offset(b, (globaloffset[0], globaloffset[1] + (i+1)*yoffset))
    #     plotter.write(b)

    # if (i == 1):
    #     g = shapes.group([])
    #     for x in xrange(5):
    #         d = dosquare2(5+6*(x+1)*(x+1),500, 550*x,0)
    #         g.append(d)
    #     transforms.offset(g, (globaloffset[0] + 200, globaloffset[1] + 400 + (i+1)*yoffset))
    #     plotter.write(g)

    # if (i == 2):
    #     # (x,y, num, decay, segs, size):
    #     cc = brokenrotatedcircle(500,300,10,0.9,4, 500)
    #     transforms.offset(cc, (globaloffset[0] + 200, globaloffset[1] + 400 + (i+1)*yoffset))
    #     plotter.write(cc)
    #     cc = brokenrotatedcircle(1100,300,10,0.9,8, 500)
    #     transforms.offset(cc, (globaloffset[0] + 200, globaloffset[1] + 400 + (i+1)*yoffset))
    #     plotter.write(cc)
    #     cc = brokenrotatedcircle(1700,300,10,0.8,12, 500)
    #     transforms.offset(cc, (globaloffset[0] + 200, globaloffset[1] + 400 + (i+1)*yoffset))
    #     plotter.write(cc)
    #     cc = brokenrotatedcircle(2300,300,10,0.6,16, 500)
    #     transforms.offset(cc, (globaloffset[0] + 200, globaloffset[1] + 400 + (i+1)*yoffset))
    #     plotter.write(cc)

    # if (i == 3):
    #     p = shapes.group([])
    #     for x in xrange(1):
    #         # plotter.select_pen(x+1)        
    #         for y in xrange(1):
    #             xs = x*random.randint(0,100)
    #             ys = y*random.randint(0,100)
    #             w = random.randint(0,3500)
    #             h = random.randint(0,1000)
    #             p.append(subdivpattern(xs+(x*100),ys+(y*100),w,h,3,4))
    #     transforms.offset(p, (globaloffset[0] + 200, globaloffset[1] + 200 + (i+1)*yoffset))
    #     plotter.write(p)

    r = shapes.rectangle(businesscardsize[0],businesscardsize[1])
    transforms.offset(r, (businesscardsize[0]/2 + globaloffset[0], businesscardsize[1]/2 + globaloffset[1] + (i+1)*yoffset))
    plotter.write(r)
    
    logozone[0][0] = logozone[0][0] 
    logozone[1][0] = logozone[1][0] 
    logozone[0][1] = logozone[0][1] + yoffset
    logozone[1][1] = logozone[1][1] + yoffset
    
    addresszone[0][0] = addresszone[0][0]
    addresszone[1][0] = addresszone[1][0]
    addresszone[0][1] = addresszone[0][1] + yoffset
    addresszone[1][1] = addresszone[1][1] + yoffset

    backgroundzone[0][0] = backgroundzone[0][0]
    backgroundzone[1][0] = backgroundzone[1][0]
    backgroundzone[0][1] = backgroundzone[0][1] + yoffset
    backgroundzone[1][1] = backgroundzone[1][1] + yoffset

    # # plotlogo(logozone)
    # stuff = plotSVG(plotter,logozone,'nerdlabflat.svg')
    # # stuff2 = plotSVG(plotter,100,0,200,200,'nerdlabplotoptimized.svg')
    # plotter.select_pen(1)
    # plotter.write(stuff['groups'][0])
    # # plotter.write(stuff2['groups'][0])
    # plotter.select_pen(2)
    # plotter.write(stuff['groups'][1])
    # # plotter.write(stuff2['groups'][1])
    # plotter.select_pen(3)
    # plotter.write(stuff['groups'][2])
    # # plotter.write(stuff2['groups'][2])


    stuff = plotSVG(plotter,backgroundzone,'nerdlabflat.svg')
    plotter.select_pen(1)
    plotter.write(stuff['groups'][0])
    
    
    plotter.select_pen(2)
    cc = brokenrotatedcircle(600,700,random.randint(9,12),random.randint(80,99)/100.0,random.randint(4,12), 500)
    transforms.offset(cc, (globaloffset[0] + 200, globaloffset[1] + 400 + (i+1)*yoffset))
    plotter.write(cc)

    plotter.select_pen(3)
    cc = brokenrotatedcircle(2200,250,random.randint(9,20),random.randint(60,85)/100.0,random.randint(4,12), 500)
    transforms.offset(cc, (globaloffset[0] + 200, globaloffset[1] + 400 + (i+1)*yoffset))
    plotter.write(cc)

    plotter.select_pen(1)
    plotter.write(writeaddress(address, addresszone))

    plotter.write(writeword("NERDLAB",5, "SansSerif.ttf", 15/plotunit, 10/plotunit +i*yoffset, "left" ))

if (plotPlotterOutline):
    bounds = shapes.rectangle(pltmax[0],pltmax[1])
    transforms.offset(bounds,(pltmax[0]/2,pltmax[1]/2))
    preview.append(bounds)
    plotter.write(bounds)

if (plotPaperOutline):
    paper = shapes.rectangle(papermm[0]/plotunit, papermm[1]/plotunit)
    transforms.offset(paper,(papermm[0]/plotunit/2,papermm[1]/plotunit/2))
    preview.append(paper)
    plotter.write(paper)

if (plotDrawingOutline):
    drawing = shapes.rectangle(preview.width, preview.height)
    transforms.offset(drawing,(preview.width/2,preview.height/2))
    preview.append(drawing)
    plotter.write(drawing)





io.view(plotter)
