from __future__ import division
from chiplotle import *

from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")
# plotter.margins.hard.draw_outline()
#plotter = instantiate_plotters( )[0]
# real plotter says
#    Drawing limits: (left 0; bottom 0; right 16158; top 11040)

pltmax = [16158, 11040]
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

#additive syths, 
#	plot a sine wave using a shape (circle)
#	plot a saw wave using a shape (triangle)
# 	plot the results using a combination shape
# first wave

rez = 200 #keep it below 300 unless you know what you do
size = 200
noise = size*1.5
interval = 120
randpointer = 90
randpointerjump = 10
randpointerbackrange = 0.5 #(number between 0.50-0.99)
wav1 = np.linspace(0,2*np.pi,rez)
wav2 = np.linspace(0,np.pi,rez)
wav3 = np.linspace(0,8*np.pi,rez)
randwavesize = size/10
g = shapes.group([])


def plotchar(char, size, font, xpos, ypos):
#code adapted from freetype-py vector example
  global plotter
  face = freetype.Face(font)
  face.set_char_size( size*64 )
  face.load_char(char)
  slot = face.glyph
  outline = slot.outline
  points = np.array(outline.points, dtype=[('x',float), ('y',float)])
  x, y = points['x'], points['y']
  start, end = 0, 0
  VERTS, CODES = [], []
  # Iterate over each contour
  for i in range(len(outline.contours)):
      end    = outline.contours[i]
      points = outline.points[start:end+1]
      points.append(points[0])
      tags   = outline.tags[start:end+1]
      tags.append(tags[0])

      segments = [ [points[0],], ]
      for j in range(1, len(points) ):
          segments[-1].append(points[j])
          if tags[j] & (1 << 0) and j < (len(points)-1):
              segments.append( [points[j],] )
      verts = [points[0], ]
      # codes = [Path.MOVETO,]
      for segment in segments:
          if len(segment) == 2:
              verts.extend(segment[1:])
              # codes.extend([Path.LINETO])
          elif len(segment) == 3:
              verts.extend(segment[1:])
              # codes.extend([Path.CURVE3, Path.CURVE3])
          else:
              verts.append(segment[1])
              # codes.append(Path.CURVE3)
              for i in range(1,len(segment)-2):
                  A,B = segment[i], segment[i+1]
                  C = ((A[0]+B[0])/2.0, (A[1]+B[1])/2.0)
                  verts.extend([ C, B ])
                  # codes.extend([ Path.CURVE3, Path.CURVE3])
              verts.append(segment[-1])
              # codes.append(Path.CURVE3)
      VERTS.extend(verts)
      # CODES.extend(codes)
      start = end+1
  g = shapes.group([])
  g.append(shapes.path(VERTS))
  transforms.offset(g, (xpos, ypos))
  #print "size is ", g.width
  plotter.write(g)
  return g.width




  # print VERTS
def writeword(textstring, size, font, xpos, ypos):
	print (textstring)
	tt = xpos
	for char in textstring:
		tt = tt + plotchar(char, size, font, tt, ypos)






def getrandompoint(wave, table, Vsize):	
	global randpointer
	# global randpointerjump
	randpointer = randpointer + int(randpointerjump*randpointerbackrange - random.randint(0, randpointerjump))
	if randpointer < 0:
		randpointer = 0
	if randpointer >= rez:
		randpointer = rez-1
	# print randpointer
	if table == "sin":
		return (randpointer*interval, np.sin(wave[randpointer])*Vsize)
	if table == "cos":
		return (randpointer*interval, np.cos(wave[randpointer])*Vsize)
	if table == "saw":
		return (randpointer*interval, signal.sawtooth(wave[randpointer])*Vsize)


def somewaves(pen,waves, subwaves, wavperiod = [], wavtype = [], wavesize = [], waveshape = []):
	global noise
	global plotter
	global g
	plotter.select_pen(pen)
	for idx, wav in enumerate(wavperiod):
		p1 = getrandompoint(wav, wavtype[idx], wavesize[idx])
		p2 = getrandompoint(wav, wavtype[len(wavtype) - 1], wavesize[len(wavtype) -1])
		# print p1
		while randpointer < rez-1:
			print randpointer
		# for i in range(int(randwavesize)):
			for w in range(len(wavtype)):
				l = shapes.line(p1, p2)
				transforms.noise(l, noise)
				g.append(l)
				p1 = p2
				p2 = getrandompoint(wav, wavtype[w], wavesize[w])

	plotter.write(g)

#somewaves(2,False, True, [wav3, wav1], ["cos", "saw", "saw", "sin", "sin"], [1500, 5100, 500, 2000, 6000], ["rect", "cross", "cross", "rect", "cross"])  
#somewaves(1,False, True, [wav1, wav2, wav2, wav1], ["sin", "cos", "cos", "sin"], [5100, 1000, 6500, 1000], ["rect", "cross", "cross", "cross"])  
#somewaves(1,False, True, [wav2, wav3, wav2, wav1], ["sin", "cos", "sin", "sin"], [5100, 1000, 6500, 1000], ["rect", "cross", "cross", "cross"])  

def wavesdown(pen, freq, offset, width, min, max):
	global plotter
	global g
	density = freq
	quantity = width
	g = shapes.group([])
	plotter.select_pen((pen%2)+1)
	#offset = random.randint(0, width)
	offset = density*quantity/5*3*(pen+1) + (pen%2*density/2)
	# maxheight = random.randint(min, max)
	#max = random.randint(min + 100,3000)
	g.append(shapes.line((0+offset,max),(0+offset,0)))
	
	#baseblock
	for f in range(width):
		#set height
		p1 = (f*freq + offset , max)
		p2 = (f*freq + offset, random.randint(int(min),int(max)))
		l = shapes.line(p1, p2)
		g.append(l)
		#random toppings
		if (random.randint(0,2) == 1):
			p1 = (f*freq + offset , max)
			p2 = (width/2*freq +1000 + offset, max + 500)
			l = shapes.line(p1, p2)
			g.append(l)
		#take it up
		p1 = (width/2*freq +1000 + offset, max + 500)
		p2 = (width/2*freq +1000 + offset, max + 2000)
		l = shapes.line(p1, p2)
		g.append(l)
		#to the other shape





	g.append(shapes.line((freq*width,max),(freq*width,0)))
	#goffset = density*quantity/5*3*(pen+1) + (pen%2*density/2)
	#transforms.offset(g, (goffset, 0))
	plotter.write(g)

def wavedecay(wav, rez, height, scale, x, y):
	global plotter
	global g
	#plotter.select_pen(1)
	g = shapes.group([])
	for r in range(rez):
		#print np.log(r)
		g.append(shapes.line((np.log(r+1)*scale, -height), (np.log(r+1)*scale,height)))
		#print((np.log(r+1)*scale, -height), (np.log(r+1)*scale, height))
		#g.append(shapes.line((0,0),(1000,1000)))
	# io.view(g)
	for r in range(rez):
		#print(int(np.log(r+1)/np.log(rez)*rez))
		i1 = int(np.log(r+1)/np.log(rez)*rez)-1 
		i2 = int(np.log(r+2)/np.log(rez)*rez)-1
		x1 = np.log(r+1)*scale
		x2 = np.log(r+2)*scale
		y1 = (np.sin(wav1[i1])*np.sin(wav3[i1]))*height #*signal.sawtooth(wav2[i1])
		y2 = (np.sin(wav1[i2])*np.sin(wav3[i2]))*height #*signal.sawtooth(wav2[i2])
		g.append(shapes.line((x1, y1), (x2, y2)))
		#plot wav1
	for r in range(rez):
		i1 = int(np.log(r+1)/np.log(rez)*rez)-1 
		i2 = int(np.log(r+2)/np.log(rez)*rez)-1
		x1 = np.log(r+1)*scale
		x2 = np.log(r+2)*scale
		y1 = np.sin(wav1[i1])*height
		y2 = np.sin(wav1[i2])*height
		g.append(shapes.line((x1, y1), (x2, y2)))
	transforms.offset(g,(x,y))

	plotter.write(g)

#wavedecay("wav1", rez, 1000, 1000, 0, 0)


def simplelines(pen, freq, height, density, densityscale):
	global plotter
	global g
	g = shapes.group([])
	plotter.select_pen(pen+1)
	for f in range(freq):
		l = shapes.line((f*density,0),(f*(pen+1)*density/densityscale,height))
		g.append(l)
	#fitpage(g)
	plotter.write(g)

def simplelines2(pen, density, quantity, height):
	global plotter
	global g
	g = shapes.group([])
	plotter.select_pen(pen+1)
	for f in range(quantity):
		l = shapes.line(((2%(pen+1)*density/4)+quantity+f*density,0) , ((2%(pen+1)*density/4)+quantity+f*density,1000))
		#l = shapes.line((f*density,0),(f*density,height))
		g.append(l)
	#fitpage(g)
	goffset = density*quantity/2*(pen+1) + (pen%2*density/2)
	transforms.offset(g, (goffset, 0))
	plotter.write(g)

def fitpage(shape):		
	if (pltmax[0]/g.width < pltmax[1]/g.height):
		transforms.scale(shape, (pltmax[0]-100)/shape.width)
	else:
		transforms.scale(shape, (pltmax[1]-100)/shape.height)
	# print g.width, g.height
	transforms.offset(shape, (shape.width, shape.height))


shaperez = 20
layerarticulation = 4

def shapelayerrect(layer, pen, x, y, width, height):
	plotter.select_pen(pen)
	global plotter
	global g
	g = shapes.group([])	
	for i in range(int(width/shaperez)):
		x1 = x + i*shaperez + layer*layerarticulation
		x2 = x1 
		y1 = y
		y2 = y + height
		g.append(shapes.line((x1,y1),(x2,y2))) 
	plotter.write(g)


def length(v):
  return math.sqrt(np.dot(v, v))

def angle(v1, v2):
  return math.acos(np.dot(v1, v2) / (length(v1) * length(v2)))
def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            angle_between((1, 0, 0), (1, 0, 0))
            0.0
            angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle



#(0,0) ,(100,100), (200,0) (0,0), (50,50,) (200,0)
def polygonlayer(layer, pen, x, y, toppoints = [], bottompoints = []):
	#toppoints/bottompoints must have same start/end
	plotter.select_pen(pen)
	global plotter
	global g
	g = shapes.group([])
	#calculatetoprowheights
	# for point in toppoints:
		#calculate angle to next stop
		# if point < len(toppoints):
	# print(ange((1,1),(10,10)))

def dotproduct(a,b):
	return sum([a[i]*b[i] for i in range(len(a))])

from math import acos

#Calculates the size of a vector
def veclength(a):
	return sum([a[i] for i in range(len(a))])**.5

#Calculates the angle between two vector
def ange(a,b):
	dp=dotproduct(a,b)
	la=veclength(a)
	lb=veclength(b)
	costheta=dp/(la*lb)
	print(costheta)
	return np.arccos(costheta)

x = np.array([2,2])
y = np.array([2,3])
np.dot(x,y)
dot = np.dot(x,y)
x_modulus = np.sqrt((x*x).sum())
y_modulus = np.sqrt((y*y).sum())
cos_angle = dot / x_modulus / y_modulus # cosine of angle between x and y
angle = np.arccos(cos_angle)
# angle * 360 / 2 / np.pi # angle in degrees
print math.degrees(angle)

#polygonlayer(1,1,1,1)
#print(np.dot((2,3,4) , (2,1,1)))
#print(length((100,100)))

def roundup(x,ceiling):
    return int(math.ceil(x / ceiling)) * ceiling

def rounddown(x,flooring):
    return int(math.floor(x / flooring)) * flooring


def getspace(p1,p2,interval):
	bottomX = roundup(p1[0], interval)
	topX = roundup(p2[0], interval)
	# bottomY = roundup(p1[1])
	# topY = roundup(p2[1], interval)
	ydiff = topX - bottomX
	spaceX = np.linspace(bottomX+interval ,topX , abs(ydiff)/interval  )
	spaceY = np.linspace(p1[1] ,p2[1], len(spaceX))
	#print "spaceX=" ,spaceX
	#print "spaceY=" ,spaceY
	space = []
	for v in range(len(spaceX)):
		space.append((spaceX[v],spaceY[v]))
	return space

def constructshape(spacearraytop, spacearraybottom, layer, xpos, ypos):
	# top = [spacearraytop[0][0]]
	layeroffset = interspace/layermax*layer
	print "layeroffset" , layeroffset
	top =[]
	# print "TOP", top
	bottom = []
	# bottom = [spacearraybottom[0][0]]
	for space in spacearraytop:
		#print "printing space" , space
		#space.remove[0]
		top.append(space)
	for space in spacearraybottom:
		#space.remove[0]
		bottom.append(space)
		#bottom = bottom + [space]
	print "top = " , len(top) , " bottom = " , len(bottom)
	#plotter.select_pen(1)
	global plotter
	global g
	g = shapes.group([])
	for i in range(len(top)):
		# print("TOPTOP" ,top[i])
		g.append(shapes.line((top[i][0]+layeroffset, top[i][1]),(bottom[i][0]+layeroffset, bottom[i][1])))
	# plotter.select_pen(1)
	transforms.offset(g, (xpos,ypos))
	plotter.write(g)

	#draw it

interspace = 60
layermax = interspace/4
# print "GETTINGSPACE"
# print(getspace((0,0),(100,100), interspace))

#print "CONSTRUCTION"
#print [getspace((0,0),(3000,84), interspace),getspace((3000,84),(5000,3000), interspace),getspace((5000,3000),(6000,2000), interspace)]
#constructshape([(20.0, 0.0), (40.0, 25.0), (60.0, 50.0), (80.0, 75.0), (100.0, 100.0)],[(20.0, 0.0), (40.0, 5.0), (60.0, 5.0), (80.0, 7.0), (100.0, 100.0)],3)
#constructshape([getspace((0,0),(3000,84), interspace),getspace((3000,84),(5000,3000), interspace),getspace((5000,3000),(6000,2000), interspace)], 
#			   [getspace((0,0),(3000,84), interspace),getspace((0,84),(5000,3000), interspace),getspace((2000,3000),(6000,2000), interspace)] )

# constructshape([getspace((0,0),(1000,1000), interspace) + getspace((1000,1000),(2000,1000), interspace)],
#  			   [getspace((0,0),(1000,500), interspace) + getspace((1000,500), (1500,200),  interspace) +  getspace((1500,200),(2000,1000), interspace)],
#  			   10)

def gentop(start,stop,min,max,steps,layer,xpos,ypos): #(0,0),(10000,1000),(0,2000),(2500,5000),(3,2), 3
	gtop = []
	gbottom = []
	baseX = stop[0] - start[0]
	baseY = stop[1] - start[1]
	basestepTop = baseX/(steps[0]+1)
	print(basestepTop)
	basestepBottom = baseX/(steps[1]+1)
	gtop.append(start)
	gbottom.append(start)
	for i in range(steps[0]):
		gtop.append((basestepTop*1*(i+1), random.randint(max[0],max[1])))		
	for i in range(steps[1]):
		gbottom.append((basestepBottom*1*(i+1), random.randint(min[0],min[1])))
	gtop.append(stop)
	gbottom.append(stop)
	# print "printing gbottom"
	# print gbottom
	# print "printing gtop"
	# print gtop
	totaltop = []
	totalbottom = []
	for t in range(len(gtop)-1):
		print "length gtop", len(gtop)
		totaltop = totaltop + getspace(gtop[t], gtop[t+1], interspace)
		# print totaltop , "iteration ",gtop[t+1], "and gtop t" , getspace(gtop[t], gtop[t+1], interspace)
	for t in range(len(gbottom)-1):
		print "length gbottom", len(gbottom)
		totalbottom = totalbottom + getspace(gbottom[t], gbottom[t+1], interspace)
	# print "PRINTING TOTALTOP"
	# print totaltop
	#plotter.select_pen(2)
	# print "totalbottom", totalbottom
	# print "totaltop", totaltop
	constructshape(totaltop,totalbottom,layer,xpos,ypos)

#gentop((0,0),(1000,100),(0,2000),(1000,5000),(4,4),3)


def dobox(pen,xpos,ypos,width,height,subdiv1,subdiv2,globalx, globaly):
	global plotter
	global g
	g = shapes.group([])
	plotter.select_pen(pen)
	g.append(shapes.rectangle(abs(width),height))
	transforms.offset(g, (abs(width)/2,height/2))
	if (width > 0):
		for i in range(subdiv1):
			y1 = random.randint(0,height)
			# y1 = height/subdiv1*i
			y2 = random.randint(0,height/2)
			# g.append(shapes.line((x1,y1),(x2,y2))) 
			g.append(shapes.line((0,y1)	,(width, y2)))
	transforms.offset(g, (xpos+globalx,ypos+globaly))
	plotter.write(g)

# for i in range(5):
# 	dobox(2,i*1000,random.randint(0,2000),1000,2000,20,20)
#from fractions import Fraction
def rhythmboxes(pen,rhythm, width16, height16, xpos, ypos):
	print len(rhythm)
	cursor = 0
	for i in range(len(rhythm)):
		print ("doing " , rhythm[i], "cursor = ", cursor ) #, "looks like ", Fraction(rhythm[i])
		#dobox(pen,i*width16*Fraction(rhythm[i]),random.randint(0,height16),width16*Fraction(rhythm[i]),height16,20,20)
		dobox(pen, width16*cursor, random.randint(0,height16) ,width16*rhythm[i],height16,int(4/rhythm[i]),20, xpos,ypos)
		cursor = cursor + abs(rhythm[i])

#rhythmboxes(2,["1/1", "3/16", "1/16", "1/8", "1/8", "1/8", "1/8", "3/16", "1/16"],500,2000)

###vorige versie

#rhythmboxes(2,[1/1, 3/16, 1/16, 1/8, 1/8, 1/8, 1/8, 3/16, 1/16],5000,2000,0,0)
# rhythmboxes(1,[2/12,2/12,2/12, 3/16, 1/16, 3/16, 1/16, 3/16, 1/16, -1/4, 1/16, 1/16, 1/16, 1/16],5000,2000,0,6000)

# #for i in range(3):
# #	length = random.randint(3,8)
# #	gentop((random.randint(0,2000),random.randint(0, 2000)),(random.randint(2000,4000),random.randint(2000,4000)),(0,0),(2500,4000),(length, length),i*2) 
plotter.select_pen(5)
gentop((0,1500),(10000,1500),(0,1500),(1500,3500),(3,7),9, 0, 2500)
# plotter.select_pen(3)
# gentop((0,1700),(10000,1700),(0,1500),(1500,3500),(3,7),5, 0, 2500)
# plotter.select_pen(2)
# gentop((0,1900),(10000,1900),(0,1500),(1500,3500),(3,7),1, 0, 2500)


###probeersel  gentop(start,stop,min,max,steps,layer,xpos,ypos):

# plotter.select_pen(4)
# gentop((1000,2000),(9000,7000),(2000,3500),(5500,10000),(3,3),9, 0, 0)
# plotter.select_pen(1)
# gentop((0,5000),(10000,5000),(3000,5000),(5000,7000),(9,3),5, 0, 0)
# plotter.select_pen(2)
# gentop((1000,7000),(9000,2000),(0,2500),(3500,8000),(9,9),1, 0, 0)

# writeword("Sondervan", 16, "USSR.ttf", 12500,9000)
# plotter.select_pen(4)
# writeword("Triangel", 12, "rus.ttf", 17000,9000)
# writeword("Yur", 12, "rus.ttf", 17000,8200)
# plotter.select_pen(3)

# writeword("A1", 10, "USSR.ttf", 12500, 900)
# writeword("Goto_Loopit", 10, "USSR.ttf", 17500, 900)

# writeword("A2", 10, "USSR.ttf", 12500, 1900)
# writeword("SeaClone", 10, "USSR.ttf", 17500, 1900)

# writeword("A3", 10, "USSR.ttf", 12500, 2900)
# writeword("ThreeMoleculesOne", 10, "USSR.ttf", 17500, 2900)

# writeword("A4", 10, "USSR.ttf", 12500, 3900)
# writeword("Cluster89", 10, "USSR.ttf", 17500, 3900)

# rhythmboxes(2,[1/2, 1/4],5000,2000,13500,0)

# rhythmboxes(4,[1/4, 1/4, 1/4],5000,2000,13500,4000)
# plotter.select_pen(2)

# writeword("B1", 10, "USSR.ttf", 12500, 5900)
# writeword("Mass_Inversion", 10, "USSR.ttf", 17500, 5900)

# writeword("B2", 10, "USSR.ttf", 12500, 6900)
# writeword("Triangle_Yur", 10, "USSR.ttf", 17500, 6900)

# writeword("B2", 10, "USSR.ttf", 12500, 6900)
# writeword("Automatic3cc", 10, "USSR.ttf", 17500, 7900)

writeword("cover_gfx_coded_by", 10, "USSR.ttf", 12500, 6900)
writeword("kaosbeat", 10, "USSR.ttf", 17500, 7900)
writeword("KaOSbEat", 12, "rus.ttf", 17000,8200)



# Kant A :
# Goto Loopit
# SeaClone
# ThreeMoleculesOne
# Cluster89
 
# B

# Mass Inversion

# Triangle Yur

# Automatic3cc




# print getspace((0,37),(300,84), 5)
# print getspace((300,84),(500,115), 5)
# print"blah"
# print(np.interp(0.2,[0,1], [0,2]))
# x = np.linspace(0, 2*np.pi, 10)
# print x
# y = np.sin(x)
# print y
# xvals = np.linspace(0, 2*np.pi, 50)

size = 30
for i in range(size):
	# width = random.randint(20,30)
	width = 30
	freq= 25
	# print np.sin((wav3[int(rez/size*i)]))
	#wavesdown(i,freq,i*width*freq,width,random.randint(500,1903),3000)
	#wavesdown(i+1,freq,i*width*freq,width,random.randint(0,int((np.sin((wav1[int(rez/size*i)])) +1 )*500)),(np.sin((wav1[int(rez/size*i)]))+1)*2000)
	#simplelines(i, 200, 8000, 50, 5)
	#simplelines2(i, 20, 10, 1000)

#shapelayerrect(0, 1, 0, 0, 5000, 5000)
#shapelayerrect(1, 1, 2000, 2000, 1000, 1000)
#shapelayerrect(1, 1, 4000, 3000, 1000, 5000)

# for i in range(5):
# 	shapelayerrect(i,1, random.randint(200*i,500*i), random.randint(500*i,1000*i), random.randint(500,1000), random.randint(500,1000))
# for i in range(5):
# 	shapelayerrect(i,1, random.randint(0*i,2000*i), random.randint(0*i,2000*i), random.randint(200,1000), random.randint(200,1000))



#wavedecay(wav3, rez/1, 1500,1100,0, 2500)


io.view(plotter)

