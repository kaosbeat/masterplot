#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
# address = ["KAOTEC []<>", "Modular Mountains", "kaotec.bandcamp.com"]
# address   = ["Johannes Taelman", "Axoloti HQ", "Ghent", "Belgium"]
# address   = ["Tom", "Van de Wiele"] 
# address   = ["Today is the oldest you have been ", 
# 			 "and the youngest you will ever be.",
# 			 "Make the most of it!              "]
# address   = ["Just remember," ,"once you're over the hill,", "you begin to pick up speed."] #Charles Schulz
#"You don't get older, you get better." #Shirley Bassey
#“You are only young once, but you can be immature for a lifetime. Happy birthday!”
# address = ["Forget about the past, you can't change it.", "Forget about the future, you can't predict it.","Forget about the present, and just drink it"]

# address = [
# 		"towards the decapod of estrange              ",
# 		"we happen pertinent two despairing           ", 
# 		"phoenix bathing upstage a marine bucket      ",
# 		"           balance the dextrous inquiry      ",
# 		"           supporter of sweeping             ",
# 		"we beg surplus air entry the stellar         ",
# 		"we desire also clean absorption the astronaut",
# 		"squirrel taste diner on a camel              ",
# 		"the philanthropic of parking                 ",
# 		"complete pigeonhole of choreographer         ",
# 		"the virtuoso reply if you suppose            ",
# 		"ambitious of doing voting someday            ",
# 		"I manufacture music                          "
# 		]

address = ["een vrolijke kerst", "en een spetterend 2021", "Sarah & Kasper", "Merel, Josse & Ireen"]



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
envelopesizemm = [210,297]
cardsize = (100,130)
card1zone = [(0/plotunit, 0/plotunit), (cardsize[0]/plotunit, cardsize[1]/plotunit)]
card2zone = [(cardsize[0]/plotunit, 0/plotunit), (cardsize[0]*2/plotunit, cardsize[1]/plotunit)]
card3zone = [(0/plotunit, cardsize[1]/plotunit), (cardsize[0]/plotunit, cardsize[1]*2/plotunit)]
card4zone = [(cardsize[0]/plotunit, cardsize[1]/plotunit), (cardsize[0]*2/plotunit, cardsize[1]*2/plotunit)]
card5zone = [(cardsize[0]*2/plotunit, 0/plotunit), (cardsize[0]*3/plotunit, cardsize[1]/plotunit)]
card6zone = [(cardsize[0]*3/plotunit, 0/plotunit), (cardsize[0]*4/plotunit, cardsize[1]/plotunit)]
card7zone = [(cardsize[0]*2/plotunit, cardsize[1]/plotunit), (cardsize[0]*3/plotunit, cardsize[1]*2/plotunit)]
card8zone = [(cardsize[0]*3/plotunit, cardsize[1]/plotunit), (cardsize[0]*4/plotunit, cardsize[1]*2/plotunit)]
addresszone = [(10/plotunit, 180/plotunit), (200/plotunit, 10/plotunit)]
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




def xmasball1a():
	g = shapes.group([])
	g.append(shapes.line((0,0),(1,1)))
	g.append(shapes.line( 	(cardsize[0]/plotunit-1,cardsize[1]/plotunit-1), (cardsize[0]/plotunit,cardsize[1]/plotunit) ) )
	r = shapes.rectangle(cardsize[0]/plotunit,cardsize[1]/plotunit)
	transforms.offset(r, (cardsize[0]/plotunit/2,cardsize[1]/plotunit/2))
	# g.append(r)


	xpos = cardsize[0]*0.3/plotunit
	ypos = cardsize[1]/plotunit
	linelength = cardsize[1]*0.55/plotunit
	cwidth = 4
	cfactor = 1.2
	cheight = 5
	ballsize = 1000
	c = shapes.group([])
	c.append(shapes.line((0,-linelength),(0,0)))
	c.append(shapes.line(((-cwidth/2)/plotunit,-linelength ), ((cwidth/2)/plotunit, -linelength )))
	c.append(shapes.line(((-cwidth/2)/plotunit  ,-linelength) , ((-cfactor*cwidth/2)/plotunit  ,-linelength - cheight/plotunit)))
	c.append(shapes.line((0 ,-linelength) , (0  ,-linelength - cheight*cfactor/plotunit)))
	c.append(shapes.line(((cwidth/2)/plotunit  ,-linelength) , ((cfactor*cwidth/2)/plotunit  ,-linelength - cheight/plotunit)))
	transforms.offset(c, (xpos,ypos))
	g.append(c)

	b = shapes.random_walk_polar(50,ballsize)
	transforms.offset(b,(xpos,ypos-linelength-ballsize-cheight/plotunit))
	g.append(b)


	addressz = [(cardsize[0]/plotunit, 100/plotunit), (cardsize[0]/plotunit, cardsize[1]/plotunit/3)]
	a = writeaddress(address,addressz)

	transforms.offset(a, (cardsize[0]/plotunit*0.5,-cardsize[1]/plotunit))
	transforms.scale(a, 0.7)
	# g.append(a)



	return g

def xmasball1b():
	g = shapes.group([])
	g.append(shapes.line((0,0),(1,1)))
	g.append(shapes.line( 	(cardsize[0]/plotunit-1,cardsize[1]/plotunit-1), (cardsize[0]/plotunit,cardsize[1]/plotunit) ) )
	r = shapes.rectangle(cardsize[0]/plotunit,cardsize[1]/plotunit)
	transforms.offset(r, (cardsize[0]/plotunit/2,cardsize[1]/plotunit/2))
	# g.append(r)


	xpos = cardsize[0]*0.6/plotunit
	ypos = cardsize[1]/plotunit
	linelength = cardsize[1]*0.15/plotunit
	cwidth = 4
	cfactor = 1.2
	cheight = 5
	ballsize = 2200
	c = shapes.group([])
	c.append(shapes.line((0,-linelength),(0,0)))
	c.append(shapes.line(((-cwidth/2)/plotunit,-linelength ), ((cwidth/2)/plotunit, -linelength )))
	c.append(shapes.line(((-cwidth/2)/plotunit  ,-linelength) , ((-cfactor*cwidth/2)/plotunit  ,-linelength - cheight/plotunit)))
	c.append(shapes.line((0 ,-linelength) , (0  ,-linelength - cheight*cfactor/plotunit)))
	c.append(shapes.line(((cwidth/2)/plotunit  ,-linelength) , ((cfactor*cwidth/2)/plotunit  ,-linelength - cheight/plotunit)))
	transforms.offset(c, (xpos,ypos))
	g.append(c)

	b = shapes.ellipse(ballsize, ballsize, 36)
	transforms.offset(b,(xpos,ypos-linelength-ballsize/2-cheight/plotunit))
	# g.append(b)



	addressz = [(cardsize[0]/plotunit, 100/plotunit), (cardsize[0]/plotunit, cardsize[1]/plotunit/3)]
	a = writeaddress(address,addressz)

	transforms.offset(a, (cardsize[0]/plotunit*0.5,-cardsize[1]/plotunit))
	transforms.scale(a, 0.7)
	# g.append(a)



	return g	



def xmasballb():
	g = shapes.group([])
	g.append(shapes.line((0,0),(1,1)))
	g.append(shapes.line( 	(cardsize[0]/plotunit-1,cardsize[1]/plotunit-1), (cardsize[0]/plotunit,cardsize[1]/plotunit) ) )
	r = shapes.rectangle(cardsize[0]/plotunit,cardsize[1]/plotunit)
	transforms.offset(r, (cardsize[0]/plotunit/2,cardsize[1]/plotunit/2))
	# g.append(r)


	xpos = cardsize[0]*0.3/plotunit
	ypos = cardsize[1]/plotunit
	linelength = cardsize[1]*0.55/plotunit
	cwidth = 4
	cfactor = 1.2
	cheight = 5
	ballsize = 1000
	c = shapes.group([])
	c.append(shapes.line((0,-linelength),(0,0)))
	c.append(shapes.line(((-cwidth/2)/plotunit,-linelength ), ((cwidth/2)/plotunit, -linelength )))
	c.append(shapes.line(((-cwidth/2)/plotunit  ,-linelength) , ((-cfactor*cwidth/2)/plotunit  ,-linelength - cheight/plotunit)))
	c.append(shapes.line((0 ,-linelength) , (0  ,-linelength - cheight*cfactor/plotunit)))
	c.append(shapes.line(((cwidth/2)/plotunit  ,-linelength) , ((cfactor*cwidth/2)/plotunit  ,-linelength - cheight/plotunit)))
	transforms.offset(c, (xpos,ypos))
	g.append(c)

	b = shapes.random_walk_polar(50,ballsize)
	transforms.offset(b,(xpos,ypos-linelength-ballsize-cheight/plotunit))
	# g.append(b)


	addressz = [(cardsize[0]/plotunit, 100/plotunit), (cardsize[0]/plotunit, cardsize[1]/plotunit/3)]
	a = writeaddress(address,addressz)

	transforms.offset(a, (cardsize[0]/plotunit*0.5,-cardsize[1]/plotunit))
	transforms.scale(a, 0.7)
	# g.append(a)



	return g






def xmasball2():
	g = shapes.group([])
	g.append(shapes.line((0,0),(1,1)))
	g.append(shapes.line( 	(cardsize[0]/plotunit-1,cardsize[1]/plotunit-1), (cardsize[0]/plotunit,cardsize[1]/plotunit) ) )
	r = shapes.rectangle(cardsize[0]/plotunit,cardsize[1]/plotunit)
	transforms.offset(r, (cardsize[0]/plotunit/2,cardsize[1]/plotunit/2))
	# g.append(r)


	xpos = cardsize[0]*0.3/plotunit
	ypos = cardsize[1]/plotunit
	linelength = cardsize[1]*0.55/plotunit
	cwidth = 4
	cfactor = 1.2
	cheight = 5
	ballsize = 1000
	c = shapes.group([])
	c.append(shapes.line((0,-linelength),(0,0)))
	c.append(shapes.line(((-cwidth/2)/plotunit,-linelength ), ((cwidth/2)/plotunit, -linelength )))
	c.append(shapes.line(((-cwidth/2)/plotunit  ,-linelength) , ((-cfactor*cwidth/2)/plotunit  ,-linelength - cheight/plotunit)))
	c.append(shapes.line((0 ,-linelength) , (0  ,-linelength - cheight*cfactor/plotunit)))
	c.append(shapes.line(((cwidth/2)/plotunit  ,-linelength) , ((cfactor*cwidth/2)/plotunit  ,-linelength - cheight/plotunit)))
	transforms.offset(c, (xpos,ypos))
	# g.append(c)

	b = shapes.random_walk_polar(50,ballsize)
	transforms.offset(b,(xpos,ypos-linelength-ballsize-cheight/plotunit))
	# g.append(b)

	xpos = cardsize[0]*0.6/plotunit
	linelength = cardsize[1]*0.35/plotunit
	ballsize = 2800
	c = shapes.group([])
	c.append(shapes.line((0,-linelength),(0,0)))
	c.append(shapes.line(((-cwidth/2)/plotunit,-linelength ), ((cwidth/2)/plotunit, -linelength )))
	c.append(shapes.line(((-cwidth/2)/plotunit  ,-linelength) , ((-cfactor*cwidth/2)/plotunit  ,-linelength - cheight/plotunit)))
	c.append(shapes.line((0 ,-linelength) , (0  ,-linelength - cheight*cfactor/plotunit)))
	c.append(shapes.line(((cwidth/2)/plotunit  ,-linelength) , ((cfactor*cwidth/2)/plotunit  ,-linelength - cheight/plotunit)))
	transforms.offset(c, (xpos,ypos))
	g.append(c)

	b = shapes.ellipse(ballsize, ballsize, 36)
	transforms.offset(b,(xpos,ypos-linelength-ballsize/2-cheight/plotunit))
	# g.append(b)



	addressz = [(cardsize[0]/plotunit, 100/plotunit), (cardsize[0]/plotunit, cardsize[1]/plotunit/3)]
	a = writeaddress(address,addressz)

	transforms.offset(a, (cardsize[0]/plotunit*0.5,-cardsize[1]/plotunit))
	transforms.scale(a, 0.7)
	# g.append(a)



	return g	

def xmasball2b():
	g = shapes.group([])
	g.append(shapes.line((0,0),(1,1)))
	g.append(shapes.line( 	(cardsize[0]/plotunit-1,cardsize[1]/plotunit-1), (cardsize[0]/plotunit,cardsize[1]/plotunit) ) )
	
	xpos = 0.15*cardsize[1]/plotunit
	ypos = 0.8*cardsize[1]/plotunit
	twinklewidth = 1
	twinklesize = 600
	for i in xrange(twinklewidth):
		jitX = random.randint(0,10)/10.0
		jitY = random.randint(0,10)/10.0
		print (jitX,jitY)
		t = twinkle(twinklesize,12)
		# transforms.offset(t,(xpos+(jitX-0.5)*cardsize[0]/plotunit/3,ypos+(jitY-0.5)*cardsize[0]/plotunit/3))
		transforms.offset(t, (xpos,ypos))
		g.append(t)
	return g	




def twinkle(size,div):
	t = shapes.group([])
	# t.append(shapes.random_walk_polar(20,1000))
	
	for i in xrange(div+1):
		a = 2*3.14/div*i
		fact = random.random() +0.5
		l = shapes.line((0,0),(math.sin(i)*size*fact,math.cos(i)*size*fact))
		t.append(l)
	# t.append(shapes.star_crisscross(1000, 1000, num_points=5))
	return t



# ruler = shapes.ruler((0,0),(320/plotunit,0), [40, 400], 200, False)



plotter.select_pen(1)
# plotter.write(writeaddress(address, addresszone))
# plotter.write(xmasball())
# p = decorate()
# transforms.offset(p, (500,500))
# plotter.write(p)
globaloffset = (cardsize[0]/2/plotunit,cardsize[1]/2/plotunit)


cards = shapes.group([])
cards.append(plotgroupnew(xmasball1a(),card1zone, 1.05))
cards.append(plotgroupnew(xmasball1b(),card1zone, 1.05))
cards.append(plotgroupnew(xmasball2(),card2zone, 1.05))
cards.append(plotgroupnew(xmasball1a(),card3zone, 1.05))
cards.append(plotgroupnew(xmasball1b(),card3zone, 1.05))
cards.append(plotgroupnew(xmasball2(),card4zone, 1.05))
cards.append(plotgroupnew(xmasball1a(),card5zone, 1.05))
cards.append(plotgroupnew(xmasball1b(),card5zone, 1.05))
cards.append(plotgroupnew(xmasball2(),card6zone, 1.05))
cards.append(plotgroupnew(xmasball1a(),card7zone, 1.05))
cards.append(plotgroupnew(xmasball1b(),card7zone, 1.05))
cards.append(plotgroupnew(xmasball2(),card8zone, 1.05))
transforms.offset(cards, (globaloffset[0], globaloffset[1]))
plotter.write(cards)

plotter.select_pen(2)

cards = shapes.group([])

cards.append(plotgroupnew(xmasball2b(),card1zone, 1.05))
cards.append(plotgroupnew(xmasball2b(),card2zone, 1.05))
cards.append(plotgroupnew(xmasball2b(),card3zone, 1.05))
cards.append(plotgroupnew(xmasball2b(),card4zone, 1.05))
cards.append(plotgroupnew(xmasball2b(),card5zone, 1.05))
cards.append(plotgroupnew(xmasball2b(),card6zone, 1.05))
cards.append(plotgroupnew(xmasball2b(),card7zone, 1.05))
cards.append(plotgroupnew(xmasball2b(),card8zone, 1.05))
transforms.offset(cards, (globaloffset[0], globaloffset[1]))
plotter.write(cards)

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


# text = shapes.group([])
# text.append(writeword("This_is_not", 15, "USSR.ttf",0,0, "right"))
# transforms.offset(text, ( 190/plotunit,70/plotunit))
# plotter.write(text)
# text = shapes.group([])
# text.append(writeword("an_album", 15, "USSR.ttf",0,0, "right"))
# transforms.offset(text, ( 190/plotunit,40/plotunit))
# plotter.write(text)
# text = shapes.group([])
# text.append(writeword("#1/12", 15, "USSR.ttf",0,0, "right"))
# transforms.offset(text, ( 190/plotunit,10/plotunit))
# # transforms.rotate(text, math.radians(45))
# plotter.write(text)

# plotter.write(ruler)
# plotter.select_pen(1)
# plotter.write(bounds)
# plotter.write(paper)
# plotter.write(a)


if (plotPaperOutline):
	paper = shapes.rectangle(envelopesizemm[0]/plotunit, envelopesizemm[1]/plotunit)
	transforms.offset(paper,(envelopesizemm[0]/plotunit/2,envelopesizemm[1]/plotunit/2))

	plotter.write(paper)
io.view(plotter)
