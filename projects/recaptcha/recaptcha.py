from copy import deepcopy
from chiplotle import *
from PIL import Image
import sys
from lib.texttools  import plotfilledchar,writeword,plotchar
from svgpathtools import svg2paths, Path, Line, Arc, CubicBezier, QuadraticBezier
from chiplotle.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from chiplotle.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from lib.plothelpers import sign
from lib.recaptcha import recaptcha
from lib.tweetplot import TweetImgTxt, convertSVGtoTweet

filename = sys.argv[1]
virtualplotting = sys.argv[2]

#print(virtualplotting)
if (virtualplotting == 'virtual'):
		plotter = instantiate_virtual_plotter(type="DXY1300")
if (virtualplotting == 'real'):
		plotter = instantiate_plotters()[0]
		print("plotting for real")

# plotter.margins.hard.draw_outline()
# plotter = instantiate_plotters( )[0]
# real plotter says
#    Drawing limits: (left 0; bottom 0; right 16158; top 11040)
plotunit = 0.025
pltmax = [16158, 11040]
A3mm = [420,297]
A3 = [A3mm[0]/plotunit, A3mm[1]/plotunit]
paper = shapes.rectangle(A3mm[0]/plotunit, A3mm[1]/plotunit)
transforms.offset(paper,(A3mm[0]/plotunit/2,A3mm[1]/plotunit/2))
plotter.select_pen(2)
plotter.write(paper)
#coords = plotter.margins.soft.all_coordinates
# plotter.select_pen(1)
b = 0

# viewport = (10320,7920)
# horizon = (viewport[0] / 2, viewport[1] / 2)

import math
import random
import numpy as np
from scipy import signal
# from texttools  import *
import freetype



topCoord = []
plotter.select_pen(1)

def distortchar(char, size, font, xpos, ypos, distiter, distsize):
	c,w = plotfilledchar(char, size, font, xpos, ypos)
	g = shapes.group([])
	for r in range(distiter):
		bg = shapes.group([])
		k = deepcopy(c)
		for p in k:
			d = []
			for i in range(len(p)):
				d.append(random.randint(10,r*distsize+11))
			transforms.perpendicular_displace(p, d)
			bg.append(p)
		g.append(bg)
	w = g.width
	return g,w

def distortchar2(char, size, font, xpos, ypos, distiter, distsize):
	c,w = plotfilledchar(char, size, font, xpos, ypos)
	g = shapes.group([])
	for r in range(distiter):
		bg = shapes.group([])
		k = deepcopy(c)
		for p in k:
			d = []
			for i in range(len(p)):
				if (random.random() > 0.2):
					d.append(random.randint(r*20,r*21+distsize))
				else:
					d.append(0)

			transforms.perpendicular_displace(p, d)
			bg.append(p)
		g.append(bg)
	w = g.width
	return g,w

def plotdistortedword(word,xpos,ypos,size,font,pen,penundistorted):
	distiter = 4
	distsize = 100
	dcg = shapes.group([])
	cg = shapes.group([])
	for i,c in enumerate(str(word)):
		print("plotting :", c)
		# plotter.select_pen(pen)
		dcgb,dcwb = distortchar(c,size,font,xpos,ypos,distiter,distsize)
		dcg.append(dcgb)
		# plotter.select_pen(penundistorted)
		cgb,cwb = plotchar(c,size,font,xpos,ypos)
		cg.append(cgb)
		# plotter.write(cg)
		if i == 0:
			transforms.offset(dcg, (dcwb,0))
		xpos = xpos + dcwb
	return dcg,cg,dcg.width, dcg.height

def plotdistortedword2(word,xpos,ypos,size,font,pen,penundistorted):
	distiter = 15
	distsize = 500
	dcg = shapes.group([])
	cg = shapes.group([])
	for c in str(word):
		print("plotting :", c)
		# plotter.select_pen(pen)
		dcgb,dcwb = distortchar2(c,size,font,xpos,ypos,distiter,distsize)
		dcg.append(dcgb)
		# plotter.select_pen(penundistorted)
		cgb,cwb = plotchar(c,size,font,xpos,ypos)
		cg.append(cgb)
		# plotter.write(cg)
		xpos = xpos + dcwb
	return dcg,cg,dcg.width, dcg.height




# word = writeword("testmeNOW", 50, "poir.ttf",100, 230, "left" )

# plotter.write(word)
font = "subatomic.ttf"
# font = "poir.ttf"
print(font)
tsize = 50
xpos = 0
ypos = 50
index = random.randint(0,len(recaptcha[1]["words"]))
recaptchword = recaptcha[1]["words"][index]
wordlist = recaptchword.split("_")
printgroups = {}
# printgroups2 = []
pen1 = shapes.group([])
pen2 = shapes.group([])
for i,word in enumerate(wordlist):
	printgroups[i] = {}
	dcg, cg, dcgw, dcgh = plotdistortedword2(word,xpos,ypos,tsize,font,1,2 )
	if dcgw > A3[0]:
		scale = A3[0]/(dcgw+1000)
	else:
		scale = 1
	transforms.scale(dcg,scale)
	transforms.scale(cg,scale)
	dcgw = dcg.width
	dcgh = dcg.height
	printgroups[i]["dcg"] = dcg
	printgroups[i]["cg"] = cg
	printgroups[i]["dcgw"] = dcgw
	printgroups[i]["dcgh"] = dcgh
	pen1.append(dcg)
	pen2.append(cg)
	ypos = ypos + dcgh


w = pen1.width
h = pen1.height

transforms.offset(pen1,((A3[0]-w)/2, (A3[1]-h)/2))
transforms.offset(pen2,((A3[0]-w)/2, (A3[1]-h)/2))


plotter.select_pen(1)
plotter.write(pen1)
plotter.select_pen(2)
plotter.write(pen2)
	



# # plotter.select_pen(1)
# index = random.randint(0,len(recaptcha[1]["words"]))
# dcg, cg, dcgw, dcgh = plotdistortedword(recaptcha[1]["words"][index],xpos,ypos,tsize,"poir.ttf",1,2)
# plotter.select_pen(1)
# plotter.write(dcg)
# plotter.select_pen(2)
# plotter.write(cg)




# r = shapes.rectangle(8000,8000)
# transforms.offset(r,(4000,4000))
# plotter.write(r)
plotter.write(sign("recaptcha proto", A3[0]-100, 100 ))
io.export(plotter, filename, fmt='jpg')
io.export(plotter, filename, fmt='svg')
io.view(plotter)
jpg = filename + ".jpg"
svg = filename + ".svg"

# TweetImgTxt(jpg, "recaptchaplots " + recaptchword )
convertSVGtoTweet(svg, convertSVGtoTweet)