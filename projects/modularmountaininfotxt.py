#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8


# address = 


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
plotPlotterOutline = True
plotPaperOutline = True
plotDrawingOutline = False

# pltmax = [10320, 7920] >>> ???
pltmax = [16158, 11040]
plotunit = 0.025 # 1 coordinate unit per plotter = 0.025 mm
papersize = [276,276]
textzones = [[[9/plotunit,187/plotunit], [89/plotunit,267/plotunit]], 
            [[98/plotunit,187/plotunit], [178/plotunit,267/plotunit]], 
            [[187/plotunit,187/plotunit], [267/plotunit,267/plotunit]], 
            [[98/plotunit,98/plotunit], [178/plotunit,178/plotunit]], 
            [[187/plotunit,98/plotunit], [267/plotunit,178/plotunit]], 
            [[187/plotunit,9/plotunit], [267/plotunit,89/plotunit]]]

# textzone = textzones[1]
# print(textzone[0][1])
# print("******************************")
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
    paper = shapes.rectangle(papersize[0]/plotunit, papersize[1]/plotunit)
    transforms.offset(paper,(papersize[0]/plotunit/2,papersize[1]/plotunit/2))
    plotter.write(paper)


def writetext(title, titleSize, text, textzone, frame, fill):
    charlengthparameter = 210  # tweak this to make it fit the width
    g = shapes.group([])
    rectsizeX = abs(textzone[1][0] - textzone[0][0])
    rectsizeY = abs(textzone[1][1] - textzone[0][1])
    plotter.select_pen(2)

    
    if frame:
        print("rectsize =", rectsizeX, rectsizeY)
        f = shapes.rectangle(rectsizeX, rectsizeY)
        transforms.offset(f,(textzone[0][0] + rectsizeX/2, textzone[0][1] + rectsizeY/2))
        g.append(f)
    plotter.write(g)

    if fill:
        # plotter.select_pen(2)
        t = shapes.group([])
        titlerows = len(title)
        for i,titlerow in enumerate(title):
            t.append(writeword(titlerow, titleSize, "USSR.ttf",100,-i*500, "right"))
        transforms.offset(t, (textzone[0][0] + rectsizeX - 100, textzone[0][1] + rectsizeY - 500))
        plotter.write(t)

        plotter.select_pen(1)
        textgroup = shapes.group([])
        maxheight = rectsizeY
        rowheight = maxheight/len(text)
        rows = len(text)
        maxlength = rectsizeX
        for i,l in enumerate(text):
            chars = len(l)
            if (maxlength/chars < charlengthparameter):
                charwidth = 0.33/charlengthparameter*maxlength/chars
            else:
                charwidth = 0.33
            t =  shapes.label(str(l.encode('utf-8')), charwidth, charwidth)
            transforms.offset(t, (zone[0][0] + 150, zone[0][1] - i*(charwidth/0.25*charlengthparameter) + rows*200))
            textgroup.append(t)
        plotter.write(textgroup)
    

titles = [["ElfenWander"], ["DistressFrequency"], ["TheEdgeOfThe", "administratively", "possible"], ["SineRave"], ["Palonopsia"], ["MountainDrone"]]
titlesizes= [5,4,5,5,5,5]
texts = [[  "ElfenWander refers to the   ", 
            "dreamy places I've visited  ", 
            "in Tushetii, wandering from ",
            "from mountain to mountain.  ",
            "It's also wandering through ", 
            "some preenFM2 synth settings"],
          [ "This picture was taken on   ",
            "a remote place in Georgia.  ",
            "Surrounded by an emptiness  ",
            "one wonders how to call home",
            "Until 1988, 500kHz was the  ",
            "international Morse Code    ",
            "distress frequency          " ],  
          [ "One day I walked towards the", 
            "Russian border, the edge of ",
            "where my papers would allow ",
            "me to go. The border is the ",
            "ridge. The bottom left house",
            "the last inhabited place    ",
            "before the border.          " ],
          [ "Mountains make you feel small, ",
            "they are small compared to the ",
            "planet they're on.             ",
            "This blue marble is just a pale",
            "blue dot.                      "],  
          [ "Palonopsia (Greek: 'palin' >   ",
            "'again' & 'opsia' > 'seeing') is ",
            "the persistent recurrence of a ",
            "visual image after the stimulus",
            "has been removed. The mountains",
            "are diverse and different every",
            "day, but they feel familiar.   "],  
          [ "Let the mountains take you for",
            "a walk. Follow their guidance,",
            "feel the space they create.   ",
            "Around you, inside your head. ",
            "Working on your mind. In a very",
            "good way.                     "]
    ]   

for j,zone in enumerate(textzones):
    print(titles[j])
    writetext(titles[j], titlesizes[j],texts[j],zone, 1, 1)

io.view(plotter)
