import sys
from chiplotle import *
from chiplotle.tools.io import export
from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")
# plotter.margins.hard.draw_outline()
# plotter = instantiate_plotters( )[0]
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

#additive syths, 
#	plot a sine wave using a shape (circle)
#	plot a saw wave using a shape (triangle)
# 	plot the results using a combination shape
# first wave

rez = 200 #keep it below 300 unless you know what you do
size = 120
noise = size*1.5
interval = 120
randpointer = 30
randpointerjump = 2
randpointerbackrange = 0.99 #(number between 0.50-0.99)
wav1 = np.linspace(0,2*np.pi,rez)
wav2 = np.linspace(0,np.pi,rez)
wav3 = np.linspace(0,8*np.pi,rez)
randwavesize = size/10
g = shapes.group([])
# help(shapes.cross)
# help(random)
# print (signal.sawtooth(wav3))

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
		
		# print wav, idx, wavesize[idx]
		# plotter.select_pen(random.randint(1,3))
		for i in range(0,rez):
			#print(wav, wavtype[idx], wavesize[idx], waveshape[idx])
			if waveshape[idx] == "cross":
				atom = shapes.cross(size,np.cos(wav[i])*size)
			if waveshape[idx] == "rect":
				atom = shapes.rectangle(size,np.sin(wav[i])*size)
			if waveshape[idx] == "circle":
				atom = shapes.circle(signal.sawtooth(wav[i])*size)
				transforms.perpendicular_noise(atom, noise)
			if waveshape[idx] == "spiral":
				atom = spiral_archimedean(size*20, num_turns=22, wrapping_constant=1, direction='cw', segments=30)			
			if wavtype[idx] == "sin":
				transforms.offset(atom, (i*interval, np.sin(wav[i])*wavesize[idx] )) 
			if wavtype[idx] == "cos":
				transforms.offset(atom, (i*interval, np.cos(wav[i])*wavesize[idx] )) 
			if wavtype[idx] == "saw":
				transforms.offset(atom, (i*interval, signal.sawtooth(wav[i])*wavesize[idx] )) 
			if waves:
				g.append(atom)
		#plotter.write(g)

		# plotter.select_pen(2)
		# tr = shapes.rectangle(size,np.cos(wav1[i])*size)
		# transforms.offset(tr, (i*interval, np.cos(wav1[i])*3500 )) 
		# if waves:
		# 	g.append(tr)
		# plotter.select_pen(3)
		# tr = shapes.circle(np.cos(wav2[i])*size)
		# transforms.offset(tr, (i*interval, np.cos(wav1[i])*2500 )) 
		# if waves:
		# 	g.append(tr)

		if subwaves:
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
	g = shapes.group([])			
	




def someinterference(preprism, prismlength, preprismsize, wavs = [wav1, wav2, wav3]):
	#precalc waveshapes
	#draw for debug
	for idx,wav in enumerate(wavs):
		pnts = []		
		for i in range(rez):
			q = (i*interval, np.sin(wav[i])*1000)
			#print(q)
			pnts.append(q)
		p = shapes.path(pnts)
		print("next")
		g.append(p)
	plotter.write(g)



#someinterference(100,100,100)



noise = 100
#somewaves(1,False, True, [wav1, wav2, wav2, wav3, wav1], ["sin", "saw", "cos", "sin", "cos"], [5100, 1000, 6500, 4000, 1000], ["rect", "cross", "cross", "rect", "cross"])  
print "first pass"
# print g.width, g.height
noise = 500
#plotter.select_pen(2)
somewaves(2,False, True, [wav3, wav1], ["cos", "saw", "saw", "sin", "sin"], [1500, 5100, 500, 2000, 6000], ["rect", "cross", "cross", "rect", "cross"])  
plotter.write(g)

somewaves(3,False, True, [wav1, wav3, wav1, wav2, wav2], ["sin", "sin", "sin", "cos", "saw"], [1000, 1500, 3500, 3000, 5000], ["rect", "cross", "cross", "rect", "cross"])  
# somewaves(False,True,[wav3,wav2],["sin","saw"],[1000,3000],["cross","cross"])
plotter.write(g)

print "second pass"
#print plotter.width, plotter.height

# if (pltmax[0]/g.width < pltmax[1]/g.height):
# 	transforms.scale(g, (pltmax[0]-100)/g.width)
# else:
# 	transforms.scale(g, (pltmax[1]-100)/g.height)

# print g.width, g.height

# transforms.offset(g, (g.width, g.height))

#io.save_hpgl(g, "test.plt")


export(plotter, sys.argv[1], fmt='jpg')
#plotter.write(sign(sys.argv[0]))
export(plotter, sys.argv[1], fmt='svg')
io.view(plotter)





