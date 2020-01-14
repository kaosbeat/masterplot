#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
# address = ["Gianni Degryse", "Rozenhoed 30", "9921 Vinderhoute"]
# address = ["Nana Takvarelia", "27 Betlemi street", "0105 Tbilisi", "Georgia"]
# address = ["Kasper Jordaens", "Londenstraat 40", "9000 Gent", u"Belgie"]
# address = ["KAOTEC []<>", "Modular Mountains", "kaotec.bandcamp.com"]
# address   = ["Johannes Taelman", "Axoloti HQ", "Ghent", "Belgium"]
# address   = ["Tom", "Van de Wiele"] 
address   = ["Special Suntapes Promo Copy"] 
##plot adress and artwork on envelopes
from chiplotle import *
from chiplotle.tools.io import export
from chiplotle.tools.plottertools import instantiate_virtual_plotter
from lib.plothelpers import plotgroup, plotzone, plotgroupnew, addAndPlotTextmm, calculatesvggroup
from lib.texttools import writeword
import random
import sys
import math

plotPlotterOutline = False
plotPaperOutline = True
plotDrawingOutline = False

# pltmax = [10320, 7920] >>> ???
pltmax = [16158, 11040]
plotunit = 0.025 # 1 coordinate unit per plotter = 0.025 mm
envelopesizemm = [320,260]
addresszone = [(160/plotunit, 60/plotunit), (300/plotunit, 50/plotunit)]
logozone = [(280/plotunit, 20/plotunit), (320/plotunit, 40/plotunit)]   ## verhouding X/y = 1/2
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
            charwidth = 0.66/400*maxlength/chars
        else:
            charwidth = 0.66
        # t = shapes.label(l, 0.3, 0.3)
        # transforms.offset(t,(0,i*-150))
        # transforms.offset(t,(x,y))
        t =  shapes.label(str(l.encode('utf-8')), charwidth, charwidth)
        transforms.offset(t, (addresszone[0][0],addresszone[0][1] - i*(charwidth/0.66*400)))
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
        for y in xrange(9):
            g.append(dosquare2(10 + 15*x + 10*y, 900, x*1000, y*1100))
    return g


# ruler = shapes.ruler((0,0),(320/plotunit,0), [40, 400], 200, False)



plotter.select_pen(1)
plotter.write(writeaddress(address, addresszone))
p = decorate()
transforms.offset(p, (500,500))
# plotter.write(p)



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
text.append(writeword("Modular", 20, "USSR.ttf",0,0, "right"))
transforms.offset(text, ( 310/plotunit,220/plotunit))
plotter.write(text)
text = shapes.group([])
text.append(writeword("Mountains", 20, "USSR.ttf",0,0, "right"))
transforms.offset(text, ( 310/plotunit,190/plotunit))
plotter.write(text)
text = shapes.group([])
text.append(writeword("KAOTEC", 20, "USSR.ttf",0,0, "right"))
transforms.offset(text, ( 310/plotunit,140/plotunit))
# transforms.rotate(text, math.radians(45))
plotter.write(text)

# plotter.write(ruler)
plotter.select_pen(1)
# plotter.write(bounds)
plotter.write(paper)
# plotter.write(a)
io.view(plotter)
