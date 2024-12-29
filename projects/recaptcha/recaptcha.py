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
tweetit = True
# tweetit = False
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
A3 = [A3mm[0]/plotunit, A3mm[1]/plotunit] # 16800, 11880  is bigger than pltmax!!
paper = shapes.rectangle(pltmax[0], pltmax[1])
transforms.offset(paper,(pltmax[0]/2,pltmax[1]/2))
# plotter.select_pen(2)
# plotter.write(paper)
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
					# d.append(random.randint(r*20,r*21+distsize))
					d.append(random.randint((r+1)*(distsize/4),(r+1)*distsize))
				else:
					d.append(0)
			recaptcha[1]["words"][index]
			# print(d)
			transforms.perpendicular_displace(p, d)
			bg.append(p)
		g.append(bg)
	w = g.width
	return g,w

def plotdistortedword(word,xpos,ypos,size,font,distiter,distsize):
	# distiter = 4
	# distsize = 100
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

def plotdistortedword2(word,xpos,ypos,size,font,distiter,distsize):
	# distiter = 5
	# distsize = 1500
	dcg = shapes.group([])
	cg = shapes.group([])
	for c in str(word):
		print("plotting :", c)
		# plotter.select_pen(pen)
		dcgb,dcwb = distortchar2(c,size,font,xpos,ypos,distiter,distsize)
		
		# plotter.select_pen(penundistorted)
		cgb,cwb = plotchar(c,size,font,xpos,ypos)
		minc, maxc = get_minmax_coordinates(cgb.points)
		padding = 50
		dcgb = cropPath(dcgb, minc[0]-padding,minc[1]-padding,maxc[0]+padding,maxc[1]+padding,False)

		cg.append(cgb)
		dcg.append(dcgb)
		# plotter.write(cg)
		xpos = xpos + dcwb
	return dcg,cg,dcg.width, dcg.height


# path =  shapes.path([(100,1000),(2000,1000),(340,2700)])
# print (path.points)
# plotter.write(path)

def cropPath(path, x1,y1,x2,y2,keep):
	"""
	crop a path by keeping (keep=True) or dropping (keep=False) all points inside 
	a drop zone (x1,y1)(x2,y2) and cutting line segments to a new location
	"""
	croppedpath = []
	for i,point in enumerate(path.points):
		print(point)
		x = point[0]
		y = point[1]
		if  ((x2 > x > x1) and (y2 > y > y1)):
			print("point ", i ," is in the zone")
			if keep:
				croppedpath.append((x,y))
		else:
			print("point ", i, " is outside the zone")
			if not keep:
				croppedpath.append((x,y))
		#check if first point of seg in is dropzone
		# if
	return shapes.path(croppedpath)
# cpath = cropPath(path,500,500,2500,1500, False)
# transforms.offset(cpath,(3000,0))
# plotter.write(cpath)

# word = writeword("testmeNOW", 50, "poir.ttf",100, 230, "left" )

# plotter.write(word)
# font = "USSR.ttf"
# font = "subatomic.ttf"
# font = "sqd.ttf"
font = "rus.ttf"
# font = "rale.ttf"
# font = "powerpuff.ttf"
# font = "poir.ttf"
# font = "neon.ttf"
# font = "magnetar.ttf"
# font = "Inception.ttf"
# font = "hunt.ttf"
# font = "discoduck.ttf"
# font = "Ali.ttf"
# font = "8b.ttf"
#
print(font)
tsize = 50
xpos = 0
ypos = 0
index = random.randint(0,len(recaptcha[1]["words"]))
# index = 2
recaptchword = recaptcha[1]["words"][index]
wordlist = recaptchword.split("_")
wordlist.reverse()


distiter = 9
distsize = 500
printgroups = {}
pen1 = shapes.group([])
pen2 = shapes.group([])

minmargin = 1000

for i,word in enumerate(wordlist):
	printgroups[i] = {}
	dcg, cg, dcgw, dcgh = plotdistortedword2(word,xpos,ypos,tsize,font,distiter,distsize)
	printgroups[i]["dcg"] = dcg
	printgroups[i]["cg"] = cg
	printgroups[i]["dcgw"] = dcgw
	printgroups[i]["dcgh"] = dcgh

print(printgroups)
#first we use same scale to fit evrything
maxw = []
for pg in printgroups.values():
	print(pg)
	maxw.append(pg["dcgw"])
w = max(maxw)
if w > pltmax[0]-minmargin:
	scale = (pltmax[0]-minmargin)/w * 0.9
else:
	scale = 0.9
for pg in printgroups.values():
	transforms.scale(pg["dcg"],scale)
	transforms.scale(pg["cg"],scale)

xoff = []
yoff = []
#calculate offset
for i,pg in enumerate(printgroups.values()):
	yofflen = len(printgroups)
	xoff.append((pltmax[0]-pg["dcg"].width)/2+minmargin)
	yoff.append(pg["dcg"].height)

sumy = sum(yoff)
yoffset = []
for i,pg in enumerate(printgroups.values()):
	print(i)
	print (yoff)
	print(sumy)
	if i == 0:
		yoffset.append(pltmax[1]/2 -yoff[0]/2+minmargin)
	else:
		yoffset.append(yoffset[-1]+yoff[i])
		# print(yoff)
		# yoffset.append(yoffset[-1])
#then we will build the banner 

for i,pg in enumerate(printgroups.values()):
	transforms.offset(pg["dcg"],(xoff[i],yoffset[i]))
	transforms.offset(pg["cg"],(xoff[i],yoffset[i]))
	pen1.append(pg["dcg"])
	pen2.append(pg["cg"])


preview = shapes.group([])
preview.append(paper)
preview.append(pen1)
preview.append(pen2)
io.view(preview)


ready = input('drawing ok? press 1 to continue')
print(ready)
if(ready == 1):
	plotter.select_pen(1)
	plotter.write(pen1)
	plotter.select_pen(2)
	plotter.write(pen2)
	transforms.offset(pen2,(50,0))
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

	plotter.write(sign("recaptcha " + recaptcha[1]["words"][index], pltmax[0]-200, 100 ))
	io.export(plotter, filename, fmt='jpg')
	io.export(plotter, filename, fmt='svg')
	io.view(plotter)
	jpg = filename + ".jpg"
	svg = filename + ".svg"

	# TweetImgTxt(jpg, "recaptchaplots " + recaptchword )
	if tweetit:
		convertSVGtoTweet(svg,  "recaptchaplots " + recaptchword )